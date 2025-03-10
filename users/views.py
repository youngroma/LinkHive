from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from users.models import User, Referral
import bleach

DjangoUser = get_user_model()

def sanitize_input(data):
    return bleach.clean(data)


class RegisterUser(APIView):
    def post(self, request):
        # Rate limiting check (5 requests per minute)
        ip = request.META.get('REMOTE_ADDR')
        now = datetime.now()

        # Check the number of requests for this IP in the last minute
        key = f"register_rate_limit_{ip}"
        timestamps = cache.get(key, [])

        # Remove expired timestamps
        timestamps = [ts for ts in timestamps if ts > now - timedelta(minutes=1)]

        if len(timestamps) >= 5:
            return JsonResponse({"message": "Rate limit exceeded"}, status=429)

        # Add the current timestamp
        timestamps.append(now)
        cache.set(key, timestamps, timeout=60)

        email = sanitize_input(request.data.get("email"))
        username = sanitize_input(request.data.get("username"))
        password = sanitize_input(request.data.get("password"))
        referral_code = sanitize_input(request.data.get("referral_code"))  # Ref code may be empty



        # Checking existing email
        if get_user_model().objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already in use"}, status=400)

        referrer = None
        if referral_code:
            try:
                # Check if the code is a valid UUID
                if not self.is_valid_uuid(referral_code):
                    return JsonResponse({"message": "Invalid referral code"}, status=400)

                # Get referrer on reference code
                referrer = get_user_model().objects.get(referral_code=referral_code)
            except get_user_model().DoesNotExist:
                return JsonResponse({"message": "Referrer does not exist"}, status=400)

        # Creating user
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password,
            referred_by=referrer  # If there is a referee, we assign him
        )

        # If reference code was specified, create an entry in the Referral
        if referrer:
            referral = Referral.objects.create(
                referrer=referrer,
                referred_user=user,
                status=Referral.PENDING  # Awaiting confirmation
            )

            ''' Here we add logic to upgrade status to SUCCESSFUL
            After the user has been successfully created, we update the status of the review '''

            referral.status = Referral.SUCCESSFUL
            referral.reward_earned = 10
            referral.save()

            # We award referee bonuses
            referrer.credits += 10
            referrer.save()

        # JWT Token Generation
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({
            "message": "User created successfully",
        }, status=201)

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )


        return Response({
            "message": "User created successfully",
            "access_token": access_token
        }, status=201)

    def is_valid_uuid(self, value):
        try:
            uuid.UUID(str(value))
            return True
        except ValueError:
            return False

class LoginUser(APIView):
    def post(self, request):
        # Rate limiting check (5 requests per minute)
        ip = request.META.get('REMOTE_ADDR')
        now = datetime.now()

        # Check the number of requests for this IP in the last minute
        key = f"login_rate_limit_{ip}"
        timestamps = cache.get(key, [])

        # Remove expired timestamps
        timestamps = [ts for ts in timestamps if ts > now - timedelta(minutes=1)]

        if len(timestamps) >= 5:
            return JsonResponse({"message": "Rate limit exceeded"}, status=429)

        # Add the current timestamp
        timestamps.append(now)
        cache.set(key, timestamps, timeout=60)

        email = request.data.get("email")
        password = request.data.get("password")

        # Check if a user exists with the specified email
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        # Check password
        if not user.check_password(password):
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "message": "Login successful",
            "access_token": access_token
        }, status=200)


class ReferralStats(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Try to take from cache
        referrals_count = cache.get(f'referrals_count_{user.id}')

        if referrals_count is None:
            # Count referrals through the Referral table
            referrals_count = Referral.objects.filter(referrer=user, status=Referral.SUCCESSFUL).count()

            # Cache result
            cache.set(f'referrals_count_{user.id}', referrals_count, timeout=60)

        return JsonResponse({"referrals_count": referrals_count})


class ReferralLink(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        referral_link = f"http://127.0.0.1:8000/api/register?referral_code={user.referral_code}"
        return JsonResponse({"referral_link": referral_link})




class ForgotPassword(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return JsonResponse({"message": "Email is required"}, status=400)

        # Find user by email
        try:
            user = DjangoUser.objects.get(email=email)
        except DjangoUser.DoesNotExist:
            return JsonResponse({"message": "User with this email does not exist"}, status=404)

        # Generate password recovery token
        token = default_token_generator.make_token(user)
        reset_link = f"http://127.0.0.1:8000/api/reset-password/{token}"

        # Send email with link
        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {reset_link}",
            "noreply@yourdomain.com",
            [email],
        )

        return JsonResponse({"message": "Password reset link has been sent to your email."})

class ResetPassword(APIView):
    def post(self, request, token):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        # Password match check
        if new_password != confirm_password:
            return JsonResponse({"message": "Passwords do not match."}, status=400)

        # Token check
        try:
            user = DjangoUser.objects.get(username=request.data.get("username"))
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return JsonResponse({"message": "Password reset successful."})
            else:
                return JsonResponse({"message": "Invalid or expired token."}, status=400)
        except DjangoUser.DoesNotExist:
            return JsonResponse({"message": "User not found."}, status=404)


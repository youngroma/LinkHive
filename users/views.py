from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import bcrypt
import uuid
from django.contrib.auth import authenticate, get_user_model


User = get_user_model()



class RegisterUser(APIView):
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")
        referral_code = request.data.get("referral_code")

        if get_user_model().objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already in use"}, status=400)

        referrer = None
        if referral_code:
            try:
                if not self.is_valid_uuid(referral_code):
                    return JsonResponse({"message": "Invalid referral code"}, status=400)

                referrer = get_user_model().objects.get(referral_code=referral_code)
            except get_user_model().DoesNotExist:
                return JsonResponse({"message": "Referrer does not exist"}, status=400)

        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password,
            referred_by=referrer
        )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
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
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        if not user.check_password(password):
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "message": "Login successful",
            "access_token": access_token
        }, status=200)





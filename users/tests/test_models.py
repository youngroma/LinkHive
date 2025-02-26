from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Referral


class UserModelTest(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123'
        )

        # Check the correctness of created data
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='password123'
        )

        # Check that the creapfte superuser is working as a
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertEqual(admin_user.username, 'admin')
        self.assertTrue(admin_user.check_password('password123'))
        self.assertTrue(admin_user.is_active)




class ReferralModelTest(TestCase):
    def test_referral_creation(self):
        referrer = get_user_model().objects.create_user(
            email="referrer@example.com",
            username="referrer",
            password="password123"
        )
        referred_user = get_user_model().objects.create_user(
            email="referred@example.com",
            username="referreduser",
            password="password123"
        )
        referral = Referral.objects.create(
            referrer=referrer,
            referred_user=referred_user,
            status=Referral.PENDING
        )

        # Check the reference data
        self.assertEqual(referral.referrer, referrer)
        self.assertEqual(referral.referred_user, referred_user)
        self.assertEqual(referral.status, Referral.PENDING)

    def test_referral_status_update(self):
        referrer = get_user_model().objects.create_user(
            email="referrer@example.com",
            username="referrer",
            password="password123"
        )
        referred_user = get_user_model().objects.create_user(
            email="referred@example.com",
            username="referreduser",
            password="password123"
        )
        referral = Referral.objects.create(
            referrer=referrer,
            referred_user=referred_user,
            status=Referral.PENDING
        )

        # Update the status of the review
        referral.status = Referral.SUCCESSFUL
        referral.save()

        # Checking status updated
        updated_referral = Referral.objects.get(id=referral.id)
        self.assertEqual(updated_referral.status, Referral.SUCCESSFUL)
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Referral

class ReferralSystemTest(TestCase):
    def test_valid_referral(self):
        referrer = get_user_model().objects.create_user(
            email="referrer@example.com",
            username="referrer",
            password="password123"
        )
        referred_user = get_user_model().objects.create_user(
            email="referred@example.com",
            username="referreduser",
            password="password123",
            referred_by=referrer
        )
        # Проверяем, что реферальная связь установлена правильно
        self.assertEqual(referred_user.referred_by, referrer)

    def test_self_referral(self):
        user = get_user_model().objects.create_user(
            email="user@example.com",
            username="user",
            password="password123"
        )

        # Попытка назначить referred_by как самого себя
        with self.assertRaises(ValueError):
            user.referred_by = user  # Назначаем referred_by как самого себя
            user.save()  # Это должно вызвать ValueError

    def test_referral_count(self):
        referrer = get_user_model().objects.create_user(
            email="referrer@example.com",
            username="referrer",
            password="password123"
        )
        # Создаем несколько рефералов
        for i in range(3):
            get_user_model().objects.create_user(
                email=f"referred{i}@example.com",
                username=f"referreduser{i}",
                password="password123",
                referred_by=referrer
            )
        # Проверяем количество рефералов
        referrals = get_user_model().objects.filter(referred_by=referrer)
        self.assertEqual(referrals.count(), 3)
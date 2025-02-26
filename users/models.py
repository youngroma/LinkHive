from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, referred_by=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, referred_by=referred_by, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    referral_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username


class Referral(models.Model):
    PENDING = 'pending'
    SUCCESSFUL = 'successful'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SUCCESSFUL, 'Successful'),
    ]
    referrer = models.ForeignKey(User, related_name='referrals_made', on_delete=models.CASCADE)
    referred_user = models.ForeignKey(User, related_name='referred_by_user', on_delete=models.CASCADE)
    date_referred = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    reward_earned = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['referrer']),
            models.Index(fields=['referred_user']),
        ]

    def __str__(self):
        return f"{self.referrer.username} -> {self.referred_user.username}"
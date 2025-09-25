from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import secrets

class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp')
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()

    def is_valid(self, code: str) -> bool:
        return self.code == code and timezone.now() < self.expires_at

    @staticmethod
    def issue_for(user: User) -> "OneTimeCode":
        code = f"{secrets.randbelow(1000000):06d}"  # 6 цифр
        obj, _ = OneTimeCode.objects.update_or_create(
            user=user,
            defaults={'code': code, 'expires_at': timezone.now() + timedelta(minutes=10)}
        )
        return obj

    def __str__(self):
        return f"OTP for {self.user.username} until {self.expires_at}"

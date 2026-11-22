import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Create initial site owner only when explicit bootstrap credentials are configured"

    def handle(self, *args, **kwargs):
        username = os.environ.get("ADMIN_BOOTSTRAP_USERNAME", "").strip()
        password = os.environ.get("ADMIN_BOOTSTRAP_PASSWORD", "")
        if not username or not password:
            self.stdout.write("Admin bootstrap not configured")
            return
        if len(password) < 16:
            raise ValueError("Admin bootstrap password must be at least 16 characters")
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"is_staff": True, "is_superuser": True, "is_active": True},
        )
        if created:
            user.set_password(password)
            user.save(update_fields=["password"])
            self.stdout.write(self.style.SUCCESS("Initial admin account created"))
        else:
            self.stdout.write("Admin already exists; password and permissions unchanged")

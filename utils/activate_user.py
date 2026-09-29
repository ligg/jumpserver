import os
import sys

import django

if os.path.exists('../apps'):
    sys.path.insert(0, '../apps')
elif os.path.exists('./apps'):
    sys.path.insert(0, './apps')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jumpserver.settings")
os.environ.setdefault("DJANGO_DEBUG_SHELL", "1")
django.setup()

from users.models import User
from django.utils import timezone


def activate_user(username):
    user = User.objects.filter(username=username).first()
    if not user:
        print("Not found user: ", username)
        return

    print("Activate user: ", username)
    user.is_active = True

    fields = []
    if user.is_expired:
        user.date_expired = timezone.now() + timezone.timedelta(days=365)
        fields.append('date_expired')

    if user.password_has_expired:
        user.date_password_last_updated = timezone.now()
        fields.append('date_password_last_updated')

    user.save(update_fields=['is_active'] + fields)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python activate_user.py <username>")
        sys.exit(1)
    username = sys.argv[1]
    activate_user(username)

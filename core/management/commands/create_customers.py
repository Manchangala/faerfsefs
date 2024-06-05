from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Customer

class Command(BaseCommand):
    help = 'Create Customer profiles for all users without one'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            if not hasattr(user, 'customer'):
                Customer.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Successfully created Customer profile for user {user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {user.username} already has a Customer profile'))

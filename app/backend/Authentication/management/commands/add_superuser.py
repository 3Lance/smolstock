from django.core.management.base import BaseCommand
from Authentication.models import User


class Command(BaseCommand):
    """
    Command to create superuser with username and password

    Arguments:
        email: email of the superuser (optional, default: admin@smolstock.com)
        password: password of the superuser (optional, default: smolstock)

    Usage:
        python manage.py add_superuser --email <email> --password <password>
    """

    help = 'Create superuser with username and password'

    def handle(self, *args, **kwargs):
        """Function to create superuser with username and password"""
        # reading email and password from the command line arguments
        email = kwargs.get('email', 'admin@smolstock.com')
        password = kwargs.get('password', 'smolstock')

        # checking if the user with the given email already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR('User with this email already exists'))
            return

        # creating the superuser
        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(
            self.style.SUCCESS(
                'Superuser created successfully'
                )
            )

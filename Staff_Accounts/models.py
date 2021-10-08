from django.contrib.auth.models import AbstractUser, Group, User, BaseUserManager
from django.db import models
from django.db.models import signals
from django.dispatch import receiver


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password=None):
        """
        Creates and saves a user with the given email and password.
        """
        if not password:
            raise ValueError("Users must have a password.")
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        group = Group.objects.get(name="Administrators")
        user.groups.add(group)
        user.save()
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"  # use email to recognize User
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
        managed = False
        # managed = True


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    roles = models.CharField(max_length=20, blank=True)
    activation_key = models.CharField(
        max_length=255, default=1
    )  # link for email verification
    most_recent_otp = models.CharField(
        max_length=6, blank=True
    )  # value for otp verification
    email_validated = models.BooleanField(default=False)  # verify email inputted
    is_verified = models.BooleanField(default=False)  # verify otp inputted

    def __str__(self):

        return f"{self.user}, {self.user.groups.all()[0].name}"

    class Meta:
        db_table = "staff"
        managed = False
        # managed = True


@receiver(signals.post_delete, sender=Staff)
def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()
    signals.post_delete.connect(delete_user, sender=Staff)

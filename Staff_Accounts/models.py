from django.contrib.auth.models import AbstractUser, Group, User, BaseUserManager
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_logged_out


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
        Staff.objects.create(
            user=user, roles="administrator", email_validated=True, is_verified=True
        )
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
        # managed = False
        managed = True


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
    number_of_attempts = models.IntegerField(default=0)  # count number of attempts

    def __str__(self):

        return f"{self.user}, {self.user.groups.all()[0].name}"

    class Meta:
        db_table = "staff"
        # managed = False
        managed = True


# signal to delete user from Staff table using User relation
@receiver(signals.post_delete, sender=Staff)
def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()
    signals.post_delete.connect(delete_user, sender=Staff)


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        User, related_name="logged_in_user", on_delete=models.CASCADE
    )
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "login_staff"
        # managed = False
        managed = True


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get("user"))


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get("user")).delete()

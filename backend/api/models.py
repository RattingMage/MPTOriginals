from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class UserRoles(models.TextChoices):
    USER = 'USER', _("user")
    CONSULTANT = 'CONSULTANT', _("consultant")


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=12, default="")
    code = models.CharField(max_length=4, default="")
    role = models.CharField(max_length=10, choices=UserRoles.choices, default=UserRoles.USER)
    is_verify = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]
    objects = UserManager()


class Room(models.Model):

    """
    Room Model for group calling
    {
        user: 0,
        tittle: "string",
        description: "string",
        type_of: "OTA",
    }
    """

    ROOM_TYPE = [
        ("OTA", "Open to all"),
        ("IO", "Invite only"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listener = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listener")
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(default="", blank=True, null=True)
    type_of = models.CharField(
        max_length=3,
        choices=ROOM_TYPE,
        default="OTA",
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



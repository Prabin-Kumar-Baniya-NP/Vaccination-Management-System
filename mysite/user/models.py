from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given username must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email Address', max_length=320, unique=True)
    first_name = models.CharField('First Name', max_length=30, blank=True)
    middle_name = models.CharField('Middle Name', max_length=30, blank=True)
    last_name = models.CharField('Last Name', max_length=30, blank=True)
    date_of_birth = models.DateField(
        'Date of Birth', null=True, blank=True, help_text="Enter Date in this Format: Year-Month-Day")
    gender = models.CharField("Gender", max_length=1, choices=[
                              ("M", "Male"), ("F", "Female")], null=True)
    blood_group = models.CharField(max_length=3, null=True, blank=True)
    identity_document_type = models.CharField("Identity Document Type", max_length=32, null=True, choices=[
        ("voter_id", "Voter ID"),
        ("passport", "Passport"),
        ("citizenship_number", "Citizenship Number"),
    ])
    identity_document_number = models.CharField(
        'Identity Document Number', max_length=32)
    photo = models.ImageField(
        verbose_name="Profile Picture", upload_to="profileImage/", null=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    last_updated = models.DateTimeField('Last updated', auto_now=True)
    is_email_verified = models.BooleanField("Email Verified", default=False)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_superuser = models.BooleanField('superuser status', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        return f"{self.first_name} {self.middle_name} {self.last_name}"

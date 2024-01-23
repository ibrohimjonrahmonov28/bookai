from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

GENDER_CHOICES = (("male", "male"), ("female", "female"))

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    name = models.CharField(max_length=60, null=True)
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True,)
    nickname = models.CharField(max_length=60, unique=True, null=True)
    country = models.CharField(max_length=255, null=True)
    date_birth = models.DateField(null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    password = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False) 
    motto = models.TextField()
    avatar = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # user verifications
    otp = models.CharField(max_length=6, null=True)
    otp_max_try = models.IntegerField(default=3, null=True)
    otp_expiry = models.DateTimeField(null=True)
    otp_max_out = models.DateTimeField(null=True)

    roles = (("writer", "writer"), ("moderator", "moderator"), ("user", "user"))
    role = models.CharField(null=True, choices=roles, max_length=10)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_staff

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True



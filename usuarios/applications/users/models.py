from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    """Model definition for User."""
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )

    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField()
    names = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    cod_reg = models.CharField(max_length=6, blank=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    def get_short_name(self):
        return str(self.id) + ' ' + self.username
    def get_full_name(self):
        return str(self.id) + ' ' + self.names + ' ' + self.lastname

    class Meta:
        """Meta definition for User."""
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(self.id) + ' ' + self.names + ' ' + self.lastname


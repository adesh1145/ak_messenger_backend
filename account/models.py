from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser



class UserManager(BaseUserManager):
    def create_user(self, email, number,name, password=None,otp=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not number:
            raise ValueError('Users must have an  Number')

        user = self.model(
            email=self.normalize_email(email),
            number=number,
            name=name,
            otp=otp
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def update_unverified_data(self,email,number,name,password,otp):
        if not email:
            raise ValueError('Users must have an email address')
        if not number:
            raise ValueError('Users must have an  Number')
        user=User.objects.filter(email=email,number=number)
        user.email=self.normalize_email(email=email)
        user.number=number
        user.name=name
        user.otp=otp
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, number,name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            number=number,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=150,
        unique=True,
    )
    number=models.CharField(unique=True,max_length=10)
    name=models.CharField(max_length=30)
    description=models.TextField(max_length=150)

    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    otp=models.CharField(max_length=6)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','number']

    def __str__(self):
         return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


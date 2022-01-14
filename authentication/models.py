from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.utils import timezone, dateformat
from django.core.validators import validate_image_file_extension



def user_images_path(instance, filename):
    return f'users/images/{instance.username}/{filename}'

class UserBlogManager(BaseUserManager):
    
    def create_user(self, username, email, password=None, **other_fields):
        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

    def create_superuser(self, username, email, password=None, **other_fields):
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_admin') is not True:
            raise ValueError("This user must be admin")

        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBlog(AbstractBaseUser):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    description = models.TextField(max_length=250, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserBlogManager()
    user_image = models.ImageField(upload_to=user_images_path, default='users/default_user.jpg', validators=[validate_image_file_extension])
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username


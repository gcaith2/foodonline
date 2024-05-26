from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import OneToOneField
from django.db.models.deletion import CASCADE


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username= username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
        
class User(AbstractBaseUser):

    VENDOR=1
    CUSTOMER=2

    ROLE_CHOICE=(
        (VENDOR,'Vendor'),
        (CUSTOMER,'Customer'),
    )

    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    username=models.CharField(max_length=200, unique=True)
    email=models.EmailField(max_length=200, unique=True)
    phone_number=models.CharField(max_length=12, unique=False)
    role=models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True, null=True )


    #required fields
    date_joined= models.DateTimeField(auto_now_add=True)
    last_login= models.DateTimeField(auto_now=True)
    created_date=models.DateTimeField(auto_now=True)
    modified_date=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    #added later watching github
    objects = UserManager() 

    


    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_labels):
        return True
    
    def get_role(self):
        if self.role == 1:
             user_role = 'Vendor'
        elif self.role == 2:
             user_role = 'Customer'
        return user_role
    

    #create user profiles
class UserProfile(models.Model):
    user = OneToOneField('user', on_delete=CASCADE, blank=True, null=True) #changed user to User
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photos = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city=models.CharField(max_length=50, blank=True, null=True)
    state=models.CharField(max_length=50, blank=True, null=True)
    country= models.CharField(max_length=200, blank=True, null=True)
    pin_code=models.CharField(max_length=6, blank=True, null=True)
    latitude=models.CharField(blank=True, null=True)
    longitude=models.CharField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    #def address(self):
       #return f'{self.address}, {self.city}, {self.state}, {self.country}, {self.pin_code}'
    # In your UserProfile model

def address(self):
  address_parts = [
      self.address,
      self.city if self.city else '',
      self.state if self.state else '',
      self.country if self.country else '',
      self.pin_code if self.pin_code else ''
  ]
  return ', '.join(address_parts)


def __str__(self):
        return self.user.email
    

    
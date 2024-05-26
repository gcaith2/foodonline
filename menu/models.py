from django.db import models
from vendor.models import Vendor
from tabnanny import verbose

DEFAULT_CATEGORY_ID = 1 #default category was added as there was no manual enttry to perform make migrations the same was added in category fooditem

# Create your models here.
class Category (models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name= models.CharField(max_length=50,unique=True )
    slug= models.SlugField(max_length=100, unique=True)
    description= models.CharField(max_length=250, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    #when you pgsqul is updated it would update data with plural name and auto add s at the last that will be incorrect so we need to create meta class

    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'

    def clean(self):
        self.category_name= self.category_name.capitalize()


    def __str__(self):
        return self.category_name

class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fooditems')
    food_title= models.CharField(max_length=50)
    slug= models.SlugField(max_length=100, unique=True)
    description= models.CharField(max_length=250, blank=True)
    price= models.DecimalField(max_digits=10, decimal_places=2 )
    images=models.ImageField(upload_to='foodimages')
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_title
    


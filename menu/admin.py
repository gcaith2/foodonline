from django.contrib import admin
from .models import Category, FoodItem

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug': ('category_name',)}
    list_display =('category_name', 'vendor', 'updated_at')
    search_fields=('category_name', 'vendor__vendor_name') #we add vendor__vendor__name as vendor is a foreign key 

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug': ('food_title',)}
    list_display =('food_title','category','vendor','price','is_available', 'updated_at')
    search_fields=('food_title', 'category__category_name','vendor__vendor_name','price') #we use __ when it is a foreign key
    list_filter= ('is_available',)



# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin) 

from django.shortcuts import get_object_or_404, render, redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib import messages
from accounts.models import UserProfile
from .models import Vendor
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify

def get_vendor(request):
    vendor= Vendor.objects.get(user=request.user)
    return vendor


# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile=get_object_or_404(UserProfile, user=request.user)
    vendor=get_object_or_404(Vendor, user=request.user)

    #to update the data in backend
    if request.method == 'POST':
        profile_form= UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form= VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Profile Updated')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:

        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor
    }
    return render(request, 'vendor/vprofile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor= get_vendor(request)
    categories= Category.objects.filter(vendor=vendor).order_by('created_at')
    context ={
        'categories': categories

    }
    return render(request,'vendor/menu_builder.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor= get_vendor(request)        
    category= get_object_or_404(Category, pk=pk)
    fooditems= FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'fooditems': fooditems,
        'category': category,
    }
    return render(request,'vendor/fooditems_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':

        form =CategoryForm(request.POST)
        if form.is_valid():
            category_name= form.cleaned_data['category_name']
            category= form.save(commit=False)  # commit=False when we do not want the form to be saved yet with next condition
            category.vendor= get_vendor(request)
            category.slug= slugify(category_name)
            form.save()
            messages.success(request, 'Category added Succesfully')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form=CategoryForm()
    context= {
        'form':form,

    }
    return render(request, 'vendor/add_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category= get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form =CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name= form.cleaned_data['category_name']
            category= form.save(commit=False)  # commit=False when we do not want the form to be saved yet with next condition
            category.vendor= get_vendor(request)
            category.slug= slugify(category_name)
            form.save()
            messages.success(request, 'Category updated Succesfully')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form=CategoryForm(instance=category)
        
    context={
        'form':form,
        'category':category
    }

    return render(request, 'vendor/edit_category.html',context)
   
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category= get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request, 'Category deleted succesfully')
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':

        form =FoodItemForm(request.POST, request.FILES)  # add request.files whenever you have image in form
        if form.is_valid():
            foodtitle= form.cleaned_data['food_title']
            food= form.save(commit=False)  # commit=False when we do not want the form to be saved yet with next condition
            food.vendor= get_vendor(request)
            food.slug= slugify(foodtitle)
            form.save()
            messages.success(request, 'Food item added Succesfully')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)

    else:
        form=FoodItemForm()
        #modify this form so only categories added by vendor can only be seen
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context={
        'form':form
    }

    return render(request, 'vendor/add_food.html',context)
    
   

   
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    food= get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form =FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor= get_vendor(request)
            food.slug= slugify(foodtitle)
            form.save()
            messages.success(request, 'Food Item updated Succesfully')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form=FoodItemForm(instance=food)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
        
    context={
        'form':form,
        'food':food,
    }
    return render(request, 'vendor/edit_food.html',context)
    

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, 'Food Item has been deleted succesfully')
    return redirect('fooditems_by_category', food.category.id)

from django.shortcuts import render, get_object_or_404
from vendor.models import Vendor
from menu.models import Category
from django.db.models import Prefetch 
from menu.models import FoodItem
from django.http import HttpResponse,JsonResponse
from .models import Cart 
from .context_processors import get_cart_counter

# Create your views here.
def marketplace(request):
    vendors= Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count= vendors.count()

    context= {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request,'marketplace/listings.html', context)

#prefetch is used for reverse search as in this we are looking for fooditems in category
def vendor_details(request, vendor_slug):
    vendor= get_object_or_404(Vendor,vendor_slug=vendor_slug)
    categories= Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems', 
            queryset=FoodItem.objects.filter(is_available=True))
    )
    if request.user.is_authenticated:
        cart_items= Cart.objects.filter(user=request.user)
    else:
        cart_items= None
       

    context= {
       'vendor': vendor,
       'categories': categories,
       'cart_items': cart_items,
    }
    return render(request,'marketplace/vendor_details.html', context)





def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the food item is already added to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the quantity of the food item', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity})
                except Cart.DoesNotExist:
                    Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food item to the cart'})
            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'Food item does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'Failed', 'message': 'Not logged in'})

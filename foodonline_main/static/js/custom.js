let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        // console.log('place name=>', place.name)
    }

    // get the address components and assign them to the fields
    // console.log(place);
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address': address}, function(results, status){
        // console.log('results=>', results)
        // console.log('status=>', status)
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // console.log('lat=>', latitude);
            // console.log('long=>', longitude);
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);

            $('#id_address').val(address);
        }
    });

    // loop through the address components and assign other address data
    console.log(place.address_components);
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            // get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            // get city
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            // get pincode
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_pin_code').val("");
            }
        }
    }

}


$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        
        food_id=$(this).attr('data-id');
        url=$(this).attr('data-url');
        data={
            food_id:food_id,
        }

        $.ajax({
            
            type: 'GET',
            url: url,
            data : data,
            success: function(response){
                console.log(response.cart_counter['cart_count'])
                $('#cart_counter').html(response.cart_counter['cart_count']);
            }
        })
    })

    // place the cart item quantity
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })

});
        

// Function to update the cart quantity
function updateCartQuantity(quantity) {
    // Find the HTML element with the id 'cart-quantity'
    const cartQuantityElement = document.getElementById('cart_counter');
    
    // Update the innerHTML with the new quantity
    cartQuantityElement.innerHTML = cart_count;
}

// Simulate adding an item to the cart
function addToCart() {
    // Retrieve the current quantity from the HTML element
    const cartQuantityElement = document.getElementById('item.quantity');
    let currentQuantity = parseInt(cartQuantityElement.innerHTML);

    // Increment the quantity
    currentQuantity += 1;

    // Update the cart quantity
    updateCartQuantity(currentQuantity);
}

// Add event listener to the 'Add to Cart' button
document.getElementById('add-to-cart-btn').addEventListener('click', addToCart);






let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['fr', 'bj', 'us', 'tg', 'ng']},
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

    geocoder.geocode({'address': address}, function (results, status){
        // console.log('results=>', results)
        // console.log('status=>', status)
        if(status === google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

           //console.log('lat=>', latitude);
           //console.log('lng=>', longitude);
           
           $('#id_latitude').val(latitude);
           $('#id_longitude').val(longitude);

           $('#id_address').val(address);

        }
    });
    
    // loop through the address components and assign other address data
    console.log(place.address_components);
    for(var i= 0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // Get country
            if(place.address_components[i].types[j] === 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            // Get state
            if(place.address_components[i].types[j] === 'route' ){
                $('#id_rue').val(place.address_components[i].long_name);
            }
            // Get
            if(place.address_components[i].types[j] === 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            if(place.address_components[i].types[j] === 'administrative_area_level_1'){
                $('#id_departement').val(place.address_components[i].long_name);
            }
        }

    }
}

$(document).ready(function (){
    $('.add_to_cart').on('click', function (e) {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');


        $.ajax({
            type: 'GET',
            url: url,

            success: function (response) {
               console.log(response)
               if(response.status === 'login_required') {
                   swal({
                       title: "Are you a member of  DDZone?",
                       text: response.message,
                       icon: "warning",
                       buttons: "OK",
                       dangerMode: true,
                   }).then(function () {
                       window.location = '/accounts/login';
                   })

               }if(response.status === 'Failed'){
                   swal({
                       title: "Oup'ss...!",
                       text: response.message,
                       icon: "error",
                       buttons: "OK",
                       dangerMode: true,
                   })
               }else{
                   $('#cart_counter').html(response.cart_counter['cart_count']);
                   $('#qty-'+food_id).html(response.qty);

                    // subtoal, delivery, tax, grand_total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['delivery'],
                        response.cart_amount['grand_total'],
                    )
               }
            }
        })
    })

    //place the cart item quantity on load
    $('.item_qty').each(function () {
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })

    // decrease cart
        $('.decrease_cart').on('click', function (e) {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
               console.log(response)
                if(response.status === 'login_required') {
                    swal({
                        title: "Are you a member of  DDZone?",
                        text: response.message,
                        icon: "warning",
                        buttons: "OK",
                        dangerMode: true,
                    }).then(function () {
                        window.location = '/accounts/login';
                    })
                }else if(response.status === 'Failed'){
                    swal({
                       title: "Oup'ss...!",
                       text: response.message,
                       icon: "error",
                       buttons: "OK",
                       dangerMode: true,
                   })
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    // subtoal, delivery, tax, grand_total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['delivery'],
                        response.cart_amount['grand_total'],
                    )

                    if(window.location.pathname == '/cart/'){
                        removeCartItem(response.qty, cart_id)
                        checkEmptyCart();
                    }
                }

            }
        })
    })
    // DELETE ITEM
    $('.delete_cart').on('click', function (e) {
        e.preventDefault();

        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
               console.log(response)
                if(response.status === 'Failed'){
                    swal({
                       title: "Oup'ss...!",
                       text: response.message,
                       icon: "error",
                       buttons: "OK",
                       dangerMode: true,
                   })
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal({
                       title: "Perfect !",
                       text: response.message,
                       icon: "success",
                       buttons: "OK",
                       dangerMode: true,
                   })

                    // subtoal, delivery, tax, grand_total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['delivery'],
                        response.cart_amount['grand_total'],
                    )
                    removeCartItem(0, cart_id);
                    checkEmptyCart();
                }
            }
        })
    })

    // DELETE THE CART ELEMENT IF THE QTY IS 0
    function removeCartItem(cartItemQty, cart_id) {
        if(cartItemQty <= 0){
            // remove the cart item element
            document.getElementById("cart-item-"+cart_id).remove()
        }
        
    }

    // Check if the cart is empty
    function checkEmptyCart() {
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter == 0){
            document.getElementById("empty-cart").style.display = "block";
        }
    }

    // apply cart amounts
    function applyCartAmounts(subtotal, tax, delivery, grand_total) {
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#delivery').html(delivery)
            $('#grand_total').html(grand_total)
        }

    }

    // ADD OPENING HOUR
    $('.add_hour').on('click', function(e){
        e.preventDefault();
        var day = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        var url = document.getElementById('add_hour_url').value

        // console.log(day, from_hour, to_hour, is_closed, csrf_token)

        if(is_closed){
            is_closed = 'True'
            condition = "day != ''"
        }else{
            is_closed = 'False'
            condition = day !== '' && from_hour !== '' && to_hour !== ''
        }

        if(eval (condition)) {
               $.ajax({
                   type: 'POST',
                   url: url,
                   data: {
                       'day': day,
                       'from_hour': from_hour,
                       'to_hour': to_hour,
                       'is_closed': is_closed,
                       'csrfmiddlewaretoken': csrf_token,
                   },
                   success: function (response) {
                       if(response.status === 'success'){
                           if(response.is_closed === 'Closed'){
                              html = '<tr id="hour-'+response.id+'"><td style="text-align: left"><b>'+response.day+'</b></td><td><span class="badge badge-warning text-uppercase">Closed</span></td><td><a href="#" class="remove_hour" data-url="/accounts/vendor/opening-hours/remove/'+response.id+'/"><i style="margin-top: -02rem; font-size: 15px" class="fa fa-trash text-danger" aria-hidden="true"></i></a></td></tr>';
                           }else{
                               html = '<tr id="hour-'+response.id+'"><td style="text-align: left"><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="/accounts/vendor/opening-hours/remove/'+response.id+'/"><i style="margin-top: -02rem; font-size: 15px" class="fa fa-trash text-danger" aria-hidden="true"></i></a></td></tr>';
                           }

                           $('.opening_hours').append(html)
                           document.getElementById("opening_hours").reset();

                       }else{
                           swal({
                               title: "Oup'sss",
                               text: response.message,
                               icon: "error",
                               buttons: "OK",
                               dangerMode: true,
                           })
                       }
                   }
               })
        }else{
            swal({
               title: "No !",
               text: "Please fill all fields",
               icon: "info",
               buttons: "OK",
               dangerMode: true,
           })
        }
    });

    //Remove opening hour
    $(document).on('click', '.remove_hour', function(e){

        e.preventDefault();
        url = $(this).attr('data-url');
        console.log(url)
        $.ajax({
            type: "GET",
            url: url,
            success: function (response) {
                if(response.status == 'success'){
                    document.getElementById('hour-'+response.id).remove()
                }
            }
        })
    });



    // document ready close
});

function googleTranslateElementInit() {
    new google.translate.TranslateElement({
      pageLanguage: 'en',
      autoDisplay: false,
      includedLanguages: 'en,fr,de,es',

  }, 'google_translate_element');
}

function triggerAutoTranslate() {
  // Detect user's language
  var userLang = navigator.language || navigator.userLanguage;
  // Map userLang to a google translate language code
  // and trigger the translation to that language
}

// Load the Google Translate script and then apply auto translation
var googleTranslateScript = document.createElement('script');
googleTranslateScript.type = 'text/javascript';
googleTranslateScript.async = true;
googleTranslateScript.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
document.body.appendChild(googleTranslateScript);

googleTranslateScript.onload = function() {
    googleTranslateElementInit();
    triggerAutoTranslate();
};
















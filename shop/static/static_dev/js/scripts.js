$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);


    function cartUpdating(product_id, nmb, is_delete) {
        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;
        // var csrf_token = $('#csrf_getting_form [name="csrfmiddlewaretoken"]').val(); # if ajax withot form
        var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        var url = form.attr('action');

        if (is_delete){
            data['is_delete'] = true;
        };

        console.log(data);

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("OK!!");
                console.log(data.products_total_nmb);
                if (data.products_total_nmb || data.products_total_nmb == 0) {
                    $('#cart_total_nmb').text("("+data.products_total_nmb+")");
                    console.log(data.products);
                    $('.cart-items ul').html('');
                    $.each(data.products, function(k, v) {
                        $('.cart-items ul').append('<li>' +v.name+ ': ' +v.nmb+ ' unit(s) per ' +v.price_per_item+ ' UAH ' +
                            '<a class="delete-item" href="" data-product_id="'+v.id+'">x</a>' +
                            '</li>');
                        // $('.cart-items ul').append('<li>'+ammount+'</li>');
                    });
                }

                // $('#likes_list').html();
                // $.each(data, function (key, value) {
                //     $('#likes_list').append('<p>'+value.username+'</p>')
                // });
                // $('#modal_message_likes').modal('show');
            },
            error: function () {
                console.log("error!!!")
            }
        });
    };

    form.on('submit', function(e){
        e.preventDefault();
        console.log('123');
        var nmb = $('#number').val();
        console.log(nmb);
        var submit_btn = $('#submit_btn');
        var product_id = submit_btn.data('product_id');
        var product_name = submit_btn.data('product_name');
        var product_price = submit_btn.data('product_price');
        var ammount = nmb * product_price;
        console.log(product_id);
        console.log(product_name);
        console.log(product_price);


    cartUpdating(product_id, nmb, is_delete=false);

    });

    function showCart() {
        $('.cart-items').removeClass('hidden');
    };

    $('.cart-container').on('click, hover', function(e){
        e.preventDefault();
        showCart();
    });

    $('.cart-container').mouseover(function(){
        showCart();
    });

    // $('.cart-container').mouseout(function(){
    //     showCart();
    // }) 

    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        // $(this).closest('li').remove();
        product_id = $(this).data('product_id');
        nmb = 0;
        // data['is_delete'] = true;
        cartUpdating(product_id, nmb, is_delete=true);
    });


    function calculateCartAmount () {
        var total_order_ammount = 0;
        $('.product-in-cart-sum').each(function() {
            total_order_ammount = total_order_ammount + parseFloat($(this).text());

        });
        // $('#total_order_ammount').text((total_order_ammount + ' UAH').toFixed(2));
        $('#total_order_ammount').text(total_order_ammount.toFixed(2) + ' UAH');
    };

    $(document).on('change', '.product-in-cart-nmb', function() {
        var current_nmb = $(this).val();
        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-price').text());
        var total_amount = parseFloat(current_nmb * current_price).toFixed(2);
        current_tr.find('.product-in-cart-sum').text(total_amount);

        calculateCartAmount ()

    })


    calculateCartAmount ()
});

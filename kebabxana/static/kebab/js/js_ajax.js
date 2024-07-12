$(document).ready(function () {
    $(document).on("click", ".add-cart", function (e) {
        e.preventDefault();
        
        var productsInCartCount = $("#cart-count");
        var cartCount = parseInt(productsInCartCount.text() || 0);
        
        var product_id = $(this).data("product-id");
        var add_to_cart_url = $(this).data("cart-add-url");;
       
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                cartCount++;
                productsInCartCount.text(cartCount);
                
                var cartItemsContainer = $("#cart-items");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });


    $(document).on("click", ".remove-cart", function (e) {
        e.preventDefault();
        
        var productsInCartCount = $("#cart-count");
        var cartCount = parseInt(productsInCartCount.text() || 0);
        
        var cart_id = $(this).data("cart-id");
        var cart_remove_url = $(this).data("cart-remove-url")

        $.ajax({

            type: "POST",
            url: cart_remove_url,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                cartCount --;
                productsInCartCount.text(cartCount);

                var cartItemsContainer = $("#cart-items");
                cartItemsContainer.html(data.cart_items_html);
            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });


    $(document).on("click", ".minus", function(e) {
        e.preventDefault();

        var cart_id = $(this).data("cart-id");
        var quantity = $(".count");
        var currentCount = parseInt(quantity.text());
        var change_url = $(this).data("cart-change-url");

        if (currentCount > 1) {
            updateCart(cart_id, currentCount - 1, -1, change_url);
        }

    });

    $(document).on("click", ".plus", function(e) {
        e.preventDefault();

        var cart_id = $(this).data("cart-id");
        var quantity = $(".count");
        var currentCount = parseInt(quantity.text());
        var change_url = $(this).data("cart-change-url");

        updateCart(cart_id, currentCount + 1, +1, change_url);


    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                var productsInCartCount = $("#cart-count");
                var cartCount = parseInt(productsInCartCount.text() || 0);

                cartCount += change;
                productsInCartCount.text(cartCount);

                var cartItemsContainer = $("#cart-items");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    };
});
$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N Svagrant 
    // ****************************************

    // Updates the form with data from the response
    function update_item_form_data(res) {
        $("#shopcart_id_2").val(res.shopcart_id);
        $("#item_id").val(res.id);
        $("#item_name").val(res.item_name);
        $("#item_quantity").val(res.item_quantity);
        $("#item_price").val(res.item_price);
    }

    function update_shopcart_form(res){
        $("#shopcart_id").val(res.id);
        $("#shopcart_customerid").val(res.customer_id);
        $("#shopcart_id_2").val(res.id);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#shopcart_id").val("");
        $("#shopcart_customerid").val("");
        $("#shopcart_id_2").val("");
        $("#item_id").val("");
        $("#item_name").val("");
        $("#item_quantity").val("");
        $("#item_price").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Shopcart
    // ****************************************

    $("#create-shopcart-btn").click(function () {

        var customer_id = $("#shopcart_customerid").val();
        var items_list = [];

        var data = {
            "customer_id": customer_id,
            "items_list":[]
        };

        console.log(data)

        var ajax = $.ajax({
            type: "POST",
            url: "/shopcarts",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_shopcart_form(res)
            var shopcart = res;
            shopcart_id = shopcart.id;
            flash_message("Successfully created the shopcart for customer: " + customer_id + ". Shopcart ID is "+ shopcart_id);
            //flash_message(res.responseJSON.message)
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ***************************************
    // Add Items to cart
    // ***************************************
    $("#add-item-btn").click(function(){
        var shopcart_id = $("#shopcart_id_2").val();
        var item_name = $("#item_name").val();
        var item_quantity =$("#item_quantity").val();
        var item_price=$("#item_price").val();

        var data ={
            "shopcart_id": shopcart_id,
            "item_name": item_name,
            "item_quantity": item_quantity,
            "item_price":item_price
        };

        var ajax = $.ajax({
            type:"POST",
            url:"/shopcarts/"+shopcart_id+"/items",
            contentType: "application/json",
            data: JSON.stringify(data)
        });

        ajax.done(function(res){
            update_item_form_data(res)
            flash_message("Success: Added the item "+item_name + "to shopcart "+shopcart_id)
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update items in a shopcart
    // ****************************************

    $("#update-item-btn").click(function () {

        var shopcart_id = $("#shopcart_id_2").val();
        var item_id =  $("#item_id").val();
        var item_name = $("#item_name").val();
        var item_quantity = $("#item_quantity").val();
        var item_price = $("#item_price").val();

        var data = {
            "item_name": item_name,
            "item_quantity": item_quantity,
            "item_price": item_price,
            "shopcart_id":shopcart_id,
            "id":item_id
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/shopcarts/" + shopcart_id + "/items/" + item_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            });

        ajax.done(function(res){
            update_item_form_data(res)
            flash_message("Successesfully updated item with id:"+ item_id)
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Shopcart
    // ****************************************

    $("#retrieve-btn").click(function () {
        console.log("Function works")
        var shopcart_id = $("#shopcart_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts/" + shopcart_id,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function(res){
            //alert(res.toSource())
            update_shopcart_form(res)
            flash_message("Shopcart with ID "+ shopcart_id + " Exists.")
            //flash_message(res.responseJSON.message)
        });

        ajax.fail(function(res){
            clear_form_data()
            //flash_message(res.responseJSON.message)
            flash_message("Shopcart with ID "+ shopcart_id + " Does not exist.")
        });

    });

    // ****************************************
    // Delete a Shopcart
    // ****************************************

    $("#delete-btn").click(function () {

        var shopcart_id = $("#shopcart_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/shopcarts/" + shopcart_id,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function(res){
            clear_form_data()
            flash_message("shopcart " + shopcart_id + " has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Delete an item in a shopcart
    // ****************************************

    $("#delete-item-btn").click(function () {

        var shopcart_id = $("#shopcart_id_2").val();
        var item_id = $("#item_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/shopcarts/" + shopcart_id+"/items/"+item_id,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function(res){
            clear_form_data()
            flash_message("Item with id: " + item_id + "in shopcart: " + shopcart_id + " has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });


    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        
        clear_form_data()
    });

    // ****************************************
    // List all shopcarts
    // ****************************************
    $("#list-shopcarts-btn").click(function(){
        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts",
            contentType: "application/json",
            data: ''
            });

            ajax.done(function(res){
                //alert(res.toSource())
                $("#search_results").empty();
                $("#search_results").append('<table class="table-striped" cellpadding="100">');
                var header = '<tr>';
                header += '<th style="width:50%">Shopcart ID</th>'
                header += '<th style="width:50%">Customer ID</th>'
                $("#search_results").append(header);
                var firstShopcart = "";
                for(var i = 0; i < res.length; i++) {
                    var shopcart = res[i];
                    var row = "<tr><td>"+shopcart.id+"</td><td>"+shopcart.customer_id;
                    $("#search_results").append(row);
                    if (i == 0) {
                        firstShopcart = shopcart;
                    }
                };
                $("#search_results").append('</table>');

                flash_message("Success");
            });

            ajax.fail(function(res){
            flash_message(res.responseJSON.message)
            });

            

        });


    // ****************************************
    // List all items in a shopcart
    // ****************************************

    $("#list-items-btn").click(function(){
        var shopcart_id = $("#shopcart_id_2").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/shopcarts/" + shopcart_id + "/items",
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">Item ID</th>'
            header += '<th style="width:40%">Item Name</th>'
            header += '<th style="width:40%">Item Quantity</th>'
            header += '<th style="width:10%">Item Price</th ></tr>'
            $("#search_results").append(header);
            var firstItem = "";

            for(var i = 0; i < res.length; i++) {
                var item = res[i];
                var row = "<tr><td>"+item.id+"</td><td>"+item.item_name+"</td><td>"+item.item_quantity+"</td><td>"+item.item_price+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstItem = item;
                }
            };

            $("#search_results").append('</table>');

            flash_message("Success");

        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });



    });

    // ****************************************
    // Search for a Pet
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#pet_name").val();
        var category = $("#pet_category").val();
        var available = $("#pet_available").val() == "true";

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/pets?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Category</th>'
            header += '<th style="width:10%">Available</th ></tr>'
            $("#search_results").append(header);
            var firstPet = "";
            for(var i = 0; i < res.length; i++) {
                var pet = res[i];
                var row = "<tr><td>"+pet._id+"</td><td>"+pet.name+"</td><td>"+pet.category+"</td><td>"+pet.available+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstPet = pet;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstPet != "") {
                update_form_data(firstPet)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})

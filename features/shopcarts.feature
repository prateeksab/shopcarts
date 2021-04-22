Feature: The Shopcarts service back-end
    As a Shopcart Administrator
    I need a RESTful catalog service
    So that I can keep track of all my shopcarts and items

Background:
    Given the server is started
    
Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcart REST API Service"
    And I should not see "404 Not Found"

Scenario: Add an item to a shopcart
    When I visit the "Home Page"
    And I set the "Shopcart_CustomerID" to "2020"
    And I press the "Create Shopcart" button
    And I set "Shopcart ID" to "1"
    Then I should see the message "Successfully created the shopcart for customer: 2020. Shopcart ID is 1"
    And I press the "Retrieve Shopcart" button
    And I set the "Item_ID" to "100001"
    And I set the "Item_Name" to "Hungry Hippos"
    And I set the "Item_Quantity" to "25"
    And I set the "Item_Price" to "99.99"
    And I press the "Add Item to cart" button
    Then I should see the message "Success: Added the item Hungry Hippos shopcart 1"
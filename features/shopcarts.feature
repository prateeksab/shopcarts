Feature: The Shopcarts service back-end
    As a Shopcart Administrator
    I need a RESTful catalog service
    So that I can keep track of all my shopcarts and items

Background:
    Given there are no shopcarts
    
Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcart REST API Service"
    And I should not see "404 Not Found"

Scenario: Add an item to a shopcart
    When I visit the "Home Page"
    And I set the "Shopcart_CustomerID_bottom" field to "2020"
    And I press the "Create-Shopcart" button
    Then I should see the message "Successfully created the shopcart for customer: 2020"
    When I set the "Shopcart_CustomerID_top" field to "2020"
    And I press the "Retrieve" button
    Then I should see the message "Shopcart for Customer ID 2020 exists"
    When I set the "Item_ID" field to "100001"
    And I set the "Item_Name" field to "Hungry Hippos"
    And I set the "Item_Quantity" field to "25"
    And I set the "Item_Price" field to "99.99"
    And I press the "Add-Item" button
    Then I should see the message "Success! Added 25 Hungry Hippos to this shopcart"

Scenario: Add an item to a shopcart, and then modify it
    When I visit the "Home Page"
    And I set the "Shopcart_CustomerID_bottom" field to "2020"
    And I press the "Create-Shopcart" button
    Then I should see the message "Successfully created the shopcart for customer: 2020"
    When I set the "Shopcart_CustomerID_top" field to "2020"
    And I press the "Retrieve" button
    Then I should see the message "Shopcart for Customer ID 2020 exists"
    When I set the "Item_ID" field to "101"
    And I set the "Item_Name" field to "Hungry Hippos"
    And I set the "Item_Quantity" field to "25"
    And I set the "Item_Price" field to "99.99"
    And I press the "Add-Item" button
    Then I should see the message "Success! Added 25 Hungry Hippos to this shopcart"
    When I set the "Shopcart_CustomerID_top" field to "2020"
    And I press the "Retrieve" button
    Then I should see the message "Shopcart for Customer ID 2020 exists"
    When I set the "Item_Quantity" field to "5000"
    And I press the "Update-Item" button
    Then I should see the message "Successfully updated Hungry Hippos"
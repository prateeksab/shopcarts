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
    And I set the "Shopcart_CustomerID" field to "2020"
    And I press the "Create-Shopcart" button
    Then I should see the message "Successfully created the shopcart for customer: 2020"
    When I copy the "Shopcart_ID_bottom" field
    When I press the "Clear" button
    Then the "Shopcart_ID_top" field should be empty
    And the "Shopcart_ID_bottom" field should be empty
    When I paste the "Shopcart_ID_top" field
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
    And I set the "Shopcart_CustomerID" field to "199"
    And I press the "Create-Shopcart" button
    Then I should see the message "Successfully created the shopcart for customer: 199"
    When I copy the "Shopcart_ID_bottom" field
    When I press the "Clear" button
    Then the "Shopcart_ID_top" field should be empty
    And the "Shopcart_ID_bottom" field should be empty
    When I paste the "Shopcart_ID_top" field
    And I press the "Retrieve" button
    Then I should see the message "Shopcart for Customer ID 199 exists"
    When I set the "Item_ID" field to "2"
    And I set the "Item_Name" field to "iPod Nano"
    And I set the "Item_Quantity" field to "10"
    And I set the "Item_Price" field to "699.99"
    And I press the "Add-Item" button
    Then I should see the message "Success! Added 10 iPod Nano to this shopcart"
    When I paste the "Shopcart_ID_top" field
    And I press the "Retrieve" button
    Then I should see the message "Shopcart for Customer ID 199 exists"
    When I set the "Item_Quantity" field to "4567"
    And I press the "Update-Item" button
    Then I should see the message "Successfully updated iPod Nano"

Scenario: Add an item to a shopcart, and then delete the entire shopcart
    When I visit the "Home Page"
    And I set the "Shopcart_CustomerID" field to "245"
    And I press the "Create-Shopcart" button
    Then I should see the message "Successfully created the shopcart for customer: 245"
    When I copy the "Shopcart_ID_bottom" field
    When I press the "Clear" button
    Then the "Shopcart_ID_top" field should be empty
    And the "Shopcart_ID_bottom" field should be empty
    When I paste the "Shopcart_ID_top" field
    And I press the "Retrieve" button
    Then I should see the message "Shopcart for Customer ID 245 exists"
    When I set the "Item_ID" field to "2"
    And I set the "Item_Name" field to "iPod MAX"
    And I set the "Item_Quantity" field to "5"
    And I set the "Item_Price" field to "999.99"
    And I press the "Add-Item" button
    Then I should see the message "Success! Added 5 iPod MAX to this shopcart"
    When I paste the "Shopcart_ID_top" field
    And I press the "Delete" button
    Then I should see the message "Shopcart deleted"

Scenario: List all items in a shopcart
    When I visit the "Home Page"
    And I set the "Shopcart_ID_bottom" to "1"
    And I press the "List-Items" button
    Then I should see "burger" in the results
    And I should not see "toy" in the results
    And I should not see "watch" in the results
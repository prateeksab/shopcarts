Feature: The Shopcart service back-end
    As a Shopcart developer
    I need a RESTful service
    So that I can check which shopcarts exist and what items each shopcart holds

Background:
    Given the following shopcarts
        | id         | customer_id | items_list    |
        | 1          | 1           | empty         |
        | 2          | 2           | empty         |
        | 3          | 3           | empty         |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcarts Demo RESTful Service" in the title
    And I should not see "404 Not Found"
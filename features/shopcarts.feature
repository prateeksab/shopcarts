Feature: The Shopcarts service back-end
    As a Shopcart Administrator
    I need a RESTful catalog service
    So that I can keep track of all my shopcarts and items

Background:
    Given the server is started
    
Scenario: The server is running
    When I visit the "home page"
    Then I should see "Shopcart REST API Service"
    And I should not see "404 Not Found"
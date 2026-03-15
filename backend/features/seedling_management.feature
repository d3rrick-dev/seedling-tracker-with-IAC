Feature: Seedling Management
  As a farmer
  I want to register my seedlings and upload photos
  So that I can track their growth and show them to buyers

  Scenario: Create a seedling and upload a photo successfully
    Given the seedling API is running
    When I create a new seedling with crop "Avocado" and quantity 10
    Then the seedling should be created with an ID
    When I upload a photo "avocado_tree.jpg" for this seedling
    Then the seedling image URL should be updated
    When I fetch the seedling details for this ID
    Then the response should contain valid "mangoes" data with status "Growing"
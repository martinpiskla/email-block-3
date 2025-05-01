@test-feature
Feature: test feature

@test-01
Scenario: first test
    Given I go to the login page
    When I fill in login details
    And I print $Env.USERNAME variable content
    Then I am logged in
    And I print $Config.API_KEY variable content
    And I save John as $Var.username variable
    And I say Hello $Var.username

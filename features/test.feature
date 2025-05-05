@test-feature
Feature: Send an email via Gmail

#  @test-01
#  Scenario: first test
#    Given I go to the login page
#    When I fill in login details
#    And I print $Env.USERNAME variable content
#    Then I am logged in
#    And I print $Config.API_KEY variable content
#    And I save John as $Var.username variable
#    And I say Hello $Var.username

  @test-02
  Scenario: 01. User logs into Gmail web application, creates an email, selects recipient from contact list,
  adds attachment, sends an email and logs out

    Given I open Home page
    When I execute login with:
      | Username | $Env.EMAIL_USERNAME |
      | Password | $Env.EMAIL_PASSWORD |
    Then I am on Inbox page

    When I click on New Message button
    Then To Recipients element is visible

    When I click on Select Contacts button
    Then Saved Contact element is visible

    When I click on Saved Contact element
    Then saved contact in to recipients element is visible

    When I execute write email and add attachment with:
      | Subject    | testEmailSubject.txt |
      | Attachment | attachment.txt       |
    When I click on Send Email button
    Then I execute validate email is in sent folder

    When I click on Logout button
    Then I am on Home page

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

    Given I open Gmail page
    When I execute login
    When I execute login with:
      | Username | usernametest |
      #| Username | $Env.EMAIL_USERNAME |
    And I click on Next button
    Then I am on Inbox page

    When I click on write new email button
    Then I am on New Email page

    When I click on select contacts button
    Then I am on Select Contacts page

    When I execute select and insert contacts with:
      | Contacts | $Env.EMAIL_ADDRESS |
    Then I am on New Email page

    When I execute validate recipients with:
      | To  | $Env.EMAIL_ADDRESS |
      | Cc  |                    |
      | Bcc |                    |
    And I execute write email with:
      | Subject | testEmailSubject.txt |
      | Body    | testEmailBody.txt    |
    And I click on Send email button
    Then I am on Inbox page

    When I execute validate message sent banner
    And I execute logout from gmail
    Then I am on Gmail Login page

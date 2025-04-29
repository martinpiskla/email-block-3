Feature: Send an email via Gmail

  Scenario: 01. User logs into Gmail web application, creates an email, selects recipient from contact list,
  adds attachment, sends an email and logs out

    Given I open Gmail page
    When I execute login with:
      | Username | $Env.EMAIL_USERNAME |
      | Password | $Env.EMAIL_PASSWORD |
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



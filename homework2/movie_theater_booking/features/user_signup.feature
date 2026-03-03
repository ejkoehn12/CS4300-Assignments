Feature: User is able make a account

Scenario: Use the website signup portal
      Given User wants to create a account
      And User has navigated to the signup page
      When we enter a new username and password
      Then the user should be register a account

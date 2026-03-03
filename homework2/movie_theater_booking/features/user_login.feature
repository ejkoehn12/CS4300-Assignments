Feature: User is able to login

Scenario: Use the website login portal
      Given User has created a account
      And User has navigated to the login page
      When we enter a username and password
      Then the user should be logged in

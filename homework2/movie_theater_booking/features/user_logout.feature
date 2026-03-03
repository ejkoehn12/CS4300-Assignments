
Feature: User is able to log out
      Scenario: User is able to log out
            Given User has created a account
            Given User is logged in
            When User has clicked the logout button
            Then User should be logged out
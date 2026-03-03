Feature: User is booking tickets for a movie

Scenario: Use the website login portal
      Given User logged into a account
      Given There are movies to be booked
      When User has clicks on the book button for a movie
      Then the user should be able to select a seat
      Then the user should be able to click book selected 

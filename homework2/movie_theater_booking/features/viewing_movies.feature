Feature: User is able to view currently open movies

Scenario: Use the website homepage to view current movies
      Given There are movies
      Given User has navigated to the homepage
      Then the user should be able to see open movies to book

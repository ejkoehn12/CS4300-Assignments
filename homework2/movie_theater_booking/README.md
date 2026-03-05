Name: Ethan Koehn
Date: 3/5/26
School: University of Colorado Colorado Springs
Class: Advanced Software Engineering (CS 4300 001)
Assignment: Homework 2

Overview:

As this assignment is a django centric assignment I tried to follow proper django standards for where items were located. Majority of important code can be found inside of the bookings directory, it contains everything important to the assignment with the exception of a few things for user authentication which lives in ./accounts/. 

Inside of ./bookings/ you can find all of the website logic for things like booking movies, viewing movies, and also the test cases that have been created to make sure proper functionality exists. In order to find Behave tests you will need to look inside of the ./bookings directory.

How to Run:

Online Via Render at: https://cs4300-assignments.onrender.com


Locally by running: python -m gunicorn mysite.asgi:application -k uvicorn.workers.UvicornWorker

Misc: 
Admin Credentials
      Admin Username: administrator
      Admin Password: fNR]rdiTU}2hi_0T91}/,VRSm

AI Disclosure: Use of AI was used in this assignment, primarly Microsoft Copilot and its integration into Microsoft Visual Studio Code for the following purposes
      - HTML/CSS creation
      - Troubleshooting code errors
      - formatting issues
      - Logical questions and suggestions

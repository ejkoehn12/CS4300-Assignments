from django.urls import reverse
from django.test import Client
from behave import given, when, then
from django.contrib.auth.models import User
@given('User wants to create a account')
def step_user_wants_to_create_account(context):
      context.client = Client()
@given('User has navigated to the signup page')
def step_user_navigates_to_signup(context):
      context.signup_url = reverse('sign_up')  
      response = context.client.get(context.signup_url)
      assert response.status_code == 200, f"Signup page returned {response.status_code}"
@when('we enter a new username and password')
def step_enter_signup_credentials(context):
      context.username = 'newuser'
      context.password = 'newpass123'
      context.response = context.client.post(context.signup_url, {
            'username': context.username,
            'password1': context.password,
            'password2': context.password
      })
@then('the user should be register a account')
def step_user_can_login_with_new_account(context):
      # Verify the user was created successfully
      assert User.objects.filter(username=context.username).exists(), "User was not created"
      
      # Attempt to log in with the new account
      login_url = reverse('login') 
      login_response = context.client.post(login_url, {
            'username': context.username,
            'password': context.password
      })
      assert login_response.wsgi_request.user.is_authenticated, "User is not authenticated after signup"
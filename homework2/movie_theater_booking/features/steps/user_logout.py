from behave import given, when, then
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse 

@given('user has a account')
def step_user_created_account(context):
      """Create a test user account"""
      context.username = 'testuser'
      context.password = 'testpass123'
      context.user = User.objects.create_user(
            username=context.username,
            password=context.password
      )
      context.client = Client()

@given('User is logged in')
def step_user_logged_in(context):
      login_url = reverse('login') 
      context.response = context.client.post(login_url,{
            'username': context.username,
            'password': context.password
        })
      assert context.response.wsgi_request.user.is_authenticated, "User is not authenticated after login"
@when('User has clicked the logout button')
def step_user_clicks_logout(context):
      """Simulate clicking the logout button"""
      context.logout_url = reverse('logout')  
      context.response = context.client.get(context.logout_url)
@then('User should be logged out')
def step_user_should_be_logged_out(context):
      """Verify the user is logged out"""
      assert context.client.session.get('_auth_user_id') is None, "User is still authenticated"
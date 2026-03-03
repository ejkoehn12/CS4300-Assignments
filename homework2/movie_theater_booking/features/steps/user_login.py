from behave import given, when, then
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

@given('User has created a account')
def step_user_created_account(context):
    """Create a test user account"""
    context.username = 'testuser'
    context.password = 'testpass123'
    context.user = User.objects.create_user(
        username=context.username,
        password=context.password
    )
    context.client = Client()

@given('User has navigated to the login page')
def step_navigate_to_login(context):
    """Navigate to the login page"""
    context.login_url = reverse('login') 
    response = context.client.get(context.login_url)
    assert response.status_code == 200, f"Login page returned {response.status_code}"

@when('we enter a username and password')
def step_enter_credentials(context):
    """Submit login form with username and password"""
    context.response = context.client.post(
        context.login_url,
        {
            'username': context.username,
            'password': context.password
        }
    )

@then('the user should be logged in')
def step_user_logged_in(context):
    """Verify the user is logged in"""
    assert context.client.session.get('_auth_user_id') is not None, "User is not authenticated"
    # Alternative: check if user is in the response context
    assert int(context.client.session.get('_auth_user_id')) == context.user.id

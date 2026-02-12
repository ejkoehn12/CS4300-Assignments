import sys
import os
#Task: Run Test cases for task3.py

#Pointing src outside of the test folder over into the src folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import task3

#Test Function for check_sign()
def test_check_sign():
    test_case_positive = 1
    test_case_negative = -1
    test_case_zero = 0

    assert task3.check_sign(test_case_positive) == "positive"
    assert task3.check_sign(test_case_negative) == "negative"
    assert task3.check_sign(test_case_zero) == "zero"
    


#Test function for get_prime_numbers()
def test_get_prime_numbers():
    test_pass_status = True
    test_case = task3.get_prime_numbers()
    test_list_of_prime_numbers = [2,3,5,7,11,13,17,19,23,29]
    if test_case != test_list_of_prime_numbers:
        test_pass_status = False
    
    assert test_pass_status == True

#Test function for find_sum()
def test_find_sum():
    test_case = task3.find_sum()
    test_expect_result = 5050

    assert test_case == test_expect_result
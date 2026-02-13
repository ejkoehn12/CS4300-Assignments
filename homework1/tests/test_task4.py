import sys
import os
#Task: Run Test cases for task4.py

#Pointing src outside of the test folder over into the src folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import task4

#Test function for calculate_discount()
def test_calculate_discount():
    int_test_case_price = 300
    float_test_case_price = 500.0
    int_test_case_discount = 20
    float_test_case_discount = 50.0

    assert task4.calculate_discount(int_test_case_price, int_test_case_discount) == 240
    assert task4.calculate_discount(int_test_case_price, float_test_case_discount) == 150.0
    assert task4.calculate_discount(float_test_case_price, int_test_case_discount) == 400.0
    assert task4.calculate_discount(float_test_case_price, float_test_case_discount) == 250.0
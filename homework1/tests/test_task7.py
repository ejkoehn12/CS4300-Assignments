import sys
import os
#Task: Run Test cases for task7.py

#Pointing src outside of the test folder over into the src folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import task7

#Function to test and make sure that calculate_mean() is working as intended
test_case = [1,2,3,4,5]
expected_ouput = 3.0
def test_calculate_mean():
    test_output = task7.calculate_mean(test_case)
    assert test_output == expected_ouput

import sys
import os
#Task: Run Test cases for task2.py

#Pointing src outside of the test folder over into the src folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import task2


#Checking to make sure task2 int function returns a int
def test_int():
    assert isinstance(task2.return_integer(), int)

#Checking to make sure task2 floating point function returns a float
def test_float():
    assert isinstance(task2.return_float(), float)

#Checking to make sure task 2 string function returns a string
def test_string():
    assert isinstance(task2.return_string(), str)

#Checking to make sure task 2 boolean function returns correct data type
def test_bool():
    assert isinstance(task2.return_Bool(), bool)

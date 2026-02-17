import sys
import os
#Task: Run Test cases for task6.py

#Pointing src outside of the test folder over into the src folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import task6

#Function to test output of count_file_contents()
def test_count_file_contents():
    #Getting the output from the function in task6
    num_of_words_in_file = task6.count_file_contents()
    #Checking and making sure that the two outputs are the same as the known number of words in the file
    assert num_of_words_in_file == 162
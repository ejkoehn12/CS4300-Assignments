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

    #Independaently getting the number of words from the file
    file_name = "/home/student/CS4300-Assignments/homework1/src/task6_read_me.txt"
    with open(file_name, 'r') as file:
        file_content = file.read()
    split_file_content = file_content.split(" ")
    
    #Checking and making sure that the two outputs are the same
    assert num_of_words_in_file == len(split_file_content)
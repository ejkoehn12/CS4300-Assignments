import sys
import os
#Task: Run Test cases for task4.py

#Pointing src outside of the test folder over into the src folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import task5

def test_return_list_of_books():
    correct = True
    list_of_books = task5.return_first_three_list_of_books()
    correct_list_of_books = ["Leviathan Wakes", "Calibans War", "The Eye of the World"]
    assert list_of_books == correct_list_of_books
       
    
    


#Test function for return_student_database()
def test_return_student_database():
    student_database = task5.return_student_database()
    assert str(student_database[0].get("student_name")) == "John" and student_database[0].get("student_id") == 1234
    assert str(student_database[1].get("student_name")) == "Will" and student_database[1].get("student_id") == 5678
    assert str(student_database[2].get("student_name")) == "Logan" and student_database[2].get("student_id") == 9101

import subprocess
import os
#Task: Write a test function to make sure that task1.py is returning "Hello World!"


TestCase = "Hello World!"
#Function to test and make sure output equals the TestCase variable
def test_result():
    assert runTask1() == TestCase
#Function to run and catch output of task1.py   
def runTask1():
    base_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(base_dir, ".."))
    task_path = os.path.join(project_root, "src", "task1.py")
    command = ["python", task_path]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    #Need to use .strip() on result to get rid of hidden \n that might show up
    captured_stdout = result.stdout.strip()
    return captured_stdout




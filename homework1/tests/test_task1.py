import subprocess
#Task: Write a test function to make sure that task1.py is returning "Hello World!"

#Function to run and catch output of task1.py

TestCase = "Hello World!"

def test_result():
    assert runTask1() == TestCase
    
def runTask1():
    command = ["python", "../src/task1.py"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    #Need to use .strip() on result to get rid of hidden \n that might show up
    captured_stdout = result.stdout.strip()
    return captured_stdout




#Function to open task6_read_me.txt and output the number of words in the file
def count_file_contents():
    file_name = "/home/student/CS4300-Assignments/homework1/src/task6_read_me.txt"
    with open(file_name, 'r') as file:
        file_content = file.read()

    split_file_content = file_content.split(" ")
    return len(split_file_content)
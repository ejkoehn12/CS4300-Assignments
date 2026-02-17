list_of_books = [["Leviathan Wakes","James Corey"],["Calibans War", "James Corey"],["The Eye of the World","Robert Jordan"],["The Way of Kings","Brandon Sanderson"],["Mistborn","Brandon Sanderson"]]

#Function to return the list_of_boots variable
def return_first_three_list_of_books():
    index = 0
    return_Var = []
    for item in list_of_books:
        if index < 3:
            return_Var.append(item[0])
            index += 1
        else:
            break
    return return_Var


student1 = {"student_name": "John", "student_id": 1234}
student2 = {"student_name": "Will", "student_id": 5678}
student3 = {"student_name": "Logan", "student_id": 9101}
student_database = [student1, student2, student3]

#Function to return student_database variable
def return_student_database():
    return student_database


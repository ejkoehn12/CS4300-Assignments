

#Function to check if a given number if positive, negative, or zero
def check_sign(num):
    if num > 0:
        return "positive"
    elif num == 0:
        return "zero"
    elif num < 0:
        return "negative"
    else:
        return "not a number"
  

#Function to get out the first 10 prime numbers
def get_prime_numbers():
    list_of_prime_numbers = []
    index = 2
    while len(list_of_prime_numbers) < 10:
        if is_prime(index) is True:
            list_of_prime_numbers.append(index)
            index += 1
        else:
            index +=1
    return list_of_prime_numbers
#Helper function for get_prime_numbers()      
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) +1):
        if num % i == 0:
            return False
    return True


#Function to find the sum of all numbers from 1 to 100
def find_sum():
    total_sum = 0
    end_index = 101
    index = 1
    while index < end_index:
        total_sum+=index
        index+=1
    return total_sum
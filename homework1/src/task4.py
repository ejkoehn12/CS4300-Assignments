

#Function to calculate discount using a base price input and a discount input as a percentage
def calculate_discount(base_price, base_discount):
    if is_number(base_price) and is_number(base_discount):
        discount = base_price * base_discount/100
        print(discount)
        return base_price - discount
    else:
        return "Error, a non numeric character was entered"

#Function to help with verifiying that a number has been inputted
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
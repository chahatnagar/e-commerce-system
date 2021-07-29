import variables
import datetime

#Function to login user inside the main application function by fetching details from the user table
def login_function():
    variables.login_detail = input("Enter email address or phone number: ")
    variables.password = input("Enter password: ")
    query = "SELECT email_id, phone_number, password, user_id from users"
    return (query)

#Function used to sign up a new account for the user
def signup_function():
    variables.name = input("Enter your first name: ").capitalize()
    variables.surname = input("Enter your last name: ").capitalize()
    variables.email_id = input("Enter email address: ")
    variables.password = input("Enter password: ")
    variables.phone_number = input("Enter phone number: ")
    variables.address = input("Enter delivery address: ").capitalize()
    query = "INSERT INTO users (name_user, surname_user, email_id, password, address, phone_number) values('%s', '%s', '%s', '%s', '%s', '%s')"%(variables.name, variables.surname, variables.email_id,variables.password,variables.address,variables.phone_number)
    return(query)

#Function for returning user related information by fetching details from user table either by using email or phone number
def user_information(log_det_val):
    if ".com" in log_det_val:
        query = "SELECT name_user,surname_user,address,phone_number from users where email_id = '%s'"%(log_det_val)
    else:
        query = "SELECT name_user,surname_user,address,phone_number from users where phone_number = '%s'"%(log_det_val)
    return(query)

#Special admin function to view and edit the tables of the database
def admin_display_function():
    query = "SELECT * FROM users"
    return(query)

#Function to search and fetch product details from the product_table database
def product_search(product_name):
    query = "SELECT * FROM product_table where product_name like '%s' or product_type like '%s' or product_description like '%s'"%("%"+product_name+"%","%"+product_name+"%","%"+product_name+"%")
    return query

#Function containing query to add product inside the cart
def add_into_cart(product_name):
    query = "INSERT INTO product_table (cart) values('[%s]'')"%(product_name)

#Function to form new string by adding proper @split@ string between product names
def modified_cart_products_insertion(modified_list):
    final_insertion_string = ""
    for i in modified_list:
        final_insertion_string+=(i+'@split@')
    return final_insertion_string

#Function to form new string by adding @orders@ string between products of the list received as argument
def modified_order_insertion(modified_orders):
    final_insertion_string = ""
    for i in modified_orders:
        final_insertion_string+=(i+'@orders@')
    return final_insertion_string

#Function to form a new string by adding @wishlist@ string between products of the list received as argument
def modified_wishlist_insertion(modified_wishlist):
    final_insertion_string = ""
    for i in modified_wishlist:
        final_insertion_string+=(i+'@wishlist@')
    return final_insertion_string

#Function to return pickup date after 5 days of submitting return request
def five_day_from_now():
    a = datetime.date.today() + datetime.timedelta(days=5)
    return a.strftime("%d-%b-%y")

#Function to clear the screen upto 50 lines
def cls():
    print("\n"*50)

import mysql.connector as my
import function
import variables

con = my.connect(user="root",password="chagar@85200258",host="localhost",database="madyum")

cur1 = con.cursor()

#Access Function
#Access to the main application is given by this function

def access_function():
    function.cls()
    print("========================Welcome to MADYUM========================")
    try:

        op1 = int(input("1. Login\n2. Sign Up\n3. Admin Login"))

        #Operations for the main menu panel

        #Operation for logging in existing accounts
        if op1==1:
            cur1.execute(function.login_function())
            res = cur1.fetchall()
            if ".com" in variables.login_detail:
                variables.email_id = variables.login_detail
            else:
                variables.phone_number = variables.login_detail
            for i in res:
                if (i[0]==variables.email_id or i[1]==variables.phone_number) and i[2]==variables.password:
                    print("Login Successful")
                    cur1.execute(function.user_information(variables.login_detail))
                    res1 = cur1.fetchone()
                    application_function(res1[0].strip(" "),i[-1],res1[1].strip(" "),res1[2].strip(" "),res1[3].strip(" "))
                    break;

                elif (str(variables.email_id) in str(res) or str(variables.phone_number) in str(res)) and str(variables.password) in str(res):
                    continue
                else:
                    print("Incorrect Login Details. Please Try Again...")
                    access_function()

        #Operation to sign up a new account
        elif op1==2:
            cur1.execute(function.signup_function())
            con.commit()
            print("Please wait...")
            function.cls()
            print("Login in with your new sign up details")
            access_function()

        #Operation to access administration settings
        elif op1==3:
            def admin():
                user = input("Enter admin username: ")
                password = input("Enter admin password: ")
                if (user == "chahat0014" and password =="chagar123") or (user == "prasad" and password =="prasad123"):
                    def admin_main_panel():
                        function.cls()
                        print("===============Welcome to Admin Panel===============")
                        admin_op1 = int(input("1. Access Database \n2. Return to main panel"))

                        #Admin panel operations

                        #Operation to access entire database of users
                        if admin_op1 == 1:
                            admin_op2 = int(input("1. User Database\n2. Product Database"))

                            #Operation to choose the users table
                            if admin_op2 == 1:
                                cur1.execute("SELECT * FROM users")
                                res = cur1.fetchall()
                                for i in res:
                                    print(i,"\n")

                                #Admin authorization and commands to control and administer database
                                admin_auth_cmds = int(input("1. Return to admin panel \n2. Make Changes"))
                                if admin_auth_cmds == 1:
                                    admin_main_panel()

                            #Operation to choose the product_table
                            elif admin_op2 == 2:
                                cur1.execute("SELECT * FROM product_table")
                                res = cur1.fetchall()
                                for i in res:
                                        print(i,"\n")

                                #Admin authorization and commands to control and administer database
                                admin_auth_cmds = int(input("1. Return to admin panel \n2. Make Changes"))
                                if admin_auth_cmds == 1:
                                    admin_main_panel()

                            else:
                                admin_main_panel()


                        #Operation to return to access function/main panel
                        elif admin_op1 == 2:
                                access_function()

                    admin_main_panel()

                #When incorrect login details are given by the user
                else:
                    print("Incorrect Admin Login Details. Try Again")
                    function.cls()
                    access_function()

        #Calling admin function to access the admin settings
        admin()

    except:
        access_function()

#Applications Operation Function
#After logging in or signing up the application_function is executed to operate and use the main functioning of the Applications

def application_function(username,user_identification,last_name,address,phn_num):
    function.cls()
    print("Hey there!",username+". Welcome to Madyum!\n")
    variables.user_id=user_identification

    try:
        app_input = int(input("1. Search for a product \n2. What's in my cart! \n3. Orders in progess... \n4. Wishlist \n5. Previous Orders \n6. Request a return \n7. Customer Care Complain Form \n8. Terms & Conditions \n9. Account Settings \n10. Not "+username+"? Logout."))
        #Operation to search for a product in the database
        if app_input == 1:
            function.cls()
            product_list = []
            product_query = input(("What are you looking for?"))
            cur1.execute(function.product_search(product_query))
            desired_products = cur1.fetchall()
            for i in desired_products:
                print(str((desired_products.index(i))+1)+".","    Product Name:",i[3],"\n        Price: ₹",i[4],"\n        Product Description:",i[1],"\n        Product Type: ",i[2],"\n")
                individual_product_detail = [i[3],i[4]]
                product_list.append(individual_product_detail)
            gen_op = int(input(("1. Buy \n2. Add to Cart \n3. Add to Wishlist \n4. Return to Main Menu")))

            #Operation to buy a product
            if gen_op == 1:

                #Function to choose mode of payment
                def payment_gateway():
                    print("SELECT MODE OF PAYMENT\n1. Pay On Delivery\n2. Use Card")
                    payment_op = input()
                    if payment_op == "1":
                        print("MODE OF PAYEMENT: Pay On Delivery")
                    elif payment_op == "2":
                        cur1.execute("SELECT bank_details from users where user_id=%s"%(user_identification,))
                        bank_dtls_raw = cur1.fetchone()[0]
                        bank_dtls = bank_dtls_raw.split('@card@')
                        for i in bank_dtls:
                            if i =="":
                                continue
                            else:
                                j = i.split(":")
                                print(str(bank_dtls.index(i)+1)+".","Name on Card: ",j[0],"\nAccount Number: ",j[1], "\nExp. Date: ",j[3],"\n")
                        card_select = int(input("Select card for payment\n"))
                        card_number = card_select-1
                        cvv = input("Enter CVV Number\n")
                        if cvv == bank_dtls[card_number].split(':')[2]:
                            print("MODE OF PAYEMENT: Debit/Credit Card")
                        else:
                            payment_gateway()

                #Function to place an order
                def order_confirmation(username,last_name,address,phn_num,user_identification):
                    buy_operation = int(input("Enter product number to buy"))
                    payment_gateway()
                    function.cls()
                    print("REVIEW YOUR ORDER\n")
                    print("Shipping Address: ")
                    print(username,last_name)
                    print(address)
                    print("Phone: ",phn_num,"\n\n")
                    product_name = product_list[buy_operation-1][0]
                    print("Product Name: ",product_name)
                    product_price = product_list[buy_operation-1][1]
                    print("Price: ₹",product_price)
                    order_confirmation = int(input("1. Place your order \n2. Cancel? Return to main menu"))

                    #Operation to place the final order
                    if order_confirmation==1:
                        final_order_details = product_name+":"+str(product_price)+"@orders@"
                        cur1.execute("UPDATE users SET orders = '%s' where user_id = %s"%(final_order_details,user_identification,))
                        con.commit()
                        print("Order successfully placed! \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nCustomers also bought")
                        cur1.execute("SELECT product_type from product_table where product_name = '%s'"%(product_name))
                        product_type = cur1.fetchone()
                        cur1.execute("SELECT * FROM product_table where product_type = '%s'"%(product_type))
                        suggestion_products = cur1.fetchmany(5)
                        for i in suggestion_products:
                            print(str((suggestion_products.index(i))+1)+".","    Product Name:",i[3],"\n        Price: ₹",i[4],"\n        Product Description:",i[1],"\n        Product Type: ",i[2],"\n")
                            individual_product_detail = [i[3],i[4]]
                            product_list.append(individual_product_detail)
                        suggestion_products_loop = int(input("1. Enter product number to buy  \n2. Return to main menu"))
                        if suggestion_products_loop == 1:
                            order_confirmation(username,last_name,address,phn_num,user_identification)
                        elif suggestion_products_loop == 2:
                            application_function(username,user_identification,last_name,address,phn_num)

                    #Operation to cancel the order and return back to the main menu by calling main menu function
                    elif order_confirmation==2:
                        application_function(username,user_identification,last_name,address,phn_num)
                order_confirmation(username,last_name,address,phn_num,user_identification)

            #Operation to insert desired product in the users cart by inserting product_name and product_price in the cart column of the users table
            elif gen_op == 2:
                prod_num_to_be_added_in_cart = int(input("Enter product number to add to cart"))
                cur1.execute("SELECT cart from users where user_id=%s"%(user_identification))
                old_cart = str(cur1.fetchone()).lstrip("('").rstrip("',)")
                new_cart_item = product_list[prod_num_to_be_added_in_cart-1][0]+":"+(str(product_list[prod_num_to_be_added_in_cart-1][1]))+"@split@"
                final_cart_item = (old_cart+new_cart_item)
                cur1.execute("UPDATE users set cart = '%s' where user_id = %s"%(final_cart_item,user_identification,))
                con.commit()
                print("Item successfully Added To Cart")
                gen_op1 = input("1. Click anywhere to return to main menu")
                if gen_op1 == "":
                    application_function(username,user_identification,last_name,address,phn_num)
                else:
                    application_function(username,user_identification,last_name,address,phn_num)

            #Operation to add product to the wishlist of the user
            elif gen_op==3:
                prod_num_to_be_added_to_wishlist = int(input("Enter product number to add to wishlist"))
                cur1.execute("SELECT wishlist from users where user_id=%s"%(user_identification))
                old_wishlist = str(cur1.fetchone()).lstrip("('").rstrip("',)")
                new_wishlist_item = product_list[prod_num_to_be_added_to_wishlist-1][0]+":"+(str(product_list[prod_num_to_be_added_to_wishlist-1][1]))+"@wishlist@"
                final_wishlist_item = (old_wishlist+new_wishlist_item)
                cur1.execute("UPDATE users set wishlist = '%s' where user_id = %s"%(final_wishlist_item,user_identification,))
                con.commit()
                print("Item successfully Added To Wishlist")
                gen_op1 = input("1. Click anywhere to return to main menu")
                if gen_op1 == "":
                    application_function(username,user_identification,last_name,address,phn_num)

            #Operation to return back to the main menu
            elif gen_op==4:
                application_function(username,user_identification,last_name,address,phn_num)

        #Operation to see what's in the cart of the user
        elif app_input == 2:
            cur1.execute("SELECT cart FROM users WHERE user_id = %s"%(user_identification,))
            cart_items_raw = cur1.fetchone()[0]
            try:

                if cart_items_raw[0]!='':
                    print("\n",username,"'s Cart \n")
                    cart_items = str(cart_items_raw).split('@split@')
                    del cart_items[-1]
                    for i in cart_items:
                        if i=="'":
                            continue
                        else:
                            indiv_details_cart = i.split(':')
                            print(str(cart_items.index(i)+1)+".","Product Name: ",indiv_details_cart[0].lstrip("''"),"\n"+"    Price: ₹",indiv_details_cart[1].strip("'"),"\n\n")

                    #Operation to delete a product from the cart by updating the existing string with modified string
                    my_cart_op = int(input("1. Delete an item from cart \n2. Return to main menu"))
                    if my_cart_op == 1:
                        my_cart_modify_input = int(input("Enter product number to delete it from cart"))
                        del cart_items[my_cart_modify_input-1]
                        final_cart_string = function.modified_cart_products_insertion(cart_items)
                        insertion_string = final_cart_string.lstrip("'").rstrip("'@split@")
                        query = "UPDATE users set cart = '%s' where user_id = %s"%(insertion_string,user_identification,)
                        cur1.execute(query)
                        con.commit()
                        print("Item successfully deleted")
                        application_function(username,user_identification,last_name,address,phn_num)
                    elif my_cart_op == 2:
                        application_function(username,user_identification,last_name,address,phn_num)

            except:
                print("Your cart is empty")
                inp = input("Click anywhere to return to main menu")
                if inp == "":
                    application_function(username,user_identification,last_name,address,phn_num)
                else:
                    application_function(username,user_identification,last_name,address,phn_num)

        #Operation to check the orders in progress
        elif app_input == 3:
            cur1.execute("SELECT orders from users where user_id = %s"%(user_identification,))
            order_details_raw = cur1.fetchone()

            try:
                if order_details_raw[0]!='':
                    print("\n\nOrders in progress...\n")
                    order_details = (str(order_details_raw).lstrip('[("')).rstrip('",)]').split('@orders@')
                    for i in order_details:
                        if i=="'":
                            continue
                        else:
                            indiv_details_orders = i.split(':')
                            print(str(order_details.index(i)+1)+".","Product Name: ",indiv_details_orders[0].lstrip("''"),"\n"+"   Price: ₹",indiv_details_orders[1].strip("'"),"\n\n")

                    #Operation to cancel an order in progress
                    my_orders_op = int(input("1. Delete order in progress \n2. Return to main menu"))
                    if my_orders_op == 1:
                        my_order_modify_input = int(input("Enter product number to cancel the order"))
                        del order_details[my_order_modify_input-1]
                        final_order_string = function.modified_order_insertion(order_details)
                        insertion_string = final_order_string.lstrip("'").rstrip("'@orders@")
                        print(insertion_string)
                        query = "UPDATE users set orders = '%s' where user_id = %s"%(insertion_string,user_identification,)
                        cur1.execute(query)
                        con.commit()
                        print("Order Cancelled")
                        application_function(username,user_identification,last_name,address,phn_num)

                    elif my_orders_op == 2:
                        application_function(username,user_identification,last_name,address,phn_num)

            except:
                print("You don't have any orders in progress")
                inp = input("Click anywhere to return to main menu")
                if inp == "":
                    application_function(username,user_identification,last_name,address,phn_num)
                else:
                    application_function(username,user_identification,last_name,address,phn_num)

        #Operation to review the wishlist of the user
        elif app_input == 4:
            cur1.execute("SELECT wishlist from users where user_id = %s"%(user_identification,))
            wishlist_raw = cur1.fetchone()

            try:
                if wishlist_raw[0]!='':
                    print("Your Wishlist\n")
                    wishlist = (str(wishlist_raw).lstrip('[("')).rstrip('",)]').split('@wishlist@')
                    for i in wishlist:
                        if i=="'":
                            continue
                        else:
                            indiv_details_wishlist = i.split(':')
                            print(str(wishlist.index(i)+1)+".","Product Name: ",indiv_details_wishlist[0].lstrip("''"),"\n"+"   Price: ₹",indiv_details_wishlist[1].strip("'"),"\n\n")

                    #Operation to delete product from the wishlist
                    my_wishlist_op = int(input("1. Delete product from wishlist \n2. Return to main menu"))
                    if my_wishlist_op == 1:
                        my_wishlist_modify_input = int(input("Enter product number to delete product from wishlist"))
                        del wishlist[my_wishlist_modify_input-1]
                        final_order_string = function.modified_wishlist_insertion(wishlist)
                        insertion_string = final_order_string.lstrip("'").rstrip("'@wishlist@")
                        print(insertion_string)
                        query = "UPDATE users set wishlist = '%s' where user_id = %s"%(insertion_string,user_identification,)
                        cur1.execute(query)
                        con.commit()
                        print("Product removed from wishlist")
                        application_function(username,user_identification,last_name,address,phn_num)

                    elif my_wishlist_op == 2:
                        application_function(username,user_identification,last_name,address,phn_num)

            except:
                print("Your wishlist is empty")
                inp = input("Click anywhere to return to main menu")
                if inp == "":
                    application_function(username,user_identification,last_name,address,phn_num)
                else:
                    application_function(username,user_identification,last_name,address,phn_num)

        #Operation to see the previous orders made by the user
        elif app_input == 5:
            cur1.execute("SELECT previous_orders FROM users WHERE user_id = %s"%(user_identification,))
            previous_orders_raw = cur1.fetchone()[0]
            print("Previous Orders\n")
            prev_orders = str(previous_orders_raw).split('@prevorder@')
            for i in prev_orders:
                if i == "":
                    continue
                else:
                    prev_items = i.split(':')
                    print(str(prev_orders.index(i)+1)+". Product Name: ",prev_items[0],"\n    Price: ₹"+str(prev_items[1]))
            gen_op = input("Press any key to return to main menu")
            if gen_op == "":
                application_function(username,user_identification,last_name,address,phn_num)
            else:
                application_function(username,user_identification,last_name,address,phn_num)

        #Operation to return a request for the product by inserting product details inside the return_request column
        elif app_input == 6:
            print("Select product you want to return")
            cur1.execute("SELECT previous_orders FROM users WHERE user_id = %s"%(user_identification,))
            previous_orders_raw = cur1.fetchone()[0]
            print("Previous Orders\n")
            prev_orders = str(previous_orders_raw).split('@prevorder@')
            for i in prev_orders:
                if i == "":
                    continue
                else:
                    prev_items = i.split(':')
                    print(str(prev_orders.index(i)+1)+". Product Name: ",prev_items[0])

            gen_op   = input("\n1. Continue return request \n2. Return to main menu\n")
            if gen_op == "1":
                cur1.execute("SELECT return_request from users where user_id = %s"%(user_identification,))
                prev_requests = cur1.fetchone()[0]
                prod_number = input("Enter product number of item to be returned: \n")
                return_product_string = prev_requests+(prev_orders[int(prod_number)-1])+"@return@"
                cur1.execute("UPDATE users set return_request = '%s' where user_id = %s"%(return_product_string,user_identification,))
                con.commit()
                print("Your Return Summary\n")
                print("Pickup by\t\t\t\t\tPickup Address\n"+function.five_day_from_now()+"\t\t\t\t\t"+address,"\nItem: ",prev_orders[int(prod_number)-1],"\n\nWe will pick up the item shortly and the refund will be initiated within 1 day of the item being picked up.")
                gen_input = input("\nPress any button to continue to main menu")
                if gen_input == "":
                    function.cls()
                    application_function(username,user_identification,last_name,address,phn_num)
            else:
                application_function(username,user_identification,last_name,address,phn_num)

        #Operation to register a complain
        elif app_input == 7:
            complain = input("Enter your complain briefly...\n")
            cur1.execute("UPDATE users set customer_complain = '%s' where user_id = %s"%(complain, user_identification,))
            print("Complain registered successfully. Our customer care executive will soon contact you. Hope your problem gets resolved:)")
            gen_op = input("Press any key to move to main menu")
            if gen_op == "":
                application_function(username,user_identification,last_name,address,phn_num)
            else:
                application_function(username,user_identification,last_name,address,phn_num)

        #Operation to display terms and policies of the working of the company
        elif app_input == 8:
            print("T&C")
            gen_op = input()
            if gen_op == "":
                application_function(username,user_identification,last_name,address,phn_num)
            else:
                application_function(username,user_identification,last_name,address,phn_num)


        #Opertion to review and make changes to user acccount details
        elif app_input == 9:
            def account_settings(username,user_identification,last_name,address,phn_num):
                function.cls()
                cur1.execute("SELECT * FROM users WHERE user_id = %s"%(user_identification,))
                i = cur1.fetchone()
                print("\nGENERAL SETTINGS\n")
                print("1. Name: ",i[7],i[8])
                print("2. Email Address: ",i[1])
                print("3. Phone Number: ", i[4])
                print("4. Address: ",i[3])
                print("5. Change Password")
                print("6. Add Debit/Credit Card")
                account_settings_op = input("\n\n1. Edit Details\n2. Back to main menu")
                if account_settings_op == "1":
                    setting_op = input("Enter number to edit detail...\n")
                    if setting_op == "1":
                        print("CHANGE YOUR NAME\n")
                        fname = input("Enter your first name")
                        sname = input("Enter your second name")
                        cur1.execute("UPDATE users set name_user = '%s', surname_user = '%s' where user_id = %s"%(fname,sname,user_identification,))
                        con.commit()
                        print("Changes made successfully")
                        account_settings(fname,user_identification,last_name,address,phn_num)

                    elif setting_op == "2":
                        print("CHANGE YOUR EMAIL\n")
                        email = input("Enter your email address")
                        cur1.execute("UPDATE users set email_id = '%s' where user_id = %s"%(email, user_identification,))
                        con.commit()
                        print("Changes made successfully")
                        account_settings(username,user_identification,last_name,address,phn_num)

                    elif setting_op == "3":
                        print("CHANGE YOUR PHONE NUMBER\n")
                        pnum = input("Enter your phone number")
                        cur1.execute("UPDATE users set phone_number='%s' where user_id = %s"%(pnum,user_identification,))
                        con.commit()
                        print("Changes made successfully")
                        account_settings(username,user_identification,last_name,address,phn_num)

                    elif setting_op == "4":
                        print("CHANGE YOUR ADDRESS\n")
                        address = input("Enter your address")
                        cur1.execute("UPDATE users set address = '%s' where user_id = %s"%(address,user_identification,))
                        con.commit()
                        print("Changes made successfully")
                        account_settings(username,user_identification,last_name,address,phn_num)

                    elif setting_op == "5":
                        def pass_change(user_identification):
                            print("CHANGE YOUR PASSWORD\n")
                            pass_ = input("Enter your password")
                            cpass_ = input("Confirm your password")
                            if pass_==cpass_:
                                cur1.execute("UPDATE users set password='%s' where user_id = %s"%(cpass_,user_identification,))
                                con.commit()
                                print("Changes made successfully")
                                account_settings(username,user_identification,last_name,address,phn_num)
                            elif pass_!=cpass_:
                                print("Password doesn't seem to match\nTry Again")
                                pass_change(user_identification)
                        pass_change(user_identification)

                    elif setting_op == "6":
                        print("ADD DEBIT/CREDIT CARD")
                        name = input("Name on the card: ")
                        account_number = input("Account Number")
                        cvv = input("CVV: ")
                        expdate = input("Exp. Date: ")
                        bank_dtls = name+":"+account_number+":"+cvv+":"+expdate+"@card@"
                        cur1.execute("SELECT bank_details from users where user_id = %s"%(user_identification,))
                        old_dtls = cur1.fetchone()[0]
                        new_dtls = old_dtls+bank_dtls
                        cur1.execute("UPDATE users set bank_details='%s' where user_id = %s"%(new_dtls,user_identification,))
                        con.commit()
                        print("Changes made successfully")
                        account_settings(username,user_identification,last_name,address,phn_num)

                    else:
                        account_settings(username,user_identification,last_name,address,phn_num)

                elif account_settings_op == "2":
                    application_function(username,user_identification,last_name,address,phn_num)

            account_settings(username,user_identification,last_name,address,phn_num)

        #Operation to logout from the session and return to main login page
        elif app_input == 10:
            access_function()

        #Operation to continue the program in case the user enters any other value than the expected input
        else:
            application_function(username,user_identification,last_name,address,phn_num)

    except:
        application_function(username,user_identification,last_name,address,phn_num)

#Calling Access Function which on provinding authentic credentials will give access to the main application
access_function()

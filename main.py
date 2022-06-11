from admin import *
from user import *

# import pandas as pd
import pandas as pd
import numpy as np
import re
from numpy import empty
from unicodedata import category
import warnings
from hashlib import new
import time
import ast
import sys
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=FutureWarning)


def import_dataframes():
    return pd.read_csv('admin_data.csv'), pd.read_csv('user_data.csv'), pd.read_csv('books_data.csv')

def export_dataframes(admin_df, user_df, books_df):
    admin_df.to_csv('admin_data.csv', index=False)
    user_df.to_csv('user_data.csv', index=False)
    books_df.to_csv('books_data.csv', index=False)


def login(df):

    
    flag = False
    username = input("Enter your username: ")
    for index in df.index:
        if df.loc[index,'username'].lower() == username.lower():
            #print("This username is taken by another user...Try another")
            correct_password = str(df.loc[index,'password'])
            user_id = int(df.loc[index,'id'])
            flag = True
            break

    if not flag:
        print("This username does not exist...\nTry sign up...")
        exit()
    
    else:
        tries=3
        while tries !=0:
            password = input("Enter your password: ")
            tries-=1
            if correct_password == password.lower():
                print("Welcome Back "+username+" !!!")
                return  user_id
            else:
                print("Wrong password. Try again...")
        
        print("Too many failed tries. Exiting...")
        exit()
       

def sign_up(df):

    def user_exists(new_username):
        for index in df.index:
            if df.loc[index,'username'].lower() == new_username.lower():
                #print("This username is taken by another user...Try another")
                return False
        return True

    new_username = input("To create a new account please enter a username: ")
    if not user_exists(new_username) or new_username.find("admin") != -1:
        print("\nThis username already exists or belongs to an admin!!!\nTry loggin in...\n")
        exit()
    
    new_id = df["id"].iloc[-1] + 1
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    while True:
        new_password = input("Enter a password (Password must contain: 1 symbol and length > 8): ")
        if  len(new_password) >= 8 and regex.search(new_password) != None:
            
            print("Enter some personal data: ")
            new_address = input("Enter your andress :")
            new_city = input("Enter your city: ")
            new_balance = input("Enter the amount of your balance: ")
            while not new_balance.isdigit():
                new_balance = input("Not a number. Enter the amount of your balance: ")
            new_balance = float(new_balance)

            print("Account created succesfully!!!. Select Log In to use your account... ")

            new_user = pd.Series({   
                                        'id': new_id,
                                        'username': new_username,
                                        'password': new_password,
                                        'address': new_address,
                                        'city': new_city,
                                        'orders':[],
                                        'favorites':[],
                                        'balance': new_balance 
                                    })

            df = df.append(new_user, ignore_index = True)
            return df
        else:
            print("Password not strong enough. Try different password")

 
 
########################################################################################################################################################################################
#################################################################################################################################################################################################           

#admin: True | user:False
#[False/True] [id]
current_login = []

admin_df, user_df, books_df = import_dataframes()

""" print(admin_df)
print(user_df)
print(books_df) """


#adding comments columm to books dataframe
books_df["comments"] = np.nan


print("Welcome to Book Management System\nPlease specify if you are ADMIN or USER:")
current_login.insert(0,True) if input().lower()=="admin"  else current_login.insert(0,False) 

while True:
    if current_login[0] == True:
        current_login.insert(1,login(admin_df))
        break
    elif current_login[0] == False:
        choice = input("1) Log In\n2) Sign Up\nEnter option: ")
        if choice =="1":
            current_login.insert(1,login(user_df))
            break
        elif choice =="2":
            user_df = sign_up(user_df)

""" current_login.insert(0, True)
current_login.insert(1, 2) """

while True:
    if current_login[0]:
        time.sleep(1)
        choice = input("\n\nADMIN Menu:\n0) Exit\n1) Add books (more than one)\n2) Add book\n3) Edit book\n4) Delete book\n5) Export updated books catalog\n6) Find book with title\n7) Print cost of a book\n8) Cost of all books per author/publisher\n9) Delete a user\n10) Print plots\nEnter your choice: ")
        if choice == "0":
            print("\n\nExiting...")
            print("\nByee....")
            break
        elif choice == "1":
            books_df = admin_add_books(books_df)
            
        elif choice == "2":
            books_df = admin_add_single_book(books_df)
            
        elif choice == "3":
            books_df = admin_edit_book(admin_df, books_df, current_login)
            
        elif choice == "4":
            books_df = admin_delete_book(admin_df, books_df, current_login)
            
        elif choice == "5":
            print("\nUpdated books catalog has been exported in 'updated_books.csv' file")
            books_df.to_csv('updated_books.csv', index=False)
            
        elif choice == "6":
            admin_search_with_title(books_df)
            
        elif choice == "7":
            admin_print_cost(books_df)
            
        elif choice == "8":
            admin_print_all_cost(books_df)
            
        elif choice == "9":
            user_df = admin_delete_user(user_df)
            
        elif choice == "10":
            admin_print_plots(books_df, user_df)
            
        else:
            print("\n\nNot an option...")

    if not current_login[0]:
        time.sleep(1)
        choice = input("\n\nUSER Menu:\n0) Exit\n1) Add books to favorites (more than one)\n2) Add book to favorites\n3) Edit personal info\n4) Empty favoritres list\n5) Check Balance\n6) Check price from favorites\n7) Check your orders\n8) Place Order \n9) Cancel Order \n10) Check number of copies you can order from a book \n11) Add comment\nEnter your choice: ")
        if choice == "0":
            print("\n\nExiting...")
            print("\nByee....")
            break
        elif choice == "1":
            user_df = user_add_favorites(user_df, current_login[1])
            
        elif choice == "2":
            user_df = user_add_single_favorite(user_df, books_df, current_login[1])
            
        elif choice == "3":
            user_df =  user_edit_info(user_df, current_login[1])
            print(user_df)
            
        elif choice == "4":
            user_df = user_empty_favorites(user_df, current_login[1])
            
        elif choice == "5":
            user_check_balance(user_df, current_login[1])
            
        elif choice == "6":
            user_check_favorites(user_df, books_df, current_login[1])
            
        elif choice == "7":
            user_orders_total(user_df, books_df, current_login[1])
            
        elif choice == "8":
            user_df = user_place_order(user_df, books_df, current_login[1])
            
        elif choice == "9":
            user_df = user_cancel_order(user_df, books_df, current_login[1])
            
        elif choice == "10":
            user_check_book_for_order(user_df, books_df, current_login[1])
            
        elif choice == "11":
            books_df = user_add_comments(books_df, current_login[1])
            
        else:
            print("\n\nNot an option...")


#export_dataframes(admin_df, user_df, books_df)
from admin import *

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

warnings.simplefilter(action='ignore', category=FutureWarning)


def login(df):
        df["username"] = df["username"].apply(str.lower)

        username = input("Enter username: ").lower()
        if df.loc[df['username'] == username].empty:
            print("This username does not exist!!!\nTry creating a new account...")
            exit()

        else:
            tries=3
            while tries !=0:
                password = input("Enter your password: ")
                tries-=1
                if str(df.loc[df['username'] == username].values[0][2]) == password:
                    print("Welcome Back "+str(df.loc[df['username'] == username].values[0][1])+" !!!")
                    return  df.loc[df['username'] == username].values[0][0]
                else:
                    print("Wrong password. Try again...")
            
            print("Too many failed tries. Exiting...")
            exit()
       

def sign_up(df):

    new_username  = input("To create a new account please enter a username: ")
    df["username"] = df["username"].apply(str.lower)  
    if not df.loc[df['username'] == new_username].empty or new_username.find("admin") != -1:
        print("This username already exists or belongs to an admin!!!\nTry loggin in...")
        exit()
    
    new_id = df["id"].iloc[-1] + 1
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    while True:
        print("Enter a password (Password must contain: 1 symbol and length > 8): ")
        new_password = input()
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


def user_add_favorites(user_df, login_id):
    
    new_favorites_df = pd.read_csv('new_favorites.csv')

    old_fav_list = ast.literal_eval(user_df.loc[login_id,'favorites'])
    
    new_fav_list = []
    for index in new_favorites_df.index:
            new_fav_list.append(new_favorites_df.loc[index,'id'])

    new_fav_list = list(set(old_fav_list + new_fav_list))

    user_df.loc[login_id,'favorites'] = str(new_fav_list)
    
    return user_df


def user_add_single_favorite(user_df, books_df, login_id):

    def exists(id, books_df):
        for index in books_df.index:
            if books_df.loc[index,'id'].item() == id:
                return True
        return False
    

    old_fav_list = ast.literal_eval(user_df.loc[login_id,'favorites'])   
    new_fav_list = []
    while True:
        new_id = int(input("Enter the ID of the book: "))
        if exists(new_id, books_df):
            new_fav_list.append(new_id)
            if input("Do you want to add another? (y/n): ") == "y":
                print(" ")
            else:
                new_fav_list = list(set(old_fav_list + new_fav_list))
                user_df.loc[login_id,'favorites'] = str(new_fav_list)

                print(user_df)
                
                return user_df
        else:
            print("This book does not exist...")
            if input("Do you want to add another? (y/n): ") == "y":
                print(" ")
            else:
                return user_df


def user_edit_info(user_df, login_id):

    def user_exists(new_username):
        for index in user_df.index:
            if user_df.loc[index,'username'] == new_username:
                print("This username is taken by another user...Try another")
                return False
        return True                         

    #id,username,password,address,city,orders,favorites,balance
    while True:
        print("Choose what do you want to edit:")
        option = input("0) Quit Editing\n1) Username\n2) Password\n3) Address\n4) City\nEnter: ")
        if option == "0":
            break
        if option == "1":
            while True:
                new_username = input("Enter your new username: ")
                if user_exists(new_username):
                    user_df.loc[login_id,'username'] = new_username
                    break           
        elif option == "2":
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            while True:
                new_password = input("Enter new password (Password must contain: 1 symbol and length > 8): ")
                if  len(new_password) >= 8 and regex.search(new_password) != None:
                    user_df.at[login_id,'password'] = new_password
                    break
                else:
                    print("Password not strong enough...Try again")
        elif option == "3":
            user_df.at[login_id,'address'] = input("Enter new address: ")
        elif option == "4":
            user_df.at[login_id,'city'] = input("Enter new city: ")
        else:
            print("No such choice...Want to quit? Enter '0' ")
    
    print(user_df)
    return user_df
        







########################################################################################################################################################################################
#################################################################################################################################################################################################           

#admin: True | user:False
#[False/True] [id]
current_login = []

admin_df = pd.read_csv('admin_data.csv')
user_df = pd.read_csv('user_data.csv')
books_df = pd.read_csv('books_data.csv')


""" print("Welcome to Book Management System\nPlease specify if you are ADMIN or USER:")
current_login.insert(0,True) if input().lower()=="admin"  else current_login.insert(0,False) 

while True:
    if current_login[0] == True:
        current_login.insert(1,login(admin_df))
        break
    elif current_login[0] == False:
        print("1) Log In\n2) Sign Up")
        if input().lower()=="1":
            current_login.insert(1,login(user_df))
            break
        elif input().lower()=="2":
            user_df = sign_up(user_df) """

current_login.insert(0,False)
current_login.insert(1,2)

while True:
    """ if current_login[0]:
        choice = input("\n\nADMIN Menu:\n0) Exit\n1) Add books (more than one)\n2) Add book\n3) Edit book\n4) Delete book\n5) Export updated books catalog\n6) Find book with title\n7) Print cost of a book\n8) Cost of all books per author/publisher\nEnter your choice: ")
        if choice == "0":
            print("\n\nExiting...")
            time.sleep(1)
            print("\nByee....")
            break
        elif choice == "1":
            books_df = admin_add_books(books_df)
            break
        elif choice == "2":
            books_df = admin_add_single_book(books_df)
            break
        elif choice == "3":
            books_df = admin_edit_book(admin_df, books_df, current_login)
            #break
        elif choice == "4":
            books_df = admin_delete_book(admin_df, books_df, current_login)
            break
        elif choice == "5":
            print("\nUpdated books catalog has been exported in 'updated_books.csv' file")
            books_df.to_csv('updated_books.csv', index=False)
            break
        elif choice == "6":
            admin_search_with_title(books_df)
            break
        elif choice == "7":
            admin_print_cost(books_df)
            break
        elif choice == "8":
            admin_print_all_cost(books_df)
            break
        else:
            print("\n\nNot an option...")
            time.sleep(1) """

    if not current_login[0]:
        choice = input("USER Menu:\n0) Exit\n1) Add books to favorites (more than one)\n2) Add book to favorites\n3) Edit personal info\nEnter your choice: ")
        if choice == "0":
            print("\n\nExiting...")
            time.sleep(1)
            print("\nByee....")
            break
        elif choice == "1":
            user_df = user_add_favorites(user_df, current_login[1])
            break
        elif choice == "2":
            user_df = user_add_single_favorite(user_df, books_df, current_login[1])
            break
        elif choice == "3":
            user_df =  user_edit_info(user_df, current_login[1])
            print(user_df)
            break
        elif choice == "4":
            break
        elif choice == "5":
            break
        elif choice == "6":
            break
        elif choice == "7":
            break
        elif choice == "8":
            break
        else:
            print("\n\nNot an option...")
            time.sleep(1)
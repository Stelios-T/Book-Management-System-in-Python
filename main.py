import warnings
from hashlib import new

from numpy import empty

warnings.simplefilter(action='ignore', category=FutureWarning)

import re

# import pandas as pd
import pandas as pd


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


#fix ids 
def admin_add_books(books_df):
    
    new_books_df = pd.read_csv('new_books.csv')

    #id = books_df["id"].iloc[-1]

    books_df = books_df.append(new_books_df, ignore_index = True)
    books_df.drop_duplicates(subset ="title",keep = 'first', inplace = True)
            
    print("Books have been updated!!!.\n")
    while True:      
        choice = input("Do you want to review the updated book list? (y/n)\n").lower()  
        if choice == "y":
            print(books_df)
            break
        elif choice == "n":
            break
        else:
            print("Enter 'y' or 'n'")
    return books_df


def admin_add_single_book(books_df):

    #id,title,author,publisher,categories,cost,shipping,availability,copies,bookstores
    while True: 
        new_title = input("Enter the title of the book: ")
        if not books_df.loc[books_df['title'] == new_title].empty:
            print("This book is already in the list!!!\n")
            choice = input("Add another book? (y/n)\n").lower()
            if  choice == "y":
                print(' ')
            elif choice == "n":
                break
            else:
                print("Enter 'y' or 'n'")
        else:
            break
    new_id = books_df["id"].iloc[-1] + 1
    new_author = input("Enter the author of the book: ")
    new_publisher = input("Enter the publisher of the book: ")
    new_categories = []
    while True: 
        new_categories.append(input("Enter a category of the book: "))
        choice = input("Add another category? (y/n)\n").lower()
        if  choice == "y":
            print(" ")
        elif choice == "n":
            break
        else:
            print("Enter 'y' or 'n'")
    new_cost = float(input("Add the cost of the book: "))
    new_shipping = float(input("Add the cost of shipping: "))
    new_avail = bool(input("Will the book be available? (True/False) : "))
    new_copies = int(input("Add the number of copies for book: "))
    print("Add the number of copies for each bookstore (The sum must not be > copies): ")
    while True:
        bookstore1 = int(input("Add the number of copies in bookstore 1: "))
        bookstore2 = int(input("Add the number of copies in bookstore 2: "))
        bookstore3 = int(input("Add the number of copies in bookstore 3: "))
        bookstore4 = int(input("Add the number of copies in bookstore 4: "))
        bookstore5 = int(input("Add the number of copies in bookstore 5: "))
        sum = bookstore1 + bookstore2 + bookstore3 + bookstore4 + bookstore5
        if sum <= new_copies :
            break
        else:
            print("Bookstores cant have more copies than copies genenerally available!!!. Check again...")
        

    new_book = pd.Series({'id':new_id,
                        'title':new_title,
                        'author':new_author,
                        'publisher':new_publisher,
                        'categories':new_categories,
                        'cost':new_cost,
                        'shipping':new_shipping,
                        'availability':new_avail,
                        'copies':new_copies,
                        'bookstores':{ 1: bookstore1 , 2: bookstore2, 3: bookstore3 , 4: bookstore4, 5: bookstore5}
                        })
    
    books_df = books_df.append(new_book, ignore_index = True)

    print("Books have been updated!!!.\n")
    while True:      
        choice = input("Do you want to review the updated book list? (y/n)\n").lower()  
        if choice == "y":
            print(books_df)
            break
        elif choice == "n":
            break
        else:
            print("Enter 'y' or 'n'")
    return books_df


########################################################################################################################################################################################
#################################################################################################################################################################################################           

#admin: True | user:False
#[False/True] [id]
current_login = []

admin_df = pd.read_csv('admin_data.csv')
user_df = pd.read_csv('user_data.csv')
books_df = pd.read_csv('books_data.csv')


""" print("Welcome to Book Management System\nPlease specify if you are ADMIN or USER:")
current_login.insert(0,True) if input().lower()=="admin"  else current_login.insert(0,False) """

""" while True:
    if current_login[0] == True:
        current_login.insert(1,login(admin_df))
        break
    elif current_login[0] == False:
        print("1) Log In\n2) Sign Up")
        if input().lower()=="1":
            current_login.insert(1,login(user_df))
            break
        elif input().lower()=="2":
            user_df = sign_up(user_df)
 """
current_login.insert(0,True)
current_login.insert(1,2)

while True:
    if current_login[0]:
        choice = int(input("ADMIN Menu:\n1) Add books (more than one)\n2) Add book\nEnter your choice: "))
        if choice == 1:
            books_df = admin_add_books(books_df)
            break
        elif choice == 2:
            books_df = admin_add_single_book(books_df)
            break
    else:
        choice = input("USER Menu:\n1) Add books (more than one)\n2) Add book\nEnter your choice: ")
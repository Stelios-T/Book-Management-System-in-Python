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
import random
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=FutureWarning)



def user_add_favorites(user_df, login_id):
    
    new_favorites_df = pd.read_csv('csv/new_favorites.csv')

    old_fav_list = ast.literal_eval(user_df.loc[login_id,'favorites'])
    
    new_fav_list = []
    for index in new_favorites_df.index:
            new_fav_list.append(new_favorites_df.loc[index,'id'])

    new_fav_list = list(set(old_fav_list + new_fav_list))

    user_df.loc[login_id,'favorites'] = str(new_fav_list)

    time.sleep(2)
    print("\nSuccessfully added favorites...")
    
    return user_df



def user_add_single_favorite(user_df, books_df, login_id):

    def exists(id, books_df):
        for index in books_df.index:
            if books_df.loc[index,'id'].item() == id:
                return True
        return False
    
    print("\n")
    time.sleep(0.5)
    old_fav_list = ast.literal_eval(user_df.loc[login_id,'favorites'])   
    new_fav_list = []
    while True:
        new_id = int(input("\nEnter the ID of the book: "))
        if exists(new_id, books_df):
            new_fav_list.append(new_id)
            time.sleep(0.5)
            print("\nBook added to favorites.")
            time.sleep(0.5)
            if input("\nDo you want to add another? (y/n): ") == "y":
                print(" ")
            else:
                new_fav_list = list(set(old_fav_list + new_fav_list))
                user_df.loc[login_id,'favorites'] = str(new_fav_list)
                
                return user_df
        else:
            time.sleep(1)
            print("\n\nThis book does not exist...")
            if input("\nDo you want to add another? (y/n): ") == "y":
                print(" ")
            else:
                return user_df



def user_edit_info(user_df, login_id):

    def user_exists(new_username):
        for index in user_df.index:
            if user_df.loc[index,'username'] == new_username:
                time.sleep(1)
                print("\nThis username is taken by another user...Try another")
                return False
        return True                         

    #id,username,password,address,city,orders,favorites,balance
    while True:
        time.sleep(0.5)
        print("\nChoose what do you want to edit:")
        option = input("0) Quit Editing\n1) Username\n2) Password\n3) Address\n4) City\nEnter: ")
        if option == "0":
            time.sleep(0.5)
            break
        if option == "1":
            while True:
                time.sleep(0.5)
                new_username = input("\nEnter your new username: ")
                if user_exists(new_username):
                    user_df.loc[login_id,'username'] = new_username
                    break           
        elif option == "2":
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            while True:
                time.sleep(0.5)
                new_password = input("\nEnter new password (Password must contain: 1 symbol and length > 8): ")
                if  len(new_password) >= 8 and regex.search(new_password) != None:
                    user_df.at[login_id,'password'] = new_password
                    break
                else:
                    time.sleep(0.5)
                    print("\n!!!Password not strong enough...Try again")
        elif option == "3":
            time.sleep(0.5)
            user_df.at[login_id,'address'] = input("Enter new address: ")
        elif option == "4":
            time.sleep(0.5)
            user_df.at[login_id,'city'] = input("Enter new city: ")
        else:
            time.sleep(0.5)
            print("\n\nNo such choice...Want to quit? Enter '0' ")
    
    return user_df



def user_empty_favorites(user_df,login_id):
    
    user_df.loc[login_id,'favorites'] = "[]"
    time.sleep(1.5)
    print("\nFavorites list emptied...\n")

    return user_df


    
def user_check_balance(user_df, login_id):
    time.sleep(0.5)
    print("\nPlease Wait...\n")
    time.sleep(1)
    print("Your Balance Amount is: "+str(user_df.loc[login_id,'balance'])+" $")



def user_check_favorites(user_df, books_df, login_id):

    fav_list = ast.literal_eval(user_df.loc[login_id,'favorites'])

    if fav_list:
        print("\nYour list of favorites contains: \n")
        time.sleep(1)
        for i in fav_list:
            for index in books_df.index:
                if books_df.loc[index,'id'] == i:
                    print("ID: "+str(books_df.loc[index,'id'])+" | Title: "+str(books_df.loc[index,'title'])+" | Author: "+str(books_df.loc[index,'author']))
        while True:
            time.sleep(0.5)
            choice = input("\nChoose which book you want to check (Choose books separated by ',' or enter 'all' for all): ")
            try:
                if choice == "all":
                    time.sleep(1)
                    for i in fav_list:
                        for index in books_df.index:
                            if books_df.loc[index,'id'] == i:
                                print("Book ID: "+str(books_df.loc[index,'id'])+" | Title: "+str(books_df.loc[index,'title'])+" | Availability: "+str(books_df.loc[index,'availability'])+" | Total cost: "+str(books_df.loc[index,'cost']+books_df.loc[index,'shipping']))
                elif choice.isdigit(): 
                    time.sleep(0.5)
                    choice = int(choice)
                    print("\nBook ID: "+str(books_df.loc[choice,'id'])+" | Title: "+str(books_df.loc[choice,'title'])+" | Availability: "+str(books_df.loc[choice,'availability'])+" | Total cost: "+str(books_df.loc[choice,'cost']+books_df.loc[choice,'shipping']))
               
                else:
                    print("\n")
                    time.sleep(1)
                    list = ast.literal_eval(choice)
                    for i in list:
                        for index in books_df.index:
                            if books_df.loc[index,'id'] == i:
                                print("Book ID: "+str(books_df.loc[index,'id'])+" | Title: "+str(books_df.loc[index,'title'])+" | Availability: "+str(books_df.loc[index,'availability'])+" | Total cost: "+str(books_df.loc[index,'cost']+books_df.loc[index,'shipping']))
                                
            except:
                time.sleep(0.5)
                print("\nOops! No such choice. Try again....")

            time.sleep(0.5)
            choice = input("\nDo you want to check another book? (y/n): ").lower()
            if choice == "y":
                print("")
            elif choice == "n":
                break
            else:
                time.sleep(0.5)
                print("\nOops! Choose either 'y' or 'n'. Try again....")
    else:
        time.sleep(1)
        print("\nYou have no favorites, to add favorites select '1' or '2' option from the menu...")



def user_orders_total(user_df, books_df, login_id):

    orders_list = ast.literal_eval(user_df.loc[login_id,'orders'])

    total_cost = 0
    if orders_list:
        time.sleep(1)
        print("\nYour orders are: \n\n")
        for i in orders_list:
            for index in books_df.index:
                if books_df.loc[index,'id'] == i:
                    print("Book ID: "+str(books_df.loc[index,'id'])+"\nTitle: "+str(books_df.loc[index,'title'])+"\nAuthor: "+str(books_df.loc[index,'author'])+"\nBook cost: "+str(books_df.loc[index,'cost'])+"$"+"\nShipping cost: "+str(books_df.loc[index,'shipping'])+"$"+"\n")
                    total_cost += books_df.loc[index,'cost']+books_df.loc[index,'shipping']
    else:
        time.sleep(1)
        print("No favorites is list...")

    time.sleep(1.5)
    print("\nBringing your total cost of all books up to: "+str(total_cost)+"$")



def user_place_order(user_df, books_df, login_id):

    def exists(id, books_df):
        for index in books_df.index:
            if books_df.loc[index,'id'].item() == id and books_df.loc[index,'availability'] == True:
                return True
        return False

    time.sleep(0.5)
    if input("\nDo you want to first see the catalog of book? (y): ").lower() == "y":
        print(books_df[['id', 'title', 'author', 'publisher', 'categories', 'cost', 'shipping']])
        print("\n!Note!: Some books that appear on the catalog may not be available\n")
    

    balance = float(user_df.loc[login_id,'balance'])
    old_order_list = ast.literal_eval(user_df.loc[login_id,'orders'])   
    new_order_list = []

    while True:
        time.sleep(0.5)
        new_id = int(input("\nEnter the ID of the book you want to order: "))
        if (new_id in old_order_list):
            time.sleep(1)
            print("\nThis books has already been ordered...")
            continue

        if exists(new_id, books_df):
            time.sleep(1)
            print("\nThe total cost will be: "+str(books_df.loc[new_id,'cost'] + books_df.loc[new_id,'shipping']))
            if input("\nAre you sure you want to order this book? (y): ") == "y":
                new_order_list.append(new_id)
                if balance - books_df.loc[new_id,'cost'] + books_df.loc[new_id,'shipping'] < 0:
                    time.sleep(1)
                    print("\n\nYour balance is not enough for this order...")
                    continue

                else:
                    balance -= books_df.loc[new_id,'cost'] + books_df.loc[new_id,'shipping']
            else:
                continue

            time.sleep(0.5)
            if input("\nDo you want to order another book? (y): ") == "y":
                old_order_list = list(set(old_order_list + new_order_list))
                continue
            else:
                new_order_list = list(set(old_order_list + new_order_list))
                user_df.loc[login_id,'orders'] = str(new_order_list)
                user_df.loc[login_id,'balance'] = str(balance)
                
                return user_df
        else:
            time.sleep(1)
            print("\n\nThis book does not exist or it's not available for ordering...")
            if input("\nDo you want to order another book? (y): ") == "y":
                print(" ")
            else:
                return user_df



def user_cancel_order(user_df, books_df, login_id):

    time.sleep(0.5)
    if input("\nDo you want to first see your orders? (y): ").lower() == "y":
        user_orders_total(user_df, books_df, login_id)
    

    balance = float(user_df.loc[login_id,'balance'])
    order_list = ast.literal_eval(user_df.loc[login_id,'orders'])   
    while True:
        time.sleep(1)
        new_id = int(input("\nEnter the ID of the book you want to cancel: "))
        if not (new_id in order_list):
            time.sleep(1)
            print("\n\nThis book is not on your orders...")
            continue
        else:
            time.sleep(1)
            print("\nThe total cost that will be returned to your wallet is: "+str(books_df.loc[new_id,'cost'] + books_df.loc[new_id,'shipping']))
            if input("\nAre you sure you want to cancel this book? (y): ") == "y":
                order_list.remove(new_id)
                balance += books_df.loc[new_id,'cost'] + books_df.loc[new_id,'shipping']
            else:
                continue

            time.sleep(0.5)
            if input("\nDo you want to cancel another book? (y): ") == "y":
                continue
            else:
                user_df.loc[login_id,'orders'] = str(order_list)
                user_df.loc[login_id,'balance'] = str(balance)
                
                return user_df



def user_check_book_for_order(user_df, books_df, login_id):
    

    def exists(id, books_df):
        for index in books_df.index:
            if books_df.loc[index,'id'].item() == id and books_df.loc[index,'availability'] == True:
                return True
        return False

    time.sleep(0.5)
    if input("\nDo you want to first see the catalog of book? (y): ").lower() == "y":
        print(books_df[['id', 'title', 'author', 'publisher', 'categories', 'cost', 'shipping']])
        print("\n!Note!: Some books that appear on the catalog may not be available\n")
    

    while True:
        time.sleep(0.5)
        new_id = int(input("\nEnter the ID of the book you would like to check copies for: "))

        balance = float(user_df.loc[login_id,'balance'])
        aval_copies = books_df.loc[new_id,'copies']
        book_cost = float(books_df.loc[new_id,'cost'] + books_df.loc[new_id,'shipping'])
        copies = 0

        if exists(new_id, books_df):
            while balance - book_cost >= 0 and aval_copies >= 0:
                balance -= book_cost
                aval_copies -= 1
                copies += 1

            time.sleep(1)
            print("\n\nYou can order "+str(copies)+" amount of copies ")
            return

        else:
            time.sleep(1)
            print("\nThis book does not exist or it's not available for ordering...")
            time.sleep(0.5)
            if input("\nDo you want to check copies for another book? (y): ") == "y":
                print(" ")
            else:
                return 



def user_add_comments(books_df, login_id):

    def exists(id, books_df):
        for index in books_df.index:
            if books_df.loc[index,'id'].item() == id:
                return True
        return False
    
    time.sleep(0.5)
    if input("\nDo you want to first see the catalog of book? (y): ").lower() == "y":
        print(books_df[['id', 'title', 'author', 'publisher', 'categories', 'cost', 'shipping']])
    
    while True:
        time.sleep(0.5)
        new_id = int(input("\n\nEnter the ID of the book you want to comment: "))
        if exists(new_id, books_df):
            try :
                comments = ast.literal_eval(books_df.loc[new_id,"comments"])
            except:
                comments = {}

            while True:
                time.sleep(0.5)
                rating = input("\nEnter the rating of the book (1-5): ")
                if int(rating)>=1 and int(rating)<=5:
                    break
                else:
                    time.sleep(0.5)
                    print("\nRating can only range from 1 to 5...Try again")
                    continue
                    
            comment_text = input("\nEnter the comment of the book: ")
            comments[login_id] = [rating, comment_text]
            books_df.loc[new_id,'comments'] = str(comments)
            
            time.sleep(0.5)
            if input("\n\nDo you want to comment another book? (y): ") == "y":
                continue
            else:
                return books_df
        else:
            time.sleep(1)
            print("\nThis book does not exist...")
            time.sleep(0.5)
            if input("\n\nDo you want to comment another book? (y): ") == "y":
                print(" ")
            else:
                return books_df



def user_get_recommends(books_df, user_df, login_id):

    fav_list = ast.literal_eval(user_df.loc[login_id,'favorites'])
    categories_list = []

    if fav_list:
        for i in fav_list:
            for index in books_df.index:
                if books_df.loc[index,'id'] == i:
                    for y in ast.literal_eval(books_df.loc[index,'categories']):
                        categories_list.append(y)
    else:
        time.sleep(1)
        print("\nCan't recommend a book if there's no favorites is list...")

    try:
        category = max(set(categories_list), key = categories_list.count)
    except:
        print("\nCan't recommend a book if there's no favorites is list...")
        return 

    time.sleep(1)
    print("\n\nWe recommend: \n")
    for index in books_df.index:
            for y in ast.literal_eval(books_df.loc[index,'categories']):
                if y == category and books_df.loc[index,'availability'] == True:
                    print("Book ID: "+str(books_df.loc[index,'id'])+"\nTitle: "+str(books_df.loc[index,'title'])+"\nAuthor: "+str(books_df.loc[index,'author'])+"\nBook cost: "+str(books_df.loc[index,'cost'])+"$"+"\nShipping cost: "+str(books_df.loc[index,'shipping'])+"$"+"\n")

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


def admin_add_books(books_df):
    
    new_books_df = pd.read_csv('csv/new_books.csv')

    books_df = books_df.append(new_books_df, ignore_index = True)
    books_df.drop_duplicates(subset ="title",keep = 'first', inplace = True)

    for index in books_df.index:
        if books_df.loc[index,'id'] == 0:
            books_df.loc[index,'id'] = index

    time.sleep(1)
    print("\nBooks have been updated!!!.\n")
    while True:      
        time.sleep(0.5)
        choice = input("\nDo you want to review the updated book list? (y/n)\n").lower()  
        if choice == "y":
            print(books_df)
            break
        elif choice == "n":
            break
        else:
            print("Enter 'y' or 'n'")
    return books_df


def admin_add_single_book(books_df):

    def exists(title, books_df):
        for index in books_df.index:
            if books_df.loc[index,'title'].lower() == title.lower():
                return True
        return False

    #id,title,author,publisher,categories,cost,shipping,availability,copies,bookstores
    while True: 
        time.sleep(0.5)
        new_title = input("\nEnter the title of the book: ")
        if exists(new_title, books_df):
            time.sleep(0.5)
            choice = input("\nThis book is already in the catalog!!!\nTry adding some other book? (y/n): ").lower()
            if  choice == "y":
                print(' ')
            elif choice == "n":
                break
            else:
                time.sleep(0.5)
                print("!!!Please enter only 'y' or 'n'")
        else:
            break
    new_id = books_df["id"].iloc[-1] + 1
    new_author = input("\nEnter the author of the book: ")
    new_publisher = input("\nEnter the publisher of the book: ")
    new_categories = []
    while True: 
        new_categories.append(input("\nEnter a category of the book: "))
        choice = input("    Add another category? (y/n): ").lower()
        if  choice == "y":
            print(" ")
        elif choice == "n":
            break
        else:
            print("Enter 'y' or 'n'")
    
    while True:
        try:
            new_cost = float(input("\nAdd the cost of the book: "))
            break
        except:
            time.sleep(0.5)
            print("\n!!!Only float number is acceptable!!! (ex 4.6, 30.8) ")
    while True:
        try:
            new_shipping = float(input("\nAdd the cost of shipping: "))
            break
        except:
            time.sleep(0.5)
            print("\n!!!Only float number is acceptable!!! (ex 4.6, 30.8) ")
    new_avail = bool(input("\nWill the book be available? (True/False) : "))
    while True:
        try:
            new_copies = int(input("\nAdd the number of copies for book: "))            
            break
        except:
            time.sleep(0.5)
            print("\n!!!Only integer number is acceptable!!! (ex 4, 30) ")

    time.sleep(0.5)
    print("\nAdd the number of copies for each bookstore (The sum must not be > copies): ")
    while True:
        while True:
            try:
                bookstore1 = int(input("  Add the number of copies in Bookstore 1: "))
                bookstore2 = int(input("  Add the number of copies in Bookstore 2: "))
                bookstore3 = int(input("  Add the number of copies in Bookstore 3: "))
                bookstore4 = int(input("  Add the number of copies in Bookstore 4: "))
                bookstore5 = int(input("  Add the number of copies in Bookstore 5: "))            
                break
            except:
                time.sleep(0.5)
                print("\n!!!Only integer number is acceptable!!! (ex 4, 30) ")
        
        sum = bookstore1 + bookstore2 + bookstore3 + bookstore4 + bookstore5
        if sum == new_copies :
            break
        else:
            time.sleep(0.5)
            print("\n!!!Bookstores cant have more or less copies than copies genenerally available!!!. Check again...")
        

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

    time.sleep(1.5)
    print("\n\nBooks have been updated!!!.\n")
    while True:      
        choice = input("\nDo you want to review the updated book list? (y/n)\n").lower()  
        if choice == "y":
            print(books_df)
            break
        elif choice == "n":
            break
        else:
            print("Enter 'y' or 'n'")
    return books_df


def admin_edit_book(admin_df, books_df, login):

    time.sleep(0.5)
    if input("\nDo you want to see the book catalog? (y): ").lower() == "y":
        print(books_df)

    time.sleep(0.5)
    id = int(input("\nEnter the ID of the book you want to edit: "))
    
    #check if book exists
    flag_exists = False
    for index in books_df.index:
        if books_df.loc[index,'id'].item() == id:
            flag_exists = True
            print("\nChecking if you have permission to edit the book...\n")
            time.sleep(1.5)

            #access exei mesa se poia bookstores exei prosvasi
            access = ast.literal_eval(admin_df.loc[login[1],'bookstores'])
            access = [int(x) for x in access]

            #exei mesa ton arithmo twn antitypwn se kathe bookstore
            bookstores_copies = ast.literal_eval(books_df.loc[id,'bookstores'])

            #ean kapoio apo ta bookstores pou exei prosvasi exei copies > 0 tote mporei na kanei edit
            flag = False
            for i in access:
                if bookstores_copies[i] > 0:
                    flag = True
                    break

            time.sleep(0.5)    
            if flag:
                print("\nYou have permission to edit this book\n")   
            else:
                print("\nI'm afraid you don't have permission to edit this book\n")      
                return books_df

            books_df.at[id,'id'] = id
            while True:
                print("Choose what do you want to edit:")
                option = input("\n0) Quit Editing\n1) Title\n2) Author\n3) Publisher\n4) Categories \n5) Cost \n6) Shipping \n7) Availability \n8) Copies\nEnter: ")
                time.sleep(0.5)
                if option == "0":
                    break
                if option == "1":
                    books_df.at[id,'title'] = input("\nEnter the new title of the book: ")           
                elif option == "2":
                    books_df.at[id,'author'] = input("\nEnter the new author of the book: ")
                elif option == "3":
                    books_df.at[id,'publisher'] = input("\nEnter the new publisher of the book: ")
                elif option == "4":
                    new_categories = []
                    while True: 
                        new_categories.append(input("\nEnter a new category of the book: "))
                        choice = input("\nAdd another category? (y/n): ").lower()
                        if  choice == "y":
                            print(" ")
                        elif choice == "n":
                            break
                        else:
                            print("Enter 'y' or 'n'")

                    books_df.at[id,'categories'] = str(new_categories)
                elif option == "5":
                    while True:
                        try:
                            books_df.at[id,'cost'] = float(input("\nAdd the new cost of the book: "))
                            break
                        except:
                            time.sleep(0.5)
                            print("\n!!!Only float number allowed...Try again")

                elif option == "6":
                    while True:
                        try:
                            books_df.at[id,'shipping'] = float(input("\nAdd the new cost of shipping: "))
                            break
                        except:
                            time.sleep(0.5)
                            print("\nOnly float number allowed...Try again")

                elif option == "7":
                    books_df.at[id,'availability'] = bool(input("\nWill the book be available? (True/False) : "))

                elif option == "8":
                    new_copies = int(input("\nAdd the new number of copies for book: "))
                    time.sleep(0.5)
                    print("Add the number of copies for each bookstore (The sum must not be > copies): ")
                    time.sleep(0.5)
                    while True:
                        new_bookstores_copies = [0]*5
                        for i in access:
                            print("Add the number of copies in bookstore "+str(i)+": ")
                            new_bookstores_copies[i-1] = int(input())
                        sum = new_bookstores_copies[0] + new_bookstores_copies[1] + new_bookstores_copies[2] + new_bookstores_copies[3] + new_bookstores_copies[4]
                        if sum == new_copies :
                            books_df.at[id,'copies'] = new_copies
                            break
                        else:
                            time.sleep(0.5)
                            print("\n!!!Bookstores cant have more or less copies than copies genenerally available!!!. Check again...")

                    bookstores = {}
                    bookstores[1] = new_bookstores_copies[0]
                    bookstores[2] = new_bookstores_copies[1]
                    bookstores[3] = new_bookstores_copies[2]
                    bookstores[4] = new_bookstores_copies[3]
                    bookstores[5] = new_bookstores_copies[4]

                    books_df.at[id,'bookstores'] = bookstores

                else:
                    time.sleep(0.5)
                    print("\n!!!No such choice...Want to quit? Enter '0' ")

            #id,title,author,publisher,categories,cost,shipping,availability,copies,bookstores 
            

            books_df.to_csv('csv/books_data.csv', index=False)
            books_df = pd.read_csv('csv/books_data.csv')

            time.sleep(2)
            print("\n\nBooks have been updated!!!.\n")
            while True:      
                choice = input("\nDo you want to see the updated book list? (y/n)\n").lower()  
                if choice == "y":
                    print(books_df)
                    break
                elif choice == "n":
                    break
                else:
                    print("Enter 'y' or 'n'")  
            return books_df
    
    if not flag_exists:
        time.sleep(1)
        print("\nSeems like this book does not exist. To add it select option '2' from the menu...\n")
        return books_df       


def admin_delete_book(admin_df, books_df, login):

    time.sleep(0.5)
    id = int(input("\nEnter the id of the book you want to delete: ")) 
    flag_exists = False
    for index in books_df.index:
        if books_df.loc[index,'id'] == id:

            flag_exists = True
            print("\nChecking if you have permission to delete this book...\n")
            time.sleep(2)
            access = ast.literal_eval(admin_df.loc[login[1],'bookstores'])
            access = [int(x) for x in access]
            bookstores_copies = ast.literal_eval(books_df.loc[id,'bookstores'])

            flag = False
            for i in access:
                if bookstores_copies[i] > 0:
                    flag = True
                    break
            
            time.sleep(0.5)
            if flag:
                print("\nYou have permission to delete this book\n")   
            else:
                print("\nI'm afraid you don't have permission to delete this book\n")
                return books_df

            books_df = books_df[books_df.id != id]

            time.sleep(1)
            print("\n\nBooks have been updated!!!.\n")
            while True:      
                choice = input("\nDo you want to see the updated book list? (y/n)\n").lower()  
                if choice == "y":
                    print(books_df)
                    break
                elif choice == "n":
                    break
                else:
                    print("Enter 'y' or 'n'")  
            return books_df

    if not flag_exists:
        time.sleep(1)
        print("\nSeems like this book does not exist.\n")
        return books_df


def admin_search_with_title(books_df):

    time.sleep(0.5)
    title = input("\nEnter the title of the book you want to search: ")
    book_index = -1
    for index in books_df.index:
        if books_df.loc[index,'title'].replace(" ",'').lower() == title.replace(" ",'').lower():
            book_index = index
            

    if book_index == -1:
        time.sleep(1)
        print("\nCould not find this book...\n")
        return

    bookstores_copies = ast.literal_eval(books_df.loc[book_index,'bookstores'])  

    if books_df.loc[book_index,'availability']:
        time.sleep(0.5)
        print("\nThe book is available...")   
        shops = input("\nEnter the shops you want to look for availability separated with ',' (enter 'all' to search for all): ")
        time.sleep(1)
        print("\n")
        if shops == "all":
            j = 1
            for i in bookstores_copies:
                print("Shop "+str(j)+" has "+str(bookstores_copies[i])+" copies ")
                j+=1
        else:
            shops = shops.split(',')
            shops = [int(x) for x in shops]
            for i in shops:
                print("Shop "+str(i)+" has "+str(bookstores_copies[i])+" copies ")

    elif books_df.loc[index,'availability']:
        time.sleep(0.5)
        print("\nThe book is not available...")   


def admin_print_cost(books_df):

    book_index = -1
    title = input("\nEnter the title of the book you want to search: ")
    for index in books_df.index:
        if books_df.loc[index,'title'].replace(" ",'').lower() == title.replace(" ",'').lower():
            book_index = index
            break

    if book_index == -1:
        return  

    print("Calculating...")
    time.sleep(2)
    print("The cost of the book is: "+str(books_df.loc[book_index,'cost'])+' $')
    time.sleep(2)
    print("The cost of shipping is: "+str(books_df.loc[book_index,'shipping'])+' $')
    time.sleep(2)
    print("The total cost of the book is: "+str(books_df.loc[book_index,'cost'] + books_df.loc[book_index,'shipping'])+' $')


def admin_print_all_cost(books_df):
    
    time.sleep(0.5)
    while True:
        choice = input("\nPrint per author or publisher (a/p): ")
        if choice == "a":
            avarage_cost = {}
            for index in books_df.index:
                if str(books_df.loc[index,'availability']) == "True":
                    if books_df.loc[index,'author'] in avarage_cost:
                        avarage_cost[books_df.loc[index,'author']] += books_df.loc[index,'cost'] + books_df.loc[index,'shipping'] 
                    else:
                        avarage_cost.__setitem__(books_df.loc[index,'author'], books_df.loc[index,'cost'] + books_df.loc[index,'shipping']) 
            print("\nCalculating...")
            time.sleep(1)
            for i in avarage_cost:
                print("Author: "+str(i)+" | Cost of books: "+str(avarage_cost[i])+"\n")
            
            break

        elif choice == "p":
            avarage_cost = {}
            for index in books_df.index:
                if str(books_df.loc[index,'availability']) == "True":
                    if books_df.loc[index,'publisher'] in avarage_cost:
                        avarage_cost[books_df.loc[index,'publisher']] += books_df.loc[index,'cost'] + books_df.loc[index,'shipping'] 
                    else:
                        avarage_cost.__setitem__(books_df.loc[index,'publisher'], books_df.loc[index,'cost'] + books_df.loc[index,'shipping']) 
            print("\nCalculating...")
            time.sleep(1)
            for i in avarage_cost:
                print("Publisher: "+str(i)+" | Cost of books: "+str(avarage_cost[i])+"\n")
            
            break 


def admin_delete_user(user_df):

    def user_exists(new_username):
        for index in user_df.index:
            if user_df.loc[index,'username'] == new_username:
                return True
        return False

    time.sleep(0.5)
    if input("\nDo you want to see the list of users? (y): ").lower() == "y":
        print("\n")
        print(user_df)
    
    time.sleep(0.5)
    while True:
        username = input("\nEnter the username of user you want to delete: ")
        if user_exists(username):
                user_df = user_df[user_df.username != username]
                break
        else:
            time.sleep(0.5)
            if input("This username does not exist or you mistyped his username...Want to try again? (y):") == "y":
                print("")
            else:
                break

    
    return user_df


def admin_print_plots(books_df, user_df):

    def remove_duplicate(list):
        temp_list = []
        for i in list:
            if i not in temp_list:
                temp_list.append(i)
        return temp_list
    
    def print_plot(list, col):
        
        count_copies = [0]*len(list)
        i = 0
        for ele in list:
            copies = 0
            for index in books_df.index:
                if books_df.loc[index,col] == ele:
                    copies += books_df.loc[index,'copies']
            count_copies[i] = copies       
            i += 1

        plt.plot(list, count_copies)

    def print_plot_without_copies(list, col):

        count = []
        for ele in list:
            count.append(len(books_df[books_df[col] == ele]))
        
        plt.plot(list, count)
    
    def print_category_plot_with_copies(categories):

        categories_with_copies = [0]*len(categories)
        for index in books_df.index:
            for element in ast.literal_eval(books_df.loc[index,'categories']):
                i = 0
                for category in categories:
                    if element == category:
                        categories_with_copies[i] += books_df.loc[index,'copies']
                    i += 1
                    
        plt.plot(categories, categories_with_copies) 
        
        
    def print_category_plot(categories):
        categories_no_copies = [0]*len(categories)
        for index in books_df.index:
            for element in ast.literal_eval(books_df.loc[index,'categories']):
                i = 0
                for category in categories:
                    if element == category:
                        categories_no_copies[i] += 1
                    i += 1
                    
        plt.plot(categories, categories_no_copies)
 
    

    publishers = []
    authors = []
    categories = []
    bookstores_copies = [0]*5
    cost = []

    for index in books_df.index:
        publishers.append(books_df.loc[index,'publisher'])
        authors.append(books_df.loc[index,'author'])
        for ele in ast.literal_eval(books_df.loc[index,'categories']):
            categories.append(ele)
        for i in range(0,5):
            """ bookstores[0] += bookstore_copies[1]
            bookstores[1] += bookstore_copies[2]
            bookstores[2] += bookstore_copies[3]
            bookstores[3] += bookstore_copies[4]
            bookstores[4] += bookstore_copies[5] """
            bookstores_copies[i] += ast.literal_eval(books_df.loc[index,'bookstores'])[i+1]
        if books_df.loc[index,'availability'] == True:
            cost.append(books_df.loc[index,'cost'])

    publishers = remove_duplicate(publishers)
    authors = remove_duplicate(authors)
    categories = remove_duplicate(categories)


    bookstores = []
    for i in range(0,5): bookstores.append("Bookstore "+str(i+1))    

    #city
    cities = []
    for index in user_df.index:
            cities.append(user_df.loc[index,'city'])

    cities = remove_duplicate(cities)

    cities_numb = [0]*len(cities)
    for index in user_df.index:
                i = 0
                for city in cities:
                    if city == user_df.loc[index,'city']:
                        cities_numb[i] += 1
                    i += 1        


    plt.figure(figsize=(40, 10))
    time.sleep(0.5)
    while True:
        choice = input("Available plots:\n   1) Cost for books\n   2) Cities per user\n   3) Bookstore copies\n   4) Publishers\n   5) Publishers (with copies)\n   6) Authors\n   7) Authors (with copies)\n   8) Categories (no copies)\n   9) Categories\nEnter your option: ")
        if choice == "1":
            time.sleep(1)
            plt.plot(cost)
            break
        elif choice == "2":
            time.sleep(1)
            plt.plot(cities, cities_numb)
            break
        elif choice == "3":
            time.sleep(1)
            plt.plot(bookstores, bookstores_copies)
            break
        elif choice == "4":
            time.sleep(1)
            print_plot(publishers,"publisher")
            break
        elif choice == "5":
            time.sleep(1)
            print_plot_without_copies(publishers,"publisher")
            break
        elif choice == "6":
            time.sleep(1)
            print_plot(authors,"author")
            break
        elif choice == "7":
            time.sleep(1)
            print_plot_without_copies(authors,"author")
            break
        elif choice == "8":
            time.sleep(1)
            print_category_plot(categories)
            break
        elif choice == "9":
            time.sleep(1)
            print_category_plot_with_copies(categories)
            break
        else:
            time.sleep(0.5)
            print("\nNo such choice...")



#den leitourgei swsta, den prolava na tin ftiaxw
def admin_delete_comment(books_df):

    def exists(id, books_df):
        for index in books_df.index:
            if books_df.loc[index,'id'].item() == id:
                return True
        return False
    
    while True:

        new_id = int(input("Enter the ID of the book you want to delete the comment: "))
        if exists(new_id, books_df):
            try :
                comments = ast.literal_eval(books_df.loc[new_id,"comments"])
            except:
                print("There is no comment for this book....")
                return books_df
                    
            comment_id = input("Enter the id of the user whose comment you want to delete: ")
            try:
                del comments[comment_id]
                books_df.loc[new_id,'comments'] = str(comments)
                break
            except:
                print("This user has not commented on this book...")
                if input("Do you want to try another book? (y): ") == "y":
                    print(" ")
                else:
                    return books_df

        else:
            print("This book does not exist...")
            if input("Do you want to try another book? (y): ") == "y":
                print(" ")
            else:
                return books_df

    return books_df
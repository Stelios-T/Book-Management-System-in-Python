# import pandas as pd
import pandas as pd
import re
from numpy import empty
from unicodedata import category
import warnings
from hashlib import new
import time

warnings.simplefilter(action='ignore', category=FutureWarning)



def admin_add_books(books_df):
    
    new_books_df = pd.read_csv('new_books.csv')

    #id = books_df["id"].iloc[-1]

    books_df = books_df.append(new_books_df, ignore_index = True)
    books_df.drop_duplicates(subset ="title",keep = 'first', inplace = True)

    for index in books_df.index:
        if books_df.loc[index,'id'] == 0:
            books_df.loc[index,'id'] = index
            
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
        if sum == new_copies :
            break
        else:
            print("Bookstores cant have more or less copies than copies genenerally available!!!. Check again...")
        

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


def admin_edit_book(admin_df, books_df, login):

    id = int(input("\nEnter the ID of the book you want to edit: "))
    flag_exists = False
    for index in books_df.index:
        if books_df.loc[index,'id'].item() == id:
            flag_exists = True
            print("\nChecking if you have permission to edit the book...\n")
            #time.sleep(2)
            access = admin_df.loc[login[1],'bookstores'].replace(" ",'').replace("[",'').replace("]",'').split(",")
            access = [int(x) for x in access]
            bookstores_copies = []
            flag = False
            for i in books_df.loc[id,'bookstores'].replace(" ",''):
                if flag:
                    bookstores_copies.append(int(i))
                    flag = False
                if i == ':':
                    flag = True

            flag = False
            for i in access:
                if bookstores_copies[i-1] > 0:
                    flag = True
                    break
            if flag:
                print("You have permission to change this book")   
            else:
                print("I'm afraid you don't have permission to change this book")
                return books_df

            #id,title,author,publisher,categories,cost,shipping,availability,copies,bookstores 
            new_title = input("Enter the new title of the book: ")
            new_id = id
            new_author = input("Enter the new author of the book: ")
            new_publisher = input("Enter the new publisher of the book: ")
            new_categories = []
            while True: 
                new_categories.append(input("Enter a new category of the book: "))
                choice = input("Add another category? (y/n)\n").lower()
                if  choice == "y":
                    print(" ")
                elif choice == "n":
                    break
                else:
                    print("Enter 'y' or 'n'")
            new_cost = float(input("Add the new cost of the book: "))
            new_shipping = float(input("Add the new cost of shipping: "))
            new_avail = bool(input("Will the book be available? (True/False) : "))
            new_copies = int(input("Add the new number of copies for book: "))
            print("Add the number of copies for each bookstore (The sum must not be > copies): ")
            
            while True:
                new_bookstores_copies = [0]*5
                for i in access:
                    print("Add the number of copies in bookstore:")
                    new_bookstores_copies.insert(i, int(input()))
                sum = new_bookstores_copies[0] + new_bookstores_copies[1] + new_bookstores_copies[2] + new_bookstores_copies[3] + new_bookstores_copies[4]
                if sum == new_copies :
                    break
                else:
                    print("Bookstores cant have more or less copies than copies genenerally available!!!. Check again...")
                
            new_categories = str(new_categories)
            new_book = pd.Series({'id':new_id,
                                'title':new_title,
                                'author':new_author,
                                'publisher':new_publisher,
                                'categories':new_categories,
                                'cost':new_cost,
                                'shipping':new_shipping,
                                'availability':new_avail,
                                'copies':new_copies,
                                'bookstores':{ 1: new_bookstores_copies[0] , 2: new_bookstores_copies[1], 3: new_bookstores_copies[2] , 4: new_bookstores_copies[3], 5: new_bookstores_copies[4] }
                                })
            
            books_df = books_df.append(new_book, ignore_index = True)
            books_df.drop_duplicates(subset ="id",keep = 'last', inplace = True)
            books_df = books_df.sort_values(by=['id'], ascending=True)

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
    
    if not flag_exists:
        print("\nSeems like this book does not exist. To add it select option '2' from the menu...\n")       

#eroor, most likely need to write back to csv 
def admin_delete_book(admin_df, books_df, login):

    id = int(input("\nEnter the id of the book you want to delete: ")) 
    flag_exists = False
    for index in books_df.index:
        if books_df.loc[index,'id'].item() == id:
            flag_exists = True
            print("\nChecking if you have permission to delete this book...\n")
            #time.sleep(2)
            access = admin_df.loc[login[1],'bookstores'].replace(" ",'').replace("[",'').replace("]",'').split(",")
            access = [int(x) for x in access]
            bookstores_copies = []
            flag = False
            for i in books_df.loc[id,'bookstores'].replace(" ",''):
                if flag:
                    bookstores_copies.append(int(i))
                    flag = False
                if i == ':':
                    flag = True

            flag = False
            for i in access:
                if bookstores_copies[i-1] > 0:
                    flag = True
                    break
            if flag:
                print("You have permission to delete this book")   
            else:
                print("I'm afraid you don't have permission to delete this book")
                return books_df

            books_df = books_df[books_df.id != id]

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
    
    if not flag_exists:
        print("\nSeems like this book does not exist.\n")


def admin_search_with_title(books_df):
    
    title = input("\nEnter the title of the book you want to search: ")
    book_index = -1
    for index in books_df.index:
        if books_df.loc[index,'title'].replace(" ",'').lower() == title.replace(" ",'').lower():
            book_index = index
            exists = True
            break

    if book_index == -1:
        return

    bookstores_copies = []
    for index in books_df.index:
        if books_df.loc[index,'title'].replace(" ",'').lower() == title.replace(" ",'').lower(): 
            flag = False
            for i in books_df.loc[index,'bookstores'].replace(" ",''):
                if flag:
                    bookstores_copies.append(int(i))
                    flag = False
                if i == ':':
                    flag = True   

    if books_df.loc[book_index,'availability']:
        print("The book is available...")   
        shops = input("Enter the shops you want to look for availability separated with ',' (enter 'all' to search for all): ")
        if shops == "all":
            j = 1
            for i in bookstores_copies:
                print("Shop "+str(j)+" has "+str(bookstores_copies[i])+" copies ")
                j+=1
        else:
            shops = shops.split(',')
            shops = [int(x) for x in shops]
            for i in shops:
                print("Shop "+str(i)+" has "+str(bookstores_copies[i-1])+" copies ")

    elif books_df.loc[index,'availability']:
        print("The book is not available...")   


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
    
    while True:
        choice = input("Print per author or publisher (a/p): ")
        if choice == "a":
            avarage_cost = {}
            for index in books_df.index:
                if str(books_df.loc[index,'availability']) == "True":
                    if books_df.loc[index,'author'] in avarage_cost:
                        avarage_cost[books_df.loc[index,'author']] += books_df.loc[index,'cost'] + books_df.loc[index,'shipping'] 
                    else:
                        avarage_cost.__setitem__(books_df.loc[index,'author'], books_df.loc[index,'cost'] + books_df.loc[index,'shipping']) 
            print("Calculating...")
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
            print("Calculating...")
            time.sleep(1)
            for i in avarage_cost:
                print("Publisher: "+str(i)+" | Cost of books: "+str(avarage_cost[i])+"\n")
            
            break 

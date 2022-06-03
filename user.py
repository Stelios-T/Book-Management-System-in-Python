# import pandas as pd
import pandas as pd 
import re

#admin: True | user:False
#[False/True] [id]
""" current_login = []

df = pd.read_csv('admin_data.csv')
user_df = pd.read_csv('user_data.csv')
books_df = pd.read_csv('books_data.csv')

password = "4321"
username = "admin4"

df_test = pd.DataFrame({'id':[ 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                        'username':["Stelios46", "Annavailable", "GeorgeSo", "VassoOG", "AngelaAthens", "GiannisNel", "Antonis22", "VaggosG",  "LoukasKon23", "EriniAE"],
                        'password':[ "1234", "1234", "1234", "1234", "1234", "1234", "1234", "1234", "1234", "1234" ],
                        'address':[ "Kritis 13", "Liti 5", "Tymphristoy 56", "Venizelou 217", "Kritsas 5", "Valaoriou 8", "Tsimiski 34", "Sxoleiou 26", "Fanaria 2", "Flemin 78"],
                        'city':[ "Lamia", "Thessaloniki", "Lamia", "Athina", "Athina", "Trikala", "Patra", "Athina", "Naousa", "Thessaloniki"],
                        'orders':[ [ 1, 3 ], [ 1, 4 , 6 , 2 ] , [ 2 ] , [ 9 ], [] , [ 4, 5 ], [ 1, 3 ], [] , [], [2] ],
                        'favorites':[ [ 3 ], [ 1, 4 ] , [ 2, 3 ], [], [ 7 ] , [ 2 ], [], [ 1 ] , [] , [ 5 ] ],
                        'balance':[ 100.5, 65.78, 52.0, 32.6, 90.5, 10.0, 49.7, 369.8, 56.9, 28.3 ], 
                        })

new_user = pd.Series({   
                                        'id': 11,
                                        'username': 'Anna',
                                        'password': '1234',
                                        'address': 'Liti 5',
                                        'city': 'Thessaloniki',
                                        'orders': [ 1, 4 , 6 , 2 ],
                                        'favorites':[ 1, 4 ],
                                        'balance': 65.78 
                                    })



df_test = df_test.append(new_user, ignore_index = True) """
#print(df_test)

#print(df_test.drop_duplicates(subset ="username",keep = 'first', inplace = True))

#print(df_test)

books_df = pd.read_csv('books_data.csv')
admin_df = pd.read_csv('admin_data.csv')

#print(books_df["author"])








""" counter_f = 0
counter_t = 0
for index in books_df.index:
    if str(books_df.loc[index,'availability']) == "True":
        counter_t += 1
    elif str(books_df.loc[index,'availability']) == "False":
        counter_f += 1

print(counter_f)
print(counter_t) """
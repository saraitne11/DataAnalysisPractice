import pandas as pd
import sqlite3 as sql

doc_use_log = pd.read_csv('db/doc_use_log.csv')
ios = pd.read_csv('db/ios.csv')

con = sql.connect('db/doc_use_log.db')

doc_use_log.to_sql('log', con)
ios.to_sql('ios', con)

con.close()

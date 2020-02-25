import pandas as pd
import sqlite3 as sql

funnel = pd.read_csv('../db/df_funnel.csv')

con = sql.connect('db/funnel.db')

funnel.to_sql('log', con)

con.close()

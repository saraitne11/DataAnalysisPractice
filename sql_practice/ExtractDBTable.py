import pandas as pd
import numpy as np
from pandasql import *

# pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

df = pd.read_csv('db/doc_use_log.csv').sample(frac=0.1, replace=False)

# example 1
# print(df.head())
# print(df.shape)
# print(df.info())


# example 2
# q = """
#     SELECT *
#     FROM df
#     WHERE ext = 'PDF'
#     AND ismydoc = '0'
#     LIMIT 20
#     """
#
# print(sqldf(q, locals()).to_string())
# print('\n\n', end='')
#
# print(df[(df['ext'] == 'PDF') & (df['ismydoc'] == 0)].head(10))
# print('\n\n', end='')


# example 3
q = """
    SELECT ext,
            count(ext) as count,
            count(distinct sessionid) as unq_sess
    FROM df
    GROUP BY ext
    ORDER BY count DESC
    """
print(sqldf(q, locals()).to_string())


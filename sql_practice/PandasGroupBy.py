import pandas as pd
import numpy as np


df = pd.DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
                   'key2': ['one', 'two', 'one', 'two', 'one'],
                   'data1': np.random.randn(5),
                   'data2': np.random.randint(0, 10, 5)})

print(df)
print('\n')
# print(df[df['key1'] == 'a'])
# print('\n')
# print(df[df['key1'] == 'a']['data1'])
# print('\n')
# print(df[df['key1'] == 'a']['data1'].mean())
# print('\n')

print(df.groupby('key1').mean())

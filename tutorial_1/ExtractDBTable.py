import pandas as pd
import numpy as np
from pandasql import *

# pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

df = pd.read_csv('db/doc_use_log.csv').sample(frac=0.1, replace=False)
# df = pd.read_csv('db/doc_use_log.csv')
ios = pd.read_csv('db/ios.csv')

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
# q = """
#     SELECT ext,
#             count(ext) as ext_cnt,
#             count(distinct sessionid) as session_cnt
#     FROM df
#     GROUP BY ext
#     ORDER BY ext_cnt DESC
#     """
# print(sqldf(q, locals()).to_string())
# print('\n')
#
# grouped = df.groupby('ext')
# aggregation = grouped.agg({'ext': 'count', 'sessionid': 'nunique'})
# renaming = aggregation.rename(columns={'ext': 'ext_cnt', 'sessionid': 'session_cnt'})
# sorting = renaming.sort_values('ext_cnt', ascending=False).reset_index()
# print(sorting)


# example 4
# print(ios.head())
# print('\n')
# print(ios.info())
# print('\n')
# print(len(ios.sessionid))
# print(len(ios.sessionid.unique()))
#
# q = """
#     SELECT count(sessionid) as session_all_cnt,
#             count(distinct sessionid) as session_uniq_cnt
#     FROM ios
#     """
#
# print(sqldf(q, locals()))
# print('\n')
#
# q = """
#     SELECT
#         A.*,
#         B.flag
#     FROM df A
#         LEFT JOIN
#         (
#         SELECT sessionid, flag
#         FROM ios
#         ) B
#         ON A.sessionid = B.sessionid
#     WHERE B.flag = 'iOS'
#     """
#
# print(sqldf(q, locals()).to_string())
# print('\n')
#
# merged = df.merge(ios, on='sessionid', how='left').drop('idx', axis=1)
# print(merged[merged['flag'] == 'iOS'])
# print('\n')
# print(merged.query("flag == 'iOS'"))


# Question 1
# df 테이블의 Action Type 값(항목)별 유니크한 세션수는?
# 유니크 세션수 기준으로 내림차순 정렬하기

# q = """
#     SELECT actiontype,
#             count(distinct sessionid) as cnt_uniq_sessid
#     FROM df
#     GROUP BY actiontype
#     ORDER BY cnt_uniq_sessid DESC
#     """
# print(sqldf(q, locals()).to_string())
# print('\n')
#
# grouped = df.groupby('actiontype')
# agg = grouped.agg({'sessionid': 'nunique'})
# renaming = agg.rename(columns={'sessionid': 'cnt_uniq_sessid'})
# print(renaming.sort_values('cnt_uniq_sessid', ascending=False).reset_index())
# print('\n')


# Question 2
# ismydoc이 1(True)인 경우에 한해, 날짜별 세션수의 유니크 빈도 구하기
# 유니크 빈도가 가장 큰 top 5 날짜 확인하기

# q = """
#     SELECT datetime,
#             count(distinct sessionid) as cnt_uniq_sessid
#     FROM df
#     WHERE ismydoc = '1'
#     GROUP BY datetime
#     ORDER BY cnt_uniq_sessid DESC
#     LIMIT 5
#     """
#
# print(sqldf(q, locals()).to_string())
# print('\n')
#
#
# grouped = df[df['ismydoc'] == 1].groupby('datetime')
# agg = grouped.agg({'sessionid': 'nunique'}).rename(columns={'sessionid': 'cnt_uniq_sessid'})
# print(agg.sort_values(by='cnt_uniq_sessid', ascending=False).head(5).reset_index())
# print('\n')


# Question 3
# 문서 포지션별(documentposition)로 자주 OPEN 되는 확장자(ext)를 확인하기
# 카운트 기준: unique sessionid
# 그룹별, 세션카운트 기준 desc 정렬

q = """
    SELECT documentposition,
            ext,
            count(distinct sessionid) as cnt_uniq_sessid
    FROM df
    WHERE actiontype = 'OPEN'
    GROUP BY documentposition, ext
    ORDER BY documentposition, cnt_uniq_sessid DESC
    """

print(sqldf(q, locals()).to_string())
print('\n')

grouped = df[df['actiontype'] == 'OPEN'].groupby(['documentposition', 'ext'])
agg = grouped.agg({'sessionid': 'nunique'})
print(agg.unstack().fillna(0))

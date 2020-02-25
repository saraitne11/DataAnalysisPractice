import pandas as pd
import pandasql as sql
import matplotlib.pyplot as plt


# actiontype: 문서 이용시 행동(OPEN, CLOSE, SAVE..)
# ismydoc: 내 문서 해당 여부
# ext: 문서 확장자
# sessionid: 유저 식별자
# documentposition: 문서 이용시 위치 정보(CLOUD, OTHERAPP)
# datetime: TimeStamp
# screen: 앱내 화면 이름


pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

# ###################################################
# ############## 1. Read DataSet ####################
# ###################################################
df = pd.read_csv('db/df_funnel.csv', index_col=0)
# print(df.head(5))
# print()
# print(df.tail(5))
# print()
# print(df.info())

# ###################################################
# ################ 2. Pre-Processing ################
# ###################################################
# 2.1 string으로 저장된 datetime column을 datatime형으로 변환
# print(type(df['datetime'][0]))
# <class 'str'>
df['datetime'] = pd.to_datetime(df['datetime'])
# print(df.head())
# print()
# print(df.info())

# q = """
#     SELECT datetime,
#             count(datetime) as uniq_cnt
#     FROM df
#     GROUP BY datetime
#     ORDER BY uniq_cnt DESC
#     """
# print(sql.sqldf(q, locals()))

# print(df.groupby('datetime').agg({'datetime': 'count'}).rename(columns={'datetime': 'count'}))
# print(df['datetime'].dt.year[:5])
# print(df['datetime'].dt.month[:5])
# print(df['datetime'].dt.day[:5])


# Quiz.
# 요일 컬럼 생성
# 요일별 로그 수 카운트
weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# df['weekday'] = list(map(lambda x: weekdays[x.weekday()], df['datetime']))
df['weekday'] = df['datetime'].map(lambda x: weekdays[x.weekday()])
columns_order = ['actiontype', 'ismydoc', 'ext', 'sessionid', 'documentposition', 'datetime', 'weekday', 'screen']
df = df[columns_order]      # 컬럼 순서 변경
# print(df.head(5))

# q = """
#     SELECT weekday,
#             count(weekday) as count
#     FROM df
#     GROUP BY weekday
#     ORDER BY count DESC
#     """
# print(sql.sqldf(q, locals()))


# 2.2 Missing Value 확인
# print(df.info())
# print()
# print(df.isnull().sum(axis=0))


# 2.3 결측치 처리
# q = """
#     SELECT datetime,
#             screen,
#             count(distinct sessionid) as cnt
#     FROM df
#     GROUP BY datetime, screen
#     """
# print(sql.sqldf(q, locals()))
# grouped = df.groupby(['datetime', 'screen'])
# cnt_by_screen = grouped['sessionid'].nunique().unstack()
# print(cnt_by_screen)
# print()
# print(cnt_by_screen.isnull().sum(axis=0))
# print()
# print(cnt_by_screen.info())

# NaN 0으로 채우기
# cnt_by_screen = cnt_by_screen.fillna(0)
# print(cnt_by_screen)
# print()
# print(cnt_by_screen.isnull().sum(axis=0))
# print()
# print(cnt_by_screen.info())

# 레코드에 하나라도 NaN이 있으면 드롭
# print(cnt_by_screen.dropna(how='any'))
# 레코드의 모든 필드가 NaN이면 드롭
# print(cnt_by_screen.dropna(how='all'))
# NaN이 하나라도 있는 레코드를 select
# print(cnt_by_screen[cnt_by_screen.isnull().any(axis=1)])
# NaN을 median값으로 채우기
# print(cnt_by_screen.fillna(cnt_by_screen.median()))     # mean, max, min


# 2.4 결측치가 카테고리 변수인 경우
# Option 1. 최빈치 (mode)
# Option 2. 예측모델을 이용한 예측치


# 2.5 확장자명(ext) 통일
# print(df.ext.value_counts())
# print()
ext_dic = {'DOCX': 'DOC',
           'XLSX': 'XLS',
           'PPTX': 'PPT',
           'PPSX': 'PPT',
           'PPS': 'PPT',
           'ODT': 'TXT',
           'PNG': 'JPG'}
df['ext'] = df['ext'].replace(ext_dic)
# print(df['ext'].value_counts())


# 2.6 actiontype 통일
# print(df['actiontype'].value_counts())
# print()
act_dic = {'SAVEAS': 'SAVE',
           'SAVEAS_OTHER': 'SAVE',
           'EXPORT_SAME': 'EXPORT'}
df['actiontype'] = df['actiontype'].replace(act_dic)
# print(df.actiontype.value_counts())


# 2.7 신규 session_id 부여
# 필수는 아니나 계산량 감소를 위해 텍스트 사이즈 축소
# print(df.head(10))
uniq_sess = df['sessionid'].unique()
sess_dic = {sess: i for i, sess in enumerate(uniq_sess)}
df['sessionid'] = df['sessionid'].map(lambda x: sess_dic[x])
# print()
# print(df.head(10))
# print()
# print(df.tail(10))

df.to_csv('db/df_funnel_preprocessed.csv', mode='w')

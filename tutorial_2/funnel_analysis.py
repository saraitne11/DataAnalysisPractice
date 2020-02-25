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

df = pd.read_csv('db/df_funnel_preprocessed.csv', index_col=0)

# ###################################################
# ########### 2. EDA (탐색적 데이터 분석) #############
# ###################################################
# 일별 주요 통계
# 변수별 특성
# 구간별 전환율 (Funnel Analysis)
# 클러스터링
# 클러스터별 전환율 차이 파악


# 3.1 일별 Trend
# 일별 로그 카운트
# df.groupby('datetime').size().plot(c='r')
# plt.title('Daily Log Count')
# plt.grid(color='lightgrey', alpha=0.5, linestyle='--')
# plt.tight_layout()

# 일별 세션 카운트
# plt.figure()
# df.groupby('datetime')['sessionid'].nunique().plot(c='b')
# # df.groupby('datetime').agg({'sessionid': 'nunique'}).plot(c='b')
# plt.title('Daily Unique Session')
# plt.grid(color='lightgrey', alpha=0.5, linestyle='--')
# plt.tight_layout()


# 요일별 세션 카운트
plt.figure()
s = df.groupby('datetime')['sessionid'].nunique()
weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
s.index = pd.to_datetime(s.index).dayofweek
s.index = s.index.map(lambda x: weekdays[x])
s.plot(color='grey', kind='bar', rot=0)
plt.title('Count Session by day of the week')
plt.grid(color='lightgrey', alpha=0.5, linestyle='--')
plt.tight_layout()


# 요일별 세션 카운트2
plt.figure()
df.groupby('weekday')['sessionid'].nunique().plot(color='grey', kind='bar', rot=0)
plt.title('Count Session by day of the week')
plt.grid(color='lightgrey', alpha=0.5, linestyle='--')
plt.tight_layout()


plt.show()

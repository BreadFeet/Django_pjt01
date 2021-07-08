import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline: iPython의 magic fx은 사용할 수 없다!!!
import seaborn as sns
from sklearn import preprocessing
import folium
from config.settings import DATA_DIR, TEMPLATES
from config.settings import STATICFILES_DIRS

# 데이터 파일을 dataframe으로 바꾸기
df = pd.read_excel(DATA_DIR[0] + '/city_pop.xlsx')    # 시도별 전출입 인구수
elec = pd.read_excel(DATA_DIR[0] + '/elec_energy.xlsx')    # 남북한 전력 이용
auto = pd.read_csv(DATA_DIR[0] + '/auto-mpg.csv', header=None)     # 자동차 정보
auto.columns = ['mpg', 'cylinders', 'displacement', 'hp', 'weight', 'acceleration', 'model_year', 'origin', 'name']
ttn = sns.load_dataset('titanic')
col = pd.read_excel(DATA_DIR[0] + '/col_location.xlsx', index_col=0)     # 서울 대학교 위치정보
ggd = pd.read_excel(DATA_DIR[0] + '/gg_pop.xlsx')        # 경기도 인구 정보
stock = pd.read_csv(DATA_DIR[0] + '/stock-data.csv')

## 데이터 전처리 학습 ###############################################################################################

class P5:
    # 1. 누락 데이터 삭제
    def p172():      # 일부러 self 인수 안 넣어봤음!
        # print(ttn.info())       # 누락 정보 확인
        # print(ttn['deck'].value_counts(dropna=True))   # 누락 데이터 포함하여 unique의 count?????????????dropna 차이 없음????
        # print(ttn.isnull())     # 자료가 커서 t/f 개수 전부 확인 불가능
        # print(ttn.isnull().sum())    # null이어서 True인 것들의 합으로 개수 확인 가능

        ttn.dropna(axis=1, inplace=True, thresh=500)     # 결측치가 500개 이상인 컬럼은 삭제
        # print(ttn)
        # print(ttn.isnull().sum())

        ttn.dropna(subset=['age'], how='any', axis=0, inplace=True)    # age 컬럼에서 결측치 있으면 행 삭제
        # print(ttn.isnull().sum())     # age 컬럼에는 null이 더이상 없어야 함
        # print(ttn.info())


    # 2. 누락 데이터를 평균으로 치환
    def p178():
        avg = ttn['age'].mean()       # 결측치 = 평균값으로 치환할 목적
        # print(avg)
        # print(ttn.isnull().sum())     # age 컬럼 결측치 177개를 치환함
        ttn['age'].fillna(avg, inplace=True)
        # print(ttn.isnull().sum())       # age 컬럼에는 더이상 결측치 없어야 함


    # 3. 누락 데이터를 최빈값으로 치환
    def p180():
        et = ttn['embark_town'].value_counts(dropna=True)    # type: series
        # print(et)
        max_et = et.idxmax()
        ttn['embark_town'].fillna(max_et, inplace=True)
        print(ttn['embark_town'][825:830])     # 829번이 Southampton으로 치환


    # 4. 누락 데이터를 이웃 데이터값으로 치환
    def p181():
        ttn['embark_town'].fillna(method='ffill', inplace=True)
        print(ttn['embark_town'][825:830])    # 829번이 828번과 같은 값을 가진다

##############################################################################################################

class P51:
    # 1. 단위 환산: mpg -> kpl
    def p186():
        # print(auto.dtypes)       # mpg: float
        mpg_to_kpl = 1.60934 / 3.78541
        auto['kpl'] = auto['mpg'] * mpg_to_kpl
        # print(auto)
        auto['kpl'] = auto['kpl'].round(2)
        print(auto)


    # 2. 자료형 변환: object -> int
    def p188():
        # print(auto['hp'].unique())      # 데이터가 object인 것을 확인 가능
        # hp가 object인 이유: 중간의 결측치가 ?로 표기되어서
        auto['hp'].replace('?', np.nan, inplace=True)
        # print(auto['hp'].isnull().sum()    # NaN: 6개 결측치 확인됨

        # NaN 제거
        auto.dropna(subset=['hp'], axis=0, inplace=True)
        auto['hp'] = auto['hp'].astype('float')    # type 바꾸기
        print(auto['hp'].dtypes)


    # 3. 암호화 코드를 문자로 바꿔주기
    def p190():
        # print(auto['origin'].unique())
        auto['origin'].replace({1: 'USA', 2: 'EU', 3: 'JPN'}, inplace=True)
        # print(auto['origin'].unique())

        # 위 3개국이 반복되기 때문에 범주형 데이터 타입으로 표현할 수 있다
        auto['origin'] = auto['origin'].astype('category')
        print(auto['origin'].dtypes)

        # dtype이 category라면 다른 범주는 못 들어오나? - NO! 추가될 수 있다!
        auto.loc['test'] = [21.3, 4, 140, 831, 13578.2, 430, 2013, 'Korea', 'SM5']
        print(auto.iloc[-1])


#####################################################################################################

class P52:
    # 1. 구간 분할: binning
    def p192():
        auto['hp'].replace('?', np.nan, inplace=True)
        auto.dropna(subset=['hp'], axis=0, inplace=True)
        auto['hp'] = auto['hp'].astype('float')

        # hp 컬럼값의 구간에 따라 bin 만들어서 category화
        cnt, bin_edges = np.histogram(auto['hp'], bins=3)   # bin은 3개, 경계값은 4개
        # print(cnt, bin_edges)

        # pd.cut 함수로 float -> category(object) 변환
        bin_names = ['Low', 'Regular', 'High']
        auto['hp_bin'] = pd.cut(x=auto['hp'], bins=bin_edges, labels=bin_names, include_lowest=True)
        # include_lowest: 최저 경계값 포함할 것인가, right: 최대 경계값 포함할 것인가
        # print(auto[['hp', 'hp_bin']])
        # print(auto[['hp', 'hp_bin']].dtypes)     # hp_bin: category

        # 2. 더미 변수
        hp_dm = pd.get_dummies(auto['hp_bin'])
        # print(hp_dm)

        # 3. 희소 행렬
        label = preprocessing.LabelEncoder()      # label encoder 객체 생성
        onehot = preprocessing.OneHotEncoder()    # onehot enoder 객체 생성

        labelled = label.fit_transform(auto['hp_bin'].head(15))
        # print(labelled)         # 0, 1, 2 값으로 바꿈(label 순서는 다를 수 있음): binning?????????????????????????????
        # print(type(labelled))   # np.array

        reshaped = labelled.reshape(len(labelled), 1)     # (15, 1) 2차원 행렬 모양으로 변환
        # print(reshaped)

        # 희소 행렬로 만들기
        onehot_t = onehot.fit_transform(reshaped)
        print(onehot_t)    # [2] -> 0행 2열에 숫자 1을 채움. (0, 0, 1)를 간단히 표현!
        print(type(onehot_t))      # type: csr_matrix
        print(onehot_t[2, 2])      # 희소행렬에서 (2, 2) 값인 1을 반환한다


    # 4. 정규화
    def p198():
        auto['hp'].replace('?', np.nan, inplace=True)
        auto.dropna(subset=['hp'], axis=0, inplace=True)
        auto['hp'] = auto['hp'].astype('float')

        # 컬럼의 최대값으로 나누기
        auto['hp'] = auto['hp'] / abs(auto['hp'].max())
        print(auto['hp'].describe())   # 최소값: 0.2 , 최대값: 1

######################################################################################################

class P53:
    # 1. 시계열 데이터 - Timestamp
    def p201():
        # print(stock.info())    # Date 컬럼: object
        stock['new_Date'] = pd.to_datetime(stock['Date'])
        # print(stock)
        # print(stock['new_Date'].dtypes)      # datetime64[ns]
        stock.set_index('new_Date', inplace=True)
        # print(stock)


    # 2. 시계열 데이터 - Period
    def p205():
        dates = ['2019-01-01', '2019-03-01', '2019-06-01']
        # string list -> datetime timestamp 변환
        ts_dates = pd.to_datetime(dates)
        # print(ts_dates)
        # print(type(ts_dates))     # DatetimeIndex object

        # datetime timestamp -> period 변환
        day = ts_dates.to_period(freq='D')
        print(day)
        month = ts_dates.to_period(freq='M')
        print(month)
        year = ts_dates.to_period(freq='A')
        print(year)
        print(type(year))         # PeriodIndex object


    # 3. 시계열 데이터 - timestamp - 만들기
    def p206():
        ts_ms = pd.date_range(start='2019-01-01',
                              end=None,
                              periods=6,
                              freq='MS',          # month start: 1월 시작일 기준으로 6개
                              tz='Asia/Seoul')
        print(ts_ms)

        ts_m = pd.date_range(start='2019-01-01',
                             periods=6,
                             freq='M',            # month (end): 1월 마지막일 기준으로 6개
                             tz='Asia/Seoul')
        print(ts_m)


    # 4. 시계열 데이터 날짜 자르기
    def p209():
        stock['new_Date'] = pd.to_datetime(stock['Date'])
        # print(stock)
        # print(stock['new_Date'].dt)     # dt: DatetimeProperties object?????????????????????????????
        stock['Year'] = stock['new_Date'].dt.year
        stock['Month'] = stock['new_Date'].dt.month
        stock['Day'] = stock['new_Date'].dt.day
        # print(stock)

        # Period 정보 만들기
        stock['Year2'] = stock['new_Date'].dt.to_period(freq='A')
        # print(stock)
        stock['Yr_Mon'] = stock['new_Date'].dt.to_period(freq='M')
        print(stock)


    # 5. 시계열 데이터를 인덱스로 활용
    def p212():
        stock['new_Date'] = pd.to_datetime(stock['Date'])
        stock.set_index('new_Date', inplace=True)
        # print(stock)

        # st_18 = stock['2018']     # index를 마치 컬럼처럼 호출함 -> deprecated 예정 -> loc 사용
        # print(st_18)
        # st_1872 = stock['2018-07-02']
        # print(st_1872)
        # st_range = stock['2018-06-01':'2018-10-31']
        # print(st_range)               # 왜 안나오지???????????????????????????????????????/

        st_1807 = stock.loc['2018-07']
        # print(st_1807)
        slice = stock.loc['2018-07', 'Start':'High']
        # print(slice)

        # 오늘과 index 날짜 사이의 시간 간격 계산
        today = pd.to_datetime('2021-07-08')
        stock['time_delta'] = today - stock.index
        stock.set_index('time_delta', inplace=True)
        # print(stock)
        diff = stock['1120 days':'1125 days']
        print(diff)



if __name__ == '__main__':
    P53.p212()
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
stock = pd.read_csv(DATA_DIR[0] + '/stock.csv')

## Part5. 데이터 전처리 학습 ###############################################################################################

class P5:
    # 1. 누락 데이터 삭제
    def p172():      # 일부러 self 인수 안 넣어봤음!
        # print(ttn.info())       # 누락 정보 확인
        # print(ttn['deck'].value_counts(dropna=False))   # 누락 데이터 포함하여 unique의 count
        # print(ttn.isnull())     # 자료가 커서 t/f 개수 전부 확인 불가능
        # print(ttn.isnull().sum())    # null이어서 True인 것들의 합으로 개수 확인 가능

        ttn.dropna(axis=1, thresh=500, inplace=True)     # 결측치가 500개 이상인 컬럼은 삭제
        # print(ttn)
        # print(ttn.isnull().sum())

        ttn.dropna(subset=['age'], how='any', axis=0, inplace=True)    # age 컬럼에서 결측치 있으면 행 삭제. any/all 차이 없음
        print(ttn.isnull().sum())     # age 컬럼에는 null이 더이상 없어야 함
        print(ttn.info())


    # 2. 누락 데이터를 평균으로 치환
    def p178():
        avg = ttn['age'].mean()       # 결측치 = 평균값으로 치환할 목적
        print(avg)
        print(ttn.isnull().sum())     # age 컬럼 결측치 177개를 치환함
        ttn['age'].fillna(avg, inplace=True)
        print(ttn.isnull().sum())       # age 컬럼에는 더이상 결측치 없어야 함


    # 3. 누락 데이터를 최빈값으로 치환
    def p180():
        et = ttn['embark_town'].value_counts(dropna=False)    # type: series
        print(et)
        max_et = et.idxmax()
        print(max_et)
        ttn['embark_town'].fillna(max_et, inplace=True)
        print(ttn['embark_town'][825:830])     # 829번이 Southampton으로 치환


    # 4. 누락 데이터를 이웃 데이터값으로 치환
    def p181():
        ttn['embark_town'].fillna(method='bfill', inplace=True)
        print(ttn['embark_town'][825:831])    # 829번이 830번과 같은 값을 가진다

##############################################################################################################

class P51:
    # 1. 단위 환산: mpg -> kpl
    def p186():
        print(auto.dtypes)       # mpg: float
        mpg_to_kpl = 1.60934 / 3.78541
        auto['kpl'] = auto['mpg'] * mpg_to_kpl
        print(auto)
        auto['kpl'] = auto['kpl'].round(2)
        print(auto)


    # 2. 자료형 변환: object -> int
    def p188():
        # print(auto['hp'].unique())      # 고유한 값 확인 가능
        # hp가 object인 이유: 중간의 결측치가 ?로 표기되어서
        auto['hp'].replace('?', np.nan, inplace=True)
        # print(auto['hp'].isnull().sum())    # NaN: 6개 결측치 확인됨
        # print(auto['hp'].notnull().sum())   # 392개의 값이 있음

        # NaN 6개 제거하고 dtype 변경
        auto.dropna(subset=['hp'], axis=0, inplace=True)
        print(auto['hp'].dtypes)       # object
        auto['hp'] = auto['hp'].astype('float')    # type 바꾸기
        print(auto['hp'].dtypes)       # float


    # 3. 암호 코드를 문자로 바꿔주기
    def p190():
        # print(auto['origin'].unique())
        auto['origin'].replace({1: 'USA', 2: 'EU', 3: 'JPN'}, inplace=True)
        # print(auto['origin'].unique())

        # 위 3개국이 반복되기 때문에 범주형 데이터 타입으로 표현할 수 있다
        auto['origin'] = auto['origin'].astype('category')
        # print(auto['origin'].dtypes)

        # dtype이 category라면 다른 범주(KOR)는 못 들어오나? - NO! 추가될 수 있다!
        auto.loc['test'] = [21.3, 4, 140, 831, 13578.2, 430, 2013, 'KOR', 'SM5']
        print(auto.iloc[-3:])


#####################################################################################################

class P52:
    def p192():
        auto['hp'].replace('?', np.nan, inplace=True)
        auto.dropna(subset=['hp'], axis=0, inplace=True)
        auto['hp'] = auto['hp'].astype('float')

        # 1. 구간 분할: binning--------------------------------------------------------------------------
        # hp 컬럼값의 구간에 따라 bin 만들어서 category화
        cnt, bin_edges = np.histogram(auto['hp'], bins=3)   # bin은 3개, 경계값은 4개
        # print(cnt, bin_edges)

        # pd.cut 함수로 float -> category(object) 변환
        bin_names = ['Low', 'Regular', 'High']
        auto['hp_bin'] = pd.cut(x=auto['hp'], bins=bin_edges, labels=bin_names, include_lowest=True, right=True)
        # include_lowest: 최저 경계값 포함할 것인가, right: 최대 경계값 포함할 것인가
        # print(auto[['hp', 'hp_bin']])
        # print(auto[['hp', 'hp_bin']].dtypes)     # hp_bin: category

        # pd.cut에도 bins를 구할 수 있는데, 꼭 np.histogram에서 bins을 얻어야 하나? - Nope!
        result = pd.cut(auto['hp'], bins=3, labels=bin_names, include_lowest=True, right=True, retbins=True)
        # print(result)   # bins: 최소, 최대값 포함하기 위해서 0.1% 양쪽으로 연장된 것 외에 큰 차이 없음

        # 카테고리로 변환 후 값이 똑같은지 비교
        sr = pd.cut(auto['hp'], bins=3, labels=bin_names, include_lowest=True, right=True)
        # print(auto['hp_bin'] is sr)       # False...이럴수가! 출력도 같은데 왜 다르다고 나오는지 모르겠음??????????????
        # 몇번째가 다른지 확인
        # for hist, cut in zip(auto['hp_bin'], sr):
        #     if hist != cut:
        #         print(hist, cut)    # 출력값 없고, 실제로 hist=cut
        # 카테고리 별 개수 확인해서 다른지 보기
        # print(auto['hp_bin'].value_counts())
        # print(sr.value_counts())     # 결과 같음....


        # 2. 더미 변수---------------------------------------------------------------------------------------
        hp_dm = pd.get_dummies(auto['hp_bin'])
        # print(hp_dm)

        # 3. 희소 행렬---------------------------------------------------------------------------------------
        label = preprocessing.LabelEncoder()      # label encoder 객체 생성
        onehot = preprocessing.OneHotEncoder(sparse=True)    # onehot encoder 객체 생성
        # sparse=True: 연관배열로 바뀜, False: 희소행렬 그대로 출력

        # 3-1. [low, regular, high] 카테고리를 onehot-encoding
        t = onehot.fit_transform(auto['hp_bin'].to_numpy().reshape(-1, 1))   # 입력 data는 2D여야 함
        # print(t)

        # 3-2. [low, regular, high]를 [0, 1, 2]로 라벨링을 바꾼 뒤 onehot-encoding
        labelled = label.fit_transform(auto['hp_bin'].head(15))
        # print(labelled)         # 카테고리 라벨값을 0, 1, 2 값으로 바꿈(label 순서는 다를 수 있음)
        # print(type(labelled))   # np.array
        t = onehot.fit_transform(labelled.reshape(-1, 1))
        # print(t)
        # print(type(t))          # type: csr_matrix
        # print(t[2, 1], t[2, 2])      # 희소행렬에서 (2, 2) 값인 1을 반환한다


    # 4. 정규화
    def p198():
        auto['hp'].replace('?', np.nan, inplace=True)
        auto.dropna(subset=['hp'], axis=0, inplace=True)
        auto['hp'] = auto['hp'].astype('float')

        # 1. 컬럼의 최대값으로 나누기
        # auto['hp'] = auto['hp'] / abs(auto['hp'].max())
        # print(auto['hp'].describe())   # 최소값: 0.2 , 최대값: 1

        # 2. 최대-최소 차로 나누기
        auto['hp'] = (auto['hp'] - auto['hp'].min()) / (auto['hp'].max() - auto['hp'].min())
        print(auto['hp'].describe())


######################################################################################################

class P53:
    # 1. 시계열 데이터 - Timestamp
    def p201():
        print(stock.info())    # Date 컬럼: object
        stock['new_Date'] = pd.to_datetime(stock['Date'])
        print(stock)
        print(stock['new_Date'].dtypes)      # datetime64[ns]
        stock.set_index('new_Date', inplace=True)
        print(stock)


    # 2. 시계열 데이터 - Period
    def p205():
        dates = ['2019-01-01', '2019-03-01', '2019-06-01']
        # string list -> timestamp 변환
        ts_dates = pd.to_datetime(dates)
        # print(ts_dates)
        # print(type(ts_dates))     # DatetimeIndex object

        # datetime timestamp -> period 변환
        day = ts_dates.to_period(freq='D')
        # print(day)      # 각각의 값이 하루의 0~24시의 기간을 말함!!
        month = ts_dates.to_period(freq='M')
        # print(month)    # 각각의 값이 각 월의 1~마지막일의 기간을 말함!!
        year = ts_dates.to_period(freq='A')
        # print(year)
        # print(type(year))         # PeriodIndex object

        # 기간의 시작과 끝을 확인
        print(month.start_time)
        print(month.end_time)


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
        # print(stock['new_Date'].dt)     # dt: DatetimeProperties object: datetime 속성에 접근할 수 있다
        stock['Year'] = stock['new_Date'].dt.year
        stock['Month'] = stock['new_Date'].dt.month
        stock['Day'] = stock['new_Date'].dt.day
        # print(stock)

        # Period 정보 만들기
        stock['Year2'] = stock['new_Date'].dt.to_period(freq='A')   # A: annum
        # print(stock)     # 각 시점을 1년 기간으로 만듦
        stock['Yr_Mon'] = stock['new_Date'].dt.to_period(freq='M')
        # print(stock)     # 각 시점을 1달 기간으로 만듦
        # print(stock['Year2'][0].start_time, stock.loc[0, 'Year2'].end_time)

        # Year 컬럼과 Year2 컬럼의 차이
        print(stock['Year'].dtype, type(stock['Year'][0]))     # 둘다 int
        print(stock['Year2'].dtype, type(stock['Year2'][0]))   # period, Period

    # 5. 시계열 데이터를 인덱스로 활용
    def p212():
        stock['new_Date'] = pd.to_datetime(stock['Date'])
        stock.set_index('new_Date', inplace=True)
        # print(stock)

        st_18 = stock['2018']     # index를 마치 컬럼처럼 호출함 -> deprecated 예정 -> loc 사용
        # print(st_18)
        st_1872 = stock['2018-07-02']
        # print(st_1872)
        st_range = stock['2018-06-05':'2018-06-01']     # 날짜 역순으로 정렬되어 있음
        # print(st_range)

        st_1807 = stock.loc['2018-07']
        # print(st_1807)
        slice = stock.loc['2018-07', 'Start':'High']
        # print(slice)


        # 6. 오늘과 index 날짜 사이의 시간 간격 계산------------------------------------------------
        today = pd.to_datetime('2021-07-08')
        stock['time_delta'] = today - stock.index     # datetime 하나에서 datetime series를 뺌
        # print(stock)
        stock.set_index('time_delta', inplace=True)
        # print(stock)
        # print(stock.index)               # TimedeltaIndex, dtype: timedelta64

        # print(stock.loc['1130 days'])        # indexing
        diff = stock['1120 days':'1125 days']         # slicing
        # print(diff)


if __name__ == '__main__':
    P53.p212()
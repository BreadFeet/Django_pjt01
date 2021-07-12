## 교재 part6 수업 내용
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

class Util:
    def add_10(n):
        return n + 10

    def add_both(a, b):
        return a + b


class P6:
    def p218(self):
        df = ttn.loc[:, ['age', 'fare']]
        df['ten'] = 10
        # print(df)

        # Apply 함수 >> Jupyter로 이사감...





if __name__ == '__main__':
    P6().p218()


# Day34
import pandas as pd
import matplotlib.pyplot as plt
from config.settings import DATA_DIR

df = pd.read_csv(DATA_DIR[0] + '/auto-mpg.csv', header=None)
df.columns = ['mpg', 'cylinders', 'displacement', 'hp', 'weight', 'acceleration', 'model_year', 'origin', 'name']

ddf = pd.read_excel(DATA_DIR[0] + '/elec_energy.xlsx')

class P084:
    def df01(self):
        print(df.head())
        # print(df.shape)
        # print(df.info())    # hp, name: object
        # print(df['hp'])       # 내용은 숫자임!!!
        # print(df.dtypes)
        # print(df.describe(include='all'))    # object 컬럼도 포함

    def df02(self):
        vc = df['origin'].value_counts()     # unique의 종류와 개수 출력
        # print(vc)
        df2 = df[['mpg', 'weight']].mean()
        # print(df2)      # type: series
        df3 = df[(df['mpg'] > df['mpg'].mean()) & (df['mpg'] < 20)]
        print(df3)

    def df03(self):
        # print(ddf)
        ddf2 = ddf.iloc[[0, 5], 3:]     # 남한, 북한 합계 row & 연도 col만 가져오기
        # print(ddf2)
        ddf2.index=['South', 'North']
        print(ddf2)
        # print(ddf2.columns)      # 컬럼명이 str
        ddf2.columns = ddf2.columns.map(int)   # int로 바꾸기 - plotting과는 상관 없음!!!!
        ddf2.T.plot()       # x축이 str, int 상관없이 plotting 가능
        plt.show()          # 이 코드 없으면 화면 안뜸!




if __name__ == '__main__':
    P084().df03()
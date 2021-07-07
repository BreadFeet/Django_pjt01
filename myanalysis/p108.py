import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from config.settings import DATA_DIR


class P108:
    def p108(self):
        df = pd.read_excel(DATA_DIR[0] + '/city_pop.xlsx', engine='openpyxl', header=0)   # engine: 경로를 넣은게 아니라면 파일 형태 확인을 위해서 지정해야 함
        df.fillna(method='ffill', inplace=True)  # method: 채우는 방법, ffill: forward fill - 앞 유효값을 사용
        mask = (df['전출지별'] == '서울특별시') & (df['전입지별'] != '서울특별시')   # 서울에서 나가서 타지역으로 간 경우
        seoul = df[mask]
        seoul.drop('전출지별', axis=1, inplace=True)
        seoul.rename({'전입지별':'전입지'}, axis=1, inplace=True)
        seoul.set_index('전입지', inplace=True)
        ggd = seoul.loc['경기도']           # 경기도 전출 사례만 추출
        # print(ggd.to_list())

        # Plotting
        # plt.plot(ggd.index, ggd.values)
        # plt.show()

        result = []
        d = {}
        d['name'] = '경기도'
        d['data'] = ggd.to_list()
        result.append(d)

        return result






if __name__ == '__main__':
    P108().p108()
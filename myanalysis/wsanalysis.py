# 2021년 7월 7일 오전 워크샵 분석페이지
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from config.settings import DATA_DIR, TEMPLATES, STATICFILES_DIRS


class wsAnalysis:
    def P130(self, frm):    # frm은 문자열로 들어온다
        df = pd.read_excel(DATA_DIR[0] + '/city_pop.xlsx')
        # print(df)
        df.fillna(method='ffill', inplace=True)
        # print(df)

        # from으로 받은 전출지 --> 충청남도, 경상북도, 강원도, 전라남도 전출 인구 확인
        mask = (df['전출지별'] == frm) & (df['전입지별'].isin(['충청남도', '경상북도', '강원도', '전라남도']))
        ct_from = df[mask]
        # print(ct_from)

        ct_from.drop(columns=['전출지별'], inplace=True)
        ct_from.set_index('전입지별', inplace=True)
        # print(ct_from)

        # Highcharts에 맞게 전송할 데이터 준비
        data = []
        for i in range(len(ct_from.index)):
            dic = {}
            dic['name'] = ct_from.index[i]
            dic['data'] = ct_from.iloc[i].to_list()
            data.append(dic)

        result = {
            'title': frm,
            'data': data
        }               # json으로 보내야 하니까 []에 담으면 안된다!!!

        return result

#########################################################################################################
    def P136(self, start, end, con):    # 시작/끝/나라명 연도 모두 문자열로 들어옴. 컬럼명도 string
        df = pd.read_excel(DATA_DIR[0] + '/elec_energy.xlsx')
        # print(df)

        if con == 'nk':
            kr = df.iloc[5:9]
            # print(kr)
            title = 'North Korea'
        elif con == 'sk':
            kr = df.iloc[:5]
            title = 'South Korea'
        # print(kr)
        # print(type(kr.loc[4, '1990']))    # '-' 결측치의 데이터 타입 확인: string
        kr.replace('-', 0, inplace=True)
        # print(kr)

        kr.drop('전력량 (억㎾h)', axis=1, inplace=True)
        kr.rename(columns={'발전 전력별':'발전'}, inplace=True)
        kr.set_index('발전', inplace=True)
        if con == 'nk':
            kr.drop('원자력', axis=0, inplace=True)
        # print(kr)
        # print(kr.columns)      # 연도: 문자열

        # 입력받은 start, end에 따라 데이터 추출하기 - 북한만 있을 때
        # 수력 데이터
        # water = kr.loc['수력', start:end].to_list()
        # print(water)
        # 화력 데이터
        # fire = kr.loc['화력', start:end].to_list()

        # x축 데이터
        xaxis = list(map(int, range(int(start), int(end) + 1)))

        # 증감률 계산
        t = kr.T
        # print(t)
        t['전년합계'] = t['합계'].shift(periods=1, axis=0)
        # print(t)
        t['증감률'] = ((t['합계']-t['전년합계'])/t['전년합계']) * 100
        # print(t)
        # NaN은 0으로 지정 - NaN인 상태이면 highcharts에서 인식 못해서 그래프 못 그림
        t.fillna(0, inplace=True)
        # print(t)
        # 지정한 start, end만 추출
        rate = t.loc[start:end, '증감률'].to_list()
        # print(rate)

        # # Highcharts에 보낼 json 만들기 - 북한만 있었을 때
        # result = {
        #     'xaxis': xaxis,
        #     'water': water,
        #     'fire': fire,
        #     'rate': rate
        # }

        # 발전 종류(index)별 데이터를 순서대로 모음
        amount = []
        for src in kr.index[1:]:
            amount.append(kr.loc[src, start:end].to_list())

        # Highcharts에 보낼 json 만들기 - 남북한 모두 있을 때
        data = []
        # data에 발전량 추가
        for i in range(len(kr.index[1:])):
            dic = {}
            dic['name'] = kr.index[1:][i]
            dic['type'] = 'column'
            dic['yAxis'] = 1               # line: 0, bar: 1
            dic['data'] = amount[i]
            dic['tooltip'] = {'valueSuffix':' kWh'}
            data.append(dic)
        # data에 증감률 추가
        dic = {}
        dic['name'] = '전년대비 증감률'
        dic['type'] = 'spline'
        dic['data'] = rate
        dic['tooltip'] = {'valueSuffix':'%'}
        data.append(dic)

        result = {
            'title': title,
            'xaxis': xaxis,
            'data': data
        }
        print(result)
        return result


################################################################################################

    def P154(self):
        ttn = sns.load_dataset('titanic')
        # print(ttn)

        # subplot 만들기
        fig = plt.figure(figsize=(15, 8))
        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(132)
        ax3 = fig.add_subplot(133)

        # 그래프 1
        sns.barplot(x='sex', y='survived', data=ttn, ax=ax1)  # groupby 한 결과처럼 나온다
        # plt.savefig(STATICFILES_DIRS[0] + '/barchart1.png')   # 차트 1개 그린채로 저장됨

        # 그래프 2
        sns.barplot(x='sex', hue='class', y='survived', data=ttn, ax=ax2)   # hue: sub_x처럼 나뉜다. dodge=True 상태 -> stacked
        # plt.savefig(STATICFILES_DIRS[0] + '/barchart2.png')

        # 그래프 3
        sns.barplot(x='sex', hue='class', y='survived', data=ttn, ax=ax3, dodge=False)
        plt.savefig(STATICFILES_DIRS[0] + '/barchart3.png')
        plt.show()

#################################################################################################

    def P168(self, year):    # year: int
        df = pd.read_excel(DATA_DIR[0] + '/gg_pop.xlsx')
        # print(df)
        # print(df.columns)     # 컬럼명: int

        # Folium으로 Choropleth 그릴 경계 json 데이터 준비 - load 안해도 됨
        # geo_data = json.load(open(DATA_DIR[0] + '/gg_boundary.json'))

        # threshold 계산
        legend_scale = np.linspace(df[year].min(), df[year].max(), num=6).tolist()

        # 기본 맵 그리기
        map = folium.Map(location=[37.55, 127], zoom_start=8, tiles='Stamen Terrain')

        # Choropleth 그려서 기본 맵에 추가하기
        folium.Choropleth(
            geo_data=DATA_DIR[0] + '/gg_boundary.json',
            data=df,
            columns=['구분', year],
            key_on='feature.properties.name',
            threshold_scale=legend_scale,
            fill_color='BuPu', fill_opacity=0.7,
            line_color='white', line_weight=2, line_opacity=0.7
,         ).add_to(map)
        map.save(TEMPLATES[0]['DIRS'][0] + '/map.html')

        print('작동 완료')



if __name__ == '__main__':
    wsAnalysis().P136('1995', '2005', 'sk')
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline: iPython의 magic fx은 사용할 수 없다!!!
import seaborn as sns
import folium
# print(folium.__version__)    # 0.12.1
from config.settings import DATA_DIR, TEMPLATES
from config.settings import STATICFILES_DIRS

# 데이터 파일을 dataframe으로 바꾸기
df = pd.read_excel(DATA_DIR[0] + '/city_pop.xlsx')    # 시도별 전출입 인구수
elec = pd.read_excel(DATA_DIR[0] + '/elec_energy.xlsx')    # 남북한 전력 이용
auto = pd.read_csv(DATA_DIR[0] + '/auto-mpg.csv', header=None)     # 자동차 정보
ttn = sns.load_dataset('titanic')
col = pd.read_excel(DATA_DIR[0] + '/col_location.xlsx', index_col=0)     # 서울 대학교 위치정보
ggd = pd.read_excel(DATA_DIR[0] + '/gg_pop.xlsx')        # 경기도 인구 정보


class P109:
    def mat01(self):
        # print(df)
        # 카테고리 '전국' 밑에 NaN값을 '전국'으로 forward fill
        df2 = df.fillna(method='ffill')
        # print(df2)

        # 전출지: 서울 -> 전입지: 서울 외의 경우만 추려내기
        mask = (df2['전출지별'] == '서울특별시') & (df2['전입지별'] != '서울특별시')    # row별 t/f값 얻어짐
        # print(mask)
        seoul = df2[mask]
        # print(seoul)

        # 컬럼 정리
        seoul.drop(['전출지별'], axis=1, inplace=True)
        seoul.rename({'전입지별':'전입지'}, axis=1, inplace=True)
        # print(seoul)

        # 인덱스 새로 설정
        seoul.set_index('전입지', inplace=True)
        # print(seoul)

        # 서울 -> 경기도 전입 현황만 추출
        ggd = seoul.loc['경기도']      # series
        # print(ggd)

        # Plotting - series의 index와 값을 이용
        plt.plot(ggd.index, ggd.values)
        plt.title('서울 -> 경기')
        # 이미지 저장 - show()로 plt 작업이 끝나기 전에 저장해야 한다!!!!
        # plt.savefig(STATICFILES_DIRS[0] + '/chart.jpg')    # static 폴더 import
        # plt.show()

        # y만 가지고 plotting - x축은 index로자동 생성
        # plt.plot(ggd.values)
        # plt.show()

        # Series 전체를 넣어서 plotting - x축은 알아서 index로 설정됨
        # plt.plot(ggd)
        # plt.show()

        # DataFrame을 넣어도 된다고 하니까 해보기 - 가능!
        df_ggd = pd.DataFrame(ggd)      # series의 index가 그대로 index가 된 상태
        # print(df_ggd)
        # plt.plot(df_ggd)
        # plt.show()

        # x축의 값이 index가 아니라 컬럼이어도 자동으로 인식할까???? - NO! Plotting 못함!
        df_ggd.reset_index(inplace=True)
        # print(df_ggd)
        # plt.plot(df_ggd)
        # plt.show()

#########################################################################################################
    def mat02(self):
        # 카테고리 '전국' 밑에 NaN값을 '전국'으로 forward fill
        df2 = df.fillna(method='ffill')
        # print(df2)

        # 전출지: 서울 -> 전입지: 서울 외의 경우만 추려내기
        mask = (df2['전출지별'] == '서울특별시') & (df2['전입지별'] != '서울특별시')  # row별 t/f값 얻어짐
        # print(mask)   # 이게 출력 가능한 값인가?????????????????????????????????
        seoul = df2[mask]
        # print(seoul)

        # 컬럼 정리
        seoul.drop(['전출지별'], axis=1, inplace=True)
        seoul.rename({'전입지별': '전입지'}, axis=1, inplace=True)
        # print(seoul)

        # 인덱스 새로 설정
        seoul.set_index('전입지', inplace=True)
        # print(seoul)

        # 서울 -> 4개 지역 전출인구만 추출
        cggj = seoul.loc[['충청남도', '경상북도', '강원도', '전라남도']]
        # print(cggj)
        t = cggj.T
        # print(t)

        # 교재 129쪽 실습
        plt.style.use('ggplot')
        # print(t.index)                   # index값이 str
        # t.index = t.index.map(int)       # 꼭 int가 되어야 plotting 가능한 것은 아님!
        t.plot(kind="area", figsize=(10, 5), stacked=True, alpha=0.2)
        plt.rc('font', family='Malgun Gothic')    # label 한글 깨지는것 해결
        # plt.legend()
        # plt.show()

        # cggj 데이터의 우측에 total 컬럼 만들기
        cggj['Total'] = cggj.sum(axis=1)
        # print(cggj)

        # cggj 데이터의 아래측에 total 행 만들기
        cggj.loc['Total'] = cggj.sum(axis=0)
        # print(cggj)

        # Total 컬럼으로 정렬
        cggj.sort_values(by='Total', ascending=False, inplace=True)
        # print(cggj)

#####################################################################################################
    def mat03(self):
        # print(elec)
        # 교재 136쪽 그래프를 어떻게 코드로 구현할 수 있을까?
        north = elec.loc[5:9]
        north.drop('전력량 (억㎾h)', axis=1, inplace=True)
        north.set_index('발전 전력별', inplace=True)
        # print(north)
        t = north.T
        # print(t)
        t.drop('원자력', axis=1, inplace=True)
        # print(t)
        t.rename(columns={'합계':'총발전량'}, inplace=True)
        # print(t)

        # 올해 발전량과 전년 발전량을 비교하기 위해서 shift!!!!!!!!!!!!!!
        t['1년전'] = t['총발전량'].shift(1, axis=0)
        # print(t)         # 한 행에 올해와 전년 정보같이 담김!!!!!!!!

        # 증감률
        t['증감률'] = ((t['총발전량'] - t['1년전']) / t['1년전']) * 100
        # print(t)

############################################################################################
    def mat04(self):
        auto.columns = ['mpg', 'cylinders', 'displacement', 'hp', 'weight', 'acceleration', 'model_year', 'origin', 'name']
        # print(auto)

        # 국가별(origin) 차량의 개수 구하기
        auto['count'] = 1             # 데이터 개수 카운트 목적으로 삽입
        df = auto.groupby(by='origin').sum()
        # print(df)
        df.index = ['USA', 'EU', 'JPN']
        # print(df)


############################################################################################
    def mat05(self):
        auto.columns = ['mpg', 'cylinders', 'displacement', 'hp', 'weight', 'acceleration', 'model_year', 'origin', 'name']
        df = auto[auto['origin'] == 1]['mpg']
        print(df)


############################################################################################
    def mat06(self):
        # print(ttn)
        # pivot table 만들기
        ttn2 = ttn.pivot_table(index=['sex'], columns=['class'], aggfunc='size')   # size: 개수
        # print(ttn2)
        ttn3 = ttn.pivot_table(index=['sex'], columns=['class'], values='survived', aggfunc=np.size)
        # print(ttn3)    # ttn2와 같은 결과

        # pivot 함수를 써서 만들어보기: groupby -> pivot
        group = ttn.groupby(['sex', 'class'], as_index=False).count()[['sex', 'class', 'survived']]
        # print(group)
        ttn4 = group.pivot(index='sex', columns='class')    # 인수 index, columns는 기존 컬럼에서 골라야하므로 위에서 as_index=F 설정해야함
        print(ttn4)


#############################################################################################
    def mat07(self):
        seoul = folium.Map(location=[37.55, 126.98], zoom_start=12)
        # html 저장위치 확인
        print(TEMPLATES[0]['DIRS'][0])    # 장고 templates 경로 밑에 저장하기 위해서 templates 위치를 app밖으로 꺼내야 한다!
        seoul.save(TEMPLATES[0]['DIRS'][0] + '/seoul_map.html')


########################################################################################################
    def mat08(self):
        seoul = folium.Map(location=[37.55, 126.98], zoom_start=12)
        # 서울 지도 위에 마커로 대학교 위치 추가
        # print(col)
        for name, lat, long in zip(col.index, col['위도'], col['경도']):
            folium.Marker([lat, long], popup=name).add_to(seoul)
        seoul.save(TEMPLATES[0]['DIRS'][0] + '/seoul_col.html')


######################################################################################################
    def mat09(self):       # Choropleth 지도 그리기
        # print(ggd)
        # ggd.set_index('구분', inplace=True)
        # print(ggd)

        # 경기도구역경계 json 파일을 불러온다
        geo_path = DATA_DIR[0] + '/gg_boundary.json'
        geo_data = json.load(open(geo_path), encoding='utf-8')      # load: 파일에 있는 json -> python object
        # print(geo_data)       # encoding 문제 생기면 json 파일 자체를 ANSI로 저장하고 와야함

        ggd_map = folium.Map(location=[37.55, 126.98], zoom_start=9)

        folium.Choropleth(          # ggd_map.Choropleth 함수는 없다(IBM이랑 버전이 다름)
            geo_data=geo_path,      # json load하지 않고 바로 가져다 써도 됨
            data=ggd,
            columns=['구분', 2007],
            key_on='feature.properties.name',
            fill_color='YlOrRd', fill_opacity=0.7, line_opacitty=0.3,
            threshold_scale=[10000, 100000, 300000, 500000, 700000]     # 데이터 범위 scale legend
        ).add_to(ggd_map)
        ggd_map.save(TEMPLATES[0]['DIRS'][0] + '/gg_choromap.html')





if __name__ == '__main__':
    P109().mat09()
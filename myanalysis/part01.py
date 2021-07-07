import pandas as pd

data = {
    '수학': [90, 80, 70],
    '영어': [91, 81, 71],
    '과학': [92, 82, 72],
    '국어': [93, 83, 73]
}
df = pd.DataFrame(data, index=['A', 'B', 'C'])

class P001:
    def series01(self):
        lst = ['20202027', 3.14, 'ABC', 100, True]
        sr = pd.Series(lst)
        # print(sr)
        # print(sr.values)         # array
        lst = sr.to_list()
        # print(lst)
        print(sr[[1, 3]])          # dataframe 처럼 여러 index를 가져오려면 [[ ]]

    def df01(self):
        df2 = df.copy()     # 원 dataframe은 변형하지 않기 위해서
        # row 삭제하기
        df2.drop(['A', 'C'], axis=0, inplace=True)
        print(df2)

    def df02(self):
        df2 = df.copy()
        # column 삭제하기
        df2.drop('영어', axis=1, inplace=True)
        print(df2)

    def df03(self):
        # location
        print(df.loc['B', '수학'])
        print(df.iloc[[1, 2], [1, 3]])    # 여러 row, col은 list에 담는다

    def df04(self):
        print(df['영어':'국어'])       # column slicing은 안됨!!
        print(df[1:3])               # row slicing만 됨
        # 컬럼 추가
        df['이름'] = ['영희', '철수', '민철']
        # index 설정
        df.set_index('이름', inplace=True)
        print(df)
        # location
        print(df.loc['영희', ['국어', '과학']])
        print(df.loc['영희', '영어': '국어'])     # 여기서는 컬럼이름 slicing 가능
        print(df.iloc[:, 0:2])

    def df05(self):
        print(df)
        # row 추가 - loc만 가능!
        df.loc['D'] = [99, 88, 77, 66]
        # df.iloc[4] = [100, 90, 80, 70]    # iloc cannot enlarge its target object: iloc은 존재하는 index만 locate 가능
        print(df)
        # transpose
        # df2 = df.T
        # print(df2)
        # reindex----------------------------------------------------------------
        df3 = df.reindex(['A', 'B', 'C', 'D', 'e', 'f'], fill_value=100)   # inplace 안됨
        # print(df3)
        # reset_index
        df4 = df.reset_index()
        # print(df4)
        # sort_index
        print(df4.sort_index(ascending=False))    # 값도 같이 정렬됨
        # sort_values
        print(df4.sort_values(by='과학'))          # index도 같이 정렬됨






if __name__ == '__main__':
    P001().df05()
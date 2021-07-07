import pandas as pd
from config.settings import DATA_DIR

data = {
    '수학': [90, 80, 70],
    '영어': [91, 81, 71],
    '과학': [92, 82, 72],
    '국어': [93, 83, 73]
}
df = pd.DataFrame(data, index=['A', 'B', 'C'])

class P058:
    def read01(self):
        df.to_csv(DATA_DIR[0] + '/df.csv')
        df.to_json(DATA_DIR[0] + '/df.json')
        df.to_excel(DATA_DIR[0] + '/df.xlsx')



if __name__ == '__main__':
    P058().read01()
import numpy as np
import pandas as pd

y = np.random.randint(100)

col = ['col1','col2','col3','col4','col5']
row = ['row1','row2','row3','row4']
data = [[1,2,3,pd.NA,5],[6,pd.NA,8,pd.NA,10],[11,12,13,14,15],[pd.NA,pd.NA,pd.NA,pd.NA,pd.NA]]
df = pd.DataFrame(data, row, col)

# print(y)

# randint 는  randint(low, high) 식으로도 사용 가능
def test():
    while True:
        y = np.random.randint(101)
        print(y)
        if y == 100:
            print("100 등장 !!")
            break

def zfill():
    ex = "1234"
    print(ex.zfill(5))
    print(ex.zfill(7))

def pdnow():
    now = pd.Timestamp.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    # timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    print(timestamp)

def test2():
    print(df.dropna())

test2()
# pdnow()
# zfill()
# test()
import numpy as np
import pandas as pd

y = np.random.randint(100)

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


pdnow()
# zfill()
# test()
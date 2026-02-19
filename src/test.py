import numpy as np

y = np.random.randint(100)

print(y)

# randint 는  randint(low, high) 식으로도 사용 가능
def test():
    while True:
        y = np.random.randint(101)
        print(y)
        if y == 100:
            print("100 등장 !!")
            break

test()
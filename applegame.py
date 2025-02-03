import random

apple = [[random.randint(1, 9) for _ in range(17)] for _ in range(10)]

for i in range(10):
    for j in range(17):
        print(apple[i][j], end=" ")
    print()
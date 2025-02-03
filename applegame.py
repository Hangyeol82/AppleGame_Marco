import random

apple = [[random.randint(1, 9) for _ in range(17)] for _ in range(10)]  # 숫자 랜덤 배정

for i in range(10):
    for j in range(17):
        print(apple[i][j], end=" ")
    print()
print("----------------------------------")
score = 0

def hori(x,y):
    global score
    num = 0
    for i in range(y, 17):
        num+=apple[x][i]
        if num == 10:
            for j in range(y, i):
                if apple[x][j] != 0:
                    score+=1
                    apple[x][j] = 0
            break

def vert(x,y):
    global score
    num = 0
    for i in range(x, 10):
        num+=apple[i][y]
        if num == 10:
            for j in range(x, i):
                if apple[j][y] != 0:
                    score+=1
                    apple[j][y] = 0
            break

def square(x,y):        # 투포인터? 활용해서 오른쪽, 아래쪽 포인터를 가지고 값 더하기
    pass

def clear(x,y):
    global score
    if apple[x][y] != 0:
        hori(x,y)
        vert(x,y)
    square(x,y)

changed = True      # 점수의 변경사항 여부
while(changed):
    tmp = score
    for i in range(10):
        for j in range(17):
            clear(i,j)
    if score == tmp:
        changed = False

for i in range(10):
    for j in range(17):
        print(apple[i][j], end=" ")
    print()

print(score)
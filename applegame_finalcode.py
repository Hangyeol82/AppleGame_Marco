import pyautogui
import time
from scipy.spatial import distance

pyautogui.useImageNotFoundException(False)  # 에러 방지
pyautogui.FAILSAFE = False  # 마우스 좌표 제한 해제

N = 10
M = 17


class Apple:
    def __init__(self, num, x, y):
        self.num = num
        self.x = x
        self.y = y

    def getCoordinate(self):
        return (self.x, self.y)

# 숫자 이미지 파일 (1~5) 저장된 경로
numbers = {
    1: "1.png",
    2: "2.png",
    3: "3.png",
    4: "4.png",
    5: "5.png",
    6: "6.png",
    7: "7.png",
    8: "8.png",
    9: "9.png",
}

# 인식 전 대기 (3초)
time.sleep(3)

apple_list = []
threshold = 10  # 중복을 판별할 거리 기준 (픽셀 단위, 조정 가능)

# 1️⃣ 화면에서 숫자 이미지 찾기
for num in range(1,10):
    positions = list(pyautogui.locateAllOnScreen("%d.png" % num, confidence=0.95))

    for pos in positions:
        center_x = pos.left + pos.width // 2
        center_y = pos.top + pos.height // 2
        apple_list.append(Apple(num, center_x, center_y))

# 2️⃣ 중복된 숫자 좌표 제거 (유클리드 거리 기반)
filtered_apples = []
for apple in apple_list:
    is_duplicate = False
    for filtered in filtered_apples:
        if distance.euclidean(apple.getCoordinate(), filtered.getCoordinate()) < threshold:
            is_duplicate = True
            break
    if not is_duplicate:
        filtered_apples.append(apple)

# 3️⃣ 결과 출력
for apple in filtered_apples:
    print(f"숫자 {apple.num}: ({apple.x}, {apple.y})")

print(f"\n최종 검출된 숫자 개수: {len(filtered_apples)}")

filtered_apples = sorted(filtered_apples, key = lambda x:x.y)
for apple in filtered_apples:
    print(f"숫자 {apple.num}: ({apple.x}, {apple.y})")

print(f"\n최종 검출된 숫자 개수: {len(filtered_apples)}")

apple_map = [[] * 17 for _ in range(10)]

row = 0
col = 0
apple_row = []

# 좌표의 숫자를 이용하여 원래 위치의 배열로 다시 만듦
for i in filtered_apples:       
    apple_row.append(i)
    col+=1
    if col == 17:
        col = 0
        insert_row = sorted(apple_row, key = lambda x:x.x)
        for i in range(len(insert_row)):
            print(insert_row[i].num, end = " ")
        print()
        apple_row = []
        apple_map[row] = insert_row
        row += 1
print("----------------------------------")
score = 0

def drag(Apple1, Apple2):
    x1 = Apple1.x//2
    y1 = Apple1.y//2
    x2 = Apple2.x//2
    y2 = Apple2.y//2
    pyautogui.moveTo(x1-5, y1-5)  # 시작 지점으로 이동
    pyautogui.mouseDown()  # 마우스 클릭 (누른 상태 유지)
    pyautogui.moveTo(x2+5, y2+5, duration=0.3)  # 끝 지점으로 이동 (0.3초 동안 이동)
    pyautogui.mouseUp()  # 마우스 놓기 (드래그 완료)

def hori(x,y):
    global score
    num = 0
    if apple_map[x][y].num == 0:  # <-- num == 0이면 실행 X
        return
    for i in range(y, M):
        num+=apple_map[x][i].num
        if num == 10:
            drag(apple_map[x][y], apple_map[x][i])
            for j in range(y, i+1):
                if apple_map[x][j].num != 0:
                    score+=1
                apple_map[x][j].num = 0
            print(apple_map[x][y].num, apple_map[x][i].num)
            return

def vert(x,y):
    global score
    num = 0
    if apple_map[x][y].num == 0:  # <-- num == 0이면 실행 X
        return
    for i in range(x, N):
        num+=apple_map[i][y].num
        if num == 10:
            drag(apple_map[x][y],apple_map[i][y])
            for j in range(x, i+1):
                if apple_map[j][y].num != 0:
                    score+=1
                apple_map[j][y].num = 0
            print(apple_map[x][y].num, apple_map[x][i].num)
            return

def is_vert(x,y):
    for i in range(x+1, N):
        if apple_map[i][y].num != 0:
            return True
    return False

def is_hori(x,y):
    for i in range(y+1, M):
        if apple_map[x][i].num != 0:
            return True
    return False

def is_there(x,y, stand):       # stand는 square에 인자로 들어온 x의 좌표
    for i in range(stand, x+1):
        if apple_map[i][y].num != 0:
            return True
    return False

def square(x,y):        # 투포인터? 활용해서 오른쪽, 아래쪽 포인터를 가지고 값 더하기
    global score
    stack = []
    for i in range(x, N):
        for j in range(y, M):
            if is_there(i,j,x):     # y의 좌표가 이동했을때 의미있는 이동인지 확인하는 함수
                num = 0
                stack_2 = []        # num에 더한 숫자들의 좌표
                if apple_map[i][j].num != 0:
                    stack.append((i,j))
                for k in stack:
                    if k[0] <= i and k[1] <= j:
                        num += apple_map[k[0]][k[1]].num
                        stack_2.append((k[0],k[1]))
                if num == 10:
                    drag(apple_map[x][y], apple_map[i][j])
                    for k in stack_2:
                        apple_map[k[0]][k[1]].num = 0
                        score+=1
                    return
                elif num > N:
                    break

def clear(x,y):
    if apple_map[x][y].num != 0 and is_hori(x,y):
        hori(x,y)
    if apple_map[x][y].num != 0 and is_vert(x,y):
        vert(x,y)
    if is_hori(x,y) or is_vert(x,y):
        square(x,y)

changed = True      # 점수의 변경사항 여부
while(changed):
    tmp = score
    for i in range(N):
        for j in range(M):
            clear(i,j)
    if score == tmp:
        changed = False

for i in range(N):
    for j in range(M):
        print(apple_map[i][j].num, end=" ")
    print()
print(score)
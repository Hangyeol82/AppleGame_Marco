# 🍏 Apple Game Automation (사과 게임 자동화)

![Python](https://img.shields.io/badge/Python-3.11-blue) 
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Automation-green) 

> **플래시 게임의 사과 숫자를 인식하고 자동으로 드래그하는 Python 프로그램**  
> `PyAutoGUI`와 `pytesseract`를 활용하여 화면을 분석하고 자동 조작합니다.

---

## 📌 **프로젝트 개요**
플래시 게임에서 **숫자(1~9)를 인식**하고 **자동으로 숫자를 드래그**하는 프로그램입니다.

✅ **기능**
- PyAutoGUI를 사용한 **이미지 인식**
- 숫자의 위치를 감지하여 **2차원 배열에 저장**
- 특정 규칙을 기반으로 **자동 드래그 수행**
- Retina 디스플레이 지원 (MacBook M1/M2 대응)
- `Esc` 키 또는 마우스를 **왼쪽 상단 (0,0)** 으로 이동하면 프로그램 종료

✅ **사용 기술**
- **Python 3.11**
- **PyAutoGUI** (스크린 이미지 인식 & 마우스 자동화)
- **scipy.spatial.distance** (중복된 이미지 제거)

---

## 📥 **설치 방법**
### 1️⃣ **Python & 라이브러리 설치**
먼저 Python이 설치되어 있는지 확인하세요. (Python 3.8 이상 추천)

```bash
python --version

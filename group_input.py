"""
[사용자에게 그룹, 시간표, 우선순위 등을 입력받는 파일]
"""

import tkinter as tk
from tkinter import ttk

def group_input():
    lecture_group = [] # 그룹별 강의 목록 저장 리스트

    # 제출 버튼 클릭 시 동작하는 함수
    def submit():
        # 각 입력 필드를 순회하며 강의 목록 추출
        for entry in entries:
            lecture = entry.get().strip()
            lecture_group.append(lecture.split(' ')) # 공백으로 분리하여 리스트에 추가
        root.quit() # 창 닫기

    # 그룹 작성 버튼 클릭 시 동작하는 함수
    def open_new_window():
        global total_group_num, priority, option_series, entries
        # 필드 값 추출 및 변환
        total_group_num = int(entry1.get()) if entry1.get() else None 
        priority = list(map(int, entry2.get().split())) if entry2.get() else None 
        option_series = int(entry3.get()) if entry3.get() else None 

        # 기존 위젯 제거
        for widget in root.winfo_children():
            widget.destroy()

        # 강의 목록 입력 안내 문구
        tk.Label(root, text="\n\n").pack()  # 디자인을 위한 필드
        tk.Label(root, text="각 그룹에 들어갈 교과목명을 띄어쓰기로 구분하여 입력해주세요. \n(*교과목명에는 띄어쓰기를 하시면 안됩니다.)", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(root, text="e.g. 자아와명상1 자아와명상2", font=("Helvetica", 12)).pack()

        entries = [] # 입력 필드 저장 리스트
        for i in range(total_group_num):
            frame = tk.Frame(root)  # 프레임 생성
            frame.pack(pady=5)      # 프레임 배치
            tk.Label(frame, text=f"그룹 {i+1}: ", font=("Helvetica", 14)).pack(side="left") # 라벨 생성 후 배치
            entry = tk.Entry(frame, font=("Helvetica", 14), width=50)                       # 입력 필드 생성
            entry.pack(side="left") # 입력 필드 배치
            entries.append(entry)   # 리스트에 추가

        # 제출 버튼 생성
        ttk.Button(root, text="제출", command=submit).pack(pady=10)


    # Tkinter 창 생성
    root = tk.Tk()
    root.title("사용자 입력") # 창 제목 설정
    root.geometry("800x600") # 창 크기 설정

    # 그룹 수 입력 필드 생성
    tk.Label(root, text="").pack()  # 다자인을 위한 필드
    tk.Label(root, text='시간표를 구성할 그룹은 몇 개입니까?', font=("Helvetica", 16)).pack(pady=10)
    entry1 = tk.Entry(root, font=("Helvetica", 14))
    entry1.pack()
    entry1.insert(0, "3") # 기본값 설정

    # 우선순위 입력 필드 생성
    tk.Label(root, text='다음에 대한 우선순위를 띄어쓰기로 구분하여 작성해주세요. \n[과제량 조모임수 성적기준] ', font=("Helvetica", 16)).pack(pady=10)
    entry2 = tk.Entry(root, font=("Helvetica", 14))
    entry2.pack()
    entry2.insert(0, "1 1 1") # 기본값 설정

    # 거리 제한 입력 필드 생성
    tk.Label(root, text='연강시 건물 간의 거리 제한을 선택해주세요. \n[좁게 1 ~ 5 넓게 | 0: 제한 없음] ', font=("Helvetica", 16)).pack(pady=10)
    entry3 = tk.Entry(root, font=("Helvetica", 14))
    entry3.pack()
    entry3.insert(0, "0") # 기본값 설정

    # 그룹 작성 버튼 생성 후 배치
    button = ttk.Button(root, text="그룹 작성", command=open_new_window)
    button.pack(pady=10)

    root.mainloop() # 창 실행

    # 사용자에게 입력받은 값들 반환
    return priority, option_series, total_group_num, lecture_group

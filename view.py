def find_lecture_room(point): # 호출시 point 타입은 튜플
    return {
        (-3, 1): lambda: "신공학관",
        (-2, 3): lambda: "원흥관",
        (-3, 4): lambda: "정보문화관",
        (-2, 5): lambda: "학림관",
        (-1, -1): lambda: "중앙도서관",
        (-1, -5): lambda: "체육관",
        (0, 0): lambda: "과학관",
        (0, 1): lambda: "명진관",
        (1, 1): lambda: "만해관",
        (1, 2): lambda: "법학관",
        (2, 2): lambda: "혜화관",
        (3, 2): lambda: "사회과학관",
        (4, 1): lambda: "경영관",
        (4, 3): lambda: "학술/문화관"
    }.get(point, lambda: "상록원")()

def view(result, running_time):

    lecture_time = [[] for _ in range(5)] # 각 요일별 강의 시간저장 - 0: 월, 1: 화, 2: 수, 3: 목, 4: 금
    best_timetable = result[0][0]
    for i in range(len(best_timetable)-1):
        lectures = best_timetable[i]
        for info in lectures['information']:
            day = info[0] // 24
            if day == 0:
                lecture_time[0].append((info[0] % 24, info[1] % 24, lectures['course_number'], find_lecture_room(tuple(info[2]))))
            elif day == 1:
                lecture_time[1].append((info[0] % 24, info[1] % 24, lectures['course_number'], find_lecture_room(tuple(info[2]))))
            elif day == 2:
                lecture_time[2].append((info[0] % 24, info[1] % 24, lectures['course_number'], find_lecture_room(tuple(info[2]))))
            elif day == 3:
                lecture_time[3].append((info[0] % 24, info[1] % 24, lectures['course_number'], find_lecture_room(tuple(info[2]))))
            elif day == 4:
                lecture_time[4].append((info[0] % 24, info[1] % 24, lectures['course_number'], find_lecture_room(tuple(info[2]))))
    
    print("[[최적 시간표]]")
    for day, day_lecture in enumerate(lecture_time):
        day_lecture.sort()
        if day == 0: print('월: ', end = '')
        elif day == 1: print('화: ', end = '')
        elif day == 2: print('수: ', end = '')
        elif day == 3: print('목: ', end = '')
        elif day == 4: print('금: ', end = '')        
        print(' '.join(map(str, day_lecture)))

    print("\n생성된 시간표 수:", len(result[0]))

    # 각 알고리즘에 의해 구해진 최적 시간표의 점수 출력
    print("\n[[버블정렬 결과]]")
    for i in range(min(len(result[0]), 3)):
        print(f'{i+1}순위:', result[0][i][-1]) 

    print("\n[[퀵정렬 결과]]")
    for i in range(min(len(result[0]), 3)):
        print(f'{i+1}순위:', result[1][i][-1]) 

    print("\n[[기수정렬 결과]]")
    for i in range(min(len(result[0]), 3)):
        print(f'{i+1}순위:', result[2][i][-1]) 

    print("\n[[유전 알고리즘 결과]]")
    for i in range(min(len(result[0]), 3)):
        print(f'{i+1}순위:', result[3][i][-1]) 

    # 각 알고리즘의 실행시간 출력
    print("\n========================================")
    print(f"|   백트래킹 실행시간  |{running_time['backtracking']:13d}ns|")
    print(f"|   버블정렬 실행시간  |{running_time['bubble']:13d}ns|")
    print(f"|    퀵정렬 실행시간   |{running_time['quick']:13d}ns|")
    print(f"|   기수정렬 실행시간  |{running_time['radix']:13d}ns|")
    print(f"| 유전알고리즘 실행시간|{running_time['genetic']:13d}ns|")
    print("========================================")

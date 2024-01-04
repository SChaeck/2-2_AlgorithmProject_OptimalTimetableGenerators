"""
[프로그램에서 데이터를 보다 효율적으로 활용하기 위해
데이터베이스 내의 데이터를 전처리하는 작업을 수행하는 함수]
"""

import json, copy

# ex) '성적' 카테고리에 대한 평가(너그러움, 보통, 깐깐함)에 대해 가중치 부여
# 1. 너그러움 -> 가중치 5(array[0])
# 2. 보통 -> 가중치 3(array[1])
# 3. 깐깐함 -> 가중치 1(array[2])
def calculate_value(array):
    result = array[0]*5 + array[1]*3 + array[2]*1
    return result

def data_preprocessing(course, priority, group_index):
    # 깊은 복사를 이용하여 원본 데이터를 보호하면서 새로운 객체를 생성
    course_copy = copy.deepcopy(course)

    # 불필요한 키를 삭제하여 데이터를 정리합니다.
    # 해당 데이터는 출력양식에서 필요, 프로그램을 실행하는 과정에서는 사용하지 않는 데이터
    del course_copy['time']
    del course_copy['assignment']
    del course_copy['group_meeting']
    del course_copy['grade']
    del course_copy['lecture_room']
    
    # 강의 시간을 저장할 빈 리스트를 생성
    course_copy['information'] = []
    # 보통 하나의 과목은 일주일에 수업이 2번 있다
    for i, time in enumerate(list(course['time'])):
        if time[0] == '월': day_number = 0   # 월: 0
        elif time[0] == '화': day_number = 1 # 화: 1
        elif time[0] == '수': day_number = 2 # 수: 2
        elif time[0] == '목': day_number = 3 # 목: 3
        elif time[0] == '금': day_number = 4 # 금: 4
        else: break
        # 강의 시작 시간, 강의 종료 시간, 강의실 정보를 튜플로 생성하여 'information' 항목에 append
        course_copy['information'].append((24*day_number + time[1], 24*day_number + time[2], course['lecture_room'][i]))
    
    # 각 요소에 대한 가중치를 고려하여 'total_value'를 계산
    # 각 요소에 대한 priortiy는 사용자로부터 입력을 받아 옴
    course_copy['total_value'] = (
        (priority[0]/sum(priority)) * calculate_value(course['assignment']) 
        + (priority[1]/sum(priority)) * calculate_value(course['group_meeting'])
        + (priority[2]/sum(priority)) * calculate_value(course['grade'])
    )
    
    # 강의 그룹을 지정
    course_copy['group'] = group_index + 1
    return course_copy

def group_info_search(lecture_group, lecture_group_info, priority):
    # JSON 파일에서 데이터를 로드
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 각 그룹에 대해
    for index, group in enumerate(lecture_group):
        group_info = []
        # 각 교과목에 대해
        for lecture in group:
            find = False
            # JSON 데이터에서 교과목 정보를 찾음
            for course in data:
                if course['course_name'] == lecture:
                    # 교과목 정보를 그룹 정보에 추가(append)       
                    # append를 할 때, 데이터 전처리 과정을 수행한 뒤 추가
                    group_info.append(data_preprocessing(course, priority, index))
                    find = True
            # 사용자가 입력한 교과목이 데이터베이스에 존재하지 않는 경우
            if not find:
                print(lecture, '강의를 찾지 못했습니다.')
        # 그룹 정보를 lectureGroupInfo에 추가
        lecture_group_info.append(group_info)
        with open('lecture_group_info.json', 'w', encoding='utf-8') as f:
            json.dump(lecture_group_info, f, ensure_ascii=False, indent=4)
    return lecture_group_info
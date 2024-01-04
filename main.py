"""
[추천 시간표 알고리즘을 실행하는 메인 파일]
"""

import group_input
import preprocessing
import backtracking_and_sort
import genetic_algorithm
import view

''' 각 모델에서 사용할 변수 생성 '''
total_group_num = 0         # 시간표로 생성할 그룹의 수
lecture_group = []          # 각 그룹에 포함되는 강의명 - 0: 1번째 그룹의 강의, 1: 2번째 그룹의 강의, ...
lecture_group_info = []     # 각 그룹에 포함되는 강의정보
priority = []               # 추천 시간표에 사용할 우선순위 - 0: 과제량, 1: 조모임수, 2: 성적기준
option_series = 0           # 연강 강의 간의 거리 제한 - 0: 제한 X, 1 ~ 5: 거리
recommend_timetable = []    # 추천 시간표 결과 저장 - 0: 버블 정렬, 1: 퀵 정렬, 2: 기수 정렬, 3: 유전 알고리즘 
running_time = {}           # 정렬 및 알고리즘의 실행시간 저장

''' 모델 실행 '''
priority, option_series, total_group_num, lecture_group = group_input.group_input()                 # 사용자의 입력을 받는 모델
lecture_group_info = preprocessing.group_info_search(lecture_group, lecture_group_info, priority)   # 필요한 강의정보를 전처리하는 모델
temp = list(backtracking_and_sort.start(lecture_group_info, total_group_num, option_series))        # 가능한 모든 시간표를 만들고 최적 기준으로 정렬하는 모델
recommend_timetable = temp[:3]
running_time = temp[3]
temp = list(genetic_algorithm.start(lecture_group_info, total_group_num, option_series))            # 유전 알고리즘으로 최적 시간표를 생성하는 모델
recommend_timetable.append(temp[0]) 
running_time.update(temp[1])
view.view(recommend_timetable, running_time)                                                                      # 생성된 최적 시간표를 출력하는 모델

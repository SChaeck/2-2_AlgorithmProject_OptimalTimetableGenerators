"""
[백트래킹 기법을 활용해 생성 가능한 모든 시간표를 생성하고, 
가중치를 기준으로 정렬된 시간표 목록을 반환하는 함수]
"""

import copy
import math
import time

lecture_group_info = []     # 강의 그룹 정보를 담은 리스트
total_group_num = 0         # 전체 그룹의 수
all_possible_timetable = [] # 모든 가능한 시간표를 담은 리스트
option_series = 0           # 연강 간의 거리를 제한하는 옵션

# 두 점 사이의 거리를 계산하는 함수
def calculate_distance(point1, point2):
    # 두 점 사이의 유클리드 거리를 계산하여 반환
    # 강의실의 위치에 대한 데이터는 직교좌표(x, y)로 저장되어 있다
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

# 현재 시간표에 강의를 추가할 수 있는지 확인하는 함수
def can_add_timetable(timetable, lecture):
    global option_series
    # 현재까지 생성된 시간표에 대해 반복
    for ex_lecture in timetable:
        # 현재까지 시간표에 포함된 각각의 강의의 시간 정보에 대해 반복
        for ex_info in ex_lecture['information']:
            # 추가하려는 새로운 강의의 시간 정보에 대해 반복
            for info in lecture['information']:
                if info[1] > ex_info[0] and ex_info[1] > info[0]:
                    # 강의 시간이 겹치는 경우
                    return False
                # 연강인 경우 인접 강의실만 가능하게 설정된 옵션인 option_series가 0이 아닌 경우
                # 새로운 강의와 현재 강의가 연강이면서 거리가 option_series보다 큰 경우에는 추가 불가능
                if option_series != 0 and (info[1] == ex_info[0] or info[0] == ex_info[1]) and \
                    calculate_distance(ex_info[2], info[2]) > option_series:
                    return False
    # 모든 조건을 통과하면 새로운 강의를 추가할 수 있음
    return True

# 백트래킹을 사용하여 모든 가능한 시간표를 생성하는 함수
def create_all_possible_timetable(timetable, group_num, sum) :
    # 모든 그룹의 처리가 끝났을 때, 즉, 백트래킹으로 시간표가 모두 구성되었다면
    if group_num > total_group_num:
        global all_possible_timetable
        timetable_copy = list(timetable)  # 시간표를 복사
        timetable_copy.append(round(sum/total_group_num, 4))  # 현재까지의 강의 가중치의 평균값을 계산하여 소수점 네 자리까지 사용
        all_possible_timetable.append(timetable_copy) # 전체 가능한 시간표 리스트에 구성된 시간표를 추가
    # 모든 그룹의 처리가 아직 끝나지 않았으면, 
    else:
        # 현재 그룹의 강의를 하나씩 선택하여 추가 가능한지 확인
        for lecture in lecture_group_info[group_num-1]:
            if can_add_timetable(timetable, lecture): # 추가 요건에 부합한다면
                timetable.append(lecture) # 강의를 시간표에 추가
                # 다음 그룹으로 재귀 호출하면서 강의의 가중치를 현재까지의 총 가중치에 더함
                create_all_possible_timetable(timetable, group_num + 1, sum + lecture['total_value'])
                timetable.pop() # 백트래킹: 추가한 강의를 다시 제거하여 다른 경우의 수를 확인

# 버블 정렬을 사용하여 시간표를 가중치를 기준으로 내림차순으로 정렬하는 함수
def bubble_sort(timetables):
    length = len(timetables)
    for i in range(length - 1):
        for j in range(length - 1 - i):
            # 현재 요소의 가중치가 다음 요소의 가중치보다 작은 경우
            if timetables[j][-1] < timetables[j+1][-1]:
                # 두 요소의 위치를 바꿈 (큰 가중치가 앞으로 오도록 정렬)
                timetables[j], timetables[j+1] = timetables[j+1], timetables[j]  
    return timetables

# 가장 일반적인 퀵 정렬
# 퀵 정렬을 사용하여 시간표를 가중치를 기준으로 내림차순으로 정렬하는 함수
def quick_sort(timetables, start, end):
    if start >= end: return # 원소가 1개인 경우
    pivot = start # 피벗은 첫 번째 요소
    left, right = start + 1, end
    
    while left <= right:
        # 피벗보다 작은 데이터를 찾을 때까지 반복
        while left <= end and timetables[left][-1] >= timetables[pivot][-1]:
            left += 1
        # 피벗보다 큰 데이터를 찾을 때까지 반복
        while right > start and timetables[right][-1] <= timetables[pivot][-1]:
            right -= 1
        if left > right: # 엇갈린 경우
            timetables[right][-1], timetables[pivot][-1] = timetables[pivot][-1], timetables[right][-1]
        else: # 엇갈리지 않은 경우
            timetables[right][-1], timetables[left][-1] = timetables[left][-1], timetables[right][-1]

    # 분할 이후 왼쪽 부분과 오른쪽 부분에서 각각 정렬 수행
    quick_sort(timetables, start, right - 1)
    quick_sort(timetables, right + 1, end)

# 기수 정렬을 사용하여 시간표를 가중치를 기준으로 내림차순으로 정렬하는 함수
def radix_sort(timetables):
    RADIX = 10 # 기수: 10진법을 의미
    placement = 0.0001 # 비교하는 자리수

    # 리스트에서 각 시간표의 가중치를 추출하여 그 중 최댓값을 찾아 'max_weight'에 할당한다
    # 기수 정렬에서 비교할 최대 자릿수를 찾는다
    max_weight = max(timetable[-1] for timetable in timetables)

    # 최대 자릿수의 정렬을 완료할때까지 기수 정렬 반복 실행
    while placement < max_weight:
        # 기수에 따라 각 자리수별로 버킷을 생성
        buckets = [list() for _ in range(RADIX)]
        # 각 시간표를 해당 자리수에 따라 버킷에 추가
        for timetable in timetables:
            # 현재 시간표의 가중치를 현재 처리 중인 자리수에 맞게 계산하여 버킷 인덱스를 결정
            tmp = int((timetable[-1] / placement) % RADIX)
            # 계산된 인덱스에 해당하는 버킷에 현재 시간표를 추가
            buckets[tmp].append(timetable)
        a = 0
        # 내림차순으로 정렬된 버킷을 순회하면서 전체 리스트에 할당
        for b in range(RADIX-1, -1, -1):
            buck = buckets[b]
            # 현재 버킷에서 각 시간표를 꺼내어 전체 리스트에 할당
            for i in buck:
                timetables[a] = i
                a += 1
        
        # 다음 자리수로 이동하기 위해 기수를 곱함
        placement *= RADIX
    return timetables

def start(lecture_group_info_param, total_group_num_param, option_series_param):
    global lecture_group_info, total_group_num, all_possible_timetable, option_series
    lecture_group_info = lecture_group_info_param
    total_group_num = total_group_num_param
    option_series = option_series_param
    running_time = {} # 정렬 알고리즘의 실행 시간 저장

    # 백트래킹을 사용하여 모든 가능한 시간표 생성
    start_time = time.perf_counter_ns()
    create_all_possible_timetable([], 1, 0);    
    end_time = time.perf_counter_ns()
    running_time["backtracking"] = end_time-start_time

    # 각 정렬에 사용할 시간표 복사
    timetable_copy_bubble = copy.deepcopy(all_possible_timetable)   
    timetable_copy_quick = copy.deepcopy(all_possible_timetable)    
    timetable_copy_radix = copy.deepcopy(all_possible_timetable)    

    # 버블정렬
    start_time = time.perf_counter_ns()
    bubble_sort(timetable_copy_bubble) 
    end_time = time.perf_counter_ns()
    running_time["bubble"] = end_time-start_time
    
    # 퀵정렬
    start_time = time.perf_counter_ns()
    quick_sort(timetable_copy_quick, 0, len(timetable_copy_quick) - 1) 
    end_time = time.perf_counter_ns()
    running_time["quick"] = end_time-start_time

    # 기수정렬
    start_time = time.perf_counter_ns()
    radix_sort(timetable_copy_radix) 
    end_time = time.perf_counter_ns()
    running_time["radix"] = end_time-start_time

    # 정렬이 완료된 시간표와 실행 시간 반환
    return timetable_copy_bubble, timetable_copy_quick, timetable_copy_radix, running_time
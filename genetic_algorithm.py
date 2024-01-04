"""
[Genetic(유전) 알고리즘을 활용하여 최적 시간표를 3개 생성하여 반환하는 함수]
"""

import random
import math
import time

total_group_num = 0
best_timetables = []        # 최적해 집합을 저장하는 전역 변수
lecture_group_info = []     # 각각의 그룹에 해당하는 강의 정보 리스트를 저장하는 전역 변수
option_series = 0           # 연강 시 강의실 간의 거리를 얼마나 제한할 것인지를 저장하는 전역 변수

# 강의실 간의 거리를 계산하는 함수
def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

# 새로운 강의를 시간표에 추가할 수 있는지 판단하는 함수
# 강의 시간 겹침 여부, 연강인 경우 강의실이 인접하는지 여부를 확인
def can_add_timetable(timetable, lecture):
    global option_series
    for ex_lecture in timetable:
        for ex_info in ex_lecture['information']:
            for info in lecture['information']:
                # 강의 시간이 겹치는 경우
                if info[1] > ex_info[0] and ex_info[1] > info[0]:
                    return False
                # 연속하는 강의의 경우 강의실이 인접해야 함
                if option_series != 0 and (info[1] == ex_info[0] or info[0] == ex_info[1]) and \
                    calculate_distance(ex_info[2], info[2]) > option_series:  # 연강인 경우 인접 강의실만 가능하게
                    return False
    return True

def fitness(timetable):
    # 이미 최적의 시간표 리스트에 있는 시간표라면 적합성을 0으로 반환
    if timetable in best_timetables:
        return 0
    
    total_weight = 0  # 총 가치를 저장하는 변수

    # 시간표에 있는 각 강의에 대해 반복
    for i in range(len(timetable)):
        lecture = timetable[i]

        # 만약 현재의 강의를 시간표에 추가할 수 없다면 적합성을 0으로 반환
        # can_add_timetable 함수는 시간표에 강의를 추가할 수 있는지를 판단
        if not can_add_timetable(timetable[:i], lecture):
            return 0

        # 강의를 시간표에 추가할 수 있다면, 강의의 가치를 총 가치에 더함
        total_weight += lecture['total_value']

    # 총 가치를 반환하여 시간표의 적합성을 나타냄
    return total_weight



def crossover(timetable1, timetable2):
    # 새로운 시간표를 저장할 리스트를 생성
    new_timetable = []

    # 각 그룹에 대해 반복
    for group in range(len(timetable1)):
        # 랜덤하게 timetable1 또는 timetable2에서 강의를 선택하여 자식 시간표 new_timetable을 생성
        # random.random() < 0.5 조건은 50%의 확률로 참 또는 거짓을 반환
        # 50% 확률로 아버지, 50% 확률로 어머니에게 유전자를 물려받는 것과 동일한 작업
        lecture = timetable1[group] if random.random() < 0.5 else timetable2[group]

        # 선택한 강의를 새로운 시간표에 추가
        new_timetable.append(lecture)

    # 생성된 새로운 시간표를 반환
    return new_timetable

def mutate(timetable):
    # 새로운 시간표를 생성하기 위해 기존 시간표를 복사
    new_timetable = timetable.copy()

    # 시간표의 강의 중 일부를 랜덤하게 선택하여 다른 강의로 변경(변이를 가함)
    # 시간표의 절반의 강의를 랜덤하게 변경하도록 설정
    for i in range(len(new_timetable) // 2):
        # 변경할 강의를 랜덤하게 선택(변경할 강의의 인덱스를 랜덤하게 생성)
        index_to_change = random.randint(0, len(new_timetable) - 1)

        # 선택한 강의와 같은 그룹의 강의들 중에서 랜덤하게 하나를 선택하여 변경
        new_timetable[index_to_change] = random.choice(lecture_group_info[new_timetable[index_to_change]['group'] - 1])

    return new_timetable


def generate_initial_population(population_size):
    # 각 그룹에서 랜덤하게 강의를 선택하여 개체를 생성하고, 이를 population_size만큼 반복하여 초기 인구를 생성합니다.
    return [[random.choice(lecture_group) for lecture_group in lecture_group_info] for _ in range(population_size)]

# 유전 알고리즘을 사용하여 최적의 시간표를 찾는 함수
def genetic_algorithm(population_size, mutation_rate):
    global best_timetables
    # 초기 인구를 생성
    population = generate_initial_population(population_size)

    while(True):
        # 인구 내의 개체를 적합성에 따라 정렬
        population = sorted(population, key=fitness, reverse=True)

        # 상위 50% 개체가 모두 동일한 경우를 체크
        # population[] 배열의 첫 번째 원소와, 중간 원소가 같은지만 체크하면 됨, 정렬 후 확인을 하는 것이므로
        if population[population_size//2] == population[0] :
            if fitness(population[0]) == 0: # 생성될 수 있는 시간표가 없으면 함수를 종료한다.
                return 

            # 현재 개체를 최적해로 저장
            if population[0] not in best_timetables:
                best_timetables.append(population[0])
            # 최적 시간표가 3개가 되면 프로그램을 종료, 적합도 높은 순서대로 시간표 3개만 생성하는 것이 목적이므로
            if len(best_timetables) == 3:
                return 
            # 새로운 인구를 생성하여 탐색을 계속
            population = generate_initial_population(population_size)
        else:
            # 상위 50% 개체와 새로 생성된 개체를 합쳐 새로운 인구를 구성
            population = population[:population_size//2] + [crossover(random.choice(population[:population_size//2]), random.choice(population[:population_size//2])) for _ in range(population_size//2)]

        # 변이율에 따라 일부 개체에 변이를 가한다
        for i in range(len(population)):
            if random.random() < mutation_rate:
                population[i] = mutate(population[i])

    return 


def start(lecture_group_info_param, total_group_num_param, option_series_param):
    global lecture_group_info, option_series, total_group_num, best_timetables
    option_series = option_series_param
    lecture_group_info = lecture_group_info_param 
    total_group_num = total_group_num_param
    
    # genetic_algorithm 함수를 호출하여 최적 시간표를 계산하고, 이를 best_timetables에 할당
    start_time = time.perf_counter_ns()
    genetic_algorithm(100, 0.1)
    
    for timetable in best_timetables:
        # 각 시간표 내의 강의들에 대한 총 value를 계산
        total_value = sum(lecture['total_value'] for lecture in timetable)
        # 시간표에 'total_value' 항목을 추가하고 총 value를 할당
        # value는 total_value의 계산값을 각 그룹의 수로 나눈 값으로, 소수점 네 번째 자리까지 반올림
        timetable.append(round(total_value / total_group_num, 4))
    end_time = time.perf_counter_ns()
    running_time = {"genetic": end_time-start_time}
    
    # 최종적으로 계산된 최적 시간표와 실행 시간 반환
    return best_timetables, running_time 
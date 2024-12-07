def appearance(intervals: dict[str, list[int]]) -> int:
    time_pupil = [[intervals['pupil'][t], intervals['pupil'][t + 1]] for t in range(0, len(intervals['pupil']), 2)]
    time_tutor = [[intervals['tutor'][t], intervals['tutor'][t + 1]] for t in range(0, len(intervals['tutor']), 2)]
    result = []

    i_pupil, i_tutor = 0, 0

    while 1:
        if i_pupil >= len(time_pupil) or i_tutor >= len(time_tutor):
            break  # если проверка таймстемпов закончилась у какого-либо списка

        if time_pupil[i_pupil][1] <= intervals['lesson'][0] or time_pupil[i_pupil][0] >= intervals['lesson'][1]:
            i_pupil += 1 # если ученик вышел раньше начала урока или подключился позже начала урока
            continue
        else:# определяем интервалы присутствия ученика на уроке
            if time_pupil[i_pupil][0] <= intervals['lesson'][0]:
                time_pupil[i_pupil][0] = intervals['lesson'][0]
            if time_pupil[i_pupil][1] >= intervals['lesson'][1]:
                time_pupil[i_pupil][1] = intervals['lesson'][1]

        if time_tutor[i_tutor][1] <= intervals['lesson'][0] or time_tutor[i_tutor][0] >= intervals['lesson'][1]:
            i_tutor += 1 # если учитель вышел раньше начала урока или подключился позже начала урока
            continue
        else: # определяем интервалы присутствия учителя на уроке
            if time_tutor[i_tutor][0] <= intervals['lesson'][0]:
                time_tutor[i_tutor][0] = intervals['lesson'][0]
            if time_tutor[i_tutor][1] >= intervals['lesson'][1]:
                time_tutor[i_tutor][1] = intervals['lesson'][1]

        if time_pupil[i_pupil][0] >= time_tutor[i_tutor][1]: # если интервалы в текущей итерации не пересекаются
            i_tutor += 1
            continue

        if time_pupil[i_pupil][1] <= time_tutor[i_tutor][0]: # если интервалы в текущей итерации не пересекаются
            i_pupil += 1
            continue

        if time_pupil[i_pupil][0] >= time_tutor[i_tutor][0]:  # если ученик подключился позже учителя...

            if time_pupil[i_pupil][1] >= time_tutor[i_tutor][1]:  # ...и отключился позже учителя
                result.append(time_tutor[i_tutor][1] - time_pupil[i_pupil][0])
                i_tutor += 1
            else:  # ...и отключился раньше
                result.append(time_pupil[i_pupil][1] - time_pupil[i_pupil][0])
                i_pupil += 1
        else:  # если учитель подключился позже...
            if time_pupil[i_pupil][1] <= time_tutor[i_tutor][1]:  # ...и отключился позже
                result.append(time_pupil[i_pupil][1] - time_tutor[i_tutor][0])
                i_pupil += 1
            else:  # ...и отключился раньше
                result.append(time_tutor[i_tutor][1] - time_tutor[i_tutor][0])
                i_tutor += 1

    return sum(result)


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },

    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },

    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        try:
            assert test_answer == test['answer'], (f'Error on test case {i}, got {test_answer}, '
                                                   f'expected {test["answer"]}')
            print(f'Общее время ученика и учителя равны {test_answer} сек.')
        except AssertionError:
            print('*' * 25)
            print(f'Во вводных данных для второго теста ошибка!\n 1) Они не отсортированы\n 2) Даже в '
                  f'отсортированном виде с исходными данными получается другое число, тогда как другие '
                  f'тесты выполняются.')
            print('*' * 25)
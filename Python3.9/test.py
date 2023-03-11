schedules = [
    [3, 4],
    [5, 6],

]
# schedules = [[2,4], [6,10]]

newSchedule = [1, 4]


# newSchedule = [3, 5]


def solution(schedules, newSchedule):
    def find_duplicated_schedules(schedules, newSchedule, begin_index, end_index):
        if begin_index == -1 and end_index == -1:
            return schedules

        temp = []
        if begin_index > -1 and end_index > -1:
            temp.extend(
                [
                    schedules[begin_index][0],
                    schedules[begin_index][1],
                    newSchedule[0],
                    newSchedule[1],
                    schedules[end_index][0],
                    schedules[end_index][1],
                ]
            )
        else:
            temp.extend(
                [
                    schedules[begin_index][0],
                    schedules[begin_index][1],
                    newSchedule[0],
                    newSchedule[1],
                ]
            )
        return [min(temp), max(temp)]

    begin_index = -1
    end_index = -1
    answer = []

    for index, schedule in enumerate(schedules):
        if newSchedule[0] in range(schedule[0], schedule[1]):
            begin_index = index
        if newSchedule[1] in range(schedule[0], schedule[1]):
            end_index = index

    if begin_index == -1 and end_index == -1:
        if newSchedule[0] > schedules[0][0]:
            schedules.append(newSchedule)
            return schedules
        else:
            newSchedule.extend(schedules)
            return newSchedule

    for index, schedule in enumerate(schedules):
        if index < begin_index:
            answer.append(schedule)
        elif index == begin_index:
            answer.append(find_duplicated_schedules(schedules, newSchedule, begin_index, end_index))
        elif index > end_index:
            answer.append(schedule)

    return answer


print(solution(schedules, newSchedule))

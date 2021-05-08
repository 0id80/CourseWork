from django.db.utils import cached_property
from datetime import datetime
from math import floor, ceil
from json import loads, dumps
from copy import deepcopy
from HanoiTowersApp.models import Iteration

task_hint = "8 шпинделей, пронумерованых от 8 до 1 слева направо" \
            "\nДиски, в количестве, равном соответствующей цифре из ID студента" \
            "\n Шпиндели: 8 7 6 5 4 3 2 1" \
            "\n Диски:    7 0 1 5 1 6 3 1" \
            "\nДиаметр диска равен M * 10 + N, где " \
            "  М – номер шпинделя, на котором надет диск, " \
            "а N – это номер диска на шпинделе, считая сверху вниз." \
            "\nСо шпинделя номер 8 можно перекладывать диски только на шпиндели 7 и 6" \
            "\nСо шпинделя номер 1 можно перекладывать диски только на шпиндели номер 2 и 3" \
            "\nСо шпинделей от 2 по 7 можно перекладывать диски только на два соседних шпинделя."


class HanoiTowers:
    def __init__(self, id="70151631"):
        self.id = id
        self.scheme = self.prepare_data
        self.prev_scheme = None
        self.__current_iteration = 0
        self.__current_percent = 1

    @property
    def prepare_data(self) -> list:
        data_towers = [[] for _ in self.id]

        for shaft_num, shaft_scheme, disks_count in zip(range(len(self.id), 0, -1),
                                                        data_towers,
                                                        map(int, self.id)):
            for disk_num in range(disks_count, 0, -1):
                shaft_scheme.append(shaft_num * 10 + disk_num)

        return data_towers

    @cached_property
    def iteration_count(self) -> int:
        iteration_count = int()
        disk_sum = int()
        for disks_count in map(int, self.id[:1:-1] + self.id[1]):
            disk_sum += disks_count
            iteration_count += 2 ** disk_sum - 1

        disk_sum = sum(map(int, self.id))

        for _ in range(len(self.id) // 2):
            iteration_count += 2 ** disk_sum - 1

        return iteration_count

    @cached_property
    def iterations_numbers(self):
        result = []
        for percent in range(1, 101):
            iteration = (67439623 * percent / 100)  # FIXME
            if iteration.is_integer():
                result.append(iteration)
            else:
                result.append((floor(iteration), ceil(iteration), iteration))
        return result

    @staticmethod
    def combine_iteration(current, prev):
        result = list()
        for cur, pre in zip(current, prev):
            if len(cur) < len(pre):
                result.append(cur)
            elif len(cur) == len(pre):
                result.append(cur)
            else:
                result.append(pre)
        return result

    def calculate_tower(self):

        def hanoi(n, a, b, c, _reverse=False):
            if n != 0:
                hanoi(n - 1, a, c, b)
                disk = self.scheme[a].pop()
                self.scheme[c].append(disk)
                self.__current_iteration += 1
                if isinstance(self.iterations_numbers[0], tuple):
                    if self.__current_iteration == self.iterations_numbers[0][0]:
                        if _reverse:
                            self.prev_scheme = deepcopy(self.scheme[::-1])
                        else:
                            self.prev_scheme = deepcopy(self.scheme)
                    elif self.__current_iteration == self.iterations_numbers[0][1]:
                        disk_in_motion = [disk, a, c]
                        if _reverse:
                            iteration_number = self.iterations_numbers.pop(0)[2]
                            combine = self.combine_iteration(deepcopy(self.scheme[::-1]), self.prev_scheme)
                            iteration = Iteration(percent=self.__current_percent,
                                                  iteration_number=iteration_number,
                                                  scheme=dumps(combine),
                                                  disk_in_motion=disk_in_motion)
                            iteration.save()
                        else:
                            iteration_number = self.iterations_numbers.pop(0)[2]
                            combine = self.combine_iteration(deepcopy(self.scheme), self.prev_scheme)
                            iteration = Iteration(percent=self.__current_percent,
                                                  iteration_number=iteration_number,
                                                  scheme=dumps(combine),
                                                  disk_in_motion=disk_in_motion)
                            iteration.save()
                        self.__current_percent += 1
                else:
                    if self.__current_iteration == self.iterations_numbers[0]:
                        if _reverse:
                            iteration = Iteration(percent=self.__current_percent,
                                                  iteration_number=self.iterations_numbers.pop(0),
                                                  scheme=dumps(deepcopy(self.scheme[::-1])),
                                                  disk_in_motion=None)
                            iteration.save()
                        else:
                            iteration = Iteration(percent=self.__current_percent,
                                                  iteration_number=self.iterations_numbers.pop(0),
                                                  scheme=dumps(deepcopy(self.scheme)),
                                                  disk_in_motion=None)
                            iteration.save()
                        self.__current_percent += 1
                hanoi(n - 1, b, a, c)

        def step():
            iteration = Iteration(percent=0,
                                  iteration_number=0,
                                  scheme=self.scheme,
                                  disk_in_motion=None)
            iteration.save()

            self.scheme = self.scheme[::-1]

            for index in range(0, len(self.scheme)-2):
                towers = index, index+2, index+1
                disk_counts = len(self.scheme[index])
                hanoi(disk_counts, *towers, _reverse=True)
                print(self.__current_iteration)

            hanoi(len(self.scheme[index+1]), index+1, index, index+2, _reverse=True)

            self.scheme = self.scheme[::-1]

            for index in range(0, len(self.scheme)-2):
                towers = index, index+1, index+2
                disk_counts = len(self.scheme[index])
                hanoi(disk_counts, *towers)

            if not len(self.scheme) % 2:
                hanoi(len(self.scheme[index+1]), index+1, index, index+2)

        start = datetime.now()
        step()
        print("Finished")
        end = datetime.now()
        print(end-start)


if __name__ == '__main__':
    task = HanoiTowers(id="70151631")


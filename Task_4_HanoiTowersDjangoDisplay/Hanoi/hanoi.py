from django.db.utils import cached_property
from datetime import datetime

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
        self.__current_iteration = 0
        print(self.iteration_count)
        self.calculate_tower()

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

    def calculate_tower(self):
        self.scheme = self.scheme[::-1]

        def hanoi(n, a, b, c):

            if n != 0:
                hanoi(n - 1, a, c, b)
                # self.start_position[c].add_disk(self.start_position[a].take_first())
                self.scheme[c].append(self.scheme[a].pop())
                self.__current_iteration += 1
                hanoi(n - 1, b, a, c)

        def step():
            for index in range(0, len(self.scheme)-2):
                towers = index, index+2, index+1
                # disk_counts = len(self.start_position[index].disks)
                disk_counts = len(self.scheme[index])
                hanoi(disk_counts, *towers)
                print(self.__current_iteration)

            # hanoi(len(self.start_position[index+1].disks), index+1, index, index+2)
            hanoi(len(self.scheme[index+1]), index+1, index, index+2)

            self.scheme = self.scheme[::-1]

            for index in range(0, len(self.scheme)-2):
                towers = index, index+1, index+2
                disk_counts = len(self.scheme[index])
                hanoi(disk_counts, *towers)

            if not len(self.scheme) % 2:
                # hanoi(len(self.start_position[index + 1].disks), index + 1, index, index + 2)
                hanoi(len(self.scheme[index+1]), index+1, index, index+2)

        start = datetime.now()
        step()
        print(self.scheme)

        print("Finished")
        print(self.__current_iteration)
        end = datetime.now()
        print(end-start)


if __name__ == '__main__':
    task = HanoiTowers(id="70151631")


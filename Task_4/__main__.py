from random import randint
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


class Disk:
    def __init__(self, tower, number):
        self.tower = tower
        self.number = number
        self.size = self.tower * 10 + self.number
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    def __str__(self):
        return f"T{self.tower} N{self.number} S{self.size} C{self.color}"

    def __repr__(self):
        # return f"Disk: {self.size}"
        return f"{self.size}"


class Tower:
    def __init__(self, number):
        self.number = number
        self.disks = []
        self.disk_count = len(self.disks)

    def __repr__(self):
        return f"T{self.number}: {self.disks}"
        # return f"{self.disks}"

    def fill_tower(self, disk_count):
        for disk in range(disk_count):
            self.disks.append(Disk(tower=self.number, number=disk+1))

    def add_disk(self, disk_in_motion):
        disk_in_motion.number = 1
        disk_in_motion.tower = self.number
        if len(self.disks) != 0:
            for disk in self.disks:
                disk.number += 1
            self.disks.insert(0, disk_in_motion)
        else:
            self.disks.append(disk_in_motion)

    def take_first(self):
        first = self.disks.pop(0)
        for disk in self.disks:
            disk.number -= 1
        return first


class HanoiTowers:
    def __init__(self, id=70151631):
        self.id = id
        self.disks_sequence = [int(str(self.id)[i]) for i in range(len(str(self.id)))]
        self.towers_count = len(self.disks_sequence)
        self.start_position = self.prepare_data()
        self.need_position = tuple()
        self.iterations_count = 0
        # 117771268
        # self.calculate_tower()

    def prepare_data(self) -> list:
        data_towers = [Tower(number=tower) for tower in range(self.towers_count, 0, -1)]
        for tower in range(len(data_towers)):
            data_towers[tower].fill_tower(self.disks_sequence[tower])
        return data_towers[::-1]

    def calculate_tower(self, progress=100):
        need_iteration = 67439623 * progress // 100

        def hanoi(n, a, b, c):
            if self.iterations_count == need_iteration:
                print("HERE", self.start_position)
                self.need_position = self.start_position
                print(self.need_position, file=open("need_position.txt", "w+"))
            if n != 0:
                hanoi(n - 1, a, c, b)
                self.iterations_count += 1
                self.start_position[c].add_disk(self.start_position[a].take_first())
                hanoi(n - 1, b, a, c)

        def step():
            for index in range(0, self.towers_count-2):
                towers = index, index+2, index+1
                disk_counts = len(self.start_position[index].disks)
                hanoi(disk_counts, *towers)
                # print(self.iterations_count)

            hanoi(len(self.start_position[index+1].disks), index+1, index, index+2)
            # print(self.iterations_count)

            self.start_position = self.start_position[::-1]

            # print("MIDDLE:", self.start_position)

            for index in range(0, self.towers_count-2):
                towers = index, index+1, index+2
                disk_counts = len(self.start_position[index].disks)
                hanoi(disk_counts, *towers)
                # print(self.iterations_count)

            hanoi(len(self.start_position[index + 1].disks), index + 1, index, index + 2)
            # print(self.iterations_count)

        step()

        print(self.start_position, file=open("end_position.txt", "w+"))
        return True


if __name__ == '__main__':
    task = HanoiTowers(id=70151631)
    start = task.start_position[::-1]
    print("START", start)
    if task.calculate_tower(progress=50):
        print("!!", task.need_position)


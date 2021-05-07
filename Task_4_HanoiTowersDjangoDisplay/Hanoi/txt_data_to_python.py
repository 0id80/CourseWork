from re import sub
from json import loads, dumps

def to_output(need_position, output_type="dict"):
    def to_dict(list_data):
        length = len(list_data)
        list_data = list_data[::-1]
        towers_dict = dict()
        for tower in range(length, 0, -1):
            towers_dict[f"Tower {tower}"] = list_data[tower-1]
        return towers_dict

    data = sub('T\d:', "", need_position[1:-1])
    data = data.replace(" ", "").replace("[", "").split("],")
    temp = dict()
    for tower in data:
        if tower == "]" or tower == "":
            data[data.index(tower)] = []
        elif "," in tower:
            data[data.index(tower)] = [int(disk) for disk in tower.split(",")]

        elif tower == str(tower):
            data[data.index(tower)] = [int(tower)]

    if output_type == "list":
        return data
    elif output_type == "dict":
        return to_dict(data)


if __name__ == '__main__':
    example = "[T8: [], T7: [], T6: [11, 23, 31, 32, 33, 34, 35, 51, 52, 53, 54, 81], T5: [61], " \
              "T4: [21, 22, 36, 41, 55, 82, 83, 84, 85, 86, 87], T3: [], T2: [], T1: []]"
    result = to_output(example, output_type="dict")
    print(result)
    print(dumps(result))
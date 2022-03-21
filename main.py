import pandas as pd

data = pd.read_csv('data.txt', sep=";", header=0, decimal=',')

overall_time = 48
sleep_time = 8
sleep_quantity = 2
day_time = 24

path = {}
data = data.sort_values('Важность', ascending=False, ignore_index=True)


def find_steps(data, remaining_time):
    res = data[data["Затраты времени на посещение"] == remaining_time].reset_index(drop=True)
    if len(res) > 0:
        return res.loc[[0]]
    else:
        res = data[data["Затраты времени на посещение"] < remaining_time].reset_index(drop=True)
        if len(res) > 0:
            data = data.drop(
                data[data["Название достопримечательности"] == res["Название достопримечательности"][0]].index)
            return [res.loc[[0]], find_steps(data, remaining_time - res["Затраты времени на посещение"][0])]
        else:
            return None


def flatten(l1):
    if len(l1) == 1:
        if type(l1[0]) == list:
            result = flatten(l1[0])
        else:
            result = l1[0]
    elif type(l1[0]) == list:
        result = pd.concat([flatten(l1[0]), flatten(l1[1:])], axis=0)
    else:
        result = pd.concat([l1[0], flatten(l1[1:])], axis=0)
    return result


def pretty_print(result_dict):
    for k, v in result_dict.items():
        time_passed = 0
        print(f"Расписание {k} дня:")
        if type(v) != str:
            for k1, v1 in v.items():
                if k1 == "Сон":
                    time_passed += v1
                    print(f"{k1}: потрачено времени {v1}")
                else:
                    time_passed += v1['время']
                    print(f"{k1}: потрачено времени {v1['время']}, важность: {v1['важность']}")
            print(f'Всего забито времени из суток: {time_passed}\n')
        else:
            print(v + "\n")


for day in range(1, overall_time // day_time + 1):
    path[day] = {"Сон": sleep_time}
    found_activities = find_steps(data, day_time - sleep_time)
    if found_activities:
        found_activities = flatten(found_activities)
        for act_index in range(found_activities["Название достопримечательности"].count()):
            path[day][found_activities["Название достопримечательности"].values[act_index]] = \
                {'время': found_activities["Затраты времени на посещение"].values[act_index],
                 'важность': found_activities["Важность"].values[act_index]}
        for name in found_activities["Название достопримечательности"].values:
            data = data.drop(data[data["Название достопримечательности"] == name].index)
    else:
        path[day] = "не удалось подобрать места для посещения"


pretty_print(path)

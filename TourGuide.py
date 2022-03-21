import pandas as pd


class TourGuide(object):
    """Класс организатора путешествий"""

    def __init__(self, data, overall_time=48, sleep_time=8):
        self.data = data.sort_values('Важность', ascending=False, ignore_index=True)
        self.data_storage = self.data
        self.overall_time = overall_time
        self.sleep_time = sleep_time
        self.day_time = 24
        self.path = {}

    def __find_steps(self, remaining_time):
        res = self.data[self.data["Затраты времени на посещение"] == remaining_time].reset_index(drop=True)
        if len(res) > 0:
            return res.loc[[0]]
        else:
            res = self.data[self.data["Затраты времени на посещение"] < remaining_time].reset_index(drop=True)
            if len(res) > 0:
                self.data = self.data.drop(
                    self.data[self.data["Название достопримечательности"] ==
                              res["Название достопримечательности"][0]].index)
                return [res.loc[[0]], self.__find_steps(remaining_time - res["Затраты времени на посещение"][0])]
            else:
                return None

    def __flatten(self, l1):
        if len(l1) == 1:
            if type(l1[0]) == list:
                result = self.__flatten(l1[0])
            else:
                result = l1[0]
        elif type(l1[0]) == list:
            result = pd.concat([self.__flatten(l1[0]), self.__flatten(l1[1:])], axis=0)
        else:
            result = pd.concat([l1[0], self.__flatten(l1[1:])], axis=0)
        return result

    def __pretty_print(self):
        for k, v in self.path.items():
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

    def __restore(self):
        self.data = self.data_storage
        self.path = {}

    def build_route(self):
        self.__restore()
        for day in range(self.overall_time // self.day_time):
            self.path[day + 1] = {"Сон": self.sleep_time}
            found_activities = self.__find_steps(self.day_time - self.sleep_time)
            if found_activities:
                found_activities = self.__flatten(found_activities)
                for act_index in range(found_activities["Название достопримечательности"].count()):
                    self.path[day + 1][found_activities["Название достопримечательности"].values[act_index]] = \
                        {'время': found_activities["Затраты времени на посещение"].values[act_index],
                         'важность': found_activities["Важность"].values[act_index]}
                for name in found_activities["Название достопримечательности"].values:
                    self.data = self.data.drop(self.data[self.data["Название достопримечательности"] == name].index)
            else:
                self.path[day + 1] = "не удалось подобрать места для посещения"
        self.__pretty_print()

    def set_data(self, new_data):
        self.data = new_data.sort_values('Важность', ascending=False, ignore_index=True)
        self.data_storage = self.data

    def set_overall_time(self, new_time):
        self.overall_time = new_time

    def set_sleep_time(self, new_time):
        self.sleep_time = new_time

import itertools

import numpy as np


class cartesian(object):
    def __init__(self):
        self._data_list = []
        self._data_lists = []

    def add_data(self, data=[]):  # 添加生成笛卡尔积的数据列表
        self._data_list.append(data)

    def build(self):  # 计算笛卡尔积
        for item in itertools.product(*self._data_list):
            item=list(item)
            x = []
            for items in item:
                x.append(str(items))

            self._data_lists.append(",".join(x))
            print(item)

        return self._data_lists


if __name__ == "__main__":
    car = cartesian()
    car.add_data([1, 2, 3, 4])
    car.add_data([5, 6, 7, 8])
    car.add_data([9, 10, 11, 12])
    car.build()
import csv


class Data_pre():
    def __init__(self):
        self.attributes = []  # 存储属性名
        self.column = []  # 按列存储原始数据
        self.length = 0  # 数据条数
        self.max_frequent = []  # 按列存储用最高频率值来填补缺失值的数据
        self.result = []  # 按行存储原始数据
        self.support = 0.15  # 最小支持度
        self.first_frequent = []  # 频繁一项集
        self.data = []  # 啊按行存储转化后的数据

    # 读取csv文件并初始化
    def read_csv(self, path):
        with open(path, 'r', encoding='mac_roman') as f:
            reader = csv.reader(f)
            self.result = list(reader)
            self.length = len(self.result) - 2
            self.attributes = self.result[0]
            for i in range(len(self.attributes)):
                ss = [row[i] for row in self.result]
                self.column.append(ss[1:-2])

    # 生成频繁一项集
    def get_first_requent(self, mark):
        for i in range(len(mark)):
            if mark[i] == 1:
                values = []
                map = {}  # 存储值和频数的对应关系
                count = 0
                for ss in self.max_frequent[i]:
                    if ss == "":
                        count += 1
                    else:
                        if ss not in values:
                            values.append(ss)
                            map[ss] = 1
                        else:
                            map[ss] += 1
                # for key in list(map.keys()):
                #     print(key + ":" + str(map[key]))
                for key in list(map.keys()):
                    if map[key] / self.length * 1.0 > self.support:
                        self.first_frequent.append(key)
        y = []
        for ss in self.first_frequent:
            x = []
            x.append(ss)
            y.append(x)
        return y

    # 处理Beat数值数据
    def handle_heat(self, column_count):
        for i in range(len(self.column[column_count])):
            if "00X" < self.column[column_count][i] < "11X":
                self.column[column_count][i] = "1-10X"
            elif "00Y" < self.column[column_count][i] < "11Y":
                self.column[column_count][i] = "1-10Y"
            elif "10X" < self.column[column_count][i] < "21X":
                self.column[column_count][i] = "11-20X"
            elif "10Y" < self.column[column_count][i] < "21Y":
                self.column[column_count][i] = "11-20Y"
            elif "20X" < self.column[column_count][i] < "31X":
                self.column[column_count][i] = "21-30X"
            elif "20Y" < self.column[column_count][i] < "31Y":
                self.column[column_count][i] = "21-30Y"
            elif "30X" < self.column[column_count][i] < "41X":
                self.column[column_count][i] = "31-40X"
            elif "30Y" < self.column[column_count][i] < "41Y":
                self.column[column_count][i] = "31-40Y"

    # 处理Area Id和Priority具有相同取值的情况
    def handle_id(self, column_count1, column_count2):
        for i in range(len(self.column[column_count1])):
            if self.column[column_count1][i] == "1":
                self.column[column_count1][i] = "AreaId_1"
            elif self.column[column_count1][i] == "2":
                self.column[column_count1][i] = "AreaId_2"
            elif self.column[column_count1][i] == "3":
                self.column[column_count1][i] = "AreaId_3"
        for i in range(len(self.column[column_count2])):
            if self.column[column_count2][i] == "1":
                self.column[column_count2][i] = "Priority_1"
            elif self.column[column_count2][i] == "2":
                self.column[column_count2][i] = "Priority_2"
            elif self.column[column_count2][i] == "3":
                self.column[column_count2][i] = "Priority_3"

    #  处理缺失数据，用最高频率值来填补缺失值，并存入self.max_frequent
    def handle_max_frequent(self, mark):
        count = 0
        for i in mark:
            # 0代表不用处理
            if i == 0:
                self.max_frequent.append(self.column[count])
            else:
                values = []
                map = {}
                for ss in self.column[count]:
                    if ss == "":
                        continue
                    else:
                        if ss not in values:
                            values.append(ss)
                            map[ss] = 1
                        else:
                            map[ss] += 1
                # 得到最高频率值
                s1 = list(map.keys())
                s2 = list(map.values())
                index = s2.index(max(s2))
                max_num = s1[index]

                tmp = []
                for ss in self.column[count]:
                    if ss != "":
                        tmp.append(ss)
                    else:
                        tmp.append(max_num)
                self.max_frequent.append(tmp)
            count += 1

    # 按记录得到预处理后的数据
    def get_dataset(self, mark):
        indexs = []
        for i in range(len(mark)):
            if mark[i] == 1:
                indexs.append(i)
        for i in range(len(self.max_frequent[0])):
            tmp = []
            for j in indexs:
                tmp.append(self.max_frequent[j][i])
            self.data.append(tmp)
        return self.data


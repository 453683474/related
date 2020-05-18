import numpy as np
import matplotlib.pyplot as plt
import copy
from itertools import combinations
from pre import Data_pre


class Apriori():
    def __init__(self):
        self.related = Data_pre()
        self.support = 0.15
        self.confidence = 0.7
        self.data = []
        self.first_frequent = []
        self.length = 0
        self.rules = []
        self.rules_support = []
        self.rules_confidence = []
        self.rules_X2 = []
        self.rules_lift = []

    def init(self):
        path = "D:/data/oakland_crime/records-for-2011.csv"
        # path = "D:/data/oakland_crime/records-for-2012.csv"
        # path = "D:/data/oakland_crime/records-for-2013.csv"
        # path = "D:/data/oakland_crime/records-for-2014.csv"
        # path = "D:/data/oakland_crime/records-for-2015.csv"
        # path = "D:/data/oakland_crime/records-for-2016.csv"
        self.related.read_csv(path)
        self.related.handle_heat(4)
        # self.related.handle_heat(3)
        self.related.handle_id(3, 5)
        # self.related.handle_id(2, 4)
        mark = [0, 0, 1, 1, 1, 1, 1, 0, 0, 0]  # 要处理的列位置索引
        # mark = [0, 0, 1, 1, 1, 1, 0, 0, 0, 0]  # 要处理的列位置索引
        self.related.handle_max_frequent(mark)
        self.first_frequent = self.related.get_first_requent(mark)
        # print(self.first_frequent)
        self.data = self.related.get_dataset(mark)
        # print(self.data)
        self.length = len(self.data)

    # 统计元素共同出现次数
    def count(self, tmp):
        count = 0
        for ss in self.data:
            judge = True
            for x in tmp:
                if x not in ss:
                    judge = False
                    break
            if judge:
                count += 1
        return count

    # 生成候选k+1项集
    def merge(self, tmp, k):
        n = len(tmp)
        values = []
        for i in range(n - 1):
            for j in range(i + 1, n):
                # ss = tmp[i] + tmp[j]
                # ss = list(set(ss))
                # if len(ss) == k + 1:
                #     values.append(ss)
                for q in tmp[j]:
                    if q not in tmp[i]:
                        x = copy.deepcopy(tmp[i])
                        x.append(q)
                        x = tuple(sorted(x))
                        values.append(x)
        values = list(set(values))
        values = [list(ss) for ss in values]
        return values, tmp

    # 生成频繁k项集
    def compute_support(self, tmp, k):
        print("候选" + str(k) + "项集：")
        srcc = []
        for ss in tmp:
            support = self.count(ss) / self.length * 1.0
            print(ss, end="")
            print(":" + str(support) + "  ", end="")
            if support >= self.support:
                srcc.append(ss)
        print()
        print("频繁" + str(k) + "项集：")
        print(srcc)
        return srcc

    # 生成关联规则，计算其置信度和支持度，卡方系数和Lift值
    def compute_confidence(self, s):
        end_list = []
        for tmp in s:
            for i in range(1, len(tmp) + 1):
                xx = list(combinations(tmp, i))
                xx = sorted(xx)
                end_list += xx
        end_list = list(set(end_list))
        end_list = sorted([list(yy) for yy in end_list])
        print("生成所有可能的候选项：")
        print(end_list)
        print()
        for ss in end_list:
            for mm in end_list:
                judge = True
                for x in ss:
                    for y in mm:
                        if x == y:
                            judge = False
                            break
                if ss != mm and judge:
                    if self.count(ss) != 0:
                        num = self.count(ss + mm) / self.count(ss) * 1.0
                        if num >= self.confidence:
                            print("得出关联规则：", end="")
                            print(ss, end="")
                            print("——>", end="")
                            print(mm, end="")
                            print("，置信度为 " + str(num))
                            count = self.count(ss + mm) / self.length * 1.0
                            print("该关联规则的支持度为：" + str(count))
                            qq = str(ss) + "->" + str(mm)
                            self.rules.append(qq)
                            self.rules_support.append(round(count, 3))
                            self.rules_confidence.append(round(num, 3))
                            # 计算卡方系数
                            mm_ss_num = self.count(ss + mm)
                            mm_num = self.count(mm)
                            notmm_num = self.length - mm_num
                            ss_num = self.count(ss)
                            notss_num = self.length - ss_num
                            mm_notss_num = mm_num - mm_ss_num
                            notmm_ss_num = ss_num - mm_ss_num
                            notmm_notss_num = notss_num - mm_notss_num
                            mm_ss_expected = int((mm_num / self.length * 1.0) * ss_num)
                            notmm_ss_expected = ss_num - mm_ss_expected
                            mm_notss_expected = mm_num - mm_ss_expected
                            notmm_notss_expected = notmm_num - notmm_ss_expected
                            X2 = (mm_ss_num - mm_ss_expected) ** 2 / mm_ss_expected * 1.0 + \
                                 (mm_notss_num - mm_notss_expected) ** 2 / mm_notss_expected * 1.0 + \
                                 (notmm_ss_num -notmm_ss_expected) ** 2 / notmm_ss_expected * 1.0 + \
                                 (notmm_notss_num - notmm_notss_expected) ** 2 / notmm_notss_expected * 1.0
                            self.rules_X2.append(round(X2, 3))
                            print("该关联规则计算的卡方系数为：" + str(X2))
                            # 计算相关性系数Lift
                            Lift = self.count(mm + ss) / (self.count(mm) * self.count(ss)) * self.length
                            self.rules_lift.append(round(Lift, 3))
                            print("该关联规则计算的相关性系数Lift为：" + str(Lift))
                            print()

    def autolabel(self, rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, 1.03 * height, '%s' % float(height))

    # 可视化
    def view(self, p1, p2, k):
        plt.figure(figsize=(20, 11))
        a = plt.bar(np.arange(len(p1)) * 2, p2, tick_label=list(p1))
        # plt.legend()
        self.autolabel(a)
        plt.xlabel("related_rules")
        if k == 1:
            plt.ylabel('support')
            plt.title('related_support_view')
        elif k == 2:
            plt.ylabel('confidence')
            plt.title('related_confidence_view')
        elif k == 3:
            plt.ylabel('X2_num')
            plt.title('related_X2_view')
        elif k == 4:
            plt.ylabel('Lift_num')
            plt.title('related_Lift_view')
        plt.xticks(rotation=-45)
        plt.show()


ss = Apriori()
ss.init()
first_frequent = ss.first_frequent
k = 1
tmp, src = [], []
tmp = ss.compute_support(first_frequent, k)  # 得到频繁k项集
tmp, src = ss.merge(tmp, k)  # 得到候选k+1项集
k += 1
while len(tmp) != 0 and len(tmp) != 1:
    tmp = ss.compute_support(tmp, k)  # 得到频繁k项集
    if not tmp:
        tmp = src
        print("最终得到的频繁项集为：")
        print(tmp)
        break
    tmp, src = ss.merge(tmp, k)  # 得到候选k+1项集
    k += 1
if len(tmp) == 0:
    tmp = src
ss.compute_confidence(tmp)
x = ss.rules
y1 = ss.rules_support
y2 = ss.rules_confidence
y3 = ss.rules_X2
y4 = ss.rules_lift
ss.view(x, y1, 1)
ss.view(x, y2, 2)
ss.view(x, y3, 3)
ss.view(x, y4, 4)

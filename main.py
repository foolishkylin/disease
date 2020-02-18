from merge_set import MergeSet
from math import sin, asin, cos, radians, sqrt
import time
from db_operate import db_select, db_make, db_insert

class Model:
    def __init__(self):
        self.community_dict = {}  # 记录每个用户的社区类标
        self.pair, self.meet_time = db_select()
        self.edge_list = []
        for (key, val) in self.pair.items():
            for item in val:
                self.edge_list.append((key, item, 1))

    def geodistance(self, lng1,lat1,lng2,lat2):
        EARTH_RADIUS = 6371  # 地球平均半径，6371km
        '''根据两点经纬度计算距离,返回单位:米.'''
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
        dlon = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        dis = 2 * asin(sqrt(a)) * EARTH_RADIUS * 1000
        return dis

    def apply_algorithm(self):
        #lv = Louvain.from_list(self.edge_list)
        #self.community_result = lv.apply_louvain()
        ms = MergeSet.from_list(self.edge_list)
        self.community_result = ms.Merge()  #key:str


    def find_community_label(self):
        '''
        :return: 寻找用户的社区类标 和 每一个社区对应的成员（方便检索）
        '''
        self.apply_algorithm()
        print(self.community_result)
        self.members = {}  # 记录同一社区的成员
        for key, val in self.community_result.items():
            self.community_dict[key] = val
            if val not in self.members:
                self.members[val] = []
            else:
                self.members[val].append(key)

    def search(self, id):
        '''
        搜寻与id同一社区的用户id, 以及这些人建立边时的时间和位置(返回dict: {'ID':[(time1, lng1, lat1),(time2, lng2, lat2]}).
        存在一个问题：确诊的人，可能与社区成员是没有相连的边。
        '''
        info = {} # 社区成员的信息
        if id not in self.community_dict.keys():
            return dict()
        member_id = self.members[self.community_dict[id]] # a list
        for id2 in member_id:
            if id2 not in info:
                info[id2] = []
            neibhor_set = self.pair[id2]  # 与成员相连的id有.
            # print(neibhor_set)
            for i in neibhor_set:
                info[id2] = self.meet_time[id2][i]

        return info


if __name__ == '__main__':
    file='sample.csv'
    print('loaded')
    model = Model()
    model.find_community_label()
    print('searching')
    print(model.search('10505040'))  # 假如用户'10505040'被确诊了，返回其社区的成员，以及这些成员与哪些人在何时何地相遇了。

from merge_set import MergeSet
from math import sin, asin, cos, radians, sqrt
import time

class Model:
    def __init__(self, track_data):
        self.data = {}  # {'timestamp': {'ID' : (lng, lat)} }
        self.community_dict = {}  # 记录每个用户的社区类标，初始化为-1.
        for row in track_data:
            self.community_dict[row["user_id"]] = -1
            timestamp = int(time.mktime(time.strptime(row['time'], "%Y-%m-%d %H:%M")))
            if timestamp not in self.data:  # 以分钟作为key.
                self.data[timestamp] = {}
            # 同一个时间戳下存储用户的经纬度
            if float(row["lon"]) != 0 and float(row["lat"]) != 0:  # 可能有错误的经纬度
                self.data[timestamp][row["user_id"]] = (float(row["lon"]), float(row["lat"]))  # 以分钟作为记录.
        # with open(data_file, newline='') as csvfile:
        #     # 0 is ID, 1 is lng, 2 is lat, 5 is hour, 6 is minute.
        #     rows = csv.reader(csvfile)
        #     for row in rows:
        #         if row[0] != 'ID':
        #             self.community_dict[row[0]] = -1
        #             timestamp = int(row[5]) * 60 + int(row[6])
        #             if timestamp not in self.data:  # 以分钟作为key.
        #                 self.data[timestamp] = {}
        #             # 同一个时间戳下存储用户的经纬度
        #             if float(row[1]) != 0 and float(row[2]) != 0:  # 可能有错误的经纬度
        #                 self.data[timestamp][row[0]] = (float(row[1]), float(row[2]))  # 以分钟作为记录.

        # print(self.data)

        # compute dis.
        # 两种特殊情况：一条边在多个时间段都生成了; 已经a和b生成了，b又和a生成了(暂时无处理).
        self.meet_time={} #{'ID1': {'ID2': [(time, lng, lat)], 'ID3':[time]..}}
        self.pair = {}  # save the edge.
        for i in self.data.keys():
            for j in self.data[i].keys():
                (lng1, lat1) = self.data[i][j]
                for k in self.data[i].keys():
                    if j != k:
                        (lng2, lat2) = self.data[i][k]
                        distance = self.geodistance(lng1, lat1, lng2, lat2)  # 需要记录与谁在哪相遇
                        if distance < 1:  # threshold is 1.
                            if j not in self.meet_time:
                                self.meet_time[j] = {}
                            if k not in self.meet_time[j]:
                                self.meet_time[j][k] = []
                            self.meet_time[j][k].append((k, i, lng2, lat2))   # 可能在多个时间段相遇

                            if j not in self.pair:
                                self.pair[j] = set()
                            else:
                                self.pair[j].add(k)

        self.edge_list = []
        for (key, val) in self.pair.items():
            for item in val:
                self.edge_list.append((key, item, 1))

        print(self.pair)

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
        member_id = self.members[self.community_dict[id]] # a list
        for id2 in member_id:
            if id2 not in info:
                info[id2] = []
            neibhor_set = self.pair[id2]  # 与成员相连的id有.
            # print(neibhor_set)
            for i in neibhor_set:
                info[id2] = self.meet_time[id2][i]

        return info


# if __name__ == '__main__':
#     file='sample.csv'
#     print('loaded')
#     model = Model(file)
#     model.find_community_label()
#     print('searching')
#     print(model.search('123'))  # 假如用户'10505040'被确诊了，返回其社区的成员，以及这些成员与哪些人在何时何地相遇了。

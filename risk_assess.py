from math import sin, asin, cos, radians, sqrt
import pandas as pd
import datetime
import numpy as np

class risk_model:
    def __init__(self, lng, lat):
        self.distance = [] #距离列表
        self.time = [] #时间列表
        self.data = self.get_data(lng, lat)

    def get_data(self, lng, lat):
        data = pd.read_csv('疫情情况数据.csv')
        times = data['date']
        locations = data['geometry']
        # locations = data['point']  #利用数据的point列判断
        data_list = []
        for i in range(len(locations)):
            location = eval(locations.loc[i])['coordinates']
            L = np.array(location)
            L = L.reshape(-1, 2)
            L = L.tolist()
            for j in range(len(L)):
                tmp_dict = {}
                distance = self.geodistance(L[j][0], L[j][1], lng, lat)
                if distance <= 100.0:
                    time = str(times.loc[i])
                    tmp_dict[time] = distance
                    data_list.append(tmp_dict)
        return data_list

    def geodistance(self, lng1,lat1,lng2,lat2):
        EARTH_RADIUS = 6371  # 地球平均半径，6371km
        '''根据两点经纬度计算距离,返回单位:米.'''
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
        dlon = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        dis = 2 * asin(sqrt(a)) * EARTH_RADIUS * 1000
        return dis

    def risk_cal(self, lng, lat, user_time):
        #三个参数分别为：使用者当前的经纬度和时间
        #这里讲距离和时间比重为一半50%和50%
        #病毒假设可以存活一天，那么就把时间的50%分成24小时分计算比重
        #假设病毒可以传播100米，那么就距离的50%分成50米份计算比重
        #data = sql_search(lng,lat)  #根据用户现在所在的地理位置查找是否有患者经过该区域(范围为一百米以内）
        # 返回危险级别：0（无危险）；1（有点危险）；2（一般危险）；3（较为危险）；4（很危险）；
        counts = []
        datas = {'2020-01-07 08:15:00':[113.47706,23.149924], '2020-01-07 08:10:00':[113.48561,23.146859]}
        time1 = datetime.datetime.strptime(user_time, "%Y-%m-%d %H:%M:%S")
        if datas == None: #没有患者经过附加
            return 0,0
        else:
            for other_time in datas:
                time2 = datetime.datetime.strptime(other_time, "%Y-%m-%d %H:%M:%S")
                if (time1-time2).days > 1: #如果患者经过时间已经超过了一天，就不计算跳过
                    continue
                else:
                    accoss_seconds = (time1-time2).seconds/60 #得到患者经过附近区域经过了几分钟
                    accoss_distance = self.geodistance(datas[other_time][0], datas[other_time][1], lng, lat)
                    seconds_mark = 50 * (1- accoss_seconds/1440) #将一天分成1440分钟，经过时间越长，比重越短
                    distance_mark = 50 * (1 - accoss_distance/100) #距离越接近，比重越大
                    mark = seconds_mark + distance_mark
                    counts.append(mark)
            sum_count = 0.0
            for count in counts: #计算所有比重
                sum_count += count
            print('你经过可疑的区域有"{}"个'.format(len(counts)))
            if sum_count < 20.0 and sum_count>0.0:
                print('你现在是一级危险')
                return 1, len(counts)
            elif sum_count < 40.0 and sum_count>20.0:
                print('你现在是二级危险')
                return 2, len(counts)
            elif sum_count < 60 and sum_count>40:
                print('你现在是三级危险')
                return 3, len(counts)
            elif sum_count < 80 and sum_count>60:
                print('你现在是四级危险')
                return 4, len(counts)
            elif sum_count < 100 and sum_count>80:
                print('你现在是五级危险')
                return 5, len(counts)
            # print(sum_count)
            print('你现在是五级危险')

    def risk_pred(self):
        #返回距离小于100米的点的个数和信息
        print('你经过的危险的点有{}个'.format(len(self.data)))
        return len(self.data)

if __name__ == '__main__':
    model = risk_model(114.01765272305346, 22.53780423576629)
    model.risk_pred()
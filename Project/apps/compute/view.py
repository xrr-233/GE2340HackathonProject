import os
import re
import datetime
import math
import pytz
import requests
import tqdm
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



from flask import Blueprint, jsonify, request, url_for
from skyfield.api import load, EarthSatellite, wgs84
from tle2czml.tle2czml import Colors, read_tles, create_czml_file, create_satellite_packet
from sklearn import preprocessing
from apps.compute.LSTM import myLSTM
from apps.index.view import system_database

compute_bp = Blueprint('compute', __name__)

data = []
utc_time = None
timestep = 0

def create_dataset(data_x, data_y, look_back):
    dataX, dataY = [], []
    for i in range(data_y.shape[0] - look_back - 1):
        a = data_x[i:(i + look_back)]
        dataX.append(a)
        dataY.append(data_y[i + look_back])
    return np.array(dataX), np.array(dataY)

@compute_bp.route('/generate', endpoint='generate')
def generate():
    norad_cat_id = request.args.get('norad_cat_id')
    date = request.args.get('date')
    print(norad_cat_id)
    print(date)
    if (len(norad_cat_id) != 5 or len(date) == 0):
        print("Bad Request!")
        return jsonify({"code": 400, "msg": "Bad Request!"})

    data = []
    dirs = system_database.dirs
    base = system_database.base
    min_moment = 100000

    # region Seperate needed data from system files
    for file_name in tqdm.tqdm(dirs):
        input_path = base + '/' + file_name

        with open(input_path, "r") as f:
            all_lines = f.readlines()

        if (len(all_lines) / 3 != int(len(all_lines) / 3)):
            print("Error in " + file_name)
            continue

        for o in range(int(len(all_lines) / 3)):
            line1 = re.split(r"[ ]+", all_lines[o * 3 + 1].strip('\n'))
            line2 = re.split(r"[ ]+", all_lines[o * 3 + 2].strip('\n'))

            name = ['0'] * 5
            k = len(line2[1])
            for i in range(len(line2[1])):
                j = 4 - i
                k -= 1
                name[j] = line2[1][k]
            for i in range(1, len(name)):
                name[0] += name[i]
            name = name[0]

            moment = line1[3].split('.')
            try:
                # print(moment)
                moment_year = int(moment[0][:2])
                moment_day = int(moment[0][2:])
            except:
                # print("Wrong form!")
                continue
            moment_moment = moment[1]
            start_date = datetime.date(1940, 1, 1)
            if (moment_year < 40):
                moment_year += 2000
            else:
                moment_year += 1900
            end_date = datetime.date(moment_year, 1, 1)
            delta = datetime.timedelta(days=moment_day - 1)
            end_date += delta
            interval = (end_date - start_date).days
            moment = float(str(interval) + '.' + moment_moment)

            inclination = float(line2[2])  # in degree
            RAAN = float(line2[3])  # in degree, right ascension of ascending node
            eccentricity = float('0.' + line2[4])
            argument_of_perigee = float(line2[5])  # in degree
            mean_anomaly = float(line2[6])  # in degree, can compute perigee time
            round_per_day = float(line2[7])  # can compute periodic time

            G = 6.67259 * 10 ** (-11)
            M = 5.972 * 10 ** 24  # from Google
            a = (G * M * (1 / round_per_day * 86400) ** 2 / (4 * math.pi ** 2)) ** (1 / 3)  # semi-major axis, unit: m

            if (name == norad_cat_id):
                min_moment = min(moment, min_moment)
                data.append([str(name), moment, a, inclination, RAAN, eccentricity, argument_of_perigee, mean_anomaly])
                '''
                print("卫星ID：" + str(name))
                print("数据读取时刻：" + str(moment))
                print()
                print("轨道半长轴：" + str(a / 1000) + " km")
                print("轨道倾角：" + str(inclination))
                print("升交点赤经：" + str(RAAN))
                print("偏心率：" + str(eccentricity))
                print("近地点幅角：" + str(argument_of_perigee))
                print("平近点角：" + str(mean_anomaly)) # 现在先定下轨道的形状 之后考虑
                '''

    # 1 00005U 58002B 21303.21787226 .00000130 00000-0 19306-3 0 9990
    # 2 00005 34.2404 128.6696 1842399 81.3618 299.0274 10.84825330259536

    #         轨道倾角  升交点赤经 轨道偏心率 近地点幅角 平近点角（和时间有关）

    # endregion

    date = date.split('-')
    date = [int(d) for d in date]
    start_date = datetime.date(1940, 1, 1)
    end_date = datetime.date(date[0], date[1], date[2])
    interval = (end_date - start_date).days
    this_moment = float(str(interval) + '.50000000') # take the noon to be the representative time

    if(len(data) == 0 or this_moment < min_moment):
        print("Internal Server Error!")
        return jsonify({"code": 500, "msg": "Internal Server Error!"})

    columns = ['Name', 'Moment', 'Axis', 'Inclination', 'RAAN', 'Eccentricity', 'AOP', 'MA']

    df = pd.DataFrame(data, columns=columns, dtype=float)
    df = df.drop(columns=['Name'])
    columns = ['Moment', 'Axis', 'Inclination', 'RAAN', 'Eccentricity', 'AOP', 'MA']
    # print(df)
    # print(df.head())

    plt.figure(figsize=(15, 15))
    for i, each in enumerate(columns):
        plt.subplot(len(columns), 1, i + 1)
        plt.plot(df[each])
        plt.title(each, y=0.5, loc="right")  # center, left, right
    plt.show()
    columns.remove('Moment')

    all_df_x = []
    all_df_y = []
    all_prediction = []
    look_back = 4  # 此处可以做一个对比实验
    first_arr = []

    all_lstm = []
    for o, attr in enumerate(columns):
        # region Data standardization
        df_x = df.loc[:, ["Moment"]]
        min_max_scaler_x = preprocessing.MinMaxScaler(feature_range=(0, 1))
        standard_values_x = min_max_scaler_x.fit_transform(df_x)
        for i, col_name in enumerate(df_x.columns):
            df_x[col_name] = standard_values_x[:, i]

        # df_y = df.drop(columns=["Moment"])
        df_y = df.loc[:, [attr]]
        min_max_scaler_y = preprocessing.MinMaxScaler(feature_range=(0, 1))
        standard_values_y = min_max_scaler_y.fit_transform(df_y)
        for i, col_name in enumerate(df_y.columns):
            df_y[col_name] = standard_values_y[:, i]
        # columns.remove('Moment')
        columns_attr = [attr]
        # endregion

        # region Process time series
        df_x = np.array(df_x)
        df_y = np.array(df_y)

        df_x, df_y = create_dataset(df_x, df_y, look_back)
        print(df_x.shape, df_y.shape)
        # endregion

        # region Allocate training/testing set
        split_point1 = int(df_x.shape[0] * 0.6)
        split_point2 = int(df_x.shape[0] * 0.8)
        train_x = np.array(df_x[:split_point1])
        train_y = np.array(df_y[:split_point1])
        valid_x = np.array(df_x[split_point1:split_point2])
        valid_y = np.array(df_y[split_point1:split_point2])
        test_x = np.array(df_x[split_point2:])
        test_y = np.array(df_y[split_point2:])
        # endregion

        # region Build LSTM Network
        lstm = myLSTM(train_x.shape[1], train_x.shape[2], len(columns_attr), min_max_scaler_x, min_max_scaler_y)
        lstm.train(train_x, train_y, valid_x, valid_y)
        lstm.plot()

        score = lstm.evaluate(train_x, train_y)
        print("Train loss: " + str(score))
        score = lstm.evaluate(valid_x, valid_y)
        print("Valid loss: " + str(score))
        score = lstm.evaluate(test_x, test_y)
        print("Test loss: " + str(score))
        # endregion

        # region Predict data
        prediction = lstm.predict(df_x)

        if (o == 0):
            all_df_x = df_x[:, look_back - 1]
            all_df_x = min_max_scaler_x.inverse_transform(all_df_x)
            first_arr = df_x[0]
            first_arr = min_max_scaler_x.inverse_transform(first_arr)
            first_arr = np.vstack((first_arr, all_df_x[1:]))
            all_df_y = df_x[:, look_back - 1]
            all_prediction = df_x[:, look_back - 1]

        df_y = min_max_scaler_y.inverse_transform(df_y)

        all_df_y = np.hstack((all_df_y, df_y))
        prediction = min_max_scaler_y.inverse_transform(prediction)
        all_prediction = np.hstack((all_prediction, prediction))

        all_lstm.append(lstm)
        # endregion

    # region See fit effect
    first_arr = pd.DataFrame(first_arr, columns=['Moment'], dtype=float)
    all_df_x = pd.DataFrame(all_df_x, columns=['Moment'], dtype=float)
    all_df_y = pd.DataFrame(all_df_y[:, 1:], columns=columns, dtype=float)
    all_prediction = pd.DataFrame(all_prediction[:, 1:], columns=columns, dtype=float)
    print(all_prediction)

    plt.figure(figsize=(15, 15))
    for o, attr in enumerate(columns):
        plt.subplot(len(columns), 1, o + 1)
        # print(all_df_x.columns)
        # print(all_prediction.columns)
        # print(all_df_y.columns)
        # print(all_df_x['Moment'])
        # print(all_prediction[attr])
        plt.plot(all_df_x['Moment'], all_prediction[attr], 'r')
        plt.plot(all_df_x['Moment'], all_df_y[attr], 'g')
        plt.title(attr, y=0.5, loc="right")  # center, left, right
    plt.show()
    # endregion

    this_dataX = []
    # print(first_arr)

    if(this_moment < all_df_x['Moment'][0]):
        l = 0
        r = look_back - 1
        while(this_moment < first_arr['Moment'][r - 1]):
            this_dataX.append(first_arr['Moment'][l])
            r -= 1
        this_dataX.extend(first_arr['Moment'][l:r])
        this_dataX.append(this_moment)
    elif(this_moment <= all_df_x['Moment'][len(all_df_x) - 1]):
        r = len(first_arr['Moment'])
        l = r + 1 - look_back
        while(this_moment < first_arr['Moment'][r - 1]):
            r -= 1
            l -= 1
        this_dataX.extend(first_arr['Moment'][l:r])
        this_dataX.append(this_moment)
    else:
        r = len(first_arr['Moment'])
        l = r + 1 - look_back
        this_dataX.extend(first_arr['Moment'][l:r])
        this_dataX.append(this_moment)

    this_dataX = np.array(this_dataX)
    this_dataX.reshape((this_dataX.shape[0], 1))
    this_dataX_df = pd.DataFrame(this_dataX, columns=['Moment'], dtype=float)
    this_dataX_df = all_lstm[0].min_max_scaler_x.transform(this_dataX_df)
    print(this_dataX_df)
    print(this_dataX_df.shape)
    this_dataX = np.array([this_dataX])
    print(this_dataX_df)
    print(this_dataX_df.shape)

    a = all_lstm[0].min_max_scaler_y.inverse_transform(all_lstm[0].predict(this_dataX))
    inclination = all_lstm[1].min_max_scaler_y.inverse_transform(all_lstm[1].predict(this_dataX))
    RAAN = all_lstm[2].min_max_scaler_y.inverse_transform(all_lstm[2].predict(this_dataX))
    eccentricity = all_lstm[3].min_max_scaler_y.inverse_transform(all_lstm[3].predict(this_dataX))
    argument_of_perigee = all_lstm[4].min_max_scaler_y.inverse_transform(all_lstm[4].predict(this_dataX))
    mean_anomaly = all_lstm[5].min_max_scaler_y.inverse_transform(all_lstm[5].predict(this_dataX))

    print(a)
    print(inclination)
    print(RAAN)
    print(eccentricity)
    print(argument_of_perigee)
    print(mean_anomaly)

    # 下步步骤
    # 数值读入czml
    # 可视化
    '''
    # Rewrite tle2czml
    if (not os.access(output_path, os.F_OK)):
        print('Generating ' + file_name_pre + '.czml')

        with open(input_path, 'r') as f:
            rgbs = Colors()
            satellite_array = read_tles(f.read(), rgbs)

        start_time = datetime.utcnow().replace(tzinfo=pytz.UTC)
        end_time = start_time + timedelta(hours=24)
        doc = create_czml_file(start_time, end_time)

        for sat in tqdm.tqdm(satellite_array):  # 以后还要把进度条返回前端 现在先不管 这不是特别重要
            sat_name = sat.sat_name
            orbit_time_in_minutes = sat.orbital_time_in_minutes
            tle_epoch = sat.tle_epoch

            sat_packet = create_satellite_packet(sat, start_time, end_time)

            doc.packets.append(sat_packet)

        with open(output_path, 'w') as f:
            f.write(str(doc))

        # Formalize Czml
        file = open(output_path, 'rb')
        strs = json.load(file)
        js_data = json.dumps(strs, indent=4, separators=(',', ':')).encode('utf-8').decode('raw_unicode_escape')
        with open(output_path, 'w') as f:
            f.write(js_data)
    '''


    return jsonify({"code": 200})

@compute_bp.route('/compute')
def compute():
    ts = load.timescale()

    position_list = []

    global data, utc_time, timestep
    if(len(data) == 0):
        with open('./static/data/show.txt', 'r') as f:
            data = f.readlines()
        utc_time = datetime.datetime.utcnow()
        timestep = 1
    else:
        if (int(request.args.get('timestep')) != timestep):
            timestep = int(request.args.get('timestep'))
        utc_time = utc_time + datetime.timedelta(seconds=float(timestep) * 0.333)

    # for i in range(int(len(data) / 2)):
    for i in range(100):
        line1 = data[i * 2 - 2]
        line2 = data[i * 2 - 1]

        satellite = EarthSatellite(line1, line2, ts=ts)
        geocentric = satellite.at(ts.utc(utc_time.year, utc_time.month, utc_time.day, utc_time.hour, utc_time.minute, utc_time.second))
        subpoint = wgs84.subpoint(geocentric)

        latitude = str(subpoint.latitude)
        latitude = re.sub(r'[^0-9.-]+', '*', latitude)
        latitude = latitude.strip('*')
        latitude_hour, latitude_minute, latitude_second = latitude.split('*')
        latitude_hour = float(latitude_hour)
        latitude_minute = float(latitude_minute)
        latitude_second = float(latitude_second)
        if(latitude_hour < 0):
            latitude_minute = -latitude_minute
            latitude_second = -latitude_second
        latitude = latitude_hour + latitude_minute / 60.0 + latitude_second / 3600.0

        longitude = str(subpoint.longitude)
        longitude = re.sub(r'[^0-9.-]+', '*', longitude)
        longitude = longitude.strip('*')
        longitude_hour, longitude_minute, longitude_second = longitude.split('*')
        longitude_hour = float(longitude_hour)
        longitude_minute = float(longitude_minute)
        longitude_second = float(longitude_second)
        if (longitude_hour < 0):
            longitude_minute = -longitude_minute
            longitude_second = -longitude_second
        longitude = longitude_hour + longitude_minute / 60.0 + longitude_second / 3600.0

        height = str(subpoint.elevation.km)
        height = re.sub(r'[^0-9.-]+', '*', height)
        height = height.strip('*')
        height = float(height)

        position_list.append((latitude, longitude, height))

    return jsonify({"success": 200, "msg": "Success!", "data": position_list, "time": utc_time.strftime("%Y-%m-%d %H:%M:%S"), "timestep": timestep})
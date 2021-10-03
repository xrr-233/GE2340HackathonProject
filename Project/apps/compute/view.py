from flask import Blueprint, jsonify, request
from skyfield.api import load, EarthSatellite, wgs84
import re
import datetime

compute_bp = Blueprint('compute', __name__)

data = []
utc_time = None
timestep = 0

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
    for i in range(100):  # 因为会算出nan 所以输出所有数据的被卡了 暂时先用100代替
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
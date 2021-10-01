from flask import Blueprint, render_template
from skyfield.api import load, EarthSatellite, wgs84
import re

index_bp = Blueprint('login', __name__)

@index_bp.route('/')
def render_earth():
    ts = load.timescale()

    position_list = []

    with open('./static/data/show.txt', 'r') as f:
        data = f.readlines()

        # for i in range(int(len(data) / 2)):
        for i in range(10000): # 因为会算出nan 所以输出所有数据的被卡了 暂时先用10000代替
            line1 = data[i * 2 - 2]
            line2 = data[i * 2 - 1]

            satellite = EarthSatellite(line1, line2, ts=ts)
            geocentric = satellite.at(ts.now())
            subpoint = wgs84.subpoint(geocentric)

            latitude = str(subpoint.latitude)
            latitude = re.sub(r'[^0-9.-]+', '*', latitude)
            latitude = latitude.strip('*')
            latitude_hour, latitude_minute, latitude_second = latitude.split('*')
            latitude = float(latitude_hour) + float(latitude_minute) / 60.0 + float(latitude_second) / 3600.0

            longitude = str(subpoint.longitude)
            longitude = re.sub(r'[^0-9.-]+', '*', longitude)
            longitude = longitude.strip('*')
            longitude_hour, longitude_minute, longitude_second = longitude.split('*')
            longitude = float(longitude_hour) + float(longitude_minute) / 60.0 + float(longitude_second) / 3600.0

            height = str(subpoint.elevation.km)
            height = re.sub(r'[^0-9.-]+', '*', height)
            height = height.strip('*')
            height = float(height)

            position_list.append((latitude, longitude, height))

            # break

    return render_template('index/index.html', position=position_list)
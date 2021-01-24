#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import pynmea2
import matplotlib.pyplot as plt
import math
from pyproj import CRS, Transformer
from pyproj import Proj

def trans():
    
    gga = '$GNGGA,051841.00,3017.628130,N,11337.843219,E,1,12,0.8,15.3,M,-15.3,M,,*64'

    record = pynmea2.parse(gga)

    transformer4479 = Transformer.from_crs('epsg:4326','epsg:4479')

    cgc4479_x,cgc4479_y = transformer4479.transform(record.latitude,record.longitude)

    print('4479 x:', cgc4479_x, 'y:', cgc4479_y)

    transformer4480 = Transformer.from_crs('epsg:4326','epsg:3857')

    cgc4480_x,cgc4480_y = transformer4480.transform(record.latitude,record.longitude)

    print('3857 x:', cgc4480_x, 'y:', cgc4480_y)
    
    p = Proj(proj='utm',zone=10,ellps='WGS84', preserve_units=False)
    x,y = p(113.63072031666667, 30.293802166666666)

    print('x:', x, 'y:', y)

if __name__ == '__main__':
    trans()    


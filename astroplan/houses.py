import matplotlib.pyplot as plt

import numpy as np

from datetime import datetime as dt, tzinfo

import swisseph as swe

import julian as jl

from geopy.geocoders import Nominatim
from pytz import timezone

from astroknow.astroplan.views import flags

swe.set_ephe_path('/home/gaia/Документы/eph files')

planet_list = ['sun','mercury','venus', 'moon', 'mars',
                 'jupiter','saturn', 'uranus', 'neptune','pluto']

now = dt.now(tz=timezone('Asia/Yekaterinburg'))
#
# print(now)
date = dt(1986, 2,17, 22,20, tzinfo=timezone('Asia/Yekaterinburg'))
jd_date = jl.to_jd(date,fmt='jd')

jd = jl.to_jd(now, fmt='jd')


loc = Nominatim(user_agent="GetLoc", timeout=100000)
getLoc = loc.geocode("Ufa, Russia", timeout=10000)
# houses = swe.houses(jd, getLoc.latitude, getLoc.longitude, b'P')
houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'R', flags=swe.FLG_SIDEREAL)

sun = swe.calc_ut(jd_date, 0, flags)
moon = swe.calc_ut(jd_date, 1, flags)

mercury = swe.calc_ut(jd_date, 2, flags)
venus = swe.calc_ut(jd_date, 3, flags)
mars = swe.calc_ut(jd_date, 4, flags)

jupiter = swe.calc_ut(jd_date, 5, flags)
saturn = swe.calc_ut(jd_date, 6, flags)

uranus = swe.calc_ut(jd_date, 7, flags)
neptune = swe.calc_ut(jd_date, 8, flags)
pluto = swe.calc_ut(jd_date, 9, flags)

planet_list = [sun, moon, mercury, venus, mars, jupiter,
               saturn, uranus, neptune, pluto]





print(houses)


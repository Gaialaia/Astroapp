import datetime

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from datetime import datetime as dt

import swisseph as swe

import julian as jl

import zoneinfo as zi

from geopy.geocoders import Nominatim
from pytz import timezone

from timezonefinder import TimezoneFinder


opposition = np.arange(175.0, 185.0)
trine = np.arange(115.0, 125.0)
square = np.arange(85.0, 95.0)
conjunction = np.arange(0.0, 5.0)

now = dt.now(tz=timezone('UTC'))
flags = swe.FLG_SIDEREAL | swe.SIDM_LAHIRI

date_one = dt(2025,8,17)
date = dt(1986, 2,17, 17,20)
# jd = jl.to_jd(date, fmt='jd')
jd = jl.to_jd(date_one, fmt='jd')

px = 1/plt.rcParams['figure.dpi']
matplotlib.rcParams['axes.edgecolor'] = 'darkorchid'

img = mpimg.imread('static/images/zr_one_clr.png')
fig = plt.figure(figsize=(870*px, 870*px))
fig.suptitle(f'Planet chart today,{now.strftime('%B, %d, %H:%M')}', size=17)
fig.patch.set_alpha(0.0)

ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
ax_img.imshow(img)
ax_img.axis('off')


planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar', facecolor='red')

planet_ax.set_rlim(-130,100)
planet_ax.set_theta_direction('counterclockwise')
planet_ax.set_rticks([])
planet_ax.set_axis_off() #'theta ax' is off and grid off
planet_ax.set_thetagrids(range(0, 360, 30))


house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar', facecolor='red')
house_ax.patch.set_alpha(0.0)


loc = Nominatim(user_agent="GetLoc")
getLoc = loc.geocode("Los-Angeles, USA", timeout=7000)
houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'R', flags=swe.FLG_SIDEREAL)
tf = TimezoneFinder()
loc_tz = tf.timezone_at(lng=getLoc.longitude, lat=getLoc.latitude)

# print(type(loc_tz))

d = datetime.datetime(2025,10,31,8,42,00)



# print(now)





house_ax.set_rlim(-130, 100)
house_ax.set_theta_direction(1)
house_ax.set_rticks([])
house_ax.set_thetagrids(houses[0], ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
house_ax.tick_params(labelsize=20, grid_color='red', grid_linewidth=1, labelfontfamily='monospace')
house_ax.set_theta_offset(np.pi)


pd = {swe.get_planet_name(0): ['☼', 'yellow',5, 17, swe.calc_ut(jd,0,flags)[0][0],swe.calc_ut(jd,0,flags)[0][1],10],
      swe.get_planet_name(1): ['☾', 'blue',5, 17, swe.calc_ut(jd,1,flags)[0][0],swe.calc_ut(jd,1,flags)[0][1],-25],
      swe.get_planet_name(2): ['☿', 'grey', 5, 17, swe.calc_ut(jd,2,flags)[0][0],swe.calc_ut(jd,1,flags)[0][1],-25],
      swe.get_planet_name(3): ['♀', 'sienna', 5, 17,swe.calc_ut(jd,3,flags)[0][0],swe.calc_ut(jd,1,flags)[0][1],25],
      swe.get_planet_name(4): ['♂', 'red', 5, 17,swe.calc_ut(jd,4,flags)[0][0],swe.calc_ut(jd,1,flags)[0][1], -10],
      swe.get_planet_name(5): ['♃', 'teal', 5, 17,swe.calc_ut(jd,5,flags)[0][0],swe.calc_ut(jd,1,flags)[0][1],0],
      swe.get_planet_name(6): ['♄', 'slategrey', 5, 17,swe.calc_ut(jd,6,flags)[0][0],swe.calc_ut(jd,1,flags)[0][1],-25],
      swe.get_planet_name(7): ['♅', 'chartreuse', 5, 17,swe.calc_ut(jd,7,flags)[0][0],swe.calc_ut(jd,1,flags)[0][1],0],
      swe.get_planet_name(8): ['♆', 'indigo', 5, 17,swe.calc_ut(jd,8,flags)[0][0],swe.calc_ut(jd,1,flags)[0][1],0],
      swe.get_planet_name(9): ['♇', 'darkmagenta', 5, 17,swe.calc_ut(jd,9,flags)[0][0],swe.calc_ut(jd,1,flags)[0][1],0]
      }
coords_value = list(pd.values())

for value in range(len(coords_value) - 1):
    for pl in range(0, 10):

        aspect = abs(round(coords_value[pl][4]) - round(coords_value[value + 1][4]))

        if aspect in trine and coords_value[pl][4] != coords_value[value + 1][4]:
            pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
            pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
            planet_ax.plot(pl_one, pl_two, color='green', lw=0.5)
            # print(coords_value[pl][0], aspect, coords_value[value + 1][0])

        if aspect in opposition and coords_value[pl][4] != coords_value[value + 1][4]:
            pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value+1][4])])
            pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value+1][5])])
            planet_ax.plot(pl_one, pl_two, color='pink', lw=0.5)

        if aspect in square and coords_value[pl][4] != coords_value[value + 1][4]:
            pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
            pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
            planet_ax.plot(pl_one, pl_two, color='firebrick', lw=0.5)
        planet_symbols = ['☼', '☾', '☿', '♀', '♂', '♃', '♄', '♅', '♆', '♇']

        if aspect in conjunction and coords_value[pl][4] != coords_value[value + 1][4]:
            pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
            pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
            planet_ax.plot(pl_one, pl_two, color='green', lw=0.5)
            # # if coords_value[pl][0] ==  '♂' and coords_value[pl+1][0] == '♄':
            # planet_ax.annotate(f'{coords_value[pl][0]}', textcoords='offset points', xytext=(20, 3),
            #                xycoords='data',
            #                xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                fontsize=pd[swe.get_planet_name(pl)][3],
            #                color='darkgoldenrod',
            #                arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
            # #
            # # planet_ax.annotate(f'{coords_value[pl+1][0]}', textcoords='offset points', xytext=(20, 3),
            # #                        xycoords='data',
            # #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            # #                        fontsize=pd[swe.get_planet_name(pl)][3],
            # #                        color='darkgoldenrod',
            #                        arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))






        planet_ax.plot(np.deg2rad(coords_value[pl][4]), coords_value[pl][5], 'o', mfc=pd[swe.get_planet_name(pl)][1],
                       ms=pd[swe.get_planet_name(pl)][2])

        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points', xytext=(pd[swe.get_planet_name(pl)][6],0),
                           xycoords='data',
                           xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
                           fontsize=pd[swe.get_planet_name(pl)][3],
                           color='darkgoldenrod',
                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
        # planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points', xytext=(25, 0),
        #                    xycoords='data',
        #                    xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
        #                    fontsize=pd[swe.get_planet_name(pl)][3],
        #                    color='darkgoldenrod',
        #                    arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


    # if coords_value[value][4] - coords_value[value + 1][4] < 10 and coords_value[value][4] != coords_value[value + 1][4]:
    #     planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points', xytext=(20, 3),
    #                        xycoords='data',
    #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
    #                        fontsize=pd[swe.get_planet_name(pl)][3],
    #                        color='darkgoldenrod',
    #                        arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
    #     planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
    #                                           xytext=(-20, 3),
    #                                           xycoords='data',
    #                                           xy=(np.deg2rad(coords_value[value + 1][4]), coords_value[value][5]),
    #                                           fontsize=pd[swe.get_planet_name(pl)][3],
    #                                           color='darkgoldenrod',
    #                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))



# plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/test_fig.png', pad_inches=0.0)
# plt.show()


# print(pd[swe.get_planet_name(9)][6])
#
# print(pd.values())
# #
# print(pd.items())
# k = [key for key, val in pd.items() if val == 304.2105322664011]
# print(k)



# g = [(p[4],p[0]) for p in coords_value  for q in coords_value ]
#
# print(g[0][0])
# for c in range(len(g)-1):
#     d = g[c][0] - g[c + 1][0]
#     if g[c][0] - g[c+1][0] < 10 and g[c][0] != g[c+1][0] :
#         print(g[c], d)


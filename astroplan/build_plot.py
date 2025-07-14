
import matplotlib
import matplotlib.pyplot as plt

import numpy as np

from datetime import datetime as dt

import swisseph as swe

import julian as jl

from geopy.geocoders import Nominatim
from pytz import timezone

from timezonefinder import TimezoneFinder


now = dt.now(tz=timezone('UTC'))



date = dt(1986, 2,17, 17,20)
jd = jl.to_jd(date, fmt='jd')

px = 1/plt.rcParams['figure.dpi']
matplotlib.rcParams['axes.edgecolor'] = 'darkorchid'
fig = plt.figure(figsize=(870*px, 870*px))
fig.suptitle(f'Planet chart today,{now.strftime('%B, %d, %H:%M')}', size=17 )
fig.patch.set_alpha(0.0)

ax1 = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar', facecolor='red') #center plot
transit_z = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
transit_z.patch.set_alpha(0.0)

house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar', facecolor='red')
house_ax.patch.set_alpha(0.0)
#
ax1.set_rlim(-130,100)
ax1.set_theta_direction('counterclockwise')
ax1.set_rticks([])
ax1.set_axis_off() #'theta ax' is off and grid off
ax1.set_thetagrids(range(0, 360, 30))


transit_z.set_rlim(-800,90)
transit_z.set_theta_direction('counterclockwise')
transit_z.set_rticks([])
transit_z.set_axis_off() #'theta ax' is off and grid off
transit_z.set_thetagrids(range(0, 360, 30))

opposition = np.arange(175.0, 185.0)
trine = np.arange(115.0, 125.0)
square = np.arange(85.0, 95.0)
conjunction = np.arange(0.0, 5.0)

sqaures = []
trines = []
oppositions = []
conjunctions = []

aspected_planet = []
aspected_planet_op = []
aspected_planet_t = []
aspected_planet_c = []
sq_angle = []
op_angle = []
t_angle = []
c_angle = []
#
flags = swe.FLG_SIDEREAL | swe.SIDM_LAHIRI
#
sun = swe.calc_ut(jd, 0, flags)
moon = swe.calc_ut(jd, 1, flags)

mercury = swe.calc_ut(jd, 2, flags)
venus = swe.calc_ut(jd, 3, flags)
mars = swe.calc_ut(jd, 4, flags)

jupiter = swe.calc_ut(jd, 5, flags)
saturn = swe.calc_ut(jd, 6, flags)

uranus = swe.calc_ut(jd, 7, flags)
neptune = swe.calc_ut(jd, 8, flags)
pluto = swe.calc_ut(jd, 9, flags)


planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter',
                    'Saturn', 'Uranus', 'Neptune', 'Pluto']
planet_list = [sun, moon, mercury, venus, mars, jupiter,
                   saturn, uranus, neptune, pluto]

names_and_coords = list(zip(planet_names, planet_list))


house_names = ['8', '9', 'MC', '11', '12', 'ASC', '2', '3', 'IC', '5', '6', 'DSC']

loc = Nominatim(user_agent="GetLoc")
getLoc = loc.geocode("Ufa, Russia", timeout=7000)
houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'R', flags=swe.FLG_SIDEREAL)
#
house_ax.set_rlim(-130, 100)
house_ax.set_theta_direction(1)
house_ax.set_rticks([])
house_ax.set_thetagrids(houses[0], ['8', '9', 'MC', '11', '12', 'ASC', '2', '3', 'IC', '5', '6', 'DSC'])
house_ax.tick_params(labelsize=20, grid_color='red', grid_linewidth=1, labelfontfamily='monospace')
house_ax.set_theta_offset(np.pi)

def aspect(planet_number):
        for i in range(len(names_and_coords) - 1):

            z = abs(round(names_and_coords[planet_number][1][0][0]) - round(names_and_coords[i + 1][1][0][0]))
            if z in square:
                p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
                               np.deg2rad(names_and_coords[i + 1][1][0][0])])
                p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
                ax1.plot(p1, p2, lw=0.5, color='firebrick')

                aspected_planet.append(names_and_coords[planet_number][0])
                sq_angle.append(f'{z}°')
                sqaures.append(names_and_coords[i + 1][0])
                aspect_table_squares = zip(aspected_planet, sq_angle, sqaures)

            if z in opposition:
                p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
                               np.deg2rad(names_and_coords[i + 1][1][0][0])])
                p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
                ax1.plot(p1, p2, lw=0.5, color='magenta')

                aspected_planet_op.append(names_and_coords[planet_number][0])
                op_angle.append(f'{z}°')
                oppositions.append(names_and_coords[i + 1][0])
                aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

            if z in trine:
                p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
                               np.deg2rad(names_and_coords[i + 1][1][0][0])])
                p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
                ax1.plot(p1, p2, lw=0.8, color='lime')
                aspected_planet_t.append(names_and_coords[planet_number][0])
                t_angle.append(f'{z}°')
                trines.append(names_and_coords[i + 1][0])
                aspect_table_t = zip(aspected_planet_t, t_angle, trines)


            # if z in conjunction:
            #     p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
            #                    np.deg2rad(names_and_coords[i + 1][1][0][0])])
            #     p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
            #     ax1.plot(p1, p2, lw=0.8, color='lime')
            #     aspected_planet_c.append(names_and_coords[planet_number][0])
            #     c_angle.append(f'{z}°')
            #     c_unique = list(set(c_angle))
            #
            #
            #     conjunctions.append(names_and_coords[i + 1][0])
            #     names_unique = list(set(conjunctions))
            #
            #     aspect_table_c = zip(aspected_planet_c, c_unique, names_unique)
                # print(c_unique)
                # print(list(aspect_table_c))
                # print(list(aspect_table_c))
                # print(f' names unique {names_unique}')



ax1.plot(np.deg2rad(venus[0][0]), venus[0][1], marker='o', label='venus', ms=5, mfc='deeppink')
ax1.annotate('♀', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(venus[0][0]), venus[0][1]), fontsize=15, color='blueviolet',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

aspect(3)

ax1.plot(np.deg2rad(moon[0][0]), moon[0][1], marker='o', label='moon', mfc='forestgreen', ms=5)
ax1.annotate('☾', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(moon[0][0]), moon[0][1]), fontsize=15, color='slateblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

aspect(1)

ax1.plot(np.deg2rad(sun[0][0]), sun[0][1], marker='o', label='sun', ms=8, mfc='gold')
ax1.annotate('☼', textcoords='offset points', xytext=(20, 5), xycoords='data',
                 xy=(np.deg2rad(sun[0][0]), sun[0][1]), fontsize=50, color='midnightblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

aspect(0)

ax1.plot(np.deg2rad(mercury[0][0]), mercury[0][1], 'o:b', label='merc', ms=5)
ax1.annotate('☿', textcoords='offset points', xytext=(20, 5), xycoords='data',
                 xy=(np.deg2rad(mercury[0][0]), mercury[0][1]), fontsize=15, color='orange',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

aspect(2)

ax1.plot(np.deg2rad(mars[0][0]), mars[0][1], marker='o', label='mars', ms=5, mfc='red')
ax1.annotate('♂', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(mars[0][0]), mars[0][1]), fontsize=15, color='slateblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

aspect(4)

ax1.plot(np.deg2rad(jupiter[0][0]), jupiter[0][1], 'o', label='jupiter', ms=7, mfc='steelblue')
ax1.annotate('♃', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(jupiter[0][0]), jupiter[0][1]), fontsize=17, color='slateblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

aspect(5)

ax1.annotate(f'{round(jupiter[0][0])}°', textcoords='offset points', xytext=(-20, 5), xycoords='data',
                 xy=(np.deg2rad(jupiter[0][0]), jupiter[0][1]), fontsize=8, color='navy',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

ax1.plot(np.deg2rad(saturn[0][0]), saturn[0][1], 'o:k', label='saturn', ms=6)
ax1.annotate('♄', textcoords='offset points', xytext=(20, -20), xycoords='data',
                 xy=(np.deg2rad(saturn[0][0]), saturn[0][1]), fontsize=15,
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

aspect(6)

ax1.plot(np.deg2rad(uranus[0][0]), uranus[0][1], marker='o', mfc='chartreuse', label='uranus', ms=6)
ax1.annotate('♅', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(uranus[0][0]), uranus[0][1]), fontsize=15, color='rebeccapurple',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

aspect(7)

ax1.plot(np.deg2rad(neptune[0][0]), neptune[0][1], marker='o', label='neptune', ms=5, mfc='deepskyblue')
ax1.annotate('♆', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(neptune[0][0]), neptune[0][1]), fontsize=20, color='indigo',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

aspect(8)

ax1.plot(np.deg2rad(pluto[0][0]), pluto[0][1], 'o:k', mfc='red', label='pluto', ms=5)
ax1.annotate('♇', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(pluto[0][0]), pluto[0][1]), fontsize=50, color='darkgoldenrod',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


aspect(9)
swe.close()
# plt.savefig('chart_and_houses.png')
# plt.show()



# import csv
#
# with open('names.csv', 'w', newline='') as csvfile:
#     fieldnames = ['planet', 'degrees','sign']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()


# print(list(planet_deg))


#
#

# print(names_and_coords[0][0])
for i in range(len(names_and_coords) - 1):
    z = abs(round(names_and_coords[2][1][0][0]) - round(names_and_coords[i + 1][1][0][0]))
    if z in conjunction and names_and_coords [2][1][0][0] != names_and_coords[i + 1][1][0][0]:
        aspected_planet_c.append(names_and_coords[2][0])
        ap_c_unique = list(set(aspected_planet_c))
        c_angle.append(f'{z}')
        c_unique = list(set(c_angle))
        conjunctions.append(names_and_coords[i+1][0])
        ast = zip(ap_c_unique, c_unique, conjunctions)

        print(list(ast))



    # if z in conjunction:
    #     aspected_planet_c.append(names_and_coords[8][0])
    #     print(aspected_planet_c)
    #     c_angle.append(f'{z}°')
    #
    #
    #     conjunctions.append(names_and_coords[i + 1][0])
    #
    #
    #     aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)




#
# print(f'planet name: {names_and_coords[0][0]}, lat {names_and_coords[0][1][0][0]}, long {names_and_coords[0][1][0][1]}')
#
# thirty_r_deg = [round(p[0][0], 2) % 30 for p in planet_list]  # convert from start point 360 to 30X12
# r_result = [round(n, 2) for n in thirty_r_deg]  # round divided into 30 result
# conv_r_result = [str(n).replace('.', '°').replace(',', '′,') for n in r_result]


# hr_deg = [round(p) for p in houses[0]]
#
# hr_deg_d = [round(p, 2) % 30 for p in houses[0]]
# hr_result =  [round(n, 2) for n in hr_deg_d]
# conv_hr_result = [str(n).replace('.', '°').replace(',', '′,') for n in hr_result]
# hn = zip(conv_hr_result,house_names )
#
#
# signs = []


# def set_signs(deg_intervals):




# def set_signs(name_list,deg_list):
#     round_deg = [round(d) for d in deg_list]  #rounded 360 degree list for setting signs
#     if signs:
#         signs.clear()
#     for i in range(len(deg_list)):
#         if round_deg[i] in range(300, 331):
#             sign = '♒'
#         if round_deg[i] in range(330, 361):
#             sign = 'pisces'
#         if round_deg[i] in range(0, 31):
#             sign = 'aries'
#         if round_deg[i] in range(30, 61):
#             sign = '♉'
#         if round_deg[i] in range(60, 91):
#             sign = 'gemini'
#         if round_deg[i] in range(90, 121):
#             sign = 'cancer'
#         if round_deg[i] in range(120, 151):
#             sign = 'leo'
#         if round_deg[i] in range(150, 181):
#             sign = 'virgo'
#         if round_deg[i] in range(180, 211):
#             sign = '♎'
#         if round_deg[i] in range(210, 241):
#             sign = '♏'
#         if round_deg[i] in range(240, 271):
#             sign = '♐'
#         if round_deg[i] in range(270, 301):
#             sign = '♑'
#
#
#         signs.append(sign)
#     deg_list_thirty = [round(c%30,2)for c in deg_list]
#     deg_form = [str(n).replace('.', '°').replace(',', '′,') for n in deg_list_thirty]
#     m = zip(name_list,deg_form, signs)
#
#     return list(m)


jd = jl.to_jd(date, fmt='jd')
sun = swe.calc_ut(jd, 0, flags)
moon = swe.calc_ut(jd, 1, flags)

mercury = swe.calc_ut(jd, 2, flags)
venus = swe.calc_ut(jd, 3, flags)
mars = swe.calc_ut(jd, 4, flags)

jupiter = swe.calc_ut(jd, 5, flags)
saturn = swe.calc_ut(jd, 6, flags)

uranus = swe.calc_ut(jd, 7, flags)
neptune = swe.calc_ut(jd, 8, flags)
pluto = swe.calc_ut(jd, 9, flags)

tr_planet_list = [sun, moon, mercury, venus, mars, jupiter,
                   saturn, uranus, neptune, pluto]










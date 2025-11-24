
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpi
import numpy as np

import csv

from datetime import datetime as dt

import swisseph as swe

import julian as jl

from geopy.geocoders import Nominatim
from pytz import timezone

from timezonefinder import TimezoneFinder


now = dt.now(tz=timezone('UTC'))


date = dt(1986, 2,17, 17,20)
jd = jl.to_jd(now, fmt='jd')

px = 1/plt.rcParams['figure.dpi']
matplotlib.rcParams['axes.edgecolor'] = 'darkorchid'
matplotlib.rcParams['axes.linewidth'] = 3
loc = Nominatim(user_agent="GetLoc")
flags =  swe.FLG_SIDEREAL | swe.SIDM_LAHIRI

planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter',
                'Saturn', 'Uranus', 'Neptune', 'Pluto']

house_names = ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII']
opposition = np.arange(175.0, 185.0)
trine = np.arange(115.0, 125.0)
square = np.arange(85.0, 95.0)
conjunction = np.arange(0.00, 7.00)

sqaures = []
trines = []
oppositions = []
conjunctions = []

aspected_planet_s = []
aspected_planet_op = []
aspected_planet_t = []
aspected_planet_c = []
sq_angle = []
op_angle = []
t_angle = []
c_angle = []

signs = []
sign =''

# img = mpi.imread('astroplan/static/images/tr_zr_1.png')
fig = plt.figure(figsize=(870*px, 870*px))
fig.patch.set_alpha(0.0)
# ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
# ax_img.imshow(img)
# ax_img.axis('off')

plot_date = jd
pd = {swe.get_planet_name(0): ['☼', 'yellow', 5, 25, swe.calc_ut(jd, 0, flags)[0][0],
                                   swe.calc_ut(jd, 0, flags)[0][1], 0],

          swe.get_planet_name(1): ['o', 'blue', 5, 20, swe.calc_ut(plot_date, 1, flags)[0][0],
                                   swe.calc_ut(plot_date, 1, flags)[0][1], 0],

          swe.get_planet_name(2): ['☿', 'grey', 5, 23, swe.calc_ut(plot_date, 2, flags)[0][0],
                                   swe.calc_ut(plot_date, 2, flags)[0][1], 0],

          swe.get_planet_name(3): ['♀', 'sienna', 5, 22, swe.calc_ut(plot_date, 3, flags)[0][0],
                                   swe.calc_ut(plot_date, 3, flags)[0][1],0],

          swe.get_planet_name(4): ['♂', 'red', 5, 20, swe.calc_ut(plot_date, 4, flags)[0][0],
                                   swe.calc_ut(plot_date, 4, flags)[0][1],0],

          swe.get_planet_name(5): ['♃', 'teal', 5, 26, swe.calc_ut(plot_date, 5, flags)[0][0],
                                   swe.calc_ut(plot_date, 5, flags)[0][1],0],

          swe.get_planet_name(6): ['♄', 'slategrey', 5, 25, swe.calc_ut(plot_date, 6, flags)[0][0],
                                   swe.calc_ut(plot_date, 6, flags)[0][1],0],

          swe.get_planet_name(7): ['♅', 'chartreuse', 5, 22, swe.calc_ut(plot_date, 7, flags)[0][0],
                                   swe.calc_ut(plot_date, 7, flags)[0][1],0],

          swe.get_planet_name(8): ['♆', 'indigo', 5, 22, swe.calc_ut(plot_date, 8, flags)[0][0],
                                   swe.calc_ut(plot_date, 8, flags)[0][1],0],

          swe.get_planet_name(9): ['♇', 'darkmagenta', 5, 22, swe.calc_ut(plot_date, 9, flags)[0][0],
                                   swe.calc_ut(plot_date, 9, flags)[0][1],0]}




planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar') #center plot
planet_ax.set_rlim(-130, 100)
planet_ax.set_theta_direction('counterclockwise')
planet_ax.set_rticks([])
# planet_ax.set_axis_off()  # 'theta ax' is off and grid off


planet_ax2 = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar') #center plot
planet_ax2.patch.set_alpha(0.0)
planet_ax2.set_theta_direction('counterclockwise')
planet_ax2.set_rticks([])
planet_ax.set_facecolor('teal')


# house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
# house_ax.patch.set_alpha(0.0)
# house_ax.set_facecolor('aliceblue')


plot_date =  jl.to_jd(date, fmt='jd')
getLoc = loc.geocode("Ufa, Russia", timeout=7000)
houses = swe.houses_ex(plot_date, getLoc.latitude, getLoc.longitude, b'R', flags=swe.FLG_SIDEREAL)



#
# house_ax.set_rlim(-130, 100)
# house_ax.set_theta_direction(1)
# house_ax.set_rticks([])
# house_ax.set_thetagrids(houses[0], ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
# house_ax.tick_params(labelsize=20, grid_color='#815684', grid_linewidth=1, labelfontfamily='monospace',
#                                                       labelcolor='aliceblue', pad=17.0)
# house_ax.set_theta_offset(np.pi)




coords_value = list(pd.values())

def set_signs(name_list, deg_list):
        if signs:
            signs.clear()
        round_deg = [round(d) for d in deg_list]
        for i in range(len(deg_list)):
            if round_deg[i] in range(300, 331):
                sign = '♒'
            if round_deg[i] in range(330, 361):
                sign = '♓'
            if round_deg[i] in range(0, 31):
                sign = '♈'
            if round_deg[i] in range(30, 61):
                sign = '♉'
            if round_deg[i] in range(60, 91):
                sign = '♊'
            if round_deg[i] in range(90, 121):
                sign = '♋'
            if round_deg[i] in range(120, 151):
                sign = '♌'
            if round_deg[i] in range(150, 181):
                sign = '♍'
            if round_deg[i] in range(180, 211):
                sign = '♎'
            if round_deg[i] in range(210, 241):
                sign = '♏'
            if round_deg[i] in range(240, 271):
                sign = '♐'
            if round_deg[i] in range(270, 301):
                sign = '♑'
            signs.append(sign)
        deg_list_thirty = [round(c % 30, 2) for c in deg_list]
        deg_form = [str(n).replace('.', '°').replace(',', '′,') for n in deg_list_thirty]
        sign_table = zip(name_list, deg_form, signs)
        return list(sign_table)

# aspect_table_s = None
# aspect_table_ops = None
# aspect_table_c = None
# aspect_table_t = None
#
# aspected_planet_t.clear()
# aspected_planet_op.clear()
# aspected_planet_s.clear()
# aspected_planet_c.clear()
#
# c_angle.clear()
# t_angle.clear()
# sq_angle.clear()
# c_angle.clear()
#
# oppositions.clear()
# sqaures.clear()
# conjunctions.clear()
# trines.clear()

for value in range(len(coords_value) - 1):
        for pl in range(0, 10):
            aspect = abs(round(coords_value[pl][4]) - round(coords_value[value + 1][4]))

            if aspect in trine and coords_value[pl][4] != coords_value[value + 1][4]:
                pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
                pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                planet_ax.plot(pl_one, pl_two, color='#3fff00', lw=0.8)
                planet_ax2.plot(pl_one, pl_two, color='#3fff00', lw=0.8)

                aspected_planet_t.append(coords_value[pl][0])

                t_angle.append(f'{aspect}°')
                trines.append(coords_value[value + 1][0])
                aspect_table_t = zip(aspected_planet_t, t_angle, trines)

            elif aspect in opposition and coords_value[pl][4] != coords_value[value + 1][4]:
                pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
                pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                if 179 < aspect < 181:
                    planet_ax.plot(pl_one, pl_two, color='#0400ff', lw=1.5)
                    planet_ax2.plot(pl_one, pl_two, color='#3fff00', lw=0.8)
                elif 181 < aspect < 183:
                    planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=1.0)
                    planet_ax2.plot(pl_one, pl_two, color='#0900FF', lw=1.0)
                elif 183 < aspect < 187:
                    planet_ax.plot(pl_one, pl_two, color='#0400ff', lw=0.8)
                    planet_ax2.plot(pl_one, pl_two, color='#0400ff', lw=0.8)

                # planet_ax.plot(pl_one, pl_two, color='#0400ff', lw=0.8)

                aspected_planet_op.append(coords_value[pl][0])
                op_angle.append(f'{aspect}°')
                oppositions.append(coords_value[value + 1][0])
                aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)


            elif aspect in square and coords_value[pl][4] != coords_value[value + 1][4]:
                pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
                pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                planet_ax.plot(pl_one, pl_two, color='#fd0048', lw=0.8)
                planet_ax2.plot(pl_one, pl_two, color='#0400ff', lw=0.8)

                aspected_planet_s.append(coords_value[pl][0])
                sq_angle.append(f'{aspect}°')
                sqaures.append(coords_value[value + 1][0])
                aspect_table_s = zip(aspected_planet_s,sq_angle,sqaures)


            elif aspect in conjunction and coords_value[pl][4] != coords_value[value + 1][4]:
                pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
                pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                planet_ax.plot(pl_one, pl_two, color='#8aed07', lw=0.8)
                planet_ax2.plot(pl_one, pl_two, color='#0400ff', lw=0.8)

                aspected_planet_c.append(coords_value[pl][0])
                c_angle.append(f'{aspect}°')
                conjunctions.append(coords_value[value + 1][0])
                aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

            planet_ax.plot(np.deg2rad(coords_value[pl][4]), coords_value[pl][5], 'o',
                           mfc=pd[swe.get_planet_name(pl)][1],
                           ms=pd[swe.get_planet_name(pl)][2])

            planet_ax2.plot(np.deg2rad(coords_value[pl][4]), coords_value[pl][5], 'o',
                           mfc=pd[swe.get_planet_name(pl)][1],
                           ms=pd[swe.get_planet_name(pl)][2])



            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                               xytext=(pd[swe.get_planet_name(pl)][6], 3),
                               xycoords='data',
                               xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
                               fontsize=pd[swe.get_planet_name(pl)][3],
                               color='aliceblue',
                               arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

            planet_ax2.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                               xytext=(pd[swe.get_planet_name(pl)][6], 3),
                               xycoords='data',
                               xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
                               fontsize=pd[swe.get_planet_name(pl)][3],
                               color='aliceblue',
                               arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))



            # if coords_value[pl][4] == 0 or coords_value[pl] [4] < 45:
            #     planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(-20,-8),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
            #
            #     planet_ax2.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(-20, -8),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
            #
            #
            # elif 45 < coords_value[pl][4] < 135:
            #     planet_ax2.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(-15, -25),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
            #
            #     planet_ax2.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(-15, -25),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
            #
            # elif 135 < coords_value[pl][4] < 180:
            #     planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(3, 13),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))
            #
            #     planet_ax2.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(3, 13),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))
            #
            # elif 180 < coords_value[pl][4] < 225:
            #     planet_ax2.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(0, 25),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
            #
            #     planet_ax2.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(0, 25),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
            #
            # elif 225 < coords_value[pl][4] < 270:
            #     planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(-25, -5),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
            #
            #     planet_ax2.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(-25, -5),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
            #
            #
            #
            # elif 270 < coords_value[pl][4] < 315:
            #     planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(-25, -5),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
            #
            #     planet_ax2.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(-25, -5),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
            #
            # elif 315 < coords_value[pl][4] < 360:
            #     if coords_value[pl][0]== '♆':
            #         planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                        xytext=(3, -10),
            #                        xycoords='data',
            #                        xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                        fontsize=pd[swe.get_planet_name(pl)][3],
            #                        color='teal',
            #                        arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
            #
            #         planet_ax2.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                            xytext=(3, -10),
            #                            xycoords='data',
            #                            xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                            fontsize=pd[swe.get_planet_name(pl)][3],
            #                            color='teal',
            #                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
            #     else:
            #         planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                             xytext=(-25, -5),
            #                             xycoords='data',
            #                             xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                             fontsize=pd[swe.get_planet_name(pl)][3],
            #                             color='teal',
            #                             arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
            #
            #         planet_ax2.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
            #                            xytext=(-25, -5),
            #                            xycoords='data',
            #                            xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
            #                            fontsize=pd[swe.get_planet_name(pl)][3],
            #                            color='teal',
            #                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
            #
            #




plt.show()

# plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/now_chart.png')

# with open ('planet_data.csv', 'w', newline='') as pdf:
#     fieldnames = ['planet names', 'degrees', 'sign']
#     dc_writer = csv.DictWriter(pdf, fieldnames=fieldnames)
#     writer = csv.writer(pdf)
#
#
#     dc_writer.writeheader()
#     for r in set_signs(planet_names,  [p[4] for p in coords_value]):
#         dc_writer.writerow({'planet names': r[0], 'degrees': r[1], 'sign': r[2]})



# for r in set_signs(planet_names,  [p[4] for p in coords_value]):
#      print(r)


u = [(set_signs(planet_names,  [p[4] for p in coords_value]))]

h = [set_signs(house_names, list(houses[0]))]
# print(type(f'{u[0][1][1]}'), u[0][1][2])
#
# filename = f'{now}.png'
#
# print(filename)

# print(list(aspect_table_s))
# print(aspected_planet_s)
# print(sq_angle)
# print(sqaures)
#
# from hashlib import md5
# def avatar(email, size):
#
#     digest = md5(email.lower().encode('utf-8')).hexdigest()
#     return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
#
# print(avatar('volodeya@gmail.com', 128))
#
# lc = loc.geocode("Tulip", timeout=7000)
# print(lc.latitude, lc.longitude)
# print(lc)


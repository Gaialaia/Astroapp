import os

import boto3
import matplotlib.pyplot as plt
import matplotlib.image as mpi
from pycirclize import Circos
import string, random
import numpy as np

from datetime import datetime as dt

import swisseph as swe

import julian as jl

import base64
from io import BytesIO
from django.shortcuts import render
from django.template.context_processors import request
from geopy.geocoders import Nominatim
from pytz import timezone

# from astroknow import settings

flags = swe.FLG_SIDEREAL

sectors = {"♊︎": 30, "♉︎": 30, "♈︎": 30,
           "♓︎": 30, "♒︎": 30, "♑︎": 30,
           "♐︎": 30, "♏︎": 30, "♎︎": 30,
           "♍︎": 30, "♌︎": 30, "♋︎": 30,
           }

circos = Circos(sectors)


opposition = np.arange(175.0, 185.0)
trine = np.arange(115.0, 125.0)
square = np.arange(85.0, 95.0)
conjunction = np.arange(0.00, 7.00)

squares = []
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

# def get_graph():
#     buffer = BytesIO()
#     plt.savefig('astroplan/static/plots/')
#     buffer.seek(0)
#     image_png = buffer.getvalue()
#     graph = base64.b64encode(image_png)
#     graph = graph.decode('utf-8')
#     buffer.close()
#     return graph



def draw_zodiac_one_color(face_color, edge_color, text_color, tick_clr, deg_clr, font_size, line_width):
    for s in sectors.keys():
        zodiac_sector = circos.get_sector(s)
        zodiac_track = zodiac_sector.add_track((70,94))
        zodiac_track.axis(fc=face_color, ec=edge_color, lw=line_width)
        zodiac_track.text(f'{s}',size=font_size,color=text_color)

        for sector in circos.sectors:
            track_deg = sector.add_track((94, 100))
            track_deg.axis(ec=tick_clr)
            track_deg.grid(y_grid_num=None, x_grid_interval=1, color=deg_clr)


    fig = circos.plotfig()
    fig.patch.set_alpha(0.0)

    chart_path = (os.path.join(settings.MEDIA_ROOT, 'color_chart_zodiac_ring/color_chart.png'))
    directory = os.path.dirname(chart_path)

    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    plt.savefig(chart_path, pad_inches=0.0)







def build_plot(timestamp:dt, filename):
    jd = jl.to_jd(timestamp, fmt='jd')

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


    px = 1 / plt.rcParams['figure.dpi']
    plt.switch_backend('AGG')

    img = mpi.imread('astroplan/static/images/tr_zr.png')
    fig = plt.figure(figsize=(870 * px, 870 * px))
    # fig.suptitle("Today planet positions", size=17, color='aliceblue')
    fig.patch.set_alpha(0.0)
    # graph = get_graph()

    ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
    ax_img.imshow(img)
    ax_img.axis('off')

    ax1 = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
    # center plot
    # ax1.set_theta_offset()

    ax1.set_rlim(-130, 100)
    ax1.set_theta_direction('counterclockwise')
    ax1.set_rticks([])
    ax1.set_axis_off()  # 'theta ax' is off and grid off
    ax1.set_thetagrids(range(0, 360, 30))
    # ax1.grid()  #wont work because the axis is off

    opposition = np.arange(175.0, 185.0)
    trine = np.arange(115.0, 125.0)
    square = np.arange(85.0, 95.0)
    conjunction = np.arange(0.0, 10.0)

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

    planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter',
                    'Saturn', 'Uranus', 'Neptune', 'Pluto']
    planet_list = [sun, moon, mercury, venus, mars, jupiter,
                   saturn, uranus, neptune, pluto]

    planet_symbols = ['☼', '☾', '☿', '♀', '♂', '♃', '♄', '♅', '♆', '♇']

    names_and_coords = list(zip(planet_names, planet_list))
    aspect_table_squares = zip(aspected_planet, sq_angle, sqaures)
    aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)
    aspect_table_t = zip(aspected_planet_t, t_angle, trines)
    aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

    pl_names_and_sym = {name: symbol for name, symbol in zip(planet_names, planet_symbols)}

    r_deg = [round(p[0][0], 2) for p in planet_list]
    conv_deg = [str(n).replace('.', '°').replace(',', '′,') for n in r_deg]

    thirty_r_deg = [round(p[0][0], 2) % 30 for p in planet_list]  # convert from start point 360 to 30X12
    r_result = [round(n, 2) for n in thirty_r_deg]  # round divided into 30 result
    conv_r_result = [str(n).replace('.', '°').replace(',', '′,') for n in r_result]

    deg_intervals = [round(d[0][0]) for d in planet_list]
    sign = ''
    signs = []

    for i in range(len(deg_intervals)):
        if deg_intervals[i] in range(300, 331):
            sign = '♒'
        if deg_intervals[i] in range(330, 361):
            sign = 'pisces'
        if deg_intervals[i] in range(0, 31):
            sign = 'aries'
        if deg_intervals[i] in range(30, 61):
            sign = '♉'
        if deg_intervals[i] in range(60, 91):
            sign = 'gemini'
        if deg_intervals[i] in range(90, 121):
            sign = 'cancer'
        if deg_intervals[i] in range(120, 151):
            sign = 'leo'
        if deg_intervals[i] in range(150, 181):
            sign = 'virgo'
        if deg_intervals[i] in range(180, 211):
            sign = '♎'
        if deg_intervals[i] in range(210, 241):
            sign = '♏'
        if deg_intervals[i] in range(240, 271):
            sign = '♐'
        if deg_intervals[i] in range(270, 301):
            sign = '♑'
        signs.append(sign)

    planet_deg = zip(planet_symbols, signs, conv_r_result)

    # for table with houses
    house_names = ['8', '9', 'MC', '11', '12', 'ASC', '2', '3', 'IC', '5', '6', 'DSC']

    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode("Ufa, Russia", timeout=7000)
    houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'R', flags=swe.FLG_SIDEREAL)

    table_data = {'planet_deg':planet_deg, 'ats': aspect_table_squares,'ato': aspect_table_ops,
                  'att': aspect_table_t, 'atc': aspect_table_c}

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

            if z in conjunctions:
                p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
                               np.deg2rad(names_and_coords[i + 1][1][0][0])])
                p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
                ax1.plot(p1, p2, lw=0.8, color='lime')
                aspected_planet_c.append(names_and_coords[planet_number][0])
                c_angle.append(f'{z}°')
                conjunctions.append(names_and_coords[i + 1][0])
                aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

    ax1.plot(np.deg2rad(venus[0][0]), venus[0][1], marker='o', label='venus', ms=5, mfc='deeppink')
    ax1.annotate('♀', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(venus[0][0]), venus[0][1]), fontsize=20, color='aliceblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(3)

    ax1.plot(np.deg2rad(moon[0][0]), moon[0][1], marker='o', label='moon', mfc='forestgreen', ms=5)
    ax1.annotate('☾', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(moon[0][0]), moon[0][1]), fontsize=20, color='aliceblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(1)

    ax1.plot(np.deg2rad(sun[0][0]), sun[0][1], marker='o', label='sun', ms=8, mfc='gold')
    ax1.annotate('☼', textcoords='offset points', xytext=(20, 5), xycoords='data',
                 xy=(np.deg2rad(sun[0][0]), sun[0][1]), fontsize=25, color='aliceblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(0)

    ax1.plot(np.deg2rad(mercury[0][0]), mercury[0][1], 'o:b', label='merc', ms=5)
    ax1.annotate('☿', textcoords='offset points', xytext=(20, 5), xycoords='data',
                 xy=(np.deg2rad(mercury[0][0]), mercury[0][1]), fontsize=20, color='aliceblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(2)

    ax1.plot(np.deg2rad(mars[0][0]), mars[0][1], marker='o', label='mars', ms=5, mfc='red')
    ax1.annotate('♂', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(mars[0][0]), mars[0][1]), fontsize=20, color='aliceblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(4)

    ax1.plot(np.deg2rad(jupiter[0][0]), jupiter[0][1], 'o', label='jupiter', ms=7, mfc='steelblue')
    ax1.annotate('♃', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(jupiter[0][0]), jupiter[0][1]), fontsize=20, color='aliceblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(5)

    # ax1.annotate(f'{round(jupiter[0][0])}°', textcoords='offset points', xytext=(-20, 5), xycoords='data',
    #              xy=(np.deg2rad(jupiter[0][0]), jupiter[0][1]), fontsize=20, color='navy',
    #              arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    ax1.plot(np.deg2rad(saturn[0][0]), saturn[0][1], 'o:k', label='saturn', ms=6)
    ax1.annotate('♄', textcoords='offset points', xytext=(20, -20), xycoords='data',
                 xy=(np.deg2rad(saturn[0][0]), saturn[0][1]), fontsize=20,
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(6)

    ax1.plot(np.deg2rad(uranus[0][0]), uranus[0][1], marker='o', mfc='chartreuse', label='uranus', ms=6)
    ax1.annotate('♅', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(uranus[0][0]), uranus[0][1]), fontsize=20, color='aliceblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(7)

    ax1.plot(np.deg2rad(neptune[0][0]), neptune[0][1], marker='o', label='neptune', ms=5, mfc='deepskyblue')
    ax1.annotate('♆', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(neptune[0][0]), neptune[0][1]), fontsize=20, color='aliceblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(8)

    ax1.plot(np.deg2rad(pluto[0][0]), pluto[0][1], 'o:k', mfc='red', label='pluto', ms=5)
    ax1.annotate('♇', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(pluto[0][0]), pluto[0][1]), fontsize=20, color='aliceblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(9)

    swe.close()
    plt.grid()

    chart_path = f'/astro_app/astroknow/astroplan/static/plots/{filename}.png'
    directory = os.path.dirname(chart_path)

    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    plt.savefig(chart_path)





def draw_zodiac_df_color(list_name):
    for t in list_name:
        zodiac_sector = circos.get_sector(t[0])
        zodiac_track = zodiac_sector.add_track((80, 100))
        zodiac_track.axis(fc=t[1], ec=t[2], lw=2)
        zodiac_track.text(f'{t[0]}', size=27, color=t[3])

    fig = circos.plotfig()
    fig.patch.set_alpha(0.0)
    fig.savefig('tr_for7.png')



def build_aspects(aspect_data, ax_name, planet_data):
    aspect_table_s = None
    aspect_table_ops = None
    aspect_table_c = None
    aspect_table_t = None

    for value in range(len(aspect_data) - 1):
                 for pl in range(0, 10):
                     aspect = abs(round(aspect_data[pl][4]) - round(aspect_data[value + 1][4]))

                     if aspect in trine and aspect_data[pl][4] != aspect_data[value + 1][4]:
                         pl_one = np.array(
                             [np.deg2rad(aspect_data[pl][4]), np.deg2rad(aspect_data[value + 1][4])])
                         pl_two = np.array(
                             [np.deg2rad(aspect_data[pl][5]), np.deg2rad(aspect_data[value + 1][5])])

                         if 119 < aspect < 121:
                             ax_name.plot(pl_one, pl_two, color='#01ff00', lw=3.5)
                         elif 122 < aspect < 123:
                             ax_name.plot(pl_one, pl_two, color='#01ff00', lw=2.0)
                         elif 123 < aspect < 125:
                             ax_name.plot(pl_one, pl_two, color='#01ff00', lw=1.8)
                         else:
                             ax_name.plot(pl_one, pl_two, color='#01ff00', lw=1.0)

                         aspected_planet_t.append(aspect_data[pl][0])
                         t_angle.append(f'{aspect}°')
                         trines.append(aspect_data[value + 1][0])
                         aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                     if aspect in opposition and aspect_data[pl][4] != aspect_data[value + 1][4]:
                         pl_one = np.array(
                             [np.deg2rad(aspect_data[pl][4]), np.deg2rad(aspect_data[value + 1][4])])
                         pl_two = np.array(
                             [np.deg2rad(aspect_data[pl][5]), np.deg2rad(aspect_data[value + 1][5])])
                         if aspect == range(179, 181):
                             ax_name.plot(pl_one, pl_two, color='#0400ff', lw=3.5)
                         elif aspect == range(181, 184):
                             ax_name.plot(pl_one, pl_two, color='#0400ff', lw=2.0)
                         elif aspect == range(183, 186):
                             ax_name.plot(pl_one, pl_two, color='#0400ff', lw=1.8)
                         elif aspect == 177:
                             ax_name.plot(pl_one, pl_two, color='red', lw=1.0)

                         aspected_planet_op.append(aspect_data[pl][0])
                         op_angle.append(f'{aspect}°')
                         oppositions.append(aspect_data[value + 1][0])
                         aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                     if aspect in square and aspect_data[pl][4] != aspect_data[value + 1][4]:
                         pl_one = np.array(
                             [np.deg2rad(aspect_data[pl][4]), np.deg2rad(aspect_data[value + 1][4])])
                         pl_two = np.array(
                             [np.deg2rad(aspect_data[pl][5]), np.deg2rad(aspect_data[value + 1][5])])

                         if 89 < aspect < 91:
                             ax_name.plot(pl_one, pl_two, color='#e20000', lw=3.5)
                         elif 91 < aspect < 93:
                             ax_name.plot(pl_one, pl_two, color='#e20000', lw=2.3)
                         elif 93 < aspect < 95:
                             ax_name.plot(pl_one, pl_two, color='#e20000', lw=1.8)
                         else:
                             ax_name.plot(pl_one, pl_two, color='#e20000', lw=1.0)

                         aspected_planet_s.append(aspect_data[pl][0])
                         sq_angle.append(f'{aspect}°')
                         squares.append(aspect_data[value + 1][0])
                         aspect_table_s = zip(aspected_planet_s, sq_angle, squares)

                     if aspect in conjunction and aspect_data[pl][4] != aspect_data[value + 1][4]:
                         pl_one = np.array(
                             [np.deg2rad(aspect_data[pl][4]), np.deg2rad(aspect_data[value + 1][4])])
                         pl_two = np.array(
                             [np.deg2rad(aspect_data[pl][5]), np.deg2rad(aspect_data[value + 1][5])])
                         ax_name.plot(pl_one, pl_two, color='green', lw=0.8)

                         aspected_planet_c.append(aspect_data[pl][0])
                         c_angle.append(f'{aspect}°')
                         conjunctions.append(aspect_data[value + 1][0])
                         aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

                     ax_name.plot(np.deg2rad(aspect_data[pl][4]), aspect_data[pl][5], 'o',
                                    mfc=planet_data[swe.get_planet_name(pl)][1],
                                    ms=planet_data[swe.get_planet_name(pl)][2])

                     if aspect_data[pl][4] == 0 or aspect_data[pl][4] < 45:
                         ax_name.annotate(f'{planet_data[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(-20, -8),
                                            xycoords='data',
                                            xy=(np.deg2rad(aspect_data[pl][4]), aspect_data[pl][5]),
                                            fontsize=planet_data[swe.get_planet_name(pl)][3],
                                            color='aliceblue',
                                            arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                     elif 45 < aspect_data[pl][4] < 135:
                         ax_name.annotate(f'{planet_data[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(-5, -25),
                                            xycoords='data',
                                            xy=(np.deg2rad(aspect_data[pl][4]), aspect_data[pl][5]),
                                            fontsize=planet_data[swe.get_planet_name(pl)][3],
                                            color='aliceblue',
                                            arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                     elif 135 < aspect_data[pl][4] < 180:
                         ax_name.annotate(f'{planet_data[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(3, 13),
                                            xycoords='data',
                                            xy=(np.deg2rad(aspect_data[pl][4]), aspect_data[pl][5]),
                                            fontsize=planet_data[swe.get_planet_name(pl)][3],
                                            color='aliceblue',
                                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                     elif 180 < aspect_data[pl][4] < 225:
                         ax_name.annotate(f'{planet_data[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(0, 25),
                                            xycoords='data',
                                            xy=(np.deg2rad(aspect_data[pl][4]), aspect_data[pl][5]),
                                            fontsize=planet_data[swe.get_planet_name(pl)][3],
                                            color='aliceblue',
                                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                     elif 225 < aspect_data[pl][4] < 270:
                         ax_name.annotate(f'{planet_data[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(-25, -5),
                                            xycoords='data',
                                            xy=(np.deg2rad(aspect_data[pl][4]), aspect_data[pl][5]),
                                            fontsize=planet_data[swe.get_planet_name(pl)][3],
                                            color='aliceblue',
                                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                     elif 270 < aspect_data[pl][4] < 315:
                         ax_name.annotate(f'{planet_data[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(-25, -5),
                                            xycoords='data',
                                            xy=(np.deg2rad(aspect_data[pl][4]), aspect_data[pl][5]),
                                            fontsize=planet_data[swe.get_planet_name(pl)][3],
                                            color='aliceblue',
                                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                     elif 315 < aspect_data[pl][4] < 360:
                         if aspect_data[pl][0] == '♆':
                             ax_name.annotate(f'{planet_data[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                                xytext=(3, -10),
                                                xycoords='data',
                                                xy=(np.deg2rad(aspect_data[pl][4]), aspect_data[pl][5]),
                                                fontsize=planet_data[swe.get_planet_name(pl)][3],
                                                color='aliceblue',
                                                arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                         else:
                             ax_name.annotate(f'{planet_data[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                                xytext=(-25, -5),
                                                xycoords='data',
                                                xy=(np.deg2rad(aspect_data[pl][4]), aspect_data[pl][5]),
                                                fontsize=planet_data[swe.get_planet_name(pl)][3],
                                                color='aliceblue',
                                                arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
    return aspect_table_s,aspect_table_ops, aspect_table_t, aspect_table_c




marker_size = 9
font_size = 27

PLANET_METADATA = {

    0: ['☼', 'yellow', marker_size, font_size],
    1: ['☾', 'blue', marker_size, font_size],
    2: ['☿', 'grey', marker_size, font_size],
    3: ['♀', 'sienna', marker_size, font_size],
    4: ['♂', 'red', marker_size, font_size],
    5: ['♃', 'teal', marker_size, font_size],
    6: ['♄', 'slategrey', marker_size, font_size],
    7: ['♅', 'chartreuse', marker_size, font_size],
    8: ['♆', 'indigo', marker_size, font_size],
    9: ['♇', 'darkmagenta', marker_size, font_size]
}


def get_planet_data(jd, ch_mode):

    pd = {}
    chart_mode = int(ch_mode)

    for pl_number, meta in PLANET_METADATA.items():

        planet_name = swe.get_planet_name(pl_number)

        ecliptic_latitude = swe.calc_ut(jd, pl_number, chart_mode)[0][0]
        ecliptic_longitude = swe.calc_ut(jd, pl_number, chart_mode)[0][1]

        pd[planet_name] = [meta[0], meta[1], meta[2], meta[3],ecliptic_latitude, ecliptic_longitude]

    return pd


def draw_chart(fig_name, planet_ax = None, house_ax=None, transit_ax=None, tr_house_ax=None):

    px = 1 / plt.rcParams['figure.dpi']
    img = mpi.imread('astroplan/static/images/zr_final_dp_pp.png')
    fig_name  = plt.figure(figsize=(870 * px, 870 * px))
    fig_name.patch.set_alpha(0.0)
    ax_img = fig_name.add_axes((0.05, 0.05, 0.9, 0.9))
    ax_img.imshow(img)
    ax_img.axis('off')

    if planet_ax is not None:

        planet_ax = fig_name.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
        planet_ax.set_rlim(-130, 100)
        planet_ax.set_theta_direction('counterclockwise')
        planet_ax.set_rticks([])
        planet_ax.set_axis_off()
        planet_ax.set_thetagrids(range(0, 360, 30))

    if house_ax is not None:

        house_ax = fig_name.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        house_ax.patch.set_alpha(0.0)
        house_ax.set_rlim(-130, 100)
        house_ax.set_theta_direction(1)
        house_ax.set_rticks([])
        house_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1,
                                 labelfontfamily='monospace',
                                 labelcolor='aliceblue')
    if transit_ax is not None:
        transit_ax = fig_name.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        transit_ax.patch.set_alpha(0.0)
        transit_ax.set_rlim(-130, 100)
        transit_ax.set_theta_direction(1)
        transit_ax.set_rticks([])
        transit_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1,
                             labelfontfamily='monospace',
                             labelcolor='aliceblue')

    if tr_house_ax is not None:
        tr_house_ax = fig_name.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        tr_house_ax.patch.set_alpha(0.0)
        tr_house_ax.set_rlim(-130, 100)
        tr_house_ax.set_theta_direction(1)
        tr_house_ax.set_rticks([])
        tr_house_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1,
                               labelfontfamily='monospace',
                               labelcolor='aliceblue')

    return fig_name, planet_ax, house_ax, transit_ax, tr_house_ax










jd = jl.to_jd(dt.now())
planet_data = get_planet_data(jd, swe.FLG_SIDEREAL)
planet_data_val = planet_data.values()
print(list(planet_data_val))
print(swe.calc_ut(jd, 0, swe.FLG_SIDEREAL)[0][0] )
print(swe.calc_ut(jd, 0, swe.FLG_TROPICAL)[0][0] )
print(swe.calc_ut(jd, 0,  swe.FLG_HELCTR)[0][0])





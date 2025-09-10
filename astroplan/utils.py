import matplotlib.pyplot as plt
import matplotlib.image as mpi
from pycirclize import circos
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



flags = swe.FLG_SIDEREAL


# def get_graph():
#     buffer = BytesIO()
#     plt.savefig('astroplan/static/plots/')
#     buffer.seek(0)
#     image_png = buffer.getvalue()
#     graph = base64.b64encode(image_png)
#     graph = graph.decode('utf-8')
#     buffer.close()
#     return graph


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

    img = mpi.imread('astroplan/static/images/tr_zr_1.png')
    fig = plt.figure(figsize=(870 * px, 870 * px))
    # fig.suptitle("Today chart", size=17, color='aliceblue')
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
                 xy=(np.deg2rad(venus[0][0]), venus[0][1]), fontsize=20, color='blueviolet',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(3)

    ax1.plot(np.deg2rad(moon[0][0]), moon[0][1], marker='o', label='moon', mfc='forestgreen', ms=5)
    ax1.annotate('☾', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(moon[0][0]), moon[0][1]), fontsize=20, color='slateblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(1)

    ax1.plot(np.deg2rad(sun[0][0]), sun[0][1], marker='o', label='sun', ms=8, mfc='gold')
    ax1.annotate('☼', textcoords='offset points', xytext=(20, 5), xycoords='data',
                 xy=(np.deg2rad(sun[0][0]), sun[0][1]), fontsize=25, color='midnightblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(0)

    ax1.plot(np.deg2rad(mercury[0][0]), mercury[0][1], 'o:b', label='merc', ms=5)
    ax1.annotate('☿', textcoords='offset points', xytext=(20, 5), xycoords='data',
                 xy=(np.deg2rad(mercury[0][0]), mercury[0][1]), fontsize=20, color='orange',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(2)

    ax1.plot(np.deg2rad(mars[0][0]), mars[0][1], marker='o', label='mars', ms=5, mfc='red')
    ax1.annotate('♂', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(mars[0][0]), mars[0][1]), fontsize=20, color='slateblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(4)

    ax1.plot(np.deg2rad(jupiter[0][0]), jupiter[0][1], 'o', label='jupiter', ms=7, mfc='steelblue')
    ax1.annotate('♃', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(jupiter[0][0]), jupiter[0][1]), fontsize=20, color='slateblue',
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
                 xy=(np.deg2rad(uranus[0][0]), uranus[0][1]), fontsize=20, color='rebeccapurple',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(7)

    ax1.plot(np.deg2rad(neptune[0][0]), neptune[0][1], marker='o', label='neptune', ms=5, mfc='deepskyblue')
    ax1.annotate('♆', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(neptune[0][0]), neptune[0][1]), fontsize=20, color='indigo',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(8)

    ax1.plot(np.deg2rad(pluto[0][0]), pluto[0][1], 'o:k', mfc='red', label='pluto', ms=5)
    ax1.annotate('♇', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(pluto[0][0]), pluto[0][1]), fontsize=20, color='darkgoldenrod',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(9)

    swe.close()
    plt.grid()

    plt.savefig(f'/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/{filename}.png')





def draw_zodiac_df_color(list_name):
    for t in list_name:
        zodiac_sector = circos.get_sector(t[0])
        zodiac_track = zodiac_sector.add_track((80, 100))
        zodiac_track.axis(fc=t[1], ec=t[2], lw=2)
        zodiac_track.text(f'{t[0]}', size=27, color=t[3])

    fig = circos.plotfig()
    fig.patch.set_alpha(0.0)
    fig.savefig('tr_for7.png')








# now=dt.now()
# def process_time(timestamp):
#     jd = jl.to_jd(timestamp)
#
#     return jd


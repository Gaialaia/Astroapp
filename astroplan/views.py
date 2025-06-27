from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

import matplotlib.pyplot as plt

import numpy as np

from datetime import datetime as dt

import swisseph as swe

import julian as jl
from django.urls import reverse

from geopy.geocoders import Nominatim
from pytz import timezone

from .models import Chart
from .forms import ChartForm


from timezonefinder import TimezoneFinder


swe.set_ephe_path('/home/gaia/Документы/eph files')

now = dt.now(tz=timezone('Asia/Yekaterinburg'))
#
date = dt(1986, 2,17, 22,20)
# jd_date = jl.to_jd(date,fmt='jd')

# jd = jl.to_jd(now, fmt='jd')
flags =  swe.FLG_SIDEREAL

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

planet_symbols = ['☼', '☾', '☿', '♀', '♂', '♃', '♄', '♅', '♆', '♇']

aspect_table_squares = zip(aspected_planet, sq_angle, sqaures)
aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)
aspect_table_t = zip(aspected_planet_t, t_angle, trines)
aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)
sign = ''
signs = []
pl_names_and_sym = {name: symbol for name, symbol in zip(planet_names, planet_symbols)}
tf = TimezoneFinder()
loc = Nominatim(user_agent="GetLoc")


# loc = Nominatim(user_agent="GetLoc")
# getLoc = loc.geocode("Ufa, Russia", timeout=1000000)
# # houses = swe.houses(jd, getLoc.latitude, getLoc.longitude, b'P')
# houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'P', flags=swe.FLG_SIDEREAL)

px = 1 / plt.rcParams['figure.dpi']

def show_td_chart(request):

    fig = plt.figure(figsize=(870 * px, 870 * px))
    fig.patch.set_alpha(0.0)
    fig.suptitle(f'Planet chart today,{now.strftime('%B, %d, %H:%M')}', size=17)

    ax1 = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot

    house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
    house_ax.patch.set_alpha(0.0)

    ax1.set_rlim(-130, 100)
    ax1.set_theta_direction('counterclockwise')
    ax1.set_rticks([])
    ax1.set_axis_off()  # 'theta ax' is off and grid off
    ax1.set_thetagrids(range(0, 360, 30))

    jd = jl.to_jd(dt.now(tz=timezone('Asia/Yekaterinburg')), fmt='jd')

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

    planet_list = [sun, moon, mercury, venus, mars, jupiter,
                   saturn, uranus, neptune, pluto]

    names_and_coords = list(zip(planet_names, planet_list))
         ##########################
    # r_deg = [round(p[0][0], 2) for p in planet_list]
    # conv_deg = [str(n).replace('.', '°').replace(',', '′,') for n in r_deg]
    # thirty_r_deg = [round(p[0][0], 2) % 30 for p in planet_list]  # convert from start point 360 to 30X12
    # r_result = [round(n, 2) for n in thirty_r_deg]  # round divided into 30 result
    # conv_r_result = [str(n).replace('.', '°').replace(',', '′,') for n in r_result]
    # deg_intervals = [round(d[0][0]) for d in planet_list]
            ###############################

    # for table with houses
    house_names = ['8', '9', 'MC', '11', '12', 'ASC', '2', '3', 'IC', '5', '6', 'DSC']
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode("Ufa, Russia", timeout=7000)
    houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'R', flags=swe.FLG_SIDEREAL)
    house_table = zip(house_names, houses[0])

    # hr_deg = [round(p, 2) for p in houses[0]]
    # hr_deg_d = [round(p, 2) % 30 for p in houses[0]]
    # hr_result = [round(n, 2) for n in hr_deg_d]
    # conv_hr_result = [str(n).replace('.', '°').replace(',', '′,') for n in hr_result]
    # #
    # # deg_intervals = [round(d[0][0]) for d in planet_list]
    # for i in range(len(deg_intervals)):
    #     if deg_intervals[i] in range(300, 331):
    #         sign = '♒'
    #     if deg_intervals[i] in range(330, 361):
    #         sign = 'pisces'
    #     if deg_intervals[i] in range(0, 31):
    #         sign = 'aries'
    #     if deg_intervals[i] in range(30, 61):
    #         sign = '♉'
    #     if deg_intervals[i] in range(60, 91):
    #         sign = 'gemini'
    #     if deg_intervals[i] in range(90, 121):
    #         sign = 'cancer'
    #     if deg_intervals[i] in range(120, 151):
    #         sign = 'leo'
    #     if deg_intervals[i] in range(150, 181):
    #         sign = 'virgo'
    #     if deg_intervals[i] in range(180, 211):
    #         sign = '♎'
    #     if deg_intervals[i] in range(210, 241):
    #         sign = '♏'
    #     if deg_intervals[i] in range(240, 271):
    #         sign = '♐'
    #     if deg_intervals[i] in range(270, 301):
    #         sign = '♑'
    #     signs.append(sign)

    # planet_deg = zip(planet_symbols, signs, conv_r_result)
    # house_data = zip(house_names, conv_hr_result, sign)
    def set_signs(name_list, deg_list):
        round_deg = [round(d) for d in deg_list]  # rounded 360 degree list for setting signs
        for i in range(len(deg_list)):
            if round_deg[i] in range(300, 331):
                sign = '♒'
            if round_deg[i] in range(330, 361):
                sign = 'pisces'
            if round_deg[i] in range(0, 31):
                sign = 'aries'
            if round_deg[i] in range(30, 61):
                sign = '♉'
            if round_deg[i] in range(60, 91):
                sign = 'gemini'
            if round_deg[i] in range(90, 121):
                sign = 'cancer'
            if round_deg[i] in range(120, 151):
                sign = 'leo'
            if round_deg[i] in range(150, 181):
                sign = 'virgo'
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
        m = zip(name_list, deg_form, signs)
        return list(m)





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
                 xy=(np.deg2rad(sun[0][0]), sun[0][1]), fontsize=15, color='midnightblue',
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
                 xy=(np.deg2rad(pluto[0][0]), pluto[0][1]), fontsize=15, color='darkgoldenrod',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(9)
    swe.close()

    plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/now_chart.png')

    return render(request, 'planets.html',
                  context={'planet_data':set_signs(planet_names,[p[0][0] for p in planet_list]),
                           'house_data': set_signs(house_names, list(houses[0])),
                'ats': aspect_table_squares, 'ato': aspect_table_ops,
                'att': aspect_table_t, 'atc': aspect_table_c})



# def today_chart(request):
#
#     if request.method == 'POST':
#         users_date = request.POST.get('user_date')
#
#         jd = jl.to_jd(d, fmt='jd')
#         city = request.POST.get('city')
#         country = request.POST.get('country')
#         loc = Nominatim(user_agent="GetLoc")
#         loc_coords = loc.geocode(f"{city, country}", timeout=7000)
#         loc_tz = TimezoneFinder().timezone_at(lng=loc_coords.latitude, lat=loc_coords.longitude)
#
#         fig = plt.figure(figsize=(870 * px, 870 * px), facecolor='violet', edgecolor='black')
#         fig.suptitle(f'Planet chart today,{d.strftime('%B, %d, %H:%M')}', size=17)
#         fig.patch.set_alpha(0.0)
#
#         ax1 = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
#         # ax1.set_theta_offset()
#
#         ax1.set_rlim(-130, 100)
#         ax1.set_theta_direction('counterclockwise')
#         ax1.set_rticks([])
#         ax1.set_axis_off()  # 'theta ax' is off and grid off
#         ax1.set_thetagrids(range(0, 360, 30))
#
#         sun = swe.calc_ut(jd, 0, flags)
#         moon = swe.calc_ut(jd, 1, flags)
#
#         mercury = swe.calc_ut(jd, 2, flags)
#         venus = swe.calc_ut(jd, 3, flags)
#         mars = swe.calc_ut(jd, 4, flags)
#
#         jupiter = swe.calc_ut(jd, 5, flags)
#         saturn = swe.calc_ut(jd, 6, flags)
#
#         uranus = swe.calc_ut(jd, 7, flags)
#         neptune = swe.calc_ut(jd, 8, flags)
#         pluto = swe.calc_ut(jd, 9, flags)
#
#         planet_list = [sun, moon, mercury, venus, mars, jupiter,
#                        saturn, uranus, neptune, pluto]
#
#         names_and_coords = list(zip(planet_names, planet_list))
#
#         r_deg = [round(p[0][0], 2) for p in planet_list]
#         conv_deg = [str(n).replace('.', '°').replace(',', '′,') for n in r_deg]
#
#         thirty_r_deg = [round(p[0][0], 2) % 30 for p in planet_list]  # convert from start point 360 to 30X12
#         r_result = [round(n, 2) for n in thirty_r_deg]  # round divided into 30 result
#         conv_r_result = [str(n).replace('.', '°').replace(',', '′,') for n in r_result]
#
#         deg_intervals = [round(d[0][0]) for d in planet_list]
#
#         for i in range(len(deg_intervals)):
#             if deg_intervals[i] in range(300, 331):
#                 sign = '♒'
#             if deg_intervals[i] in range(330, 361):
#                 sign = 'pisces'
#             if deg_intervals[i] in range(0, 31):
#                 sign = 'aries'
#             if deg_intervals[i] in range(30, 61):
#                 sign = '♉'
#             if deg_intervals[i] in range(60, 91):
#                 sign = 'gemini'
#             if deg_intervals[i] in range(90, 121):
#                 sign = 'cancer'
#             if deg_intervals[i] in range(120, 151):
#                 sign = 'leo'
#             if deg_intervals[i] in range(150, 181):
#                 sign = 'virgo'
#             if deg_intervals[i] in range(180, 211):
#                 sign = '♎'
#             if deg_intervals[i] in range(210, 241):
#                 sign = '♏'
#             if deg_intervals[i] in range(240, 271):
#                 sign = '♐'
#             if deg_intervals[i] in range(270, 301):
#                 sign = '♑'
#             signs.append(sign)
#
#         planet_deg = zip(planet_symbols, signs, conv_r_result)
#
#         # for table with houses
#         house_names = ['8', '9', 'MC', '11', '12', 'ASC', '2', '3', 'IC', '5', '6', 'DSC']
#
#         def aspect(planet_number):
#             for i in range(len(names_and_coords) - 1):
#
#                 z = abs(round(names_and_coords[planet_number][1][0][0]) - round(names_and_coords[i + 1][1][0][0]))
#                 if z in square:
#                     p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
#                                    np.deg2rad(names_and_coords[i + 1][1][0][0])])
#                     p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
#                     ax1.plot(p1, p2, lw=0.5, color='firebrick')
#
#                     aspected_planet.append(names_and_coords[planet_number][0])
#                     sq_angle.append(f'{z}°')
#                     sqaures.append(names_and_coords[i + 1][0])
#                     aspect_table_squares = zip(aspected_planet, sq_angle, sqaures)
#
#                 if z in opposition:
#                     p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
#                                    np.deg2rad(names_and_coords[i + 1][1][0][0])])
#                     p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
#                     ax1.plot(p1, p2, lw=0.5, color='magenta')
#
#                     aspected_planet_op.append(names_and_coords[planet_number][0])
#                     op_angle.append(f'{z}°')
#                     oppositions.append(names_and_coords[i + 1][0])
#                     aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)
#
#                 if z in trine:
#                     p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
#                                    np.deg2rad(names_and_coords[i + 1][1][0][0])])
#                     p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
#                     ax1.plot(p1, p2, lw=0.8, color='lime')
#                     aspected_planet_t.append(names_and_coords[planet_number][0])
#                     t_angle.append(f'{z}°')
#                     trines.append(names_and_coords[i + 1][0])
#                     aspect_table_t = zip(aspected_planet_t, t_angle, trines)
#
#                 if z in conjunctions:
#                     p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
#                                    np.deg2rad(names_and_coords[i + 1][1][0][0])])
#                     p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
#                     ax1.plot(p1, p2, lw=0.8, color='lime')
#                     aspected_planet_c.append(names_and_coords[planet_number][0])
#                     c_angle.append(f'{z}°')
#                     conjunctions.append(names_and_coords[i + 1][0])
#                     aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)
#
#         ax1.plot(np.deg2rad(venus[0][0]), venus[0][1], marker='o', label='venus', ms=5, mfc='deeppink')
#         ax1.annotate('♀', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                      xy=(np.deg2rad(venus[0][0]), venus[0][1]), fontsize=15, color='blueviolet',
#                      arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#         aspect(3)
#
#         ax1.plot(np.deg2rad(moon[0][0]), moon[0][1], marker='o', label='moon', mfc='forestgreen', ms=5)
#         ax1.annotate('☾', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                      xy=(np.deg2rad(moon[0][0]), moon[0][1]), fontsize=15, color='slateblue',
#                      arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#         aspect(1)
#
#         ax1.plot(np.deg2rad(sun[0][0]), sun[0][1], marker='o', label='sun', ms=8, mfc='gold')
#         ax1.annotate('☼', textcoords='offset points', xytext=(20, 5), xycoords='data',
#                      xy=(np.deg2rad(sun[0][0]), sun[0][1]), fontsize=15, color='midnightblue',
#                      arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#         aspect(0)
#
#         ax1.plot(np.deg2rad(mercury[0][0]), mercury[0][1], 'o:b', label='merc', ms=5)
#         ax1.annotate('☿', textcoords='offset points', xytext=(20, 5), xycoords='data',
#                      xy=(np.deg2rad(mercury[0][0]), mercury[0][1]), fontsize=15, color='orange',
#                      arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#         aspect(2)
#
#         ax1.plot(np.deg2rad(mars[0][0]), mars[0][1], marker='o', label='mars', ms=5, mfc='red')
#         ax1.annotate('♂', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                      xy=(np.deg2rad(mars[0][0]), mars[0][1]), fontsize=15, color='slateblue',
#                      arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#         aspect(4)
#
#         ax1.plot(np.deg2rad(jupiter[0][0]), jupiter[0][1], 'o', label='jupiter', ms=7, mfc='steelblue')
#         ax1.annotate('♃', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                      xy=(np.deg2rad(jupiter[0][0]), jupiter[0][1]), fontsize=17, color='slateblue',
#                      arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#         aspect(5)
#
#         ax1.annotate(f'{round(jupiter[0][0])}°', textcoords='offset points', xytext=(-20, 5), xycoords='data',
#                      xy=(np.deg2rad(jupiter[0][0]), jupiter[0][1]), fontsize=8, color='navy',
#                      arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#         ax1.plot(np.deg2rad(saturn[0][0]), saturn[0][1], 'o:k', label='saturn', ms=6)
#         ax1.annotate('♄', textcoords='offset points', xytext=(20, -20), xycoords='data',
#                      xy=(np.deg2rad(saturn[0][0]), saturn[0][1]), fontsize=15,
#                      arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#         aspect(6)
#
#         ax1.plot(np.deg2rad(uranus[0][0]), uranus[0][1], marker='o', mfc='chartreuse', label='uranus', ms=6)
#         ax1.annotate('♅', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                      xy=(np.deg2rad(uranus[0][0]), uranus[0][1]), fontsize=15, color='rebeccapurple',
#                      arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#         aspect(7)
#
#         ax1.plot(np.deg2rad(neptune[0][0]), neptune[0][1], marker='o', label='neptune', ms=5, mfc='deepskyblue')
#         ax1.annotate('♆', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                      xy=(np.deg2rad(neptune[0][0]), neptune[0][1]), fontsize=20, color='indigo',
#                      arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#         aspect(8)
#
#         ax1.plot(np.deg2rad(pluto[0][0]), pluto[0][1], 'o:k', mfc='red', label='pluto', ms=5)
#         ax1.annotate('♇', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                      xy=(np.deg2rad(pluto[0][0]), pluto[0][1]), fontsize=15, color='darkgoldenrod',
#                      arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#         aspect(9)
#         swe.close()
#
#         plt.grid()
#         plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/chart_for_date.png')
#
#         return render(request, 'chart_form.html', context={'planet_deg': planet_deg,
#                                                                'ats': aspect_table_squares, 'ato': aspect_table_ops,
#                                                                'att': aspect_table_t, 'atc': aspect_table_c})
#     #
#     return HttpResponseRedirect(reverse('showed chart'))

def chart_form(request):

    chart_form = ChartForm(request.POST or None, request.FILES or None)

    if chart_form.is_valid():
        chart_form.save()
        messages.success(request, 'Data sent')

        chart = Chart.objects.last()
        getLoc = loc.geocode(f'{chart.city, chart.country}', timeout=7000)
        tz = tf.timezone_at(lng=getLoc.longitude, lat=getLoc.latitude)
        d = chart.chart_date
        # d = dt.strptime(chart.chart_date, '%Y-%m-%d %H:%m:%s')



        jd = jl.to_jd(d, fmt='jd')

        houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'R', flags=swe.FLG_SIDEREAL)


        fig = plt.figure(figsize=(870 * px, 870 * px))
        fig.patch.set_alpha(0.0)
        fig.suptitle(f'Planet for date ,{d.strftime('%B, %d, %H:%M')}', size=17)

        ax1 = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot

        house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        house_ax.patch.set_alpha(0.0)

        ax1.set_rlim(-130, 100)
        ax1.set_theta_direction('counterclockwise')
        ax1.set_rticks([])
        ax1.set_axis_off()  # 'theta ax' is off and grid off
        ax1.set_thetagrids(range(0, 360, 30))

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

        planet_list = [sun, moon, mercury, venus, mars, jupiter,
                       saturn, uranus, neptune, pluto]

        names_and_coords = list(zip(planet_names, planet_list))

        r_deg = [round(p[0][0], 2) for p in planet_list]
        conv_deg = [str(n).replace('.', '°').replace(',', '′,') for n in r_deg]

        thirty_r_deg = [round(p[0][0], 2) % 30 for p in planet_list]  # convert from start point 360 to 30X12
        r_result = [round(n, 2) for n in thirty_r_deg]  # round divided into 30 result
        conv_r_result = [str(n).replace('.', '°').replace(',', '′,') for n in r_result]

        deg_intervals = [round(d[0][0]) for d in planet_list]

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
                     xy=(np.deg2rad(sun[0][0]), sun[0][1]), fontsize=15, color='midnightblue',
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
                     xy=(np.deg2rad(pluto[0][0]), pluto[0][1]), fontsize=15, color='darkgoldenrod',
                     arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

        aspect(9)
        swe.close()

        plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/chart_for_date.png')

        return render(request, 'show_by_date.html', context={'planet_deg': planet_deg,
                                                        'ats': aspect_table_squares, 'ato': aspect_table_ops,
                                                        'att': aspect_table_t, 'atc': aspect_table_c})


    return render(request, 'chart_form.html', {'chart_form':chart_form})










# def build_transit_chart(request):
#
#     chart = build_plot(dt.now(),'now_chart')
#
#     if request.method == 'POST':
#         event_date = request.POST.get('event_date')
#         transit_date = request.POST.get('transit_date')
#         d_ev = dt.strptime(event_date, '%Y-%m-%dT%H:%M')
#         d_tr = dt.strptime(transit_date, '%Y-%m-%dT%H:%M')

        # event_city = request.POST.get('event_city')
        # transit_city = request.POST.get('transit_city')
        #
        #
        # event_country = request.POST.get('event_country')
        # transit_country = request.POST.get('transit_country')
        #
        # loc = Nominatim(user_agent="GetLoc")
        # loc_coords = loc.geocode(f"{event_city, event_country}", timeout=7000)
        # loc_tz = TimezoneFinder().timezone_at(lng=loc_coords.latitude, lat=loc_coords.longitude)
        #
        # loc = Nominatim(user_agent="GetLoc")
        # loc_coords_two = loc.geocode(f"{transit_city, transit_country}", timeout=7000)
        # loc_tz = TimezoneFinder().timezone_at(lng=loc_coords_two.latitude, lat=loc_coords_two.longitude)

    #
    #     event_chart = build_plot(event_date, 'event_chart')
    #     transit_chart = build_plot(transit_date, 'transit_chart')
    #
    #     return render(request, 'transit_chart.html', {'event_chart': event_chart,
    #                   'transit_chart': transit_chart, 'chart':chart})
    #
    # return render(request, 'transit_chart.html')




















# def show_chart_houses(request):
#
#     px = 1 / plt.rcParams['figure.dpi']
#     fig = plt.figure(figsize=(870 * px, 870 * px), facecolor='violet', edgecolor='black')
#     # fig.suptitle(f'Planet chart today,{now.strftime('%B, %d, %H:%M')}', size=17)
#     fig.patch.set_alpha(0.0)
#
#     ax1 = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
#     # ax1.set_theta_offset()
#
#     loc = Nominatim(user_agent="GetLoc")
#     getLoc = loc.geocode("Ufa, Russia", timeout=7000)
#     houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'R', flags=swe.FLG_SIDEREAL)
#
#     ax1.set_alpha(0.0)
#     ax1.set_rlim(-130, 100)
#     ax1.set_theta_direction(1)
#     ax1.set_rticks([])
#     # ax1.set_axis_off()  # 'theta ax' is off
#     ax1.set_thetagrids(houses[0], ['8', '9', 'MC', '11', '12', 'ASC', '2', '3', 'IC', '5', '6', 'DSC'])
#     ax1.tick_params(labelsize=20, grid_color='red', grid_linewidth=1, labelfontfamily='monospace')
#
#
#     # ax1.set_thetagrids(range(0,360,30))
#     ax1.set_theta_offset(np.pi)
#     ax1.grid(color= '#178270', linewidth=1)
#     ax1.set_alpha(0.0)
#
#     plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/house_chart.png')  # aplha setting isn't applied if a plot saved to jpg
#     # swe.close()
#     return render(request, 'house_chart.html',  context={'planet_deg':planet_deg,'cusps_deg':cusps_deg,
#                            'ats': aspect_table_squares,'ato': aspect_table_ops,
#                             'att': aspect_table_t, 'atc': aspect_table_c})
#
# def show_birth_chart(request):
#     sun = swe.calc_ut(jd_date, 0, flags)
#     moon = swe.calc_ut(jd_date, 1, flags)
#
#     mercury = swe.calc_ut(jd_date, 2, flags)
#     venus = swe.calc_ut(jd_date, 3, flags)
#     mars = swe.calc_ut(jd_date, 4, flags)
#
#     jupiter = swe.calc_ut(jd_date, 5, flags)
#     saturn = swe.calc_ut(jd_date, 6, flags)
#
#     uranus = swe.calc_ut(jd_date, 7, flags)
#     neptune = swe.calc_ut(jd_date, 8, flags)
#     pluto = swe.calc_ut(jd_date, 9, flags)
#
#     planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter',
#                     'Saturn', 'Uranus', 'Neptune', 'Pluto']
#     planet_list = [sun, moon, mercury, venus, mars, jupiter,
#                    saturn, uranus, neptune, pluto]
#
#     planet_symbols = ['☼', '☾', '☿', '♀', '♂', '♃', '♄', '♅', '♆', '♇']
#
#
#     pl_names_and_sym = {name: symbol for name, symbol in zip(planet_names, planet_symbols)}
#
#     r_deg = [round(p[0][0],2) for p in planet_list]
#     conv_deg = [str(n).replace('.', '°').replace(',', '′,') for n in r_deg]
#
#     thirty_r_deg = [round(p[0][0], 2) % 30 for p in planet_list]  # convert from start point 360 to 30X12
#     r_result = [round(n, 2) for n in thirty_r_deg]  # round divided into 30 result
#     conv_r_result = [str(n).replace('.', '°').replace(',', '′,') for n in r_result]
#
#     deg_intervals = [round(d[0][0]) for d in planet_list]
#     sign = ''
#     signs = []
#
#     for i in range(len(deg_intervals)):
#         if deg_intervals[i] in range(300, 331):
#             sign = '♒'
#         if deg_intervals[i] in range(330, 361):
#             sign = 'pisces'
#         if deg_intervals[i] in range(0, 31):
#             sign = 'aries'
#         if deg_intervals[i] in range(30, 61):
#             sign = '♉'
#         if deg_intervals[i] in range(60, 91):
#             sign = 'gemini'
#         if deg_intervals[i] in range(90, 121):
#             sign = 'cancer'
#         if deg_intervals[i] in range(120, 151):
#             sign = 'leo'
#         if deg_intervals[i] in range(150, 181):
#             sign = 'virgo'
#         if deg_intervals[i] in range(180, 211):
#             sign = '♎'
#         if deg_intervals[i] in range(210, 241):
#             sign = '♏'
#         if deg_intervals[i] in range(240, 271):
#             sign = '♐'
#         if deg_intervals[i] in range(270, 301):
#             sign = '♑'
#         signs.append(sign)
#
#     planet_deg = zip(planet_symbols, signs, conv_r_result)
#
#     # for table with houses
#     house_names = ['8', '9', 'MC', '11', '12', 'ASC', '2', '3', 'IC', '5', '6', 'DSC']
#
#
#     loc = Nominatim(user_agent="GetLoc")
#     getLoc = loc.geocode("Ufa, Russia", timeout=7000)
#     houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'R', flags=swe.FLG_SIDEREAL)
#
#     houses_list = [round(d, 2) for d in houses[0]]
#     conv_h_deg = [str(n).replace('.', '°').replace(',', '′,') for n in houses_list]
#     thirty_r_h_deg = [round(d, 2) % 30 for d in houses_list]  # convert from start point 360 to 30X12
#     h_r_result = [round(d, 2) for d in thirty_r_h_deg]  # round divided into 30 result
#     conv_h_r_result = [str(n).replace('.', '°').replace(',', '′,') for n in h_r_result]
#     cusps_deg = zip(conv_h_deg, house_names)
#
#
#     px = 1 / plt.rcParams['figure.dpi']
#     fig = plt.figure(figsize=(870 * px, 870 * px), facecolor='violet', edgecolor='black')
#     fig.suptitle(f'Birth chart,{date.strftime('%B, %d, %H:%M')}', size=17)
#     fig.patch.set_alpha(0.0)
#
#     left = 0.05
#     bottom = 0.05
#     width = 0.9
#     height = 0.9
#     ax1 = fig.add_axes([left, bottom, width, height], projection='polar')  # center plot
#     # ax1.set_theta_offset()
#
#     ax1.set_rlim(-100, 130)
#     ax1.set_theta_direction('counterclockwise')
#     ax1.set_rticks([])
#     ax1.set_axis_off()  # 'theta ax' is off
#     ax1.set_thetagrids(range(0, 360, 30))
#
#     opposition = np.arange(175.0, 185.0)
#     trine = np.arange(115.0, 125.0)
#     square = np.arange(85.0, 95.0)
#     conjunction = np.arange(0.0, 10.0)
#
#     sqaures = []
#     trines = []
#     oppositions = []
#     conjunctions = []
#
#     aspected_planet = []
#     aspected_planet_op = []
#     aspected_planet_t = []
#     aspected_planet_c = []
#     sq_angle = []
#     op_angle = []
#     t_angle = []
#     c_angle = []
#
#     names_and_coords = list(zip(planet_names, planet_list))
#     aspect_table_squares = zip(aspected_planet, sq_angle, sqaures)
#     aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)
#     aspect_table_t = zip(aspected_planet_t, t_angle, trines)
#     aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)
#
#     def aspect(planet_number):
#         for i in range(len(names_and_coords) - 1):
#
#             z = abs(round(names_and_coords[planet_number][1][0][0]) - round(names_and_coords[i + 1][1][0][0]))
#             if z in square:
#                 p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
#                                np.deg2rad(names_and_coords[i + 1][1][0][0])])
#                 p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
#                 ax1.plot(p1, p2, lw=0.5, color='firebrick')
#
#                 aspected_planet.append(names_and_coords[planet_number][0])
#                 sq_angle.append(f'{z}°')
#                 sqaures.append(names_and_coords[i+1][0])
#                 aspect_table_squares = zip(aspected_planet, sq_angle, sqaures)
#
#             if z in opposition:
#                 p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
#                                np.deg2rad(names_and_coords[i + 1][1][0][0])])
#                 p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
#                 ax1.plot(p1, p2, lw=0.5, color='magenta')
#
#                 aspected_planet_op.append(names_and_coords[planet_number][0])
#                 op_angle.append(f'{z}°')
#                 oppositions.append(names_and_coords[i + 1][0])
#                 aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)
#
#             if z in trine:
#                 p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
#                                np.deg2rad(names_and_coords[i + 1][1][0][0])])
#                 p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
#                 ax1.plot(p1, p2, lw=0.8, color='lime')
#                 aspected_planet_t.append(names_and_coords[planet_number][0])
#                 t_angle.append(f'{z}°')
#                 trines.append(names_and_coords[i + 1][0])
#                 aspect_table_t = zip(aspected_planet_t, t_angle, trines)
#
#             if z in conjunctions:
#                 p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
#                                np.deg2rad(names_and_coords[i + 1][1][0][0])])
#                 p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
#                 ax1.plot(p1, p2, lw=0.8, color='lime')
#                 aspected_planet_c.append(names_and_coords[planet_number][0])
#                 c_angle.append(f'{z}°')
#                 conjunctions.append(names_and_coords[i + 1][0])
#                 aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)
#
#     # planet_numbers = {0: 'Sun', 1: 'Moon', 2: 'Mercury', 3: 'Venus',
#     #                   4: 'Mars', 5: 'Jupiter', 6: 'Saturn', 7: 'Uranus',
#     #                   8: 'Neptune', 9:'Pluto'}
#     ax1.plot(np.deg2rad(planet_list[3][0][0]), planet_list[3][0][1], marker='o', label='venus', ms=5, mfc='deeppink')
#     ax1.annotate('♀', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                  xy=(np.deg2rad(planet_list[3][0][0]), planet_list[3][0][1]), fontsize=15, color='blueviolet',
#                  arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#     aspect(3)
#
#
#     ax1.plot(np.deg2rad(moon[0][0]), moon[0][1], marker='o', label='moon', mfc='forestgreen', ms=5)
#     ax1.annotate('☾', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                  xy=(np.deg2rad(moon[0][0]), moon[0][1]), fontsize=15, color='slateblue',
#                  arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#     aspect(2)
#
#     ax1.plot(np.deg2rad(sun[0][0]), sun[0][1], marker='o', label='sun', ms=8, mfc='gold')
#     ax1.annotate('☼', textcoords='offset points', xytext=(20, 5), xycoords='data',
#                  xy=(np.deg2rad(sun[0][0]), sun[0][1]), fontsize=15, color='midnightblue',
#                  arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#     aspect(0)
#
#     ax1.plot(np.deg2rad(mercury[0][0]), mercury[0][1], 'o:b', label='merc', ms=5)
#     ax1.annotate('☿', textcoords='offset points', xytext=(20, 5), xycoords='data',
#                  xy=(np.deg2rad(mercury[0][0]), mercury[0][1]), fontsize=15, color='orange',
#                  arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#     aspect(2)
#
#     ax1.plot(np.deg2rad(mars[0][0]), mars[0][1], marker='o', label='mars', ms=5, mfc='red')
#     ax1.annotate('♂', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                  xy=(np.deg2rad(mars[0][0]), mars[0][1]), fontsize=15, color='slateblue',
#                  arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#     aspect(4)
#
#     ax1.plot(np.deg2rad(jupiter[0][0]), jupiter[0][1], 'o', label='jupiter', ms=7, mfc='steelblue')
#     ax1.annotate('♃', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                  xy=(np.deg2rad(jupiter[0][0]), jupiter[0][1]), fontsize=17, color='slateblue',
#                  arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#
#     ax1.annotate(f'{round(jupiter[0][0])}°', textcoords='offset points', xytext=(-20, 5), xycoords='data',
#                  xy=(np.deg2rad(jupiter[0][0]), jupiter[0][1]), fontsize=8, color='navy',
#                  arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#     aspect(5)
#
#     ax1.plot(np.deg2rad(saturn[0][0]), saturn[0][1], 'o:k', label='saturn', ms=6)
#     ax1.annotate('♄', textcoords='offset points', xytext=(20, -20), xycoords='data',
#                  xy=(np.deg2rad(saturn[0][0]), saturn[0][1]), fontsize=15,
#                  arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#     aspect(6)
#
#     ax1.plot(np.deg2rad(uranus[0][0]), uranus[0][1], marker='o', mfc='chartreuse', label='uranus', ms=6)
#     ax1.annotate('♅', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                  xy=(np.deg2rad(uranus[0][0]), uranus[0][1]), fontsize=15, color='rebeccapurple',
#                  arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#     aspect(7)
#     ax1.plot(np.deg2rad(neptune[0][0]), neptune[0][1], marker='o', label='neptune', ms=5, mfc='deepskyblue')
#     ax1.annotate('♆', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                  xy=(np.deg2rad(neptune[0][0]), neptune[0][1]), fontsize=20, color='indigo',
#                  arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#     aspect(8)
#
#     ax1.plot(np.deg2rad(pluto[0][0]), pluto[0][1], 'o:k', mfc='red', label='pluto', ms=5)
#     ax1.annotate('♇', textcoords='offset points', xytext=(20, 3), xycoords='data',
#                  xy=(np.deg2rad(pluto[0][0]), pluto[0][1]), fontsize=15, color='darkgoldenrod',
#                  arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
#     aspect(9)
#
#     # x = np.array([np.deg2rad(mars[0][0]),np.deg2rad(venus[0][0])])
#     # y = np.array([mars[0][1], venus[0][1]])
#     # ax1.plot(x, y)
#     # ax1.plot([np.deg2rad(mars[0][1])])
#
#     ax1.grid(False)
#     plt.grid(False)
#
#     plt.savefig(
#         '/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/birth_plot.png')  # aplha setting isn't applied if a plot saved to jpg
#     swe.close()
#
#     return render(request, 'birth_chart.html',
#                   context={'planet_deg':planet_deg,'cusps_deg':cusps_deg,
#                            'ats': aspect_table_squares,'ato': aspect_table_ops,
#                             'att': aspect_table_t, 'atc': aspect_table_c})

# planet_numbers = {0:'Sun' , 1:'Moon', 2:'Mercury', 3:'Venus',
#                   4:'Mars',5:'Jupiter', 6:'Saturn', 7:'Uranus',
#                   8:'Neptune','Pluto':9}
#
# jd_date = jl.to_jd(date, fmt='jd')
# sun = swe.calc_ut(jd_date, 0, flags)
# moon = swe.calc_ut(jd_date, 1, flags)
#
# mercury = swe.calc_ut(jd_date, 2, flags)
# venus = swe.calc_ut(jd_date, 3, flags)
# mars = swe.calc_ut(jd_date, 4, flags)
#
# jupiter = swe.calc_ut(jd_date, 5, flags)
# saturn = swe.calc_ut(jd_date, 6, flags)
#
# uranus = swe.calc_ut(jd_date, 7, flags)
# neptune = swe.calc_ut(jd_date, 8, flags)
# pluto = swe.calc_ut(jd_date, 9, flags)
# #
# planet_list = [sun, moon, mercury, venus, mars, jupiter,
#                    saturn, uranus, neptune, pluto]
# planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter',
#                 'Saturn', 'Uranus', 'Neptune', 'Pluto']



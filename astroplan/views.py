import csv, os

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.defaultfilters import length

from pycirclize import Circos
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpi

import numpy as np

from datetime import datetime as dt

import swisseph as swe

import julian as jl

from geopy.geocoders import Nominatim
from pytz import timezone

from .models import Chart, TransitChart, ZodiacInColors, FullChart, TransitFullChart
from .forms import ChartForm, ZodiacInColorForm, TestForm, TransitForm, ColorfulZodiacForm, ColorForm, \
    OneColorZodiacRing
from .utils import build_plot, draw_zodiac_one_color
from timezonefinder import TimezoneFinder

swe.set_ephe_path('/home/gaia/Документы/eph files')

now = dt.now(tz=timezone('UTC'))
#
date = dt(1986, 2, 17, 22, 20)
# jd_date = jl.to_jd(date,fmt='jd')

# jd = jl.to_jd(now, fmt='jd')
flags = swe.FLG_SIDEREAL | swe.SIDM_LAHIRI

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

planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter',
                'Saturn', 'Uranus', 'Neptune', 'Pluto']

cur_tr_pn = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter',
             'Saturn', 'Uranus', 'Neptune', 'Pluto', 'tr_Sun',
             'tr_Moon', 'tr_Mercury', 'tr_Venus', 'tr_Mars', 'tr_Jupiter',
             'tr_Saturn', 'tr_Uranus', 'tr_Neptune', 'tr_Pluto']

tr_planet_names = ['tr_Sun', 'tr_Moon', 'tr_Mercury', 'tr_Venus', 'tr_Mars',
                   'tr_Jupiter', 'tr_Saturn', 'tr_Uranus', 'tr_Neptune', 'tr_Pluto']

cur_tr_coords = []

cur_tr_aspects = []
aspects = []

planet_symbols = ['☼', '☾', '☿', '♀', '♂', '♃', '♄', '♅', '♆', '♇']
# house_names = ['8', '9', 'MC', '11', '12', 'ASC', '2', '3', 'IC', '5', '6', 'DSC']

house_names = ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII']

sign = ''
signs = []

pl_names_and_sym = {name: symbol for name, symbol in zip(planet_names, planet_symbols)}
tf = TimezoneFinder()

loc = Nominatim(user_agent="GetLoc")

sectors = {"♊︎": 30, "♉︎": 30, "♈︎": 30,
           "♓︎": 30, "♒︎": 30, "♑︎": 30,
           "♐︎": 30, "♏︎": 30, "♎︎": 30,
           "♍︎": 30, "♌︎": 30, "♋︎": 30,
           }

circos = Circos(sectors)

px = 1 / plt.rcParams['figure.dpi']
matplotlib.rcParams['axes.edgecolor'] = 'aliceblue'


def show_td_chart(request):
    img = mpi.imread('astroplan/static/images/tr_zr_1.png')
    fig = plt.figure(figsize=(870 * px, 870 * px))
    fig.patch.set_alpha(0.0)
    ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
    ax_img.imshow(img)
    ax_img.axis('off')

    planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
    house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
    house_ax.patch.set_alpha(0.0)
    house_ax.set_facecolor('aliceblue')

    planet_ax.set_rlim(-130, 100)
    planet_ax.set_theta_direction('counterclockwise')
    planet_ax.set_rticks([])
    planet_ax.set_axis_off()  # 'theta ax' is off and grid off

    jd = jl.to_jd(dt.now(tz=timezone('UTC')), fmt='jd')

    getLoc = loc.geocode("Ufa, Russia", timeout=7000)
    houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'R', flags=swe.FLG_SIDEREAL)

    house_ax.set_rlim(-130, 100)
    house_ax.set_theta_direction(1)
    house_ax.set_rticks([])
    house_ax.set_thetagrids(houses[0], ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
    house_ax.tick_params(labelsize=20, grid_color='#815684', grid_linewidth=1, labelfontfamily='monospace',
                         labelcolor='aliceblue', pad=17.0)
    house_ax.set_theta_offset(np.pi)

    pd = {swe.get_planet_name(0): ['☼', 'yellow', 5, 25, swe.calc_ut(jd, 0, flags)[0][0],
                                   swe.calc_ut(jd, 0, flags)[0][1]],
          swe.get_planet_name(1): ['☾', 'blue', 5, 20, swe.calc_ut(jd, 1, flags)[0][0],
                                   swe.calc_ut(jd, 1, flags)[0][1]],
          swe.get_planet_name(2): ['☿', 'grey', 5, 23, swe.calc_ut(jd, 2, flags)[0][0],
                                   swe.calc_ut(jd, 2, flags)[0][1]],
          swe.get_planet_name(3): ['♀', 'sienna', 5, 22, swe.calc_ut(jd, 3, flags)[0][0],
                                   swe.calc_ut(jd, 3, flags)[0][1]],
          swe.get_planet_name(4): ['♂', 'red', 5, 20, swe.calc_ut(jd, 4, flags)[0][0], swe.calc_ut(jd, 4,
                                                                                                   flags)[0][1], -10],
          swe.get_planet_name(5): ['♃', 'teal', 5, 26, swe.calc_ut(jd, 5, flags)[0][0],
                                   swe.calc_ut(jd, 5, flags)[0][1], 0],
          swe.get_planet_name(6): ['♄', 'slategrey', 5, 25, swe.calc_ut(jd, 6, flags)[0][0],
                                   swe.calc_ut(jd, 6, flags)[0][1]],
          swe.get_planet_name(7): ['♅', 'chartreuse', 5, 22, swe.calc_ut(jd, 7, flags)[0][0],
                                   swe.calc_ut(jd, 7, flags)[0][1]],
          swe.get_planet_name(8): ['♆', 'indigo', 5, 22, swe.calc_ut(jd, 8, flags)[0][0],
                                   swe.calc_ut(jd, 8, flags)[0][1]],
          swe.get_planet_name(9): ['♇', 'darkmagenta', 5, 22, swe.calc_ut(jd, 9, flags)[0][0],
                                   swe.calc_ut(jd, 9, flags)[0][1]]
          }
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

    aspect_table_s = None
    aspect_table_ops = None
    aspect_table_c = None
    aspect_table_t = None

    aspected_planet_t.clear()
    aspected_planet_op.clear()
    aspected_planet_s.clear()
    aspected_planet_c.clear()

    c_angle.clear()
    t_angle.clear()
    sq_angle.clear()
    c_angle.clear()

    oppositions.clear()
    sqaures.clear()
    conjunctions.clear()
    trines.clear()

    for value in range(len(coords_value) - 1):
        for pl in range(0, 10):
            aspect = abs(round(coords_value[pl][4]) - round(coords_value[value + 1][4]))

            if aspect in trine and coords_value[pl][4] != coords_value[value + 1][4]:
                pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
                pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                if 119 < aspect < 121:
                    planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.5)
                elif 122 < aspect < 123:
                    planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.0)
                elif 123 < aspect < 125:
                    planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=0.8)
                else:
                    planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=0.6)

                aspected_planet_t.append(coords_value[pl][0])

                t_angle.append(f'{aspect}°')
                trines.append(coords_value[value + 1][0])
                aspect_table_t = zip(aspected_planet_t, t_angle, trines)

            if aspect in opposition and coords_value[pl][4] != coords_value[value + 1][4]:
                pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
                pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                if 179 < aspect < 181:
                    planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=1.5)
                elif 181 < aspect < 183:
                    planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=1.0)
                elif 183 < aspect < 185:
                    planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=0.8)
                else:
                    planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=0.6)

                aspected_planet_op.append(coords_value[pl][0])
                op_angle.append(f'{aspect}°')
                oppositions.append(coords_value[value + 1][0])
                aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

            if aspect in square and coords_value[pl][4] != coords_value[value + 1][4]:
                pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
                pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                if 89 < aspect < 91:
                    planet_ax.plot(pl_one, pl_two, color='#e20000', lw=1.5)
                elif 91 < aspect < 93:
                    planet_ax.plot(pl_one, pl_two, color='#e20000', lw=1.0)
                elif 93 < aspect < 95:
                    planet_ax.plot(pl_one, pl_two, color='#e20000', lw=0.8)
                else:
                    planet_ax.plot(pl_one, pl_two, color='#e20000', lw=0.6)

                aspected_planet_s.append(coords_value[pl][0])
                sq_angle.append(f'{aspect}°')
                sqaures.append(coords_value[value + 1][0])
                aspect_table_s = zip(aspected_planet_s, sq_angle, sqaures)

            if aspect in conjunction and coords_value[pl][4] != coords_value[value + 1][4]:
                pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
                pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                planet_ax.plot(pl_one, pl_two, color='#8aed07', lw=0.5)

                aspected_planet_c.append(coords_value[pl][0])
                c_angle.append(f'{aspect}°')
                conjunctions.append(coords_value[value + 1][0])
                aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

            planet_ax.plot(np.deg2rad(coords_value[pl][4]), coords_value[pl][5], 'o',
                           mfc=pd[swe.get_planet_name(pl)][1],
                           ms=pd[swe.get_planet_name(pl)][2])

            if coords_value[pl][4] == 0 or coords_value[pl][4] < 45:
                planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                   xytext=(-20, -8),
                                   xycoords='data',
                                   xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
                                   fontsize=pd[swe.get_planet_name(pl)][3],
                                   color='aliceblue',
                                   arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


            elif 45 < coords_value[pl][4] < 135:
                planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                   xytext=(-15, -25),
                                   xycoords='data',
                                   xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
                                   fontsize=pd[swe.get_planet_name(pl)][3],
                                   color='aliceblue',
                                   arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

            elif 135 < coords_value[pl][4] < 180:
                planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                   xytext=(3, 13),
                                   xycoords='data',
                                   xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
                                   fontsize=pd[swe.get_planet_name(pl)][3],
                                   color='aliceblue',
                                   arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

            elif 180 < coords_value[pl][4] < 225:
                planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                   xytext=(0, 25),
                                   xycoords='data',
                                   xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
                                   fontsize=pd[swe.get_planet_name(pl)][3],
                                   color='aliceblue',
                                   arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

            elif 225 < coords_value[pl][4] < 270:
                planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                   xytext=(-25, -5),
                                   xycoords='data',
                                   xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
                                   fontsize=pd[swe.get_planet_name(pl)][3],
                                   color='aliceblue',
                                   arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

            elif 270 < coords_value[pl][4] < 315:
                planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                   xytext=(-25, -5),
                                   xycoords='data',
                                   xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
                                   fontsize=pd[swe.get_planet_name(pl)][3],
                                   color='aliceblue',
                                   arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

            elif 315 < coords_value[pl][4] < 360:
                if coords_value[pl][0] == '♆':
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(3, -10),
                                       xycoords='data',
                                       xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                else:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-25, -5),
                                       xycoords='data',
                                       xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

    plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/now_chart.png')

    # chart_form = ChartForm(request.POST or None, request.FILES or None)

    chart_form = TestForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':

        if chart_form.is_valid():
            # chart_form.save()
            # chart = chart_form.save(commit=False)

            city = chart_form.cleaned_data['city']
            country = chart_form.cleaned_data['country']
            chart_dt = chart_form.cleaned_data['date']

            # chart = Chart.objects.last()
            get_loc = loc.geocode(f'{city, country}', timeout=7000)
            tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
            d = chart_dt
            # d = dt.strptime(chart.chart_date, '%Y-%m-%d %H:%m:%s')
            jd = jl.to_jd(d, fmt='jd')

            # chart.save()

            pd = {swe.get_planet_name(0): ['☼', 'yellow', 5, 17, swe.calc_ut(jd, 0, flags)[0][0],
                                           swe.calc_ut(jd, 0, flags)[0][1], 10],
                  swe.get_planet_name(1): ['☾', 'blue', 5, 17, swe.calc_ut(jd, 1, flags)[0][0],
                                           swe.calc_ut(jd, 1, flags)[0][1], -25],
                  swe.get_planet_name(2): ['☿', 'grey', 5, 17, swe.calc_ut(jd, 2, flags)[0][0],
                                           swe.calc_ut(jd, 1, flags)[0][1], -25],
                  swe.get_planet_name(3): ['♀', 'sienna', 5, 17, swe.calc_ut(jd, 3, flags)[0][0],
                                           swe.calc_ut(jd, 1, flags)[0][1], 25],
                  swe.get_planet_name(4): ['♂', 'red', 5, 17, swe.calc_ut(jd, 4, flags)[0][0],
                                           swe.calc_ut(jd, 1, flags)[0][1], -10],
                  swe.get_planet_name(5): ['♃', 'teal', 5, 17, swe.calc_ut(jd, 5, flags)[0][0],
                                           swe.calc_ut(jd, 1, flags)[0][1], 0],
                  swe.get_planet_name(6): ['♄', 'slategrey', 5, 17, swe.calc_ut(jd, 6, flags)[0][0],
                                           swe.calc_ut(jd, 1, flags)[0][1], -25],
                  swe.get_planet_name(7): ['♅', 'chartreuse', 5, 17, swe.calc_ut(jd, 7, flags)[0][0],
                                           swe.calc_ut(jd, 1, flags)[0][1], 0],
                  swe.get_planet_name(8): ['♆', 'indigo', 5, 17, swe.calc_ut(jd, 8, flags)[0][0],
                                           swe.calc_ut(jd, 1, flags)[0][1], 0],
                  swe.get_planet_name(9): ['♇', 'darkmagenta', 5, 17, swe.calc_ut(jd, 9, flags)[0][0],
                                           swe.calc_ut(jd, 1, flags)[0][1], 0]}

            img = mpi.imread('astroplan/static/images/tr_zr_1.png')
            fig_form = plt.figure(figsize=(870 * px, 870 * px))
            fig_form.patch.set_alpha(0.0)

            ax_img = fig_form.add_axes((0.05, 0.05, 0.9, 0.9))
            ax_img.imshow(img)
            ax_img.axis('off')

            planet_ax = fig_form.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot

            house_ax = fig_form.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            house_ax.patch.set_alpha(0.0)

            planet_ax.set_rlim(-130, 100)
            planet_ax.set_theta_direction('counterclockwise')
            planet_ax.set_rticks([])
            planet_ax.set_axis_off()
            planet_ax.set_thetagrids(range(0, 360, 30))

            house_ax.set_rlim(-130, 100)
            house_ax.set_theta_direction(1)
            house_ax.set_rticks([])
            house_ax.set_thetagrids(houses[0],
                                    ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
            house_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1, labelfontfamily='monospace',
                                 labelcolor='aliceblue')

            form_coords_value = list(pd.values())

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

            houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'R', flags=swe.FLG_SIDEREAL)

            aspect_table_s = None
            aspect_table_ops = None
            aspect_table_c = None
            aspect_table_t = None

            aspected_planet_t.clear()
            aspected_planet_op.clear()
            aspected_planet_s.clear()
            aspected_planet_c.clear()

            c_angle.clear()
            t_angle.clear()
            sq_angle.clear()
            c_angle.clear()

            oppositions.clear()
            sqaures.clear()
            conjunctions.clear()
            trines.clear()

            for value in range(len(form_coords_value) - 1):
                for pl in range(0, 10):
                    aspect = abs(round(form_coords_value[pl][4]) - round(form_coords_value[value + 1][4]))

                    if aspect in trine and form_coords_value[pl][4] != form_coords_value[value + 1][4]:
                        pl_one = np.array(
                            [np.deg2rad(form_coords_value[pl][4]), np.deg2rad(form_coords_value[value + 1][4])])
                        pl_two = np.array(
                            [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
                        planet_ax.plot(pl_one, pl_two, color='green', lw=0.5)

                        aspected_planet_t.append(form_coords_value[pl][0])
                        t_angle.append(f'{aspect}°')
                        trines.append(form_coords_value[value + 1][0])
                        aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                    if aspect in opposition and form_coords_value[pl][4] != form_coords_value[value + 1][4]:
                        pl_one = np.array(
                            [np.deg2rad(form_coords_value[pl][4]), np.deg2rad(form_coords_value[value + 1][4])])
                        pl_two = np.array(
                            [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
                        if aspect == range(179, 181):
                            planet_ax.plot(pl_one, pl_two, color='#0400ff', lw=1.5)
                        elif aspect == range(181, 184):
                            planet_ax.plot(pl_one, pl_two, color='#0400ff', lw=1.0)
                        elif aspect == range(183, 186):
                            planet_ax.plot(pl_one, pl_two, color='#0400ff', lw=1.0)
                        elif aspect == 177:
                            planet_ax.plot(pl_one, pl_two, color='red', lw=1.0)

                        planet_ax.plot(pl_one, pl_two, color='#ffd700', lw=0.8)

                        aspected_planet_op.append(form_coords_value[pl][0])
                        op_angle.append(f'{aspect}°')
                        oppositions.append(form_coords_value[value + 1][0])
                        aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                    if aspect in square and form_coords_value[pl][4] != form_coords_value[value + 1][4]:
                        pl_one = np.array(
                            [np.deg2rad(form_coords_value[pl][4]), np.deg2rad(form_coords_value[value + 1][4])])
                        pl_two = np.array(
                            [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
                        planet_ax.plot(pl_one, pl_two, color='#F1A019', lw=0.8)

                        aspected_planet_s.append(form_coords_value[pl][0])
                        sq_angle.append(f'{aspect}°')
                        sqaures.append(form_coords_value[value + 1][0])
                        aspect_table_s = zip(aspected_planet_s, sq_angle, sqaures)

                    if aspect in conjunction and form_coords_value[pl][4] != form_coords_value[value + 1][4]:
                        pl_one = np.array(
                            [np.deg2rad(form_coords_value[pl][4]), np.deg2rad(form_coords_value[value + 1][4])])
                        pl_two = np.array(
                            [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
                        planet_ax.plot(pl_one, pl_two, color='green', lw=0.8)

                        aspected_planet_c.append(form_coords_value[pl][0])
                        c_angle.append(f'{aspect}°')
                        conjunctions.append(form_coords_value[value + 1][0])
                        aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

                    planet_ax.plot(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5], 'o',
                                   mfc=pd[swe.get_planet_name(pl)][1],
                                   ms=pd[swe.get_planet_name(pl)][2])
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(pd[swe.get_planet_name(pl)][6], 0),
                                       xycoords='data',
                                       xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='darkgoldenrod',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

            plt.savefig('astroplan/static/plots/chart_for_date.png')

            return render(request, 'show_by_date.html', {'chart_form': chart_form,
                                                         'planet_data': set_signs(planet_names,
                                                                                  [p[4] for p in form_coords_value]),
                                                         'house_data': set_signs(house_names, list(houses[0])),
                                                         'ats': aspect_table_s, 'ato': aspect_table_ops,
                                                         'att': aspect_table_t, 'atc': aspect_table_c,
                                                         'date': d, 'city': city, 'country': country,
                                                         'latitude': get_loc.latitude, 'longitude': get_loc.longitude})

        else:
            chart_form = TestForm()

        swe.close()

    return render(request, 'main_astro.html',
                  context={'planet_data': set_signs(planet_names, [p[4] for p in coords_value]),
                           'house_data': set_signs(house_names, list(houses[0])),
                           'ats': aspect_table_s, 'ato': aspect_table_ops,
                           'att': aspect_table_t, 'atc': aspect_table_c,
                           'date': now.strftime('%B, %d, %H:%M'),
                           'chart_form': chart_form, 'planet_names': planet_names})


def build_transit_chart(request):
    chart_date = dt.now()
    chart = build_plot(chart_date, 'tr_chart_now')

    tr_form = TransitForm(request.POST or None, request.FILES or None)

    if tr_form.is_valid():

        event_date = tr_form.cleaned_data['event_date']
        event_city = tr_form.cleaned_data['event_city']
        event_country = tr_form.cleaned_data['event_country']

        transit_date = tr_form.cleaned_data['transit_date']
        transit_country = tr_form.cleaned_data['transit_city']
        transit_city = tr_form.cleaned_data['transit_country']

        get_loc = loc.geocode(f'{event_city, event_country}', timeout=7000)
        tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
        d = event_date

        tr_chart = TransitChart.objects.last()
        get_loc = loc.geocode(f'{transit_city, transit_country}', timeout=7000)
        tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
        tr_d = transit_date

        img = mpi.imread('astroplan/static/images/tr_zr_1.png')
        fig = plt.figure(figsize=(870 * px, 870 * px))
        fig.patch.set_alpha(0.0)

        ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
        ax_img.imshow(img)
        ax_img.axis('off')

        planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
        planet_ax.set_rlim(-130, 100)
        planet_ax.set_theta_direction('counterclockwise')
        planet_ax.set_rticks([])
        planet_ax.set_axis_off()

        house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        house_ax.patch.set_alpha(0.0)
        house_ax.set_rlim(-130, 100)
        house_ax.set_theta_direction(1)
        house_ax.set_rticks([])

        transit_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        transit_ax.set_rlim(-130, 100)
        transit_ax.set_theta_direction('counterclockwise')
        transit_ax.set_rticks([])
        transit_ax.set_axis_off()

        tr_house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        tr_house_ax.patch.set_alpha(0.0)
        tr_house_ax.set_rlim(-130, 100)
        tr_house_ax.set_theta_direction(1)
        tr_house_ax.set_rticks([])

        tr_cr_aspects_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        tr_cr_aspects_ax.patch.set_alpha(0.0)
        tr_cr_aspects_ax.set_rlim(-130, 100)
        tr_cr_aspects_ax.set_theta_direction(1)
        tr_cr_aspects_ax.set_rticks([])
        tr_cr_aspects_ax.set_axis_off()

        jd_ev = jl.to_jd(d, fmt='jd')

        pd_cr = {swe.get_planet_name(0): ['☼', 'yellow', 5, 17, swe.calc_ut(jd_ev, 0, flags)[0][0],
                                          swe.calc_ut(jd_ev, 0, flags)[0][1], 10],
                 swe.get_planet_name(1): ['☾', 'blue', 5, 17, swe.calc_ut(jd_ev, 1, flags)[0][0],
                                          swe.calc_ut(jd_ev, 1, flags)[0][1], -25],
                 swe.get_planet_name(2): ['☿', 'grey', 5, 17, swe.calc_ut(jd_ev, 2, flags)[0][0],
                                          swe.calc_ut(jd_ev, 1, flags)[0][1], -25],
                 swe.get_planet_name(3): ['♀', 'sienna', 5, 17, swe.calc_ut(jd_ev, 3, flags)[0][0],
                                          swe.calc_ut(jd_ev, 1, flags)[0][1], 25],
                 swe.get_planet_name(4): ['♂', 'red', 5, 17, swe.calc_ut(jd_ev, 4, flags)[0][0],
                                          swe.calc_ut(jd_ev, 1, flags)[0][1], -10],
                 swe.get_planet_name(5): ['♃', 'teal', 5, 17, swe.calc_ut(jd_ev, 5, flags)[0][0],
                                          swe.calc_ut(jd_ev, 1, flags)[0][1], 0],
                 swe.get_planet_name(6): ['♄', 'slategrey', 5, 17, swe.calc_ut(jd_ev, 6, flags)[0][0],
                                          swe.calc_ut(jd_ev, 1, flags)[0][1], -25],
                 swe.get_planet_name(7): ['♅', 'chartreuse', 5, 17, swe.calc_ut(jd_ev, 7, flags)[0][0],
                                          swe.calc_ut(jd_ev, 1, flags)[0][1], 0],
                 swe.get_planet_name(8): ['♆', 'indigo', 5, 17, swe.calc_ut(jd_ev, 8, flags)[0][0],
                                          swe.calc_ut(jd_ev, 1, flags)[0][1], 0],
                 swe.get_planet_name(9): ['♇', 'darkmagenta', 5, 17, swe.calc_ut(jd_ev, 9, flags)[0][0],
                                          swe.calc_ut(jd_ev, 1, flags)[0][1], 0]}

        form_coords_value = list(pd_cr.values())

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

        houses = swe.houses_ex(jd_ev, get_loc.latitude, get_loc.longitude, b'R', flags=swe.FLG_SIDEREAL)
        house_ax.set_thetagrids(houses[0],
                                ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
        house_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=0.5,
                             labelfontfamily='monospace', labelcolor='aliceblue')
        house_ax.set_theta_offset(np.pi)

        jd_tr = jl.to_jd(tr_d, fmt='jd')

        pd = {swe.get_planet_name(0): ['☼ᵀᴿ', 'yellow', 5, 17, swe.calc_ut(jd_tr, 0, flags)[0][0],
                                       swe.calc_ut(jd_tr, 0, flags)[0][1], 10],
              swe.get_planet_name(1): ['☾ᵀᴿ', 'blue', 5, 17, swe.calc_ut(jd_tr, 1, flags)[0][0],
                                       swe.calc_ut(jd_tr, 1, flags)[0][1], -25],
              swe.get_planet_name(2): ['☿ᵀᴿ', 'grey', 5, 17, swe.calc_ut(jd_tr, 2, flags)[0][0],
                                       swe.calc_ut(jd_tr, 1, flags)[0][1], -25],
              swe.get_planet_name(3): ['♀ᵀᴿ', 'sienna', 5, 17, swe.calc_ut(jd_tr, 3, flags)[0][0],
                                       swe.calc_ut(jd_tr, 1, flags)[0][1], 25],
              swe.get_planet_name(4): ['♂ᵀᴿ', 'red', 5, 17, swe.calc_ut(jd_tr, 4, flags)[0][0],
                                       swe.calc_ut(jd_tr, 1, flags)[0][1], -10],
              swe.get_planet_name(5): ['♃ᵀᴿ', 'teal', 5, 17, swe.calc_ut(jd_tr, 5, flags)[0][0],
                                       swe.calc_ut(jd_tr, 1, flags)[0][1], 0],
              swe.get_planet_name(6): ['♄ᵀᴿ', 'slategrey', 5, 17, swe.calc_ut(jd_tr, 6, flags)[0][0],
                                       swe.calc_ut(jd_tr, 1, flags)[0][1], -25],
              swe.get_planet_name(7): ['♅ᵀᴿ', 'chartreuse', 5, 17, swe.calc_ut(jd_tr, 7, flags)[0][0],
                                       swe.calc_ut(jd_tr, 1, flags)[0][1], 0],
              swe.get_planet_name(8): ['♆ᵀᴿ', 'indigo', 5, 17, swe.calc_ut(jd_tr, 8, flags)[0][0],
                                       swe.calc_ut(jd_tr, 1, flags)[0][1], 0],
              swe.get_planet_name(9): ['♇ᵀᴿ', 'darkmagenta', 5, 17, swe.calc_ut(jd_tr, 9, flags)[0][0],
                                       swe.calc_ut(jd_tr, 1, flags)[0][1], 0]}

        tr_form_coords_value = list(pd.values())

        tr_houses = swe.houses_ex(jd_tr, get_loc.latitude, get_loc.longitude, b'R', flags=swe.FLG_SIDEREAL)
        tr_house_ax.set_thetagrids(tr_houses[0],
                                   ['TR ASC', 'TR II', 'TR III', 'TR IC', 'TR V', 'TR VI', 'TR DSC',
                                    'TR VIII', 'TR IX', 'TR MC', 'TR XI', 'TR XII'])
        tr_house_ax.tick_params(labelsize=20, grid_color='chartreuse', grid_linewidth=0.5,
                                labelfontfamily='monospace', pad=23.0, labelcolor='chartreuse')
        tr_house_ax.set_theta_offset(np.pi)

        aspect_table_s = None
        aspect_table_ops = None
        aspect_table_c = None
        aspect_table_t = None
        both_chart_apd = []

        aspected_planet_t.clear()
        aspected_planet_op.clear()
        aspected_planet_s.clear()
        aspected_planet_c.clear()
        both_chart_apd.clear()

        c_angle.clear()
        t_angle.clear()
        sq_angle.clear()
        c_angle.clear()

        oppositions.clear()
        sqaures.clear()
        conjunctions.clear()
        trines.clear()

        both_chart_apd.extend(form_coords_value)
        both_chart_apd.extend(tr_form_coords_value)

        for value in range(len(both_chart_apd) - 1):
            for pl in range(0, 10):
                aspect = abs(round(both_chart_apd[pl][4]) - round(both_chart_apd[value + 1][4]))

                if aspect in trine and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                    pl_one = np.array(
                        [np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                    pl_two = np.array(
                        [np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])

                    if 119 < aspect < 121:
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.5)
                    elif 122 < aspect < 123:
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.0)
                    elif 123 < aspect < 125:
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#01ff00', lw=0.8)
                    else:
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#01ff00', lw=0.6)

                    aspected_planet_t.append(both_chart_apd[pl][0])
                    t_angle.append(f'{aspect}°')
                    trines.append(both_chart_apd[value + 1][0])
                    aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                if aspect in opposition and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                    pl_one = np.array([np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                    pl_two = np.array([np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])

                    if 179 < aspect < 181:
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#0900FF', lw=1.5)
                    elif 181 < aspect < 183:
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#0900FF', lw=1.0)
                    elif 183 < aspect < 185:
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#0900FF', lw=0.8)
                    else:
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#0900FF', lw=0.6)

                    aspected_planet_op.append(both_chart_apd[pl][0])
                    op_angle.append(f'{aspect}°')
                    oppositions.append(both_chart_apd[value + 1][0])
                    aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                if aspect in square and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                    pl_one = np.array(
                        [np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                    pl_two = np.array(
                        [np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])

                    if 89 < aspect < 91:
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#e20000', lw=1.5)
                    elif 91 < aspect < 93:
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#e20000', lw=1.0)
                    elif 93 < aspect < 95:
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#e20000', lw=0.8)
                    else:
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#e20000', lw=0.6)

                    aspected_planet_s.append(both_chart_apd[pl][0])
                    sq_angle.append(f'{aspect}°')
                    sqaures.append(both_chart_apd[value + 1][0])
                    aspect_table_s = zip(aspected_planet_s, sq_angle, sqaures)

                if aspect in conjunction and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                    pl_one = np.array(
                        [np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                    pl_two = np.array(
                        [np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])
                    tr_cr_aspects_ax.plot(pl_one, pl_two, color='fuchsia', lw=0.8)

                    aspected_planet_c.append(both_chart_apd[pl][0])
                    c_angle.append(f'{aspect}°')
                    conjunctions.append(both_chart_apd[value + 1][0])
                    aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

                planet_ax.plot(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5], 'o',
                               mfc=pd_cr[swe.get_planet_name(pl)][1],
                               ms=pd_cr[swe.get_planet_name(pl)][2])
                if form_coords_value[pl][4] == 0 or form_coords_value[pl][4] < 45:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-20, -8),
                                       xycoords='data',
                                       xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                elif 45 < form_coords_value[pl][4] < 135:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-15, -25),
                                       xycoords='data',
                                       xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                elif 135 < form_coords_value[pl][4] < 180:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(3, 13),
                                       xycoords='data',
                                       xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                elif 180 < form_coords_value[pl][4] < 225:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(0, 25),
                                       xycoords='data',
                                       xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                elif 225 < form_coords_value[pl][4] < 270:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-25, -5),
                                       xycoords='data',
                                       xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                elif 270 < form_coords_value[pl][4] < 315:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-25, -5),
                                       xycoords='data',
                                       xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                elif 315 < form_coords_value[pl][4] < 360:
                    if form_coords_value[pl][0] == '♆':
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(3, -10),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                    else:
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                transit_ax.plot(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5], 'o',
                                mfc=pd[swe.get_planet_name(pl)][1],
                                ms=pd[swe.get_planet_name(pl)][2])

                if tr_form_coords_value[pl][4] == 0 or tr_form_coords_value[pl][4] < 45:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-20, -8),
                                       xycoords='data',
                                       xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                elif 45 < tr_form_coords_value[pl][4] < 135:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-15, -25),
                                       xycoords='data',
                                       xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                elif 135 < tr_form_coords_value[pl][4] < 180:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(3, 13),
                                       xycoords='data',
                                       xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                elif 180 < tr_form_coords_value[pl][4] < 225:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(0, 25),
                                       xycoords='data',
                                       xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                elif 225 < tr_form_coords_value[pl][4] < 270:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-25, -5),
                                       xycoords='data',
                                       xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                elif 270 < tr_form_coords_value[pl][4] < 315:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-25, -5),
                                       xycoords='data',
                                       xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                elif 315 < tr_form_coords_value[pl][4] < 360:
                    if tr_form_coords_value[pl][0] == '♆':
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(3, -10),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                    else:
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

        plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/transit_chart.png')

        return render(request, 'transit_chart.html',
                      context={'planet_data': set_signs(planet_names, [p[4] for p in form_coords_value]),
                               'house_data': set_signs(house_names, list(houses[0])),
                               'ats': aspect_table_s, 'ato': aspect_table_ops,
                               'att': aspect_table_t, 'atc': aspect_table_c,
                               'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_form_coords_value]),
                               'tr_house_data': set_signs(house_names, list(tr_houses[0])), 'event_date': d,
                               'event_city': event_city, 'event_country': event_country,
                               'tr_date': tr_d, 'tr_city': transit_city, 'tr_country': transit_country,
                               'lat': get_loc.latitude, 'lng': get_loc.longitude})

    return render(request, 'transit_form.html',
                  context={'tr_form': tr_form, 'chart_date': date})


def chart_form(request):
    chart_form = ChartForm(request.POST or None, request.FILES or None)

    if chart_form.is_valid():
        chart_form.save()
        messages.success(request, 'Data sent')
        chart = Chart.objects.last()
        get_loc = loc.geocode(f'{chart.city, chart.country}', timeout=7000)
        tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
        d = chart.chart_date

        jd = jl.to_jd(d, fmt='jd')

        img = mpi.imread('astroplan/static/images/tr_zr_1.png')

        fig = plt.figure(figsize=(870 * px, 870 * px))
        fig.patch.set_alpha(0.0)
        fig.suptitle(f'Planet for date ,{d.strftime('%B, %d, %H:%M')}', size=17)

        ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
        ax_img.imshow(img)
        ax_img.axis('off')

        planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
        house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        house_ax.patch.set_alpha(0.0)
        house_ax.set_facecolor('aliceblue')

        planet_ax.set_rlim(-130, 100)
        planet_ax.set_theta_direction('counterclockwise')
        planet_ax.set_rticks([])
        planet_ax.set_axis_off()

        houses = swe.houses_ex(jd, get_loc.latitude, get_loc.longitude, b'R', flags=swe.FLG_SIDEREAL)

        house_ax.set_rlim(-130, 100)
        house_ax.set_theta_direction(1)
        house_ax.set_rticks([])
        house_ax.set_thetagrids(houses[0],
                                ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
        house_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1, labelfontfamily='monospace',
                             labelcolor='aliceblue')
        house_ax.set_theta_offset(np.pi)

        pd = {swe.get_planet_name(0): ['☼', 'yellow', 5, 17, swe.calc_ut(jd, 0, flags)[0][0],
                                       swe.calc_ut(jd, 0, flags)[0][1]],
              swe.get_planet_name(1): ['☾', 'blue', 5, 17, swe.calc_ut(jd, 1, flags)[0][0],
                                       swe.calc_ut(jd, 1, flags)[0][1]],
              swe.get_planet_name(2): ['☿', 'grey', 5, 17, swe.calc_ut(jd, 2, flags)[0][0],
                                       swe.calc_ut(jd, 1, flags)[0][1]],
              swe.get_planet_name(3): ['♀', 'sienna', 5, 17, swe.calc_ut(jd, 3, flags)[0][0],
                                       swe.calc_ut(jd, 1, flags)[0][1]],
              swe.get_planet_name(4): ['♂', 'red', 5, 17, swe.calc_ut(jd, 4, flags)[0][0],
                                       swe.calc_ut(jd, 1, flags)[0][1]],
              swe.get_planet_name(5): ['♃', 'teal', 5, 17, swe.calc_ut(jd, 5, flags)[0][0],
                                       swe.calc_ut(jd, 1, flags)[0][1]],
              swe.get_planet_name(6): ['♄', 'slategrey', 5, 17, swe.calc_ut(jd, 6, flags)[0][0],
                                       swe.calc_ut(jd, 1, flags)[0][1]],
              swe.get_planet_name(7): ['♅', 'chartreuse', 5, 17, swe.calc_ut(jd, 7, flags)[0][0],
                                       swe.calc_ut(jd, 1, flags)[0][1]],
              swe.get_planet_name(8): ['♆', 'indigo', 5, 17, swe.calc_ut(jd, 8, flags)[0][0],
                                       swe.calc_ut(jd, 1, flags)[0][1]],
              swe.get_planet_name(9): ['♇', 'darkmagenta', 5, 17, swe.calc_ut(jd, 9, flags)[0][0],
                                       swe.calc_ut(jd, 1, flags)[0][1]]
              }
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

        aspect_table_s = None
        aspect_table_ops = None
        aspect_table_c = None
        aspect_table_t = None

        aspected_planet_t.clear()
        aspected_planet_op.clear()
        aspected_planet_s.clear()
        aspected_planet_c.clear()

        c_angle.clear()
        t_angle.clear()
        sq_angle.clear()
        c_angle.clear()

        oppositions.clear()
        sqaures.clear()
        conjunctions.clear()
        trines.clear()

        for value in range(len(coords_value) - 1):
            for pl in range(0, 10):
                aspect = abs(round(coords_value[pl][4]) - round(coords_value[value + 1][4]))

                if aspect in trine and coords_value[pl][4] != coords_value[value + 1][4]:
                    pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
                    pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                    planet_ax.plot(pl_one, pl_two, color='green', lw=0.5)

                    aspected_planet_t.append(coords_value[pl][0])
                    t_angle.append(f'{aspect}°')
                    trines.append(coords_value[value + 1][0])
                    aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                if aspect in opposition and coords_value[pl][4] != coords_value[value + 1][4]:
                    pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
                    pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                    planet_ax.plot(pl_one, pl_two, color='pink', lw=0.5)

                    aspected_planet_op.append(coords_value[pl][0])
                    op_angle.append(f'{aspect}°')
                    oppositions.append(coords_value[value + 1][0])
                    aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                if aspect in square and coords_value[pl][4] != coords_value[value + 1][4]:
                    pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
                    pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                    planet_ax.plot(pl_one, pl_two, color='firebrick', lw=0.5)

                    aspected_planet_s.append(coords_value[pl][0])
                    sq_angle.append(f'{aspect}°')
                    sqaures.append(coords_value[value + 1][0])
                    aspect_table_s = zip(aspected_planet_s, sq_angle, sqaures)

                if aspect in conjunction and coords_value[pl][4] != coords_value[value + 1][4]:
                    pl_one = np.array([np.deg2rad(coords_value[pl][4]), np.deg2rad(coords_value[value + 1][4])])
                    pl_two = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                    planet_ax.plot(pl_one, pl_two, color='green', lw=0.5)

                    aspected_planet_c.append(coords_value[pl][0])
                    c_angle.append(f'{aspect}°')
                    conjunctions.append(coords_value[value + 1][0])
                    aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

                planet_ax.plot(np.deg2rad(coords_value[pl][4]), coords_value[pl][5], 'o',
                               mfc=pd[swe.get_planet_name(pl)][1],
                               ms=pd[swe.get_planet_name(pl)][2])
                planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points', xytext=(20, 3),
                                   xycoords='data',
                                   xy=(np.deg2rad(coords_value[pl][4]), coords_value[pl][5]),
                                   fontsize=pd[swe.get_planet_name(pl)][3],
                                   color='darkgoldenrod',
                                   arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

        plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/chart_for_date.png')
        swe.close()

        return render(request, 'show_by_date.html',
                      context={'planet_data': set_signs(planet_names, [p[4] for p in coords_value]),
                               'ats': aspect_table_s, 'ato': aspect_table_ops,
                               'att': aspect_table_t, 'atc': aspect_table_c,
                               'date': d})
    return render(request, 'chart_form.html', {'chart_form': chart_form})


def design_chart(request):
    zodiac_form = ColorfulZodiacForm(request.POST or None, request.FILES or None, initial={
        'cz_chart_date': now,
        'cz_chart_city': 'Ufa',
        'cz_chart_country': 'Russia',

        'track_aries_axis_fc': '#F30808',
        'track_aries_axis_ec': '#F6F3EC',
        'track_aries_axis_tc': '#006992',

        'track_leo_axis_fc': '#E74417',
        'track_leo_axis_ec': '#F3C442',
        'track_leo_axis_tc': '#1F98C7',

        'track_sag_axis_fc': '#8b0000',
        'track_sag_axis_ec': '#008040',
        'track_sag_axis_tc': '#008080',

        'track_aqua_axis_fc': '#7FFF00',
        'track_aqua_axis_ec': '#00ff01',
        'track_aqua_axis_tc': '#ff007f',

        'track_gemini_axis_fc': '#666666',
        'track_gemini_axis_ec': '#8D6E83',
        'track_gemini_axis_tc': '#ffd700',

        'track_libra_axis_fc': '#5441F8',
        'track_libra_axis_ec': '#f85441',
        'track_libra_axis_tc': '#e5f841',

        'track_scorpio_axis_fc': '#808000',
        'track_scorpio_axis_ec': '#804000',
        'track_scorpio_axis_tc': '#800080',

        'track_cancer_axis_fc': '#145314',
        'track_cancer_axis_ec': '#531453',
        'track_cancer_axis_tc': '#ffa500',

        'track_pisces_axis_fc': '#4B0082',
        'track_pisces_axis_ec': '#1E0034',
        'track_pisces_axis_tc': '#E2DBEA',

        'track_taurus_axis_fc': '#FF69B4',
        'track_taurus_axis_ec': '#993F6C',
        'track_taurus_axis_tc': '#90CC54',

        'track_virgo_axis_fc': '#CE954B',
        'track_virgo_axis_ec': '#a16e2c',
        'track_virgo_axis_tc': '#4B84CE',

        'track_capricorn_axis_fc': '#291F25',
        'track_capricorn_axis_ec': '#1F2529',
        'track_capricorn_axis_tc': '#c4bcc1',

        'degrees_track_ec': '#EDEBF4',
        'degrees_ticks_color': '#EDEBF4',

        'sun_symbol_c': '#ffe900',
        'sun_marker_c': '#f7f70e',
        'sun_symbol_s': 20,

        'mars_symbol_c': '#ff0000',
        'mars_marker_c': '#CC0000',
        'mars_symbol_s': 17,

        'jupiter_symbol_c': '#1C248E',
        'jup_marker_c': '#1C5D8E',
        'jup_symbol_s': 25,

        'mercury_symbol_c': '#3F3F3F',
        'mercury_marker_c': '#ffd700',
        'mercury_symbol_s': 15,

        'uranus_symbol_c': '#7FFF00',
        'uranus_marker_c': '#d921d9',
        'uranus_symbol_s': 17,

        'saturn_symbol_c': '#444444',
        'saturn_marker_c': '#aa3b3b',
        'saturn_symbol_s': 20,

        'moon_symbol_c': '#e94b63',
        'moon_marker_c': '#606060',
        'moon_symbol_s': 20,

        'neptune_symbol_c': '#4b0082',
        'neptune_marker_c': '#f98812',
        'neptune_symbol_s': 20,

        'pluto_symbol_c': '#3b1a1a',
        'pluto_marker_c': '#b10707',
        'pluto_symbol_s': 20,

        'venus_symbol_c': '#ed0c7d',
        'venus_marker_c': '#f780bb',
        'venus_symbol_s': 18,
    })

    if zodiac_form.is_valid():

        zf_city = zodiac_form.cleaned_data['cz_chart_city']
        zf_country = zodiac_form.cleaned_data['cz_chart_country']
        zf_date = zodiac_form.cleaned_data['cz_chart_date']

        # zodiac_form.save()
        # zf = ZodiacInColors.objects.last()
        get_loc = loc.geocode(f'{zf_city, zf_country}', timeout=7000)
        tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
        d = zf_date
        jd = jl.to_jd(d, fmt='jd')

        sector_aries = circos.get_sector("♈︎")
        # track_aries = sector_aries.add_track((95, 80))
        track_aries = sector_aries.add_track((70, 95))

        zf_ta_axis_fc = zodiac_form.cleaned_data['track_aries_axis_fc']
        zf_ta_axis_ec = zodiac_form.cleaned_data['track_aries_axis_ec']
        zf_ta_axis_tc = zodiac_form.cleaned_data['track_aries_axis_tc']
        track_aries.axis(fc=f'{zf_ta_axis_fc}', ec=zf_ta_axis_ec, lw=2)
        track_aries.text(f'{"♈︎"}', size=45, color=zf_ta_axis_tc)

        sector_leo = circos.get_sector("♌︎")
        # track_leo = sector_leo.add_track((95, 80))
        track_leo = sector_leo.add_track((70, 95))

        zf_tl_axis_fc = zodiac_form.cleaned_data['track_leo_axis_fc']
        zf_tl_axis_ec = zodiac_form.cleaned_data['track_leo_axis_ec']
        zf_tl_axis_tc = zodiac_form.cleaned_data['track_leo_axis_tc']
        track_leo.axis(fc=zf_tl_axis_fc, ec=zf_tl_axis_ec, lw=2)
        track_leo.text(f'{"♌︎"}', size=45, color=zf_tl_axis_tc)

        sector_sag = circos.get_sector("♐︎")
        # track_sag = sector_sag.add_track((95, 80))
        track_sag = sector_sag.add_track((70, 95))

        zf_tsag_axis_fc = zodiac_form.cleaned_data['track_sag_axis_fc']
        zf_tsag_axis_ec = zodiac_form.cleaned_data['track_sag_axis_ec']
        zf_tsag_axis_tc = zodiac_form.cleaned_data['track_sag_axis_tc']
        track_sag.axis(fc=zf_tsag_axis_fc, ec=zf_tsag_axis_ec, lw=2)
        track_sag.text(f'{"♐︎"}', size=45, color=zf_tsag_axis_tc)

        sector_aqua = circos.get_sector("♒︎")
        # track_aqua = sector_aqua.add_track((95, 80))
        track_aqua = sector_aqua.add_track((70, 95))

        zf_taq_axis_fc = zodiac_form.cleaned_data['track_aqua_axis_fc']
        zf_taq_axis_ec = zodiac_form.cleaned_data['track_aqua_axis_ec']
        zf_taq_axis_tc = zodiac_form.cleaned_data['track_aqua_axis_tc']
        track_aqua.axis(fc=zf_taq_axis_fc, ec=zf_taq_axis_ec, lw=2)
        track_aqua.text(f'{"♒︎"}', size=45, color=zf_taq_axis_tc)

        sector_gemini = circos.get_sector("♊︎")
        # track_gemini = sector_gemini.add_track((70, 95))
        track_gemini = sector_gemini.add_track((70, 95))

        zf_tgem_axis_fc = zodiac_form.cleaned_data['track_gemini_axis_fc']
        zf_tgem_axis_ec = zodiac_form.cleaned_data['track_gemini_axis_ec']
        zf_tgem_axis_tc = zodiac_form.cleaned_data['track_gemini_axis_tc']
        track_gemini.axis(fc=zf_tgem_axis_fc, ec=zf_tgem_axis_ec, lw=2)
        track_gemini.text(f'{"♊︎"}', size=45, color=zf_tgem_axis_tc)

        sector_libra = circos.get_sector("♎︎")
        # track_libra = sector_libra.add_track((95, 80))
        track_libra = sector_libra.add_track((70, 95))

        zf_tlib_axis_fc = zodiac_form.cleaned_data['track_libra_axis_fc']
        zf_tlib_axis_ec = zodiac_form.cleaned_data['track_libra_axis_ec']
        zf_tlib_axis_tc = zodiac_form.cleaned_data['track_libra_axis_tc']
        track_libra.axis(fc=zf_tlib_axis_fc, ec=zf_tlib_axis_ec, lw=2)
        track_libra.text(f'{"♎︎"}', size=45, color=zf_tlib_axis_tc)

        sector_taurus = circos.get_sector("♉︎")
        # track_taurus = sector_taurus.add_track((95, 80))
        track_taurus = sector_taurus.add_track((70, 95))

        zf_tau_axis_fc = zodiac_form.cleaned_data['track_taurus_axis_fc']
        zf_tau_axis_ec = zodiac_form.cleaned_data['track_taurus_axis_ec']
        zf_tau_axis_tc = zodiac_form.cleaned_data['track_taurus_axis_tc']
        track_taurus.axis(fc=zf_tau_axis_fc, ec=zf_tau_axis_ec, lw=2)
        track_taurus.text(f'{"♉︎"}', size=45, color=zf_tau_axis_tc, )

        sector_virgo = circos.get_sector("♍︎")
        # track_virgo = sector_virgo.add_track((95, 80))
        track_virgo = sector_virgo.add_track((70, 95))

        zf_tvirg_axis_fc = zodiac_form.cleaned_data['track_virgo_axis_fc']
        zf_tvirg_axis_ec = zodiac_form.cleaned_data['track_virgo_axis_ec']
        zf_tvirg_axis_tc = zodiac_form.cleaned_data['track_virgo_axis_tc']

        track_virgo.axis(fc=zf_tvirg_axis_fc, ec=zf_tvirg_axis_ec, lw=2)
        track_virgo.text(f'{"♍︎"}', size=45, color=zf_tvirg_axis_tc)

        sector_capricon = circos.get_sector("♑︎")
        # track_capricon = sector_capricon.add_track((95, 80))
        track_capricon = sector_capricon.add_track((70, 95))

        zf_tcapr_axis_fc = zodiac_form.cleaned_data['track_capricorn_axis_fc']
        zf_tcapr_axis_ec = zodiac_form.cleaned_data['track_capricorn_axis_ec']
        zf_tcapr_axis_tc = zodiac_form.cleaned_data['track_capricorn_axis_tc']

        track_capricon.axis(fc=zf_tcapr_axis_fc, ec=zf_tcapr_axis_ec, lw=2)
        track_capricon.text(f'{"♑︎"}', size=45, color=zf_tcapr_axis_tc)

        sector_cancer = circos.get_sector("♋︎")
        # track_cancer = sector_cancer.add_track((95, 80))
        track_cancer = sector_cancer.add_track((70, 95))

        zf_tcan_axis_fc = zodiac_form.cleaned_data['track_cancer_axis_fc']
        zf_tcan_axis_ec = zodiac_form.cleaned_data['track_cancer_axis_ec']
        zf_tcan_axis_tc = zodiac_form.cleaned_data['track_cancer_axis_tc']
        track_cancer.axis(fc=zf_tcan_axis_fc, ec=zf_tcan_axis_ec, lw=2)
        track_cancer.text(f'{"♋︎"}', size=45, color=zf_tcan_axis_tc)

        sector_scorpio = circos.get_sector("♏︎")
        # track_scorpio = sector_scorpio.add_track((95, 80))
        track_scorpio = sector_scorpio.add_track((70, 95))

        zf_tsco_axis_fc = zodiac_form.cleaned_data['track_scorpio_axis_fc']
        zf_tsco_axis_ec = zodiac_form.cleaned_data['track_scorpio_axis_ec']
        zf_tsco_axis_tc = zodiac_form.cleaned_data['track_scorpio_axis_tc']
        track_scorpio.axis(fc=zf_tsco_axis_fc, ec=zf_tsco_axis_ec, lw=2)
        track_scorpio.text(f'{"♏︎"}', size=45, color=zf_tsco_axis_tc)

        sector_pisces = circos.get_sector("♓︎")
        # track_pisces = sector_pisces.add_track((95, 80))
        track_pisces = sector_pisces.add_track((70, 95))

        zf_tpis_axis_fc = zodiac_form.cleaned_data['track_pisces_axis_fc']
        zf_tpis_axis_ec = zodiac_form.cleaned_data['track_pisces_axis_ec']
        zf_tpis_axis_tc = zodiac_form.cleaned_data['track_pisces_axis_tc']
        track_pisces.axis(fc=zf_tpis_axis_fc, ec=zf_tpis_axis_ec, lw=2)
        track_pisces.text(f'{"♏︎"}', size=45, color=zf_tpis_axis_tc)

        zf_deg_track_ec = zodiac_form.cleaned_data['degrees_track_ec']
        zf_dtick_clr = zodiac_form.cleaned_data['degrees_ticks_color']

        for sector in circos.sectors:
            # sector.axis(lw=1, ec="thistle")  # turn off sector line (axis)
            track_deg = sector.add_track((95, 100))
            track_deg.axis(ec=zf_deg_track_ec)
            track_deg.grid(y_grid_num=None, x_grid_interval=1, color=zf_dtick_clr)

        zf_sun_symbol_c = zodiac_form.cleaned_data['sun_symbol_c']
        zf_sun_symbol_s = zodiac_form.cleaned_data['sun_symbol_s']
        zf_sun_marker_c = zodiac_form.cleaned_data['sun_marker_c']

        zf_moon_symbol_c = zodiac_form.cleaned_data['moon_symbol_c']
        zf_moon_symbol_s = zodiac_form.cleaned_data['moon_symbol_s']
        zf_moon_marker_c = zodiac_form.cleaned_data['moon_marker_c']

        zf_mercury_symbol_c = zodiac_form.cleaned_data['mercury_symbol_c']
        zf_mercury_symbol_s = zodiac_form.cleaned_data['mercury_symbol_s']
        zf_mercury_marker_c = zodiac_form.cleaned_data['mercury_marker_c']

        zf_venus_symbol_c = zodiac_form.cleaned_data['venus_symbol_c']
        zf_venus_symbol_s = zodiac_form.cleaned_data['venus_symbol_s']
        zf_venus_marker_c = zodiac_form.cleaned_data['venus_marker_c']

        zf_mars_symbol_c = zodiac_form.cleaned_data['mars_symbol_c']
        zf_mars_symbol_s = zodiac_form.cleaned_data['mars_symbol_s']
        zf_mars_marker_c = zodiac_form.cleaned_data['mars_marker_c']

        zf_jupiter_symbol_c = zodiac_form.cleaned_data['jupiter_symbol_c']
        zf_jup_symbol_s = zodiac_form.cleaned_data['jup_symbol_s']
        zf_jup_marker_c = zodiac_form.cleaned_data['jup_marker_c']

        zf_saturn_symbol_c = zodiac_form.cleaned_data['saturn_symbol_c']
        zf_saturn_symbol_s = zodiac_form.cleaned_data['saturn_symbol_s']
        zf_saturn_marker_c = zodiac_form.cleaned_data['saturn_symbol_c']

        zf_uranus_symbol_c = zodiac_form.cleaned_data['uranus_symbol_c']
        zf_uranus_symbol_s = zodiac_form.cleaned_data['uranus_symbol_s']
        zf_uranus_marker_c = zodiac_form.cleaned_data['uranus_marker_c']

        zf_neptune_symbol_c = zodiac_form.cleaned_data['neptune_symbol_c']
        zf_neptune_symbol_s = zodiac_form.cleaned_data['neptune_symbol_s']
        zf_neptune_marker_c = zodiac_form.cleaned_data['neptune_marker_c']

        zf_pluto_symbol_c = zodiac_form.cleaned_data['pluto_symbol_c']
        zf_pluto_symbol_s = zodiac_form.cleaned_data['pluto_symbol_s']
        zf_pluto_marker_c = zodiac_form.cleaned_data['pluto_marker_c']

        fig = circos.plotfig()
        fig.patch.set_alpha(0.0)

        fig.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/images/tr_zr_clr.png',
                    pad_inches=0.0)

        houses = swe.houses_ex(jd, get_loc.latitude, get_loc.longitude, b'R', flags=swe.FLG_SIDEREAL)

        img = mpi.imread('astroplan/static/images/tr_zr_clr.png')
        fig = plt.figure(figsize=(870 * px, 870 * px))
        fig.patch.set_alpha(0.0)

        ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
        ax_img.imshow(img)
        ax_img.axis('off')

        planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot

        house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        house_ax.patch.set_alpha(0.0)

        planet_ax.set_rlim(-130, 100)
        planet_ax.set_theta_direction('counterclockwise')
        planet_ax.set_rticks([])
        planet_ax.set_axis_off()
        planet_ax.set_thetagrids(range(0, 360, 30))

        pd = {swe.get_planet_name(0): ['☼', zf_sun_marker_c, zf_sun_symbol_s, 45, zf_sun_symbol_c,
                                       swe.calc_ut(jd, 0, flags)[0][0],
                                       swe.calc_ut(jd, 0, flags)[0][1], 10],
              swe.get_planet_name(1): ['☾', zf_moon_marker_c, zf_moon_symbol_s, 45, zf_moon_symbol_c,
                                       swe.calc_ut(jd, 1, flags)[0][0],
                                       swe.calc_ut(jd, 1, flags)[0][1], -25],
              swe.get_planet_name(2): ['☿', zf_mercury_marker_c, zf_mercury_symbol_s, 45, zf_mercury_symbol_c,
                                       swe.calc_ut(jd, 2, flags)[0][0],
                                       swe.calc_ut(jd, 2, flags)[0][1], -25],
              swe.get_planet_name(3): ['♀', zf_venus_marker_c, zf_venus_symbol_s, 45, zf_venus_symbol_c,
                                       swe.calc_ut(jd, 3, flags)[0][0],
                                       swe.calc_ut(jd, 3, flags)[0][1], -10],
              swe.get_planet_name(4): ['♂', zf_mars_marker_c, zf_mars_symbol_s, 45, zf_mars_symbol_c,
                                       swe.calc_ut(jd, 4, flags)[0][0],
                                       swe.calc_ut(jd, 4, flags)[0][1], -10],
              swe.get_planet_name(5): ['♃', zf_jup_marker_c, zf_jup_symbol_s, 45, zf_jupiter_symbol_c,
                                       swe.calc_ut(jd, 5, flags)[0][0],
                                       swe.calc_ut(jd, 5, flags)[0][1], 0],
              swe.get_planet_name(6): ['♄', zf_saturn_marker_c, zf_saturn_symbol_s, 45, zf_saturn_symbol_c,
                                       swe.calc_ut(jd, 6, flags)[0][0],
                                       swe.calc_ut(jd, 6, flags)[0][1], -25],
              swe.get_planet_name(7): ['♅', zf_uranus_marker_c, zf_uranus_symbol_s, 45, zf_uranus_symbol_c,
                                       swe.calc_ut(jd, 7, flags)[0][0],
                                       swe.calc_ut(jd, 7, flags)[0][1], -20],
              swe.get_planet_name(8): ['♆', zf_neptune_marker_c, zf_neptune_symbol_s, 45, zf_neptune_symbol_c,
                                       swe.calc_ut(jd, 8, flags)[0][0],
                                       swe.calc_ut(jd, 8, flags)[0][1], 0],
              swe.get_planet_name(9): ['♇', zf_pluto_marker_c, zf_pluto_symbol_s, 45, zf_pluto_symbol_c,
                                       swe.calc_ut(jd, 9, flags)[0][0],
                                       swe.calc_ut(jd, 9, flags)[0][1], 0]
              }
        coords_value = list(pd.values())

        house_ax.set_rlim(-130, 100)
        house_ax.set_theta_direction(1)
        house_ax.set_rticks([])
        house_ax.set_thetagrids(houses[0],
                                ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
        house_ax.tick_params(labelsize=20, grid_color='#e7e3f5', grid_linewidth=1, labelfontfamily='monospace',
                             labelcolor='#e7e3f5')

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

        aspect_table_s = None
        aspect_table_ops = None
        aspect_table_c = None
        aspect_table_t = None

        aspected_planet_t.clear()
        aspected_planet_op.clear()
        aspected_planet_s.clear()
        aspected_planet_c.clear()

        c_angle.clear()
        t_angle.clear()
        sq_angle.clear()
        c_angle.clear()

        oppositions.clear()
        sqaures.clear()
        conjunctions.clear()
        trines.clear()

        for value in range(len(coords_value) - 1):
            for pl in range(0, 10):
                aspect = abs(round(coords_value[pl][5]) - round(coords_value[value + 1][5]))

                if aspect in trine and coords_value[pl][5] != coords_value[value + 1][5]:
                    pl_one = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                    pl_two = np.array([np.deg2rad(coords_value[pl][6]), np.deg2rad(coords_value[value + 1][6])])

                    if 119 < aspect < 121:
                        planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.5)
                    elif 122 < aspect < 123:
                        planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.0)
                    elif 123 < aspect < 125:
                        planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=0.8)
                    else:
                        planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=0.6)

                    aspected_planet_t.append(coords_value[pl][0])
                    t_angle.append(f'{aspect}°')
                    trines.append(coords_value[value + 1][0])
                    aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                if aspect in opposition and coords_value[pl][5] != coords_value[value + 1][5]:
                    pl_one = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                    pl_two = np.array([np.deg2rad(coords_value[pl][6]), np.deg2rad(coords_value[value + 1][6])])
                    if 179 < aspect < 181:
                        planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=1.5)
                    elif 181 < aspect < 183:
                        planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=1.0)
                    elif 183 < aspect < 185:
                        planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=0.8)
                    else:
                        planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=0.6)

                    aspected_planet_op.append(coords_value[pl][0])
                    op_angle.append(f'{aspect}°')
                    oppositions.append(coords_value[value + 1][0])
                    aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                if aspect in square and coords_value[pl][5] != coords_value[value + 1][5]:
                    pl_one = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                    pl_two = np.array([np.deg2rad(coords_value[pl][6]), np.deg2rad(coords_value[value + 1][6])])
                    if 89 < aspect < 91:
                        planet_ax.plot(pl_one, pl_two, color='#e20000', lw=1.5)
                    elif 91 < aspect < 93:
                        planet_ax.plot(pl_one, pl_two, color='#e20000', lw=1.0)
                    elif 93 < aspect < 95:
                        planet_ax.plot(pl_one, pl_two, color='#e20000', lw=0.8)
                    else:
                        planet_ax.plot(pl_one, pl_two, color='#e20000', lw=0.6)

                    aspected_planet_s.append(coords_value[pl][0])
                    sq_angle.append(f'{aspect}°')
                    sqaures.append(coords_value[value + 1][0])
                    aspect_table_s = zip(aspected_planet_s, sq_angle, sqaures)

                if aspect in conjunction and coords_value[pl][5] != coords_value[value + 1][5]:
                    pl_one = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                    pl_two = np.array([np.deg2rad(coords_value[pl][6]), np.deg2rad(coords_value[value + 1][6])])
                    planet_ax.plot(pl_one, pl_two, color='green', lw=0.3)

                    aspected_planet_c.append(coords_value[pl][0])
                    c_angle.append(f'{aspect}°')
                    conjunctions.append(coords_value[value + 1][0])
                    aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

                planet_ax.plot(np.deg2rad(coords_value[pl][5]), coords_value[pl][6], 'o',
                               mfc=pd[swe.get_planet_name(pl)][1],
                               ms=pd[swe.get_planet_name(pl)][2])

                if coords_value[pl][5] == 0 or coords_value[pl][5] < 45:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-20, -8),
                                       xycoords='data',
                                       xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                elif 45 < coords_value[pl][5] < 135:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-15, -25),
                                       xycoords='data',
                                       xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                elif 135 < coords_value[pl][5] < 180:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(3, 13),
                                       xycoords='data',
                                       xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                elif 180 < coords_value[pl][5] < 225:
                    if coords_value[pl][0] == '♂':
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(0, -25),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                    else:

                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(0, 15),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                elif 225 < coords_value[pl][5] < 270:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-25, -5),
                                       xycoords='data',
                                       xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                elif 270 < coords_value[pl][5] < 315:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-25, -5),
                                       xycoords='data',
                                       xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                elif 315 < coords_value[pl][5] < 360:
                    if coords_value[pl][0] == '♆':
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(3, -10),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                    else:
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

        plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/designed_chart.png')

        return render(request, 'designed_chart.html',
                      context={'planet_data': set_signs(planet_names, [p[5] for p in coords_value]),
                               'house_data': set_signs(house_names, list(houses[0])),
                               'ats': aspect_table_s, 'ato': aspect_table_ops,
                               'att': aspect_table_t, 'atc': aspect_table_c,
                               'date': now.strftime('%B, %d, %H:%M'),
                               'planet_names': planet_names})

    return render(request, 'color_chart.html', context={'zodiac_form': zodiac_form})


def one_color_chart(request):

    zodiac_oc_form = OneColorZodiacRing(request.POST or None,initial={

        'oc_chart_data': now,
        'oc_chart_city': 'Ufa',
        'oc_chart_country': 'Russia',

        'face_color': '#300c63',
        'edge_color': '#3dffc8',
        'text_color': '#3dffc8',
        'tick_color': '#63ffd3',
        'marker_color':'#ffc83d',
        'symbol_color': '#ff3d74',
        'deg_color': '#63ffd3',
        'font_size': 20,
        'line_width': 2,
        'marker_size': 20,
        'symbol_size': 20,

    })

    if zodiac_oc_form.is_valid():
        zf_city = zodiac_oc_form.cleaned_data['oc_chart_city']
        zf_country = zodiac_oc_form.cleaned_data['oc_chart_country']
        zf_date = zodiac_oc_form.cleaned_data['oc_chart_date']

        get_loc = loc.geocode(f'{zf_city, zf_country}', timeout=7000)
        tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
        d = zf_date
        jd = jl.to_jd(d, fmt='jd')

        zf_face_color = zodiac_oc_form.cleaned_data['face_color']
        zf_edge_color = zodiac_oc_form.cleaned_data['edge_color']
        zf_text_color = zodiac_oc_form.cleaned_data['text_color']
        zf_tick_color = zodiac_oc_form.cleaned_data['tick_color']
        zf_marker_color = zodiac_oc_form.cleaned_data['marker_color']
        zf_symbol_color = zodiac_oc_form.cleaned_data['symbol_color']
        zf_deg_color = zodiac_oc_form.cleaned_data['deg_color']
        zf_font_size = zodiac_oc_form.cleaned_data['font_size']
        zf_line_width = zodiac_oc_form.cleaned_data['line_width']
        zf_marker_size = zodiac_oc_form.cleaned_data['marker_size']
        zf_symbol_size = zodiac_oc_form.cleaned_data['symbol_size']

        draw_zodiac_one_color(zf_face_color, zf_edge_color, zf_text_color, zf_tick_color,
                              zf_deg_color, zf_font_size, zf_line_width)

        img = mpi.imread('astroplan/static/images/zr_one_clr.png')
        fig = plt.figure(figsize=(870 * px, 870 * px))
        fig.patch.set_alpha(0.0)

        ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
        ax_img.imshow(img)
        ax_img.axis('off')

        planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot

        house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        house_ax.patch.set_alpha(0.0)

        planet_ax.set_rlim(-130, 100)
        planet_ax.set_theta_direction('counterclockwise')
        planet_ax.set_rticks([])
        planet_ax.set_axis_off()
        planet_ax.set_thetagrids(range(0, 360, 30))

        pd = {swe.get_planet_name(0): ['☼', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 0, flags)[0][0],
                                       swe.calc_ut(jd, 0, flags)[0][1], 10],
              swe.get_planet_name(1): ['☾', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 1, flags)[0][0],
                                       swe.calc_ut(jd, 1, flags)[0][1], -25],
              swe.get_planet_name(2): ['☿', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 2, flags)[0][0],
                                       swe.calc_ut(jd, 2, flags)[0][1], -25],
              swe.get_planet_name(3): ['♀', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 3, flags)[0][0],
                                       swe.calc_ut(jd, 3, flags)[0][1], -10],
              swe.get_planet_name(4): ['♂', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 4, flags)[0][0],
                                       swe.calc_ut(jd, 4, flags)[0][1], -10],
              swe.get_planet_name(5): ['♃', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 5, flags)[0][0],
                                       swe.calc_ut(jd, 5, flags)[0][1], 0],
              swe.get_planet_name(6): ['♄', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 6, flags)[0][0],
                                       swe.calc_ut(jd, 6, flags)[0][1], -25],
              swe.get_planet_name(7): ['♅', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 7, flags)[0][0],
                                       swe.calc_ut(jd, 7, flags)[0][1], -20],
              swe.get_planet_name(8): ['♆', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 8, flags)[0][0],
                                       swe.calc_ut(jd, 8, flags)[0][1], 0],
              swe.get_planet_name(9): ['♇', zf_marker_color, zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 9, flags)[0][0],
                                       swe.calc_ut(jd, 9, flags)[0][1], 0]
              }
        coords_value = list(pd.values())
        houses = swe.houses_ex(jd, get_loc.latitude, get_loc.longitude, b'R', flags=swe.FLG_SIDEREAL)

        house_ax.set_rlim(-130, 100)
        house_ax.set_theta_direction(1)
        house_ax.set_rticks([])
        house_ax.set_thetagrids(houses[0],
                                ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
        house_ax.tick_params(labelsize=20, grid_color='#e7e3f5', grid_linewidth=1, labelfontfamily='monospace',
                             labelcolor='#e7e3f5')

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

        aspect_table_s = None
        aspect_table_ops = None
        aspect_table_c = None
        aspect_table_t = None

        aspected_planet_t.clear()
        aspected_planet_op.clear()
        aspected_planet_s.clear()
        aspected_planet_c.clear()

        c_angle.clear()
        t_angle.clear()
        sq_angle.clear()
        c_angle.clear()

        oppositions.clear()
        sqaures.clear()
        conjunctions.clear()
        trines.clear()

        for value in range(len(coords_value) - 1):
            for pl in range(0, 10):
                aspect = abs(round(coords_value[pl][5]) - round(coords_value[value + 1][5]))

                if aspect in trine and coords_value[pl][5] != coords_value[value + 1][5]:
                    pl_one = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                    pl_two = np.array([np.deg2rad(coords_value[pl][6]), np.deg2rad(coords_value[value + 1][6])])

                    if 119 < aspect < 121:
                        planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.5)
                    elif 122 < aspect < 123:
                        planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.0)
                    elif 123 < aspect < 125:
                        planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=0.8)
                    else:
                        planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=0.6)

                    aspected_planet_t.append(coords_value[pl][0])
                    t_angle.append(f'{aspect}°')
                    trines.append(coords_value[value + 1][0])
                    aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                if aspect in opposition and coords_value[pl][5] != coords_value[value + 1][5]:
                    pl_one = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                    pl_two = np.array([np.deg2rad(coords_value[pl][6]), np.deg2rad(coords_value[value + 1][6])])
                    if 179 < aspect < 181:
                        planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=1.5)
                    elif 181 < aspect < 183:
                        planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=1.0)
                    elif 183 < aspect < 185:
                        planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=0.8)
                    else:
                        planet_ax.plot(pl_one, pl_two, color='#0900FF', lw=0.6)

                    aspected_planet_op.append(coords_value[pl][0])
                    op_angle.append(f'{aspect}°')
                    oppositions.append(coords_value[value + 1][0])
                    aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                if aspect in square and coords_value[pl][5] != coords_value[value + 1][5]:
                    pl_one = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                    pl_two = np.array([np.deg2rad(coords_value[pl][6]), np.deg2rad(coords_value[value + 1][6])])
                    if 89 < aspect < 91:
                        planet_ax.plot(pl_one, pl_two, color='#e20000', lw=1.5)
                    elif 91 < aspect < 93:
                        planet_ax.plot(pl_one, pl_two, color='#e20000', lw=1.0)
                    elif 93 < aspect < 95:
                        planet_ax.plot(pl_one, pl_two, color='#e20000', lw=0.8)
                    else:
                        planet_ax.plot(pl_one, pl_two, color='#e20000', lw=0.6)

                    aspected_planet_s.append(coords_value[pl][0])
                    sq_angle.append(f'{aspect}°')
                    sqaures.append(coords_value[value + 1][0])
                    aspect_table_s = zip(aspected_planet_s, sq_angle, sqaures)

                if aspect in conjunction and coords_value[pl][5] != coords_value[value + 1][5]:
                    pl_one = np.array([np.deg2rad(coords_value[pl][5]), np.deg2rad(coords_value[value + 1][5])])
                    pl_two = np.array([np.deg2rad(coords_value[pl][6]), np.deg2rad(coords_value[value + 1][6])])
                    planet_ax.plot(pl_one, pl_two, color='green', lw=0.3)

                    aspected_planet_c.append(coords_value[pl][0])
                    c_angle.append(f'{aspect}°')
                    conjunctions.append(coords_value[value + 1][0])
                    aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

                planet_ax.plot(np.deg2rad(coords_value[pl][5]), coords_value[pl][6], 'o',
                               mfc=pd[swe.get_planet_name(pl)][1],
                               ms=pd[swe.get_planet_name(pl)][2])

                if coords_value[pl][5] == 0 or coords_value[pl][5] < 45:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-20, -8),
                                       xycoords='data',
                                       xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                elif 45 < coords_value[pl][5] < 135:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-15, -25),
                                       xycoords='data',
                                       xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                elif 135 < coords_value[pl][5] < 180:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(3, 13),
                                       xycoords='data',
                                       xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                elif 180 < coords_value[pl][5] < 225:
                    if coords_value[pl][0] == '♂':
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(0, -25),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                    else:

                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(0, 15),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                elif 225 < coords_value[pl][5] < 270:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-25, -5),
                                       xycoords='data',
                                       xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                elif 270 < coords_value[pl][5] < 315:
                    planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(-25, -5),
                                       xycoords='data',
                                       xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                       fontsize=pd[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                elif 315 < coords_value[pl][5] < 360:
                    if coords_value[pl][0] == '♆':
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(3, -10),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                    else:
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

        plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/one_clr_chart.png')

        return render(request, 'designed_oc_chart.html',  context={'planet_data': set_signs(planet_names, [p[5] for p in coords_value]),
                               'house_data': set_signs(house_names, list(houses[0])),
                               'ats': aspect_table_s, 'ato': aspect_table_ops,
                               'att': aspect_table_t, 'atc': aspect_table_c,
                               'date': now.strftime('%B, %d, %H:%M'),
                               'planet_names': planet_names})


    return render(request, 'design_one_clr_ch.html', {'z_form': zodiac_oc_form})


def wheel_year(request):
    return render(request, 'wheel_year.html')


def interpretations(request):
    return render(request, 'interpretations.html')


def do_shopping(request):
    return render(request, 'shop.html')


def chart_detail(request, id):
    chart_to_delete = FullChart.objects.filter(id=id).first()

    username = request.user.username
    userid = request.user.id

    if request.method == 'POST':
        chart_to_delete.delete()
        messages.success(request, 'Chart deleted')
        return redirect('my chart', username=username)

    return render(request, 'user_chart_db_detail.html', {'chart': FullChart.objects.get(id=id)})


def tr_chart_detail(request, id):
    tr_chart_to_delete = TransitFullChart.objects.filter(id=id).first()

    username = request.user.username
    userid = request.user.id

    if request.method == 'POST':
        tr_chart_to_delete.delete()
        messages.success(request, 'Chart deleted')
        return redirect('my chart', username=username)

    return render(request, 'transit_chart_db_detail.html', {'tr_chart': TransitFullChart.objects.get(id=id)})


def color_form(request):
    form = ColorForm()
    return render(request, 'color_chart.html', {'form': form})

# def show_chart_houses(request):
#
#     px = 1 / plt.rcParams['figure.dpi']
#  img = mpi.imread('astroplan/static/images/tr_zr_1.png')
#     fig = plt.figure(figsize=(870 * px, 870 * px), facecolor='violet', edgecolor='black')
#     # fig.suptitle(f'Planet chart today,{now.strftime('%B, %d, %H:%M')}', size=17)
#     fig.patch.set_alpha(0.0)

# ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
# ax_img.imshow(img)
# ax_img.axis('off')
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

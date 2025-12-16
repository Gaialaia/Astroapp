import os, io, base64

from django.contrib import messages

from django.shortcuts import render, redirect

from pycirclize import Circos
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpi


import numpy as np

from datetime import datetime as dt

import swisseph as swe

import julian as jl

from geopy.geocoders import Nominatim
from pytz import timezone

from .models import Chart, FullChart, TransitFullChart, OneColorZodiacRingMF
from .forms import (ChartForm, ShowChart, TransitForm, OneColorZodiacRing,
                    HOUSE_SYSTEM_CHOICES, MODE_CHOICES)
from astroplan.utils import build_plot, draw_zodiac_one_color
from timezonefinder import TimezoneFinder


swe.set_ephe_path('/home/gaia/Документы/eph files')

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

planet_symbols = ['☼', '☾', '☿', '♀', '♂', '♃', '♄', '♅', '♆', '♇',' ⯓']
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


def show_td_chart(request):

    matplotlib.rcParams['axes.edgecolor'] = '#ffd700'
    matplotlib.rcParams['axes.linewidth'] = 1.5

    img = mpi.imread('astroplan/static/images/zr_final_dp_pp.png')
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
    planet_ax.set_axis_off()

    get_loc = loc.geocode("Ufa, Russia", timeout=7000)
    loc_tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
    jd = jl.to_jd(dt.now(tz=timezone(loc_tz)), fmt='jd')
    houses = swe.houses_ex(jd, get_loc.latitude, get_loc.longitude, b'R', flags=swe.FLG_SIDEREAL)

    house_ax.set_rlim(-130, 100)
    house_ax.set_theta_direction(1)
    house_ax.set_rticks([])
    house_ax.set_thetagrids(houses[0], ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
    house_ax.tick_params(labelsize=30, grid_color='#ffd700', grid_linewidth=1.5, labelfontfamily='monospace',
                         labelcolor='#ffd700', pad=17.0)
    house_ax.set_theta_offset(np.pi)

    flags = swe.FLG_SIDEREAL | swe.SIDM_LAHIRI

    pd = {swe.get_planet_name(0): ['☼', 'yellow', 9, 30, swe.calc_ut(jd, 0, flags)[0][0],
                                   swe.calc_ut(jd, 0, flags)[0][1]],

          swe.get_planet_name(1): ['☾', 'blue', 9, 30, swe.calc_ut(jd, 1, flags)[0][0],
                                   swe.calc_ut(jd, 1, flags)[0][1]],
          swe.get_planet_name(2): ['☿', 'grey', 9, 30, swe.calc_ut(jd, 2, flags)[0][0],
                                   swe.calc_ut(jd, 2, flags)[0][1]],
          swe.get_planet_name(3): ['♀', 'sienna',9 , 30, swe.calc_ut(jd, 3, flags)[0][0],
                                   swe.calc_ut(jd, 3, flags)[0][1]],
          swe.get_planet_name(4): ['♂', 'red', 9, 30, swe.calc_ut(jd, 4, flags)[0][0], swe.calc_ut(jd, 4,
                                                                                                   flags)[0][1], -10],
          swe.get_planet_name(5): ['♃', 'teal', 9, 30, swe.calc_ut(jd, 5, flags)[0][0],
                                   swe.calc_ut(jd, 5, flags)[0][1], 0],
          swe.get_planet_name(6): ['♄', 'slategrey', 9, 30, swe.calc_ut(jd, 6, flags)[0][0],
                                   swe.calc_ut(jd, 6, flags)[0][1]],
          swe.get_planet_name(7): ['♅', 'chartreuse', 9, 30, swe.calc_ut(jd, 7, flags)[0][0],
                                   swe.calc_ut(jd, 7, flags)[0][1]],
          swe.get_planet_name(8): ['♆', 'indigo', 9, 30, swe.calc_ut(jd, 8, flags)[0][0],
                                   swe.calc_ut(jd, 8, flags)[0][1]],
          swe.get_planet_name(9): ['♇', '#311f11', 9, 30, swe.calc_ut(jd, 9, flags)[0][0],
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
                    planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=3.5)
                elif 122 < aspect < 123:
                    planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=2.0)
                elif 123 < aspect < 125:
                    planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.8)
                else:
                    planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.0)

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
                                   xytext=(-5, -25),
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

    chart_path = '/astro_app/astroknow/astroplan/static/plots/now_chart.png'

    directory = os.path.dirname(chart_path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    plt.savefig(chart_path)


    return render(request, 'main_astro.html',
                  context={ 'planet_data': set_signs(planet_names, [p[4] for p in coords_value]),
                           'house_data': set_signs(house_names, list(houses[0])),
                           'ats': aspect_table_s, 'ato': aspect_table_ops,
                           'att': aspect_table_t, 'atc': aspect_table_c,
                           'date': dt.now(tz=timezone(loc_tz)).strftime('%B, %d, %H:%M'),'planet_names': planet_names})


def chart_for_any_date(request):

    chart_form = ShowChart(request.POST or None, request.FILES or None)

    if chart_form.is_valid():

         city = chart_form.cleaned_data['city']
         country = chart_form.cleaned_data['country']
         chart_dt = chart_form.cleaned_data['chart_date']
         mode = chart_form.cleaned_data['mode']
         house_system = chart_form.cleaned_data['house_system']
         hs_name = HOUSE_SYSTEM_CHOICES.get(house_system)
         mode_name = MODE_CHOICES.get(mode)

         get_loc = loc.geocode(f'{city, country}', timeout=7000)

         jd = jl.to_jd(chart_dt, fmt='jd')

         hs_bytes = house_system.encode('utf-8')

         pd = {swe.get_planet_name(0): ['☼', 'yellow', 9, 17, swe.calc_ut(jd, 0, int(mode))[0][0],
                                        swe.calc_ut(jd, 0, int(mode))[0][1]],

               swe.get_planet_name(1): ['☾', 'blue', 9, 17, swe.calc_ut(jd, 1, int(mode))[0][0],
                                        swe.calc_ut(jd, 1, int(mode))[0][1]],

               swe.get_planet_name(2): ['☿', 'grey', 9, 17, swe.calc_ut(jd, 2, int(mode))[0][0],
                                        swe.calc_ut(jd, 2, int(mode))[0][1]],

               swe.get_planet_name(3): ['♀', 'sienna', 9, 17, swe.calc_ut(jd, 3, int(mode))[0][0],
                                        swe.calc_ut(jd, 3, int(mode))[0][1]],
               swe.get_planet_name(4): ['♂', 'red', 9, 30, swe.calc_ut(jd, 4, int(mode))[0][0],
                                        swe.calc_ut(jd, 4, int(mode))[0][1]],
               swe.get_planet_name(5): ['♃', 'teal', 9, 30, swe.calc_ut(jd, 5, int(mode))[0][0],
                                        swe.calc_ut(jd, 5, int(mode))[0][1]],
               swe.get_planet_name(6): ['♄', 'slategrey', 9, 30, swe.calc_ut(jd, 6, int(mode))[0][0],
                                        swe.calc_ut(jd, 6, int(mode))[0][1]],
               swe.get_planet_name(7): ['♅', 'chartreuse', 9, 30, swe.calc_ut(jd, 7, int(mode))[0][0],
                                        swe.calc_ut(jd, 7, int(mode))[0][1]],
               swe.get_planet_name(8): ['♆', 'indigo', 9, 30, swe.calc_ut(jd, 8, int(mode))[0][0],
                                        swe.calc_ut(jd, 8, int(mode))[0][1]],
               swe.get_planet_name(9): ['♇', 'darkmagenta', 9, 30, swe.calc_ut(jd, 9, int(mode))[0][0],
                                        swe.calc_ut(jd, 9, int(mode))[0][1]]}

         form_coords_value = list(pd.values())

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

         if house_system != 'Without houses':

             img = mpi.imread('astroplan/static/images/zr_final_dp_pp.png')
             fig_form = plt.figure(figsize=(870 * px, 870 * px))
             fig_form.patch.set_alpha(0.0)

             ax_img = fig_form.add_axes((0.05, 0.05, 0.9, 0.9))
             ax_img.imshow(img)
             ax_img.axis('off')

             planet_ax = fig_form.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
             planet_ax.set_rlim(-130, 100)
             planet_ax.set_theta_direction('counterclockwise')
             planet_ax.set_rticks([])
             planet_ax.set_axis_off()
             planet_ax.set_thetagrids(range(0, 360, 30))

             house_ax = fig_form.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
             house_ax.patch.set_alpha(0.0)
             house_ax.set_rlim(-130, 100)
             house_ax.set_theta_direction(1)
             house_ax.set_rticks([])

             houses = swe.houses_ex(jd, get_loc.latitude, get_loc.longitude, hs_bytes, (int(mode)))

             house_ax.set_thetagrids(houses[0],
                                     ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
             house_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1,
                                  labelfontfamily='monospace',
                                  labelcolor='aliceblue')

             for value in range(len(form_coords_value) - 1):
                 for pl in range(0, 10):
                     aspect = abs(round(form_coords_value[pl][4]) - round(form_coords_value[value + 1][4]))

                     if aspect in trine and form_coords_value[pl][4] != form_coords_value[value + 1][4]:
                         pl_one = np.array(
                             [np.deg2rad(form_coords_value[pl][4]), np.deg2rad(form_coords_value[value + 1][4])])
                         pl_two = np.array(
                             [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])

                         if 119 < aspect < 121:
                             planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=3.5)
                         elif 122 < aspect < 123:
                             planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=2.0)
                         elif 123 < aspect < 125:
                             planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.8)
                         else:
                             planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.0)

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
                             planet_ax.plot(pl_one, pl_two, color='#0400ff', lw=3.5)
                         elif aspect == range(181, 184):
                             planet_ax.plot(pl_one, pl_two, color='#0400ff', lw=2.0)
                         elif aspect == range(183, 186):
                             planet_ax.plot(pl_one, pl_two, color='#0400ff', lw=1.8)
                         elif aspect == 177:
                             planet_ax.plot(pl_one, pl_two, color='red', lw=1.0)

                         aspected_planet_op.append(form_coords_value[pl][0])
                         op_angle.append(f'{aspect}°')
                         oppositions.append(form_coords_value[value + 1][0])
                         aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                     if aspect in square and form_coords_value[pl][4] != form_coords_value[value + 1][4]:
                         pl_one = np.array(
                             [np.deg2rad(form_coords_value[pl][4]), np.deg2rad(form_coords_value[value + 1][4])])
                         pl_two = np.array(
                             [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])

                         if 89 < aspect < 91:
                             planet_ax.plot(pl_one, pl_two, color='#e20000', lw=3.5)
                         elif 91 < aspect < 93:
                             planet_ax.plot(pl_one, pl_two, color='#e20000', lw=2.3)
                         elif 93 < aspect < 95:
                             planet_ax.plot(pl_one, pl_two, color='#e20000', lw=1.8)
                         else:
                             planet_ax.plot(pl_one, pl_two, color='#e20000', lw=1.0)

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
                                            xytext=(-5, -25),
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

             # chart_path = '/astro_app/astroknow/astroplan/static/plots/chart_for_date'
             # directory = os.path.dirname(chart_path)
             # if not os.path.exists(directory):
             #     os.makedirs(directory, exist_ok=True)
             # plt.savefig(chart_path)

             buffer = io.BytesIO()
             plt.savefig(buffer, format='png')
             plt.close()
             buffer.seek(0)
             chart_png = buffer.getvalue()
             graph = base64.b64encode(chart_png)
             graph = graph.decode('utf-8')
             buffer.close()

             swe.close()

             return render(request, 'show_by_date.html',
                           {'planet_data': set_signs(planet_names, [p[4] for p in form_coords_value]),
                            'house_data': set_signs(house_names, list(houses[0])),
                            'ats': aspect_table_s, 'ato': aspect_table_ops,
                            'att': aspect_table_t, 'atc': aspect_table_c,
                            'date': chart_dt, 'city': city,
                            'country': country,
                            'latitude': get_loc.latitude,
                            'longitude': get_loc.longitude,
                            'mode_name': mode_name, 'hs_name': hs_name,
                            'graph': graph })

         elif house_system == 'Without houses':

             img = mpi.imread('astroplan/static/images/zr_final_dp_pp.png')
             fig_form = plt.figure(figsize=(870 * px, 870 * px))
             fig_form.patch.set_alpha(0.0)

             ax_img = fig_form.add_axes((0.05, 0.05, 0.9, 0.9))
             ax_img.imshow(img)
             ax_img.axis('off')

             planet_ax = fig_form.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
             planet_ax.set_rlim(-130, 100)
             planet_ax.set_theta_direction('counterclockwise')
             planet_ax.set_rticks([])
             planet_ax.set_axis_off()
             planet_ax.set_thetagrids(range(0, 360, 30))

             for value in range(len(form_coords_value) - 1):
                 for pl in range(0, 10):
                     aspect = abs(round(form_coords_value[pl][4]) - round(form_coords_value[value + 1][4]))

                     if aspect in trine and form_coords_value[pl][4] != form_coords_value[value + 1][4]:
                         pl_one = np.array(
                             [np.deg2rad(form_coords_value[pl][4]), np.deg2rad(form_coords_value[value + 1][4])])
                         pl_two = np.array(
                             [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])

                         if 119 < aspect < 121:
                             planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=3.5)
                         elif 122 < aspect < 123:
                             planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=2.0)
                         elif 123 < aspect < 125:
                             planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.8)
                         else:
                             planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=1.0)

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
                             planet_ax.plot(pl_one, pl_two, color='#0400ff', lw=3.5)
                         elif aspect == range(181, 184):
                             planet_ax.plot(pl_one, pl_two, color='#0400ff', lw=2.0)
                         elif aspect == range(183, 186):
                             planet_ax.plot(pl_one, pl_two, color='#0400ff', lw=1.8)
                         elif aspect == 177:
                             planet_ax.plot(pl_one, pl_two, color='red', lw=1.0)

                         aspected_planet_op.append(form_coords_value[pl][0])
                         op_angle.append(f'{aspect}°')
                         oppositions.append(form_coords_value[value + 1][0])
                         aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                     if aspect in square and form_coords_value[pl][4] != form_coords_value[value + 1][4]:
                         pl_one = np.array(
                             [np.deg2rad(form_coords_value[pl][4]), np.deg2rad(form_coords_value[value + 1][4])])
                         pl_two = np.array(
                             [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])

                         if 89 < aspect < 91:
                             planet_ax.plot(pl_one, pl_two, color='#e20000', lw=3.5)
                         elif 91 < aspect < 93:
                             planet_ax.plot(pl_one, pl_two, color='#e20000', lw=2.3)
                         elif 93 < aspect < 95:
                             planet_ax.plot(pl_one, pl_two, color='#e20000', lw=1.8)
                         else:
                             planet_ax.plot(pl_one, pl_two, color='#e20000', lw=1.0)

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
                                            xytext=(-5, -25),
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

             # chart_path = '/astro_app/astroknow/astroplan/static/plots/chart_for_date'
             #
             # directory = os.path.dirname(chart_path)
             # if not os.path.exists(directory):
             #     os.makedirs(directory, exist_ok=True)
             # plt.savefig(chart_path)
             # swe.close()

             buffer = io.BytesIO()
             plt.savefig(buffer, format='png')
             plt.close()
             buffer.seek(0)
             chart_png = buffer.getvalue()
             graph = base64.b64encode(chart_png)
             graph = graph.decode('utf-8')
             buffer.close()

             return render(request, 'show_by_date.html',
                           {'planet_data': set_signs(planet_names,
                                                                                   [p[4] for p in
                                                                                    form_coords_value]),
                                                          'ats': aspect_table_s, 'ato': aspect_table_ops,
                                                          'att': aspect_table_t, 'atc': aspect_table_c,
                                                          'date': chart_dt, 'city': city,
                                                          'country': country, 'latitude': get_loc.latitude,
                                                          'longitude': get_loc.longitude,
                            'mode_name': mode_name, 'hs_name': hs_name,
                            'graph': graph})

    return render(request, 'chart_for_any_date.html', {'chart_form':chart_form})


def build_transit_chart(request):
    chart_date = dt.now()
    chart = build_plot(chart_date, 'tr_chart_now')

    tr_form = TransitForm(request.POST or None, request.FILES or None)

    if tr_form.is_valid():

        event_date = tr_form.cleaned_data['event_date']
        event_city = tr_form.cleaned_data['event_city']
        event_country = tr_form.cleaned_data['event_country']
        ev_mode = tr_form.cleaned_data['ev_mode']
        ev_hs = tr_form.cleaned_data['ev_house_system']
        ev_hs_name = HOUSE_SYSTEM_CHOICES.get(ev_hs)
        ev_hs_bytes = ev_hs.encode('utf-8')

        transit_date = tr_form.cleaned_data['transit_date']
        transit_country = tr_form.cleaned_data['transit_city']
        transit_city = tr_form.cleaned_data['transit_country']
        tr_mode = tr_form.cleaned_data['tr_mode']
        tr_hs = tr_form.cleaned_data['tr_house_system']
        tr_hs_name = HOUSE_SYSTEM_CHOICES.get(tr_hs)
        tr_hs_bytes = tr_hs.encode('utf-8')

        jd_ev = jl.to_jd(event_date, fmt='jd')
        jd_tr = jl.to_jd(transit_date, fmt='jd')

        get_loc = loc.geocode(f'{event_city, event_country}', timeout=7000)
        tr_get_loc = loc.geocode(f'{transit_city, transit_country}', timeout=7000)

        pd_cr = {swe.get_planet_name(0): ['☼', 'yellow', 9, 30,
                                          swe.calc_ut(jd_ev, 0, int(ev_mode))[0][0],
                                          swe.calc_ut(jd_ev, 0, int(tr_mode))[0][1], 10],
                 swe.get_planet_name(1): ['☾', 'blue', 9, 30,
                                          swe.calc_ut(jd_ev, 1, int(ev_mode))[0][0],
                                          swe.calc_ut(jd_ev, 1, int(tr_mode))[0][1], -25],
                 swe.get_planet_name(2): ['☿', 'grey', 9, 30,
                                          swe.calc_ut(jd_ev, 2, int(ev_mode))[0][0],
                                          swe.calc_ut(jd_ev, 2, int(ev_mode))[0][1], -25],
                 swe.get_planet_name(3): ['♀', 'sienna', 9, 30,
                                          swe.calc_ut(jd_ev, 3, int(ev_mode))[0][0],
                                          swe.calc_ut(jd_ev, 3, int(ev_mode))[0][1], 25],
                 swe.get_planet_name(4): ['♂', 'red', 9, 30,
                                          swe.calc_ut(jd_ev, 4, int(ev_mode))[0][0],
                                          swe.calc_ut(jd_ev, 4, int(ev_mode))[0][1], -10],
                 swe.get_planet_name(5): ['♃', 'teal', 9, 30,
                                          swe.calc_ut(jd_ev, 5, int(ev_mode))[0][0],
                                          swe.calc_ut(jd_ev, 5, int(ev_mode))[0][1], 0],
                 swe.get_planet_name(6): ['♄', 'slategrey', 9, 30,
                                          swe.calc_ut(jd_ev, 6, int(ev_mode))[0][0],
                                          swe.calc_ut(jd_ev, 6, int(ev_mode))[0][1], -25],
                 swe.get_planet_name(7): ['♅', 'chartreuse', 9, 30,
                                          swe.calc_ut(jd_ev, 7, int(ev_mode))[0][0],
                                          swe.calc_ut(jd_ev, 7, int(ev_mode))[0][1], 0],
                 swe.get_planet_name(8): ['♆', 'indigo', 9, 30,
                                          swe.calc_ut(jd_ev, 8, int(ev_mode))[0][0],
                                          swe.calc_ut(jd_ev, 8, int(ev_mode))[0][1], 0],
                 swe.get_planet_name(9): ['⯓', 'darkmagenta', 9, 30,
                                          swe.calc_ut(jd_ev, 9, int(ev_mode))[0][0],
                                          swe.calc_ut(jd_ev, 9, int(ev_mode))[0][1], 0]}

        form_coords_value = list(pd_cr.values())

        pd = {swe.get_planet_name(0): ['☼', 'yellow', 9, 30,
                                       swe.calc_ut(jd_tr, 0, int(tr_mode))[0][0],
                                       swe.calc_ut(jd_tr, 0, int(tr_mode))[0][1], 10],
              swe.get_planet_name(1): ['☾', 'blue', 9, 30,
                                       swe.calc_ut(jd_tr, 1, int(tr_mode))[0][0],
                                       swe.calc_ut(jd_tr, 1, int(tr_mode))[0][1], -25],
              swe.get_planet_name(2): ['☿', 'grey', 9, 30,
                                       swe.calc_ut(jd_tr, 2, int(tr_mode))[0][0],
                                       swe.calc_ut(jd_tr, 2, int(tr_mode))[0][1], -25],
              swe.get_planet_name(3): ['♀', 'sienna', 9, 30,
                                       swe.calc_ut(jd_tr, 3, int(tr_mode))[0][0],
                                       swe.calc_ut(jd_tr, 3, int(tr_mode))[0][1], 25],
              swe.get_planet_name(4): ['♂', 'red', 9, 30,
                                       swe.calc_ut(jd_tr, 4, int(tr_mode))[0][0],
                                       swe.calc_ut(jd_tr, 4, int(tr_mode))[0][1], -10],
              swe.get_planet_name(5): ['♃', 'teal', 9, 30,
                                       swe.calc_ut(jd_tr, 5, int(tr_mode))[0][0],
                                       swe.calc_ut(jd_tr, 5, int(tr_mode))[0][1], 0],
              swe.get_planet_name(6): ['♄', 'slategrey', 9, 30,
                                       swe.calc_ut(jd_tr, 6, int(tr_mode))[0][0],
                                       swe.calc_ut(jd_tr, 6, int(tr_mode))[0][1], -25],
              swe.get_planet_name(7): ['♅', 'chartreuse', 9, 30,
                                       swe.calc_ut(jd_tr, 7, int(tr_mode))[0][0],
                                       swe.calc_ut(jd_tr, 7, int(tr_mode))[0][1], 0],
              swe.get_planet_name(8): ['♆', 'indigo', 9, 30,
                                       swe.calc_ut(jd_tr, 8, int(tr_mode))[0][0],
                                       swe.calc_ut(jd_tr, 8, int(tr_mode))[0][1], 0],
              swe.get_planet_name(9): ['⯓', 'darkmagenta', 9, 30,
                                       swe.calc_ut(jd_tr, 9, int(tr_mode))[0][0],
                                       swe.calc_ut(jd_tr, 9, int(tr_mode))[0][1], 0]}

        tr_form_coords_value = list(pd.values())

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

        if ev_hs == 'Without houses' and tr_hs == 'Without houses':

            img = mpi.imread('astroplan/static/images/zr_final.png')

            fig = plt.figure(figsize=(870 * px, 870 * px))
            fig.patch.set_alpha(0.0)

            ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
            ax_img.imshow(img)
            ax_img.axis('off')

            planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
            planet_ax.set_rlim(-180, 100)
            planet_ax.set_theta_direction('counterclockwise')
            planet_ax.set_rticks([])
            planet_ax.set_axis_off()

            transit_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            transit_ax.patch.set_alpha(0.0)
            transit_ax.set_rlim(-130, 100)
            transit_ax.set_theta_direction('counterclockwise')
            transit_ax.set_rticks([])
            transit_ax.set_axis_off()

            tr_cr_aspects_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            tr_cr_aspects_ax.patch.set_alpha(0.0)
            tr_cr_aspects_ax.set_rlim(-130, 100)
            tr_cr_aspects_ax.set_theta_direction(1)
            tr_cr_aspects_ax.set_rticks([])
            tr_cr_aspects_ax.set_axis_off()

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
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-20, -8),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                    elif 45 < form_coords_value[pl][4] < 135:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-15, -25),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    elif 135 < form_coords_value[pl][4] < 180:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(3, 13),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                    elif 180 < form_coords_value[pl][4] < 225:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(0, 25),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 225 < form_coords_value[pl][4] < 270:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 270 < form_coords_value[pl][4] < 315:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 315 < form_coords_value[pl][4] < 360:
                        if form_coords_value[pl][0] == '♆':
                            planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(3, -10),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                        else:
                            planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
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
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(-20, -8),
                                            xycoords='data',
                                            xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                            fontsize=pd[swe.get_planet_name(pl)][3],
                                            color='chartreuse',
                                            arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                    elif 45 < tr_form_coords_value[pl][4] < 135:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(-15, -25),
                                            xycoords='data',
                                            xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                            fontsize=pd[swe.get_planet_name(pl)][3],
                                            color='chartreuse',
                                            arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    elif 135 < tr_form_coords_value[pl][4] < 180:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(3, 13),
                                            xycoords='data',
                                            xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                            fontsize=pd[swe.get_planet_name(pl)][3],
                                            color='chartreuse',
                                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                    elif 180 < tr_form_coords_value[pl][4] < 225:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(0, 25),
                                            xycoords='data',
                                            xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                            fontsize=pd[swe.get_planet_name(pl)][3],
                                            color='chartreuse',
                                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 225 < tr_form_coords_value[pl][4] < 270:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(-25, -5),
                                            xycoords='data',
                                            xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                            fontsize=pd[swe.get_planet_name(pl)][3],
                                            color='chartreuse',
                                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 270 < tr_form_coords_value[pl][4] < 315:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(-25, -5),
                                            xycoords='data',
                                            xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                            fontsize=pd[swe.get_planet_name(pl)][3],
                                            color='chartreuse',
                                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 315 < tr_form_coords_value[pl][4] < 360:
                        if tr_form_coords_value[pl][0] == '♆':
                            transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                                xytext=(3, -10),
                                                xycoords='data',
                                                xy=(np.deg2rad(tr_form_coords_value[pl][4]),
                                                    tr_form_coords_value[pl][5]),
                                                fontsize=pd[swe.get_planet_name(pl)][3],
                                                color='chartreuse',
                                                arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                        else:
                            transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                                xytext=(-25, -5),
                                                xycoords='data',
                                                xy=(np.deg2rad(tr_form_coords_value[pl][4]),
                                                    tr_form_coords_value[pl][5]),
                                                fontsize=pd[swe.get_planet_name(pl)][3],
                                                color='chartreuse',
                                                arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

            tr_chart_path = '/astro_app/astroknow/astroplan/static/plots/transit_chart.png'
            directory = os.path.dirname(tr_chart_path)

            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            plt.savefig(tr_chart_path)

            return render(request, 'transit_chart_wh.html',
                          context={'planet_data': set_signs(planet_names, [p[4] for p in form_coords_value]),
                                   'ats': aspect_table_s, 'ato': aspect_table_ops,
                                   'att': aspect_table_t, 'atc': aspect_table_c,
                                   'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_form_coords_value]),
                                   'event_date': event_date, 'event_city': event_city, 'event_country': event_country,
                                   'tr_date': transit_date, 'tr_city': transit_city, 'tr_country': transit_country,
                                   'lat': get_loc.latitude, 'lng': get_loc.longitude})

        elif ev_hs != 'Without houses' and tr_hs != 'Without houses':

            img = mpi.imread('astroplan/static/images/zr_final.png')

            fig = plt.figure(figsize=(870 * px, 870 * px))
            fig.patch.set_alpha(0.0)

            ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
            ax_img.imshow(img)
            ax_img.axis('off')

            planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
            planet_ax.set_rlim(-180, 100)
            planet_ax.set_theta_direction('counterclockwise')
            planet_ax.set_rticks([])
            planet_ax.set_axis_off()

            transit_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            transit_ax.patch.set_alpha(0.0)
            transit_ax.set_rlim(-130, 100)
            transit_ax.set_theta_direction('counterclockwise')
            transit_ax.set_rticks([])
            transit_ax.set_axis_off()

            tr_cr_aspects_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            tr_cr_aspects_ax.patch.set_alpha(0.0)
            tr_cr_aspects_ax.set_rlim(-130, 100)
            tr_cr_aspects_ax.set_theta_direction(1)
            tr_cr_aspects_ax.set_rticks([])
            tr_cr_aspects_ax.set_axis_off()

            house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            house_ax.patch.set_alpha(0.0)
            house_ax.set_rlim(-130, 100)
            house_ax.set_theta_direction(1)
            house_ax.set_rticks([])

            houses = swe.houses_ex(jd_ev, get_loc.latitude, get_loc.longitude, ev_hs_bytes, int(ev_mode))

            house_ax.set_thetagrids(houses[0],
                                    ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
            house_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1,
                                 labelfontfamily='monospace', labelcolor='aliceblue')
            house_ax.set_theta_offset(np.pi)

            tr_house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            tr_house_ax.patch.set_alpha(0.0)
            tr_house_ax.set_rlim(-130, 100)
            tr_house_ax.set_theta_direction(1)
            tr_house_ax.set_rticks([])

            tr_houses = swe.houses_ex(jd_tr, tr_get_loc.latitude, tr_get_loc.longitude, tr_hs_bytes, int(tr_mode))
            tr_house_ax.set_thetagrids(tr_houses[0],
                                       ['TR ASC', 'TR II', 'TR III', 'TR IC', 'TR V', 'TR VI', 'TR DSC',
                                        'TR VIII', 'TR IX', 'TR MC', 'TR XI', 'TR XII'])
            tr_house_ax.tick_params(labelsize=20, grid_color='chartreuse', grid_linewidth=1,
                                    labelfontfamily='monospace', pad=23.0, labelcolor='chartreuse')
            tr_house_ax.set_theta_offset(np.pi)


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
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-20, -8),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                    elif 45 < form_coords_value[pl][4] < 135:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-15, -25),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    elif 135 < form_coords_value[pl][4] < 180:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(3, 13),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                    elif 180 < form_coords_value[pl][4] < 225:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(0, 25),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 225 < form_coords_value[pl][4] < 270:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 270 < form_coords_value[pl][4] < 315:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 315 < form_coords_value[pl][4] < 360:
                        if form_coords_value[pl][0] == '♆':
                            planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(3, -10),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                        else:
                            planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
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
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-20, -8),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='chartreuse',
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                    elif 45 < tr_form_coords_value[pl][4] < 135:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-15, -25),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='chartreuse',
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    elif 135 < tr_form_coords_value[pl][4] < 180:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(3, 13),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='chartreuse',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                    elif 180 < tr_form_coords_value[pl][4] < 225:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(0, 25),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='chartreuse',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 225 < tr_form_coords_value[pl][4] < 270:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='chartreuse',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 270 < tr_form_coords_value[pl][4] < 315:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='chartreuse',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 315 < tr_form_coords_value[pl][4] < 360:
                        if tr_form_coords_value[pl][0] == '♆':
                            transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(3, -10),
                                               xycoords='data',
                                               xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='chartreuse',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                        else:
                            transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(-25, -5),
                                               xycoords='data',
                                               xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='chartreuse',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

            tr_chart_path = '/astro_app/astroknow/astroplan/static/plots/transit_chart.png'

            directory = os.path.dirname(tr_chart_path)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            plt.savefig(tr_chart_path)

            return render(request, 'transit_chart.html',
                          context={'planet_data': set_signs(planet_names, [p[4] for p in form_coords_value]),
                                   'house_data': set_signs(house_names, list(houses[0])),
                                   'ats': aspect_table_s, 'ato': aspect_table_ops,
                                   'att': aspect_table_t, 'atc': aspect_table_c,
                                   'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_form_coords_value]),
                                   'tr_house_data': set_signs(house_names, list(tr_houses[0])), 'event_date': event_date,
                                   'event_city': event_city, 'event_country': event_country,
                                   'tr_date': transit_date, 'tr_city': transit_city, 'tr_country': transit_country,
                                   'lat': get_loc.latitude, 'lng': get_loc.longitude,
                                    'ev_hs_name': ev_hs_name,'tr_hs_name': tr_hs_name})

        elif ev_hs == 'Without houses' and tr_hs != 'Without houses':

            img = mpi.imread('astroplan/static/images/zr_final.png')

            fig = plt.figure(figsize=(870 * px, 870 * px))
            fig.patch.set_alpha(0.0)

            ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
            ax_img.imshow(img)
            ax_img.axis('off')

            planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
            planet_ax.set_rlim(-180, 100)
            planet_ax.set_theta_direction('counterclockwise')
            planet_ax.set_rticks([])
            planet_ax.set_axis_off()

            transit_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            transit_ax.patch.set_alpha(0.0)
            transit_ax.set_rlim(-130, 100)
            transit_ax.set_theta_direction('counterclockwise')
            transit_ax.set_rticks([])
            transit_ax.set_axis_off()

            tr_cr_aspects_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            tr_cr_aspects_ax.patch.set_alpha(0.0)
            tr_cr_aspects_ax.set_rlim(-130, 100)
            tr_cr_aspects_ax.set_theta_direction(1)
            tr_cr_aspects_ax.set_rticks([])
            tr_cr_aspects_ax.set_axis_off()

            tr_house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            tr_house_ax.patch.set_alpha(0.0)
            tr_house_ax.set_rlim(-130, 100)
            tr_house_ax.set_theta_direction(1)
            tr_house_ax.set_rticks([])

            tr_houses = swe.houses_ex(jd_tr, tr_get_loc.latitude, tr_get_loc.longitude, tr_hs_bytes, int(tr_mode))
            tr_house_ax.set_thetagrids(tr_houses[0],
                                       ['TR ASC', 'TR II', 'TR III', 'TR IC', 'TR V', 'TR VI', 'TR DSC',
                                        'TR VIII', 'TR IX', 'TR MC', 'TR XI', 'TR XII'])
            tr_house_ax.tick_params(labelsize=20, grid_color='chartreuse', grid_linewidth=1,
                                    labelfontfamily='monospace', pad=23.0, labelcolor='chartreuse')
            tr_house_ax.set_theta_offset(np.pi)

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
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-20, -8),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                    elif 45 < form_coords_value[pl][4] < 135:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-15, -25),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    elif 135 < form_coords_value[pl][4] < 180:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(3, 13),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                    elif 180 < form_coords_value[pl][4] < 225:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(0, 25),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 225 < form_coords_value[pl][4] < 270:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 270 < form_coords_value[pl][4] < 315:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 315 < form_coords_value[pl][4] < 360:
                        if form_coords_value[pl][0] == '♆':
                            planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(3, -10),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                        else:
                            planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
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
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-20, -8),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='chartreuse',
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                    elif 45 < tr_form_coords_value[pl][4] < 135:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-15, -25),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='chartreuse',
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    elif 135 < tr_form_coords_value[pl][4] < 180:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(3, 13),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='chartreuse',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                    elif 180 < tr_form_coords_value[pl][4] < 225:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(0, 25),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='chartreuse',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 225 < tr_form_coords_value[pl][4] < 270:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='chartreuse',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 270 < tr_form_coords_value[pl][4] < 315:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='chartreuse',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 315 < tr_form_coords_value[pl][4] < 360:
                        if tr_form_coords_value[pl][0] == '♆':
                            transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(3, -10),
                                               xycoords='data',
                                               xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='chartreuse',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                        else:
                            transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(-25, -5),
                                               xycoords='data',
                                               xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='chartreuse',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

            tr_chart_path = '/astro_app/astroknow/astroplan/static/plots/transit_chart.png'

            directory = os.path.dirname(tr_chart_path)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            plt.savefig(tr_chart_path)

            return render(request, 'transit_chart_tr_hs.html',
                          context={'planet_data': set_signs(planet_names, [p[4] for p in form_coords_value]),
                                   'ats': aspect_table_s, 'ato': aspect_table_ops,
                                   'att': aspect_table_t, 'atc': aspect_table_c,
                                   'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_form_coords_value]),
                                   'tr_house_data': set_signs(house_names, list(tr_houses[0])),
                                   'event_date': event_date,
                                   'event_city': event_city, 'event_country': event_country,
                                   'tr_date': transit_date, 'tr_city': transit_city, 'tr_country': transit_country,
                                   'lat': get_loc.latitude, 'lng': get_loc.longitude,
                                   'ev_hs_name': ev_hs_name, 'tr_hs_name': tr_hs_name})

        elif ev_hs != 'Without houses' and tr_hs == 'Without houses':

            img = mpi.imread('astroplan/static/images/zr_final.png')

            fig = plt.figure(figsize=(870 * px, 870 * px))
            fig.patch.set_alpha(0.0)

            ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
            ax_img.imshow(img)
            ax_img.axis('off')

            planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')  # center plot
            planet_ax.set_rlim(-180, 100)
            planet_ax.set_theta_direction('counterclockwise')
            planet_ax.set_rticks([])
            planet_ax.set_axis_off()

            transit_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            transit_ax.patch.set_alpha(0.0)
            transit_ax.set_rlim(-130, 100)
            transit_ax.set_theta_direction('counterclockwise')
            transit_ax.set_rticks([])
            transit_ax.set_axis_off()

            house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            house_ax.patch.set_alpha(0.0)
            house_ax.set_rlim(-130, 100)
            house_ax.set_theta_direction(1)
            house_ax.set_rticks([])

            houses = swe.houses_ex(jd_ev, get_loc.latitude, get_loc.longitude, ev_hs_bytes, int(ev_mode))

            house_ax.set_thetagrids(houses[0],
                                    ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
            house_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1,
                                 labelfontfamily='monospace', labelcolor='aliceblue')
            house_ax.set_theta_offset(np.pi)

            tr_cr_aspects_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            tr_cr_aspects_ax.patch.set_alpha(0.0)
            tr_cr_aspects_ax.set_rlim(-130, 100)
            tr_cr_aspects_ax.set_theta_direction(1)
            tr_cr_aspects_ax.set_rticks([])
            tr_cr_aspects_ax.set_axis_off()

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
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-20, -8),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                    elif 45 < form_coords_value[pl][4] < 135:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-15, -25),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    elif 135 < form_coords_value[pl][4] < 180:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(3, 13),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                    elif 180 < form_coords_value[pl][4] < 225:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(0, 25),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 225 < form_coords_value[pl][4] < 270:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 270 < form_coords_value[pl][4] < 315:
                        planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color='aliceblue',
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 315 < form_coords_value[pl][4] < 360:
                        if form_coords_value[pl][0] == '♆':
                            planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(3, -10),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][4]), form_coords_value[pl][5]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                        else:
                            planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
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
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(-20, -8),
                                            xycoords='data',
                                            xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                            fontsize=pd[swe.get_planet_name(pl)][3],
                                            color='chartreuse',
                                            arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                    elif 45 < tr_form_coords_value[pl][4] < 135:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(-15, -25),
                                            xycoords='data',
                                            xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                            fontsize=pd[swe.get_planet_name(pl)][3],
                                            color='chartreuse',
                                            arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    elif 135 < tr_form_coords_value[pl][4] < 180:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(3, 13),
                                            xycoords='data',
                                            xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                            fontsize=pd[swe.get_planet_name(pl)][3],
                                            color='chartreuse',
                                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                    elif 180 < tr_form_coords_value[pl][4] < 225:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(0, 25),
                                            xycoords='data',
                                            xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                            fontsize=pd[swe.get_planet_name(pl)][3],
                                            color='chartreuse',
                                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 225 < tr_form_coords_value[pl][4] < 270:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(-25, -5),
                                            xycoords='data',
                                            xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                            fontsize=pd[swe.get_planet_name(pl)][3],
                                            color='chartreuse',
                                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 270 < tr_form_coords_value[pl][4] < 315:
                        transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                            xytext=(-25, -5),
                                            xycoords='data',
                                            xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                            fontsize=pd[swe.get_planet_name(pl)][3],
                                            color='chartreuse',
                                            arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 315 < tr_form_coords_value[pl][4] < 360:
                        if tr_form_coords_value[pl][0] == '♆':
                            transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                                xytext=(3, -10),
                                                xycoords='data',
                                                xy=(np.deg2rad(tr_form_coords_value[pl][4]),
                                                    tr_form_coords_value[pl][5]),
                                                fontsize=pd[swe.get_planet_name(pl)][3],
                                                color='chartreuse',
                                                arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                        else:
                            transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                                xytext=(-25, -5),
                                                xycoords='data',
                                                xy=(np.deg2rad(tr_form_coords_value[pl][4]),
                                                    tr_form_coords_value[pl][5]),
                                                fontsize=pd[swe.get_planet_name(pl)][3],
                                                color='chartreuse',
                                                arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

            tr_chart_path = '/astro_app/astroknow/astroplan/static/plots/transit_chart.png'

            directory = os.path.dirname(tr_chart_path)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            plt.savefig(tr_chart_path)

            return render(request, 'transit_chart_ev_hs.html',
                          context={'planet_data': set_signs(planet_names, [p[4] for p in form_coords_value]),
                                   'ats': aspect_table_s, 'ato': aspect_table_ops,
                                   'att': aspect_table_t, 'atc': aspect_table_c,
                                   'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_form_coords_value]),
                                   'event_date': event_date,
                                   'house_data': set_signs(house_names, list(houses[0])),
                                   'event_city': event_city, 'event_country': event_country,
                                   'tr_date': transit_date, 'tr_city': transit_city, 'tr_country': transit_country,
                                   'lat': get_loc.latitude, 'lng': get_loc.longitude,
                                   'ev_hs_name': ev_hs_name, 'tr_hs_name': tr_hs_name})

    return render(request, 'transit_form.html',
                  context={'tr_form': tr_form, 'chart_date': chart_date})


def one_color_chart(request):

    zodiac_oc_form = OneColorZodiacRing(request.POST or None)

    if zodiac_oc_form.is_valid():

        zf_city = zodiac_oc_form.cleaned_data['oc_chart_city']
        zf_country = zodiac_oc_form.cleaned_data['oc_chart_country']
        zf_date = zodiac_oc_form.cleaned_data['oc_chart_date']
        zf_mode = zodiac_oc_form.cleaned_data['one_clr_zr_chart_mode']
        zf_hs = zodiac_oc_form.cleaned_data['one_clr_zr_chart_hs']
        clr_ch_hs_name = HOUSE_SYSTEM_CHOICES.get(zf_hs)
        hs_en = zf_hs.encode('utf-8')


        get_loc = loc.geocode(f'{zf_city, zf_country}', timeout=7000)
        tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)

        jd = jl.to_jd(zf_date, fmt='jd')

        zf_face_color = zodiac_oc_form.cleaned_data['face_color']
        zf_edge_color = zodiac_oc_form.cleaned_data['edge_color']
        zf_text_color = zodiac_oc_form.cleaned_data['text_color']
        zf_tick_color = zodiac_oc_form.cleaned_data['tick_color']
        zf_marker_color = zodiac_oc_form.cleaned_data['marker_color']
        zf_symbol_color = zodiac_oc_form.cleaned_data['symbol_color']
        zf_deg_color = zodiac_oc_form.cleaned_data['deg_color']
        zf_house_ax_color = zodiac_oc_form.cleaned_data['house_ax_color']
        zf_house_num_color = zodiac_oc_form.cleaned_data['house_number_color']
        zf_house_track_color = zodiac_oc_form.cleaned_data['house_track_color']
        zf_font_size = zodiac_oc_form.cleaned_data['font_size']
        zf_line_width = zodiac_oc_form.cleaned_data['line_width']
        zf_marker_size = zodiac_oc_form.cleaned_data['marker_size']
        zf_symbol_size = zodiac_oc_form.cleaned_data['symbol_size']
        zf_house_ax_lw = zodiac_oc_form.cleaned_data['house_ax_lw']
        zf_house_num_fs= zodiac_oc_form.cleaned_data['house_num_fs']
        zf_house_track_lw = zodiac_oc_form.cleaned_data['house_track_lw']


        draw_zodiac_one_color(zf_face_color, zf_edge_color, zf_text_color, zf_tick_color,
                              zf_deg_color, zf_font_size, zf_line_width)

        matplotlib.rcParams['axes.edgecolor'] = zf_house_track_color
        matplotlib.rcParams['axes.linewidth'] = zf_house_track_lw

        pd = {swe.get_planet_name(0): ['☼', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 0, int(zf_mode))[0][0],
                                       swe.calc_ut(jd, 0, int(zf_mode))[0][1], 10],
              swe.get_planet_name(1): ['☾', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 1,  int(zf_mode))[0][0],
                                       swe.calc_ut(jd, 1,  int(zf_mode))[0][1], -25],
              swe.get_planet_name(2): ['☿', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 2,  int(zf_mode))[0][0],
                                       swe.calc_ut(jd, 2,  int(zf_mode))[0][1], -25],
              swe.get_planet_name(3): ['♀', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 3,  int(zf_mode))[0][0],
                                       swe.calc_ut(jd, 3,  int(zf_mode))[0][1], -10],
              swe.get_planet_name(4): ['♂', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 4,  int(zf_mode))[0][0],
                                       swe.calc_ut(jd, 4,  int(zf_mode))[0][1], -10],
              swe.get_planet_name(5): ['♃', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 5,  int(zf_mode))[0][0],
                                       swe.calc_ut(jd, 5,  int(zf_mode))[0][1], 0],
              swe.get_planet_name(6): ['♄', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 6,  int(zf_mode))[0][0],
                                       swe.calc_ut(jd, 6,  int(zf_mode))[0][1], -25],
              swe.get_planet_name(7): ['♅', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 7,  int(zf_mode))[0][0],
                                       swe.calc_ut(jd, 7,  int(zf_mode))[0][1], -20],
              swe.get_planet_name(8): ['♆', zf_marker_color,  zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 8,  int(zf_mode))[0][0],
                                       swe.calc_ut(jd, 8,  int(zf_mode))[0][1], 0],
              swe.get_planet_name(9): ['♇', zf_marker_color, zf_symbol_size, zf_marker_size,  zf_symbol_color,
                                       swe.calc_ut(jd, 9,  int(zf_mode))[0][0],
                                       swe.calc_ut(jd, 9,  int(zf_mode))[0][1], 0]
              }
        coords_value = list(pd.values())
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

        if zf_hs != 'Without houses':

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

            houses = swe.houses_ex(jd, get_loc.latitude, get_loc.longitude, hs_en,  int(zf_mode))

            house_ax.set_rlim(-130, 100)
            house_ax.set_theta_direction(1)
            house_ax.set_rticks([])
            house_ax.set_thetagrids(houses[0],
                                    ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
            house_ax.tick_params(labelsize=zf_house_num_fs, grid_color=zf_house_ax_color,
                                 grid_linewidth=zf_house_ax_lw, labelfontfamily='monospace',
                                 labelcolor=zf_house_num_color, pad=13.0)

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
                                           color=zf_symbol_color,
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                    elif 45 < coords_value[pl][5] < 135:
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-15, -25),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color=zf_symbol_color,
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    elif 135 < coords_value[pl][5] < 180:
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(3, 13),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color=zf_symbol_color,
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                    elif 180 < coords_value[pl][5] < 225:
                        if coords_value[pl][0] == '♂':
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(0, -25),
                                               xycoords='data',
                                               xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color=zf_symbol_color,
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                        else:

                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(0, 15),
                                               xycoords='data',
                                               xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color=zf_symbol_color,
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 225 < coords_value[pl][5] < 270:
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color=zf_symbol_color,
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 270 < coords_value[pl][5] < 315:
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color=zf_symbol_color,
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 315 < coords_value[pl][5] < 360:
                        if coords_value[pl][0] == '♆':
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(3, -10),
                                               xycoords='data',
                                               xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color=zf_symbol_color,
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                        else:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(-25, -5),
                                               xycoords='data',
                                               xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color=zf_symbol_color,
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

            color_chart_path = '/astro_app/astroknow/astroplan/static/plots/one_clr_chart.png'

            directory = os.path.dirname(color_chart_path)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            plt.savefig(color_chart_path)

            return render(request, 'designed_oc_chart.html',  context={'planet_data': set_signs(planet_names, [p[5] for p in coords_value]),
                                   'house_data': set_signs(house_names, list(houses[0])),
                                   'ats': aspect_table_s, 'ato': aspect_table_ops,
                                   'att': aspect_table_t, 'atc': aspect_table_c,
                                   'date': zf_date,
                                   'planet_names': planet_names,
                                    'hs_name': clr_ch_hs_name})

        elif zf_hs == 'Without houses':

            img = mpi.imread('astroplan/static/images/zr_one_clr.png')
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
            planet_ax.set_thetagrids(range(0, 360, 30))


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
                                           color=zf_symbol_color,
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                    elif 45 < coords_value[pl][5] < 135:
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-15, -25),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color=zf_symbol_color,
                                           arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    elif 135 < coords_value[pl][5] < 180:
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(3, 13),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color=zf_symbol_color,
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                    elif 180 < coords_value[pl][5] < 225:
                        if coords_value[pl][0] == '♂':
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(0, -25),
                                               xycoords='data',
                                               xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color=zf_symbol_color,
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                        else:

                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(0, 15),
                                               xycoords='data',
                                               xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color=zf_symbol_color,
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 225 < coords_value[pl][5] < 270:
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color=zf_symbol_color,
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 270 < coords_value[pl][5] < 315:
                        planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                           xytext=(-25, -5),
                                           xycoords='data',
                                           xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                           fontsize=pd[swe.get_planet_name(pl)][3],
                                           color=zf_symbol_color,
                                           arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                    elif 315 < coords_value[pl][5] < 360:
                        if coords_value[pl][0] == '♆':
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(3, -10),
                                               xycoords='data',
                                               xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color=zf_symbol_color,
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                        else:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(-25, -5),
                                               xycoords='data',
                                               xy=(np.deg2rad(coords_value[pl][5]), coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color=zf_symbol_color,
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

            color_chart_path = '/astro_app/astroknow/astroplan/static/plots/one_clr_chart.png'

            directory = os.path.dirname(color_chart_path)

            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            plt.savefig(color_chart_path)

            return render(request, 'designed_oc_chart_wh.html',
                          context={'planet_data': set_signs(planet_names, [p[5] for p in coords_value]),
                                   'ats': aspect_table_s, 'ato': aspect_table_ops,
                                   'att': aspect_table_t, 'atc': aspect_table_c,
                                   'date': zf_date,
                                   'planet_names': planet_names,
                                   'hs_name': clr_ch_hs_name})

    return render(request, 'design_one_clr_ch.html', {'z_form': zodiac_oc_form})


def chart_detail(request, id):

    chart_to_delete = FullChart.objects.filter(id=id).first()
    username = request.user.username


    if request.method == 'POST':
        chart_to_delete.delete()
        messages.success(request, 'Chart deleted')
        return redirect('user lounge', username=username)


    chart_dtl = FullChart.objects.get(id=id)

    if chart_dtl.house_system == 'Without houses':
        return render(request,'user_chart_db_dtl_wh.html', {'chart': FullChart.objects.get(id=id)})

    return render(request, 'user_chart_db_detail.html', {'chart': FullChart.objects.get(id=id)})


def tr_chart_detail(request, id):
    tr_chart_to_delete = TransitFullChart.objects.filter(id=id).first()

    tr_chart_db_dtl = TransitFullChart.objects.get(id=id)


    username = request.user.username

    if request.method == 'POST':
        tr_chart_to_delete.delete()
        messages.success(request, 'Chart deleted')
        return redirect('user lounge', username=username)


    if tr_chart_db_dtl.ev_house_system == 'Without houses' and tr_chart_db_dtl.tr_house_system == 'Without houses':
        return render(request, 'transit_chart_db_detail_nh.html', {'tr_chart': TransitFullChart.objects.get(id=id)})
    elif tr_chart_db_dtl.ev_house_system == 'Without houses' and tr_chart_db_dtl.tr_house_system != 'Without houses':
        return render(request, 'transit_chart_db_detail_th.html', {'tr_chart': TransitFullChart.objects.get(id=id)})
    elif tr_chart_db_dtl.ev_house_system != 'Without houses' and tr_chart_db_dtl.tr_house_system == 'Without houses':
        return render(request, 'transit_chart_db_detail_eh.html', {'tr_chart': TransitFullChart.objects.get(id=id)})

    else:
        return render(request, 'transit_chart_db_detail.html', {'tr_chart': TransitFullChart.objects.get(id=id)})



def clr_chart_detail(request, id):
    clr_chart_to_del = OneColorZodiacRingMF.objects.filter(id=id).first()

    username = request.user.username

    if request.method == 'POST':
        clr_chart_to_del.delete()
        messages.success(request, 'Chart deleted')
        return redirect('user lounge', username=username)

    clr_chart_dtl = OneColorZodiacRingMF.objects.get(id=id)

    if clr_chart_dtl.chart_house_system == 'Without houses':
        return render(request, 'user_clr_chart_db_dtl_wh.html', {'clr_chart': OneColorZodiacRingMF.objects.get(id=id)})

    return render(request, 'clr_chart_db_dtl.html', {'clr_chart': OneColorZodiacRingMF.objects.get(id=id)})


def user_chart_lists(request):

    my_charts = FullChart.objects.filter(drawer__id=request.user.id)
    my_tr_charts = TransitFullChart.objects.filter(drawer__id=request.user.id)
    my_clr_charts  = OneColorZodiacRingMF.objects.filter(drawer__id=request.user.id)

    return render(request, 'user_chart_lists.html', {'my_charts': my_charts,
                                                     'my_tr_charts': my_tr_charts,
                                                     'my_clr_charts': my_clr_charts})


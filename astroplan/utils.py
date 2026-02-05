import io
import os

import boto3
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpi
from adjustText import adjust_text
from matplotlib.patches import ConnectionPatch
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
#
# from astroknow import settings


matplotlib.rcParams['axes.edgecolor'] = '#ffd700'
matplotlib.rcParams['axes.linewidth'] = 1.5


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
px = 1 / plt.rcParams['figure.dpi']



def get_graph(fig_name):

    buffer = io.BytesIO()
    fig_name.savefig(buffer, format='png')
    plt.close(fig_name)
    buffer.seek(0)
    chart_png = buffer.getvalue()
    graph = base64.b64encode(chart_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph


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



def draw_chart(fig_name, planet_ax = None, house_ax=None, transit_ax=None,
               tr_house_ax=None, aspect_ax=None):
    img = mpi.imread('astroplan/static/images/zr_final_tr.png')
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
        planet_ax.set_thetagrids([])

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
        transit_ax.set_rlim(-180, 100)
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
    if aspect_ax is not None:
        aspect_ax = fig_name.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        aspect_ax.patch.set_alpha(0.0)
        aspect_ax.set_rlim(-130, 100)
        aspect_ax.set_theta_direction(1)
        aspect_ax.set_rticks([])
        aspect_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1,
                                labelfontfamily='monospace',
                                labelcolor='aliceblue')

    return fig_name, planet_ax, house_ax, transit_ax, tr_house_ax, aspect_ax

def draw_transit_chart(event_one_ax, event_two_ax, event_one_houses=None, event_two_houses=None,
                       event_one_ha=None, event_two_ha=None):

    tr_fig, (event_one_ax, event_two_ax) = (
        plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(12, 6)))
    tr_fig.patch.set_alpha(0.0)
    img = mpi.imread('astroplan/static/images/zr_final_dp_pp.png')

    hl =  ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII']


    def set_zr_ax(ax_name):
        ax_name.set_theta_direction('counterclockwise')
        ax_name.set_rlim(-130, 100)
        ax_name.set_rticks([])
        ax_name.set_axis_off()
        ax_name.imshow(img)
        ax_name.patch.set_alpha(0)
        ax_name_bg = tr_fig.add_axes(ax_name.get_position(), zorder=-1)
        ax_name_bg.imshow(img, aspect='auto', extent=(0, 1, 0, 1))
        ax_name_bg.axis('off')
        return ax_name

    set_zr_ax(event_one_ax)
    set_zr_ax(event_two_ax)


    def set_ha(position_ax, angles, labels):
        ha_pos = position_ax.get_position()
        ha = tr_fig.add_axes(ha_pos, zorder=1, polar=True)
        ha.patch.set_alpha(0.0)
        ha.set_rlim(-130, 100)
        ha.set_theta_direction(1)
        ha.set_rticks([])
        ha.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1,
                                                        labelfontfamily='monospace',
                                                        labelcolor='aliceblue')
        ha.set_thetagrids(angles, labels)

        return ha, angles

    if event_one_ha or event_two_ha is not None:

        set_zr_ax(event_one_ax)

        event_one_ha= set_ha(event_one_ax, angles=event_one_houses, labels=hl)

        set_zr_ax(event_two_ax)

        event_two_ha = set_ha(event_two_ax, angles=event_two_houses, labels=hl)



    # for i, ax in enumerate([event_one_ax, event_two_ax]):
    #     ax.set_theta_direction('counterclockwise')
    #     ax.set_rlim(-130, 100)
    #     ax.set_rticks([])
    #     ax.set_axis_off()
    #     ax.imshow(img)
    #     ax.patch.set_alpha(0)
    #     ax_bg = tr_fig.add_axes(ax.get_position(), zorder=-1)
    #     ax_bg.imshow(img, aspect='auto', extent=(0, 1, 0, 1))
    #     ax_bg.axis('off')
    #
    #
    #     if event_one_ha and event_two_ha is not None:
    #         has.append(event_one_ax)
    #         has.append(event_two_ax)
    #         pos = ax.get_position()
    #         ha = tr_fig.add_axes(pos, zorder=1, label=f"layer_ha_{i}", polar=True)
    #         ha.patch.set_alpha(0.0)
    #         ha.set_rlim(-130, 100)
    #         ha.set_theta_direction(1)
    #         ha.set_rticks([])
    #         ha.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1,
    #                                  labelfontfamily='monospace',
    #                                  labelcolor='aliceblue')
    #
    #         event_one_ha = has[0]
    #         event_one_ha.set_thetagrids(event_one_houses,event_one_hl)
    #
    #         event_two_ha = has[1]
    #         event_two_ha.set_thetagrids(event_two_houses,event_two_hl)

    return tr_fig, event_one_ax, event_two_ax, event_one_ha, event_two_ha

def build_aspects(ax_name, planet_data):

    aspect_table_s = None
    aspect_table_ops = None
    aspect_table_c = None
    aspect_table_t = None


    event_one_td = []
    event_data = []

    aspected_planet_t.clear()
    aspected_planet_op.clear()
    aspected_planet_s.clear()
    aspected_planet_c.clear()

    c_angle.clear()
    t_angle.clear()
    sq_angle.clear()
    c_angle.clear()

    oppositions.clear()
    squares.clear()
    conjunctions.clear()
    trines.clear()

    for key, value in planet_data.items():
        event_data.append((key, value[4], value[5], value[0], value[1], value[2], value[3]))
    # event_data.insert(len(event_data), 0)

    for value in range(len(event_data)):
        t_one = ax_name.text(np.deg2rad(event_data[value][1]), event_data[value][2],
                             event_data[value][3], color=event_data[value][4],
                             fontsize=event_data[value][6])
        event_one_td.append(t_one)

    for value in range(len(event_data) - 1):
        for pl in range(0, 10):

            if event_data[pl][1] != event_data[value + 1][1]:

                    aspect = abs(event_data[pl][1] - event_data[value + 1][1])

                    # pl_one = (np.deg2rad(event_data[pl][1]), event_data[pl][2])
                    # pl_two = (np.deg2rad(event_data[value+1][1]), event_data[value+1][2])

                    pl_one = np.array(
                                [np.deg2rad(event_data[pl][1]), np.deg2rad(event_data[value + 1][1])])
                    pl_two = np.array(
                                [np.deg2rad(event_data[pl][2]), np.deg2rad(event_data[value + 1][2])])

                             # if aspect in trine and [pl][4] != [value + 1][4]:
                             #     pl_one = np.array(
                             #         [np.deg2rad(event_data[pl][4]), np.deg2rad(event_data[value + 1][4])])
                             #     pl_two = np.array(
                             #         [np.deg2rad(event_data[pl][5]), np.deg2rad(event_data[value + 1][5])])

                    ax_name.plot(np.deg2rad(event_data[pl][1]), event_data[pl][2], 'o',
                                          mfc=planet_data[swe.get_planet_name(pl)][1],
                                          ms=planet_data[swe.get_planet_name(pl)][2])

                    color = None
                    line_width = None

                    if 0 <= aspect <= 7:

                        color = 'pink'
                        line_width = 1

                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_c.append(event_data[pl][3])
                        c_angle.append(f'{round(aspect,2)}°')
                        conjunctions.append(event_data[value + 1][3])
                        aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)



                    if 119 <= aspect <= 121:

                        color = '#01ff00'
                        line_width = 3.5

                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)
                        aspected_planet_t.append(event_data[pl][3])
                        t_angle.append(f'{round(aspect,2)}°')
                        trines.append(event_data[value + 1][3])
                        aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                    elif 122 <= aspect <= 123:

                        color = '#01ff00'
                        line_width = 2.0
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)
                        aspected_planet_t.append(event_data[pl][3])
                        t_angle.append(f'{round(aspect,2)}°')
                        trines.append(event_data[value + 1][3])
                        aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                    elif 123 <= aspect <= 125:

                        color = '#01ff00'
                        line_width = 1.8
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_t.append(event_data[pl][3])
                        t_angle.append(f'{round(aspect,2)}°')
                        trines.append(event_data[value + 1][3])
                        aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                    if 89 < aspect < 91:
                        color = '#e20000'
                        line_width = 3.5

                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_s.append(event_data[pl][3])
                        sq_angle.append(f'{round(aspect,2)}°')
                        squares.append(event_data[value + 1][3])
                        aspect_table_s = zip(aspected_planet_s, sq_angle, squares)

                    elif 91 < aspect < 93:
                        color = '#e20000'
                        line_width = 2.3
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_s.append(event_data[pl][3])
                        sq_angle.append(f'{round(aspect,2)}°')
                        squares.append(event_data[value + 1][3])
                        aspect_table_s = zip(aspected_planet_s, sq_angle, squares)

                    elif 93 < aspect < 95:
                        color = '#e20000'
                        line_width = 1.8
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_s.append(event_data[pl][3])
                        sq_angle.append(f'{round(aspect,2)}°')
                        squares.append(event_data[value + 1][3])
                        aspect_table_s = zip(aspected_planet_s, sq_angle, squares)


                    if 179 <= aspect <= 181:
                        color = '#0400ff'
                        line_width = 3.5
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)
                        aspected_planet_op.append(event_data[pl][3])
                        op_angle.append(f'{round(aspect,2)}°')
                        oppositions.append(event_data[value + 1][3])
                        aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                    elif 181 <= aspect <= 184:
                        color = '#0400ff'
                        line_width = 2.0
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)
                        aspected_planet_op.append(event_data[pl][3])
                        op_angle.append(f'{round(aspect,2)}°')
                        oppositions.append(event_data[value + 1][3])
                        aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                    elif 183 <= aspect <= 186:
                        color = '#0400ff'
                        line_width = 1.8
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_op.append(event_data[pl][3])
                        op_angle.append(f'{round(aspect,2)}°')
                        oppositions.append(event_data[value + 1][3])
                        aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

    if event_one_td:
        adjust_text(event_one_td, ax=ax_name,
        arrowprops=dict(arrowstyle='-', color='aliceblue', lw=1),
        expand_text=(1.5, 1.5),
        force_text=(0.5, 0.5))

    return aspect_table_s,aspect_table_ops, aspect_table_t, aspect_table_c




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

def draw_zodiac_df_color(list_name):
    for t in list_name:
        zodiac_sector = circos.get_sector(t[0])
        zodiac_track = zodiac_sector.add_track((80, 100))
        zodiac_track.axis(fc=t[1], ec=t[2], lw=2)
        zodiac_track.text(f'{t[0]}', size=27, color=t[3])

    fig = circos.plotfig()
    fig.patch.set_alpha(0.0)
    fig.savefig('tr_for7.png')

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
                print(aspect_table_t)

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



jd_ev_one = jl.to_jd(dt.now())
planet_data = get_planet_data(jd_ev_one, swe.FLG_SIDEREAL)

bd = dt(2024,1,24,22,20)
jd_ev_two = jl.to_jd(bd)


def build_transit_aspects(event_one_data, event_two_data, event_one_ax, event_two_ax, fig):

    event_one_pp = []
    event_two_pp = []

    event_one_td = []
    event_two_td = []

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
    squares.clear()
    conjunctions.clear()
    trines.clear()

    for key, value in event_one_data.items():
        event_one_pp.append((key, value[4], value[5], value[0], value[1], value[2], value[3]))
    event_one_pp.insert(len(event_one_pp), 0)

    for key, value in event_two_data.items():
        event_two_pp.append(('tr_'+ key, value[4], value[5], value[0], value[1], value[2], value[3]))
    event_two_pp.insert(len(event_two_pp), 0)

    for i in range(len(event_one_pp) - 1):
        t_one = event_one_ax.text(np.deg2rad(event_one_pp[i][1]), event_one_pp[i][2],
                                  event_one_pp[i][3], color=event_one_pp[i][4], fontsize=event_one_pp[i][6])

        event_one_td.append(t_one)

        for k in range(len(event_two_pp) - 1):
            aspect = abs(event_one_pp[i][1] - event_two_pp[k][1])


            pl_one = (np.deg2rad(event_one_pp[i][1]), event_one_pp[i][2])

            pl_two = (np.deg2rad(event_two_pp[k][1]), event_two_pp[k][2])

            event_one_ax.plot(np.deg2rad(event_one_pp[i][1]), event_one_pp[i][5], 'o',
                              mfc=event_one_pp[i][4],
                              ms=event_one_pp[i][5])
            event_two_ax.plot(np.deg2rad(event_two_pp[i][1]), event_two_pp[i][5], 'o',
                              mfc=event_two_pp[i][4],
                              ms=event_two_pp[i][5])

            color = None
            line_width = None

            if 0 <= aspect <= 7:
                color = 'pink'
                line_width = 1

                aspected_planet_c.append(event_one_pp[i][3])
                c_angle.append(f'{round(aspect,2)}°')
                conjunctions.append(event_two_pp[k][3])

            if 119 <= aspect <= 121:
                color = '#01ff00'
                line_width = 3.5
                aspected_planet_t.append(event_one_pp[i][3])
                t_angle.append(f'{round(aspect, 2)}°')
                trines.append(event_two_pp[k][3])
            elif 122 <= aspect <= 123:
                color = '#01ff00'
                line_width = 2.0
                aspected_planet_t.append(event_one_pp[i][3])
                t_angle.append(f'{round(aspect, 2)}°')
                trines.append(event_two_pp[k][3])
            elif 123 <= aspect <= 125:
                color = '#01ff00'
                line_width = 1.8
                aspected_planet_t.append(event_one_pp[i][3])
                t_angle.append(f'{round(aspect, 2)}°')
                trines.append(event_two_pp[k][3])


            if 89 < aspect < 91:
               color='#e20000'
               line_width = 3.5

               aspected_planet_s.append((event_one_pp[i][3]))
               sq_angle.append(f'{round(aspect, 2)}°')
               squares.append(event_two_pp[k][3])
            elif 91 < aspect < 93:
                color='#e20000'
                line_width=2.3

                aspected_planet_s.append((event_one_pp[i][3]))
                sq_angle.append(f'{round(aspect, 2)}°')
                squares.append(event_two_pp[k][3])
            elif 93 < aspect < 95:
                color='#e20000'
                line_width=1.8

                aspected_planet_s.append((event_one_pp[i][3]))
                sq_angle.append(f'{round(aspect, 2)}°')
                squares.append(event_two_pp[k][3])

            if 179 <= aspect <= 181:
                color='#0400ff'
                line_width=3.5
                aspected_planet_op.append(event_one_pp[i][3])
                op_angle.append(f'{round(aspect, 2)}°')
                oppositions.append(event_two_pp[k][3])
            elif 181 <= aspect <= 184:
                color='#0400ff'
                line_width=2.0
                aspected_planet_op.append(event_one_pp[i][3])
                op_angle.append(f'{round(aspect, 2)}°')
                oppositions.append(event_two_pp[k][3])
            elif 183 <= aspect <= 186:
                 color='#0400ff'
                 line_width=1.8

                 aspected_planet_op.append(event_one_pp[i][3])
                 op_angle.append(f'{round(aspect, 2)}°')
                 oppositions.append(event_two_pp[k][3])

            aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)
            aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)
            aspect_table_s = zip(aspected_planet_s, sq_angle, squares)
            aspect_table_t = zip(aspected_planet_t, t_angle, trines)

            if color:
                con = ConnectionPatch(xyA=pl_one, xyB=pl_two,
                                      coordsA='data', coordsB='data',
                                      axesA=event_one_ax, axesB=event_two_ax,
                                      color=color, lw=line_width,
                                      shrinkA=0, shrinkB=0)
                fig.add_artist(con)



    for k in range(len(event_two_pp) - 1):
        t_two = event_two_ax.text(np.deg2rad(event_two_pp[k][1]), event_two_pp[k][2],
                                  event_two_pp[k][3], color=event_two_pp[k][4], fontsize=event_two_pp[k][6])

        event_two_td.append(t_two)

    if event_one_td:
        adjust_text(event_one_td, ax=event_one_ax,
                    arrowprops=dict(arrowstyle='-', color='aliceblue', lw=1),
                    expand_text=(1.5, 1.5),
                    force_text=(0.5, 0.5))
    if event_two_td:
        adjust_text(event_two_td, ax=event_two_ax,
                    arrowprops=dict(arrowstyle='-', color='aliceblue', lw=1),
                    expand_text=(1.5, 1.5),
                    force_text=(0.5, 0.5))


    return (aspect_table_s, aspect_table_ops, aspect_table_t,aspect_table_c,
            event_one_pp, event_two_pp)

#
# px = 1 / plt.rcParams['figure.dpi']
#
# img = mpi.imread('static/images/zr_final_dp_pp.png')
# fig = plt.figure(figsize=(870 * px, 870 * px))
# fig.patch.set_alpha(0.0)
#
# ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
# ax_img.imshow(img)
# ax_img.axis('off')
#
# planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
# planet_ax.set_theta_direction('counterclockwise')
# planet_ax.set_rlim(-180, 100)
# planet_ax.set_rticks([])
# planet_ax.set_axis_off()
#
#
# event_one_pp = []
# event_one_td = []
# # event_two_pp = []
# #
# jd_ev_one = jl.to_jd(dt.now())
# bd = dt(1986,2,17,22,20)
# jd_ev_two = jl.to_jd(bd)
#
# event_one_data = get_planet_data(jd_ev_one, swe.FLG_SIDEREAL)
# for key, value in event_one_data.items():
#     event_one_pp.append((key, value[4], value[5], value[0], value[1],value[2], value[3]))
# # event_one_pp.insert(len(event_one_pp), 0)
# #
# # print(event_one_pp)
#
# for j in range(len(event_one_pp)):
#     t_one = planet_ax.text(np.deg2rad(event_one_pp[j][1]), event_one_pp[j][2],
#                            event_one_pp[j][3], color=event_one_pp[j][4],
#                            fontsize=event_one_pp[j][6])
#     event_one_td.append(t_one)
#
# for i in range(len(event_one_pp)-1):
#     for pl in range(10):
#
#         if event_one_pp[pl][1] != event_one_pp[i + 1][1]:
#
#             aspect = abs(event_one_pp[pl][1] - event_one_pp[i + 1][1])
#             print(f'{event_one_pp[pl][1], event_one_pp[pl][3]} - {event_one_pp[i + 1][1], event_one_pp[i + 1][3]} = {aspect}')
#
#             pl_one = np.array(
#                 [np.deg2rad(event_one_pp[pl][1]), np.deg2rad(event_one_pp[i + 1][1])])
#             pl_two = np.array(
#                 [np.deg2rad(event_one_pp[pl][2]), np.deg2rad(event_one_pp[i + 1][2])])
#
#             planet_ax.plot(np.deg2rad(event_one_pp[pl][1]), event_one_pp[pl][2], 'o',
#                            mfc=planet_data[swe.get_planet_name(pl)][1],
#                            ms=planet_data[swe.get_planet_name(pl)][2])
# #
#             color = 'pink'
#             line_width = None
# #
#             if 0 <= aspect <= 7:
#                 color = 'pink'
#                 line_width = 1
#                 planet_ax.plot(pl_one, pl_two, color=color, lw=4)
#                 print(aspect)
#
#             if 119 <= aspect <= 121:
# #
#                 color = '#01ff00'
#                 line_width = 3.5
#                 planet_ax.plot(pl_one, pl_two, color=color, lw=line_width)
#                 print(aspect)
#
#
#             elif 122 <= aspect <= 123:
#
#                 color = '#01ff00'
#                 line_width = 2.0
#                 # planet_ax.plot(pl_one, pl_two, color=color, lw=line_width)
#                 print(aspect)
#
#             elif 123 <= aspect <= 125:
#
#                 color = '#01ff00'
#                 line_width = 1.8
#                 planet_ax.plot(pl_one, pl_two, color=color, lw=line_width)
#                 print(aspect)
#
#             #
#             if 89 <= aspect <= 91:
#                 color = '#e20000'
#                 line_width = 3.5
#                 planet_ax.plot(pl_one, pl_two, color=color, lw=line_width)
#                 print(aspect)
#
#             elif 91 <= aspect <= 93:
#                 color = '#e20000'
#                 line_width = 2.3
#                 planet_ax.plot(pl_one, pl_two, color=color, lw=line_width)
#                 print(aspect)
#
#
#             elif 93 <= aspect <= 95:
#                 color = '#e20000'
#                 line_width = 1.8
#                 planet_ax.plot(pl_one, pl_two, color=color, lw=line_width)
#                 print(aspect)
#
#
#             elif 175 <= aspect <= 184:
#                 color = '#0400ff'
#                 line_width = 2.0
#                 planet_ax.plot(pl_one, pl_two, color=color, lw=line_width)
#                 print(aspect)
#
#             elif 183 <= aspect <= 186:
#                 color = '#0400ff'
#                 line_width = 1.8
#                 planet_ax.plot(pl_one, pl_two, color=color, lw=line_width)
#                 print(aspect)
#
#
#
# if event_one_td:
#         adjust_text(event_one_td, ax=planet_ax,
#                     arrowprops=dict(arrowstyle='-', color='aliceblue', lw=1),
#                     expand_text=(1.5, 1.5),
#                     force_text=(0.5, 0.5))
# # plt.show()
#
# print(event_one_td)
#

# for value in range(len(event_one_pp) - 1):
#
#     t_one = planet_ax.text(np.deg2rad(event_one_pp[value][1]), event_one_pp[value][2],
#                          event_one_pp[value][3], color=event_one_pp[value][4],
#                          fontsize=event_one_pp[value][6])
#     event_one_td.append(t_one)
#
#     for pl in range(0, 10):
#
#         aspect = abs(event_one_pp[pl][1] - event_one_pp[value + 1][1])
#
#         pl_one = (np.deg2rad(event_one_pp[pl][1]), event_one_pp[pl][1])
#         pl_two = (np.deg2rad(event_one_pp[value + 1][1]), event_one_pp[value + 1][1])
#
#
#
#         planet_ax.plot(np.deg2rad(event_one_pp[pl][1]), event_one_pp[pl][1], 'o',
#                      mfc=planet_data[swe.get_planet_name(pl)][1],
#                      ms=planet_data[swe.get_planet_name(pl)][2])
#
#         color = None
#         line_width = None
#
#         if 0 <= aspect <= 7:
#             color = 'pink'
#             line_width = 1
#
#             aspected_planet_c.append(event_one_pp[pl][0])
#             c_angle.append(f'{aspect}°')
#             conjunctions.append(event_one_pp[value + 1][0])
#             aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)
#
#         if 119 <= aspect <= 121:
#
#             color = '#01ff00'
#             line_width = 3.5
#             aspected_planet_t.append(event_one_pp[pl][0])
#             t_angle.append(f'{aspect}°')
#             trines.append(event_one_pp[value + 1][0])
#             aspect_table_t = zip(aspected_planet_t, t_angle, trines)
#
#         elif 122 <= aspect <= 123:
#
#             color = '#01ff00'
#             line_width = 2.0
#             aspected_planet_t.append(event_one_pp[pl][0])
#             t_angle.append(f'{aspect}°')
#             trines.append(event_one_pp[value + 1][0])
#             aspect_table_t = zip(aspected_planet_t, t_angle, trines)
#
#         elif 123 <= aspect <= 125:
#
#             color = '#01ff00'
#             line_width = 1.8
#             aspected_planet_t.append(event_one_pp[pl][0])
#             t_angle.append(f'{aspect}°')
#             trines.append(event_one_pp[value + 1][0])
#             aspect_table_t = zip(aspected_planet_t, t_angle, trines)
#
#         if 89 < aspect < 91:
#             color = '#e20000'
#             line_width = 3.5
#
#             aspected_planet_s.append(event_one_pp[pl][0])
#             sq_angle.append(f'{aspect}°')
#             squares.append(event_one_pp[value + 1][0])
#             aspect_table_s = zip(aspected_planet_s, sq_angle, squares)
#
#         elif 91 < aspect < 93:
#             color = '#e20000'
#             line_width = 2.3
#
#             aspected_planet_s.append(event_one_pp[pl][0])
#             sq_angle.append(f'{aspect}°')
#             squares.append(event_one_pp[value + 1][0])
#             aspect_table_s = zip(aspected_planet_s, sq_angle, squares)
#
#         elif 93 < aspect < 95:
#             color = '#e20000'
#             line_width = 1.8
#
#             aspected_planet_s.append(event_one_pp[pl][0])
#             sq_angle.append(f'{aspect}°')
#             squares.append(event_one_pp[value + 1][0])
#             aspect_table_s = zip(aspected_planet_s, sq_angle, squares)
#
#         if 179 <= aspect <= 181:
#             color = '#0400ff'
#             line_width = 3.5
#             aspected_planet_op.append(event_one_pp[pl][0])
#             op_angle.append(f'{aspect}°')
#             oppositions.append(event_one_pp[value + 1][0])
#             aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)
#
#         elif 181 <= aspect <= 184:
#             color = '#0400ff'
#             line_width = 2.0
#             aspected_planet_op.append(event_one_pp[pl][0])
#             op_angle.append(f'{aspect}°')
#             oppositions.append(event_one_pp[value + 1][0])
#             aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)
#
#         elif 183 <= aspect <= 186:
#             color = '#0400ff'
#             line_width = 1.8
#
#             aspected_planet_op.append(event_one_pp[pl][0])
#             op_angle.append(f'{aspect}°')
#             oppositions.append(event_one_pp[value + 1][0])
#             aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)
#
#         planet_ax.plot(pl_one, pl_two, color=color, lw=line_width)
#
#         if event_one_td:
#             adjust_text(event_one_td, ax=planet_ax,
#                         arrowprops=dict(arrowstyle='-', color='aliceblue', lw=1),
#                         expand_text=(1.5, 1.5),
#                         force_text=(0.5, 0.5))
#
# plt.show()


        # aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)
        # aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)
        # aspect_table_s = zip(aspected_planet_s, sq_angle, squares)
        # aspect_table_t = zip(aspected_planet_t, t_angle, trines)

# event_two_data = get_planet_data(jd_ev_two, swe.FLG_SIDEREAL)

# for key, value in event_one_data.items():
#     event_one_pp.append((key, value[4], value[5], value[0], value[1],value[2], value[3]))
# event_one_pp.insert(len(event_one_pp), 0)
# print(event_one_pp[0][3])
# #
# coords = [(item[1], item[0]) for item in event_one_pp if isinstance(item, (list, tuple))]
# coords_n = [item[3] for item in event_one_pp if isinstance(item, (list, tuple))]
# print(coords_n)

# for key, value in event_two_data.items():
#     event_two_pp.append(('tr_'+ key, value[4], value[5], value[0], value[1],value[2], value[3]))
# event_two_pp.insert(len(event_two_pp), 0)

# print(event_two_pp)
#
# for i in range(len(event_one_pp)-1):
#     pass
#     for k in range(len(event_two_pp)-1):
#         aspect = event_one_pp[i][1] - event_two_pp[k][1]
#         # print(f'{event_one_pp[i][1], event_one_pp[i][3] } - {event_two_pp[k][1], event_two_pp[k][3]} = '
#         #       f'{abs(round(aspect,2))} \n',)
#
#         pl_one = np.array([np.deg2rad(event_one_pp[i][1]), np.deg2rad(event_two_pp[k][1])])
#         pl_two = np.array([np.deg2rad(event_one_pp[i][2]), np.deg2rad(event_two_pp[k][2])])
#
#         if 115 <= aspect <= 125: #trine
#             planet_ax.plot(pl_one, pl_two, color='#01ff00', lw=3.5)
#
#             aspected_planet_t.append(event_one_pp[i][0])
#             t_angle.append(f'{aspect}°')
#             trines.append(event_two_pp[k][0])
#             aspect_table_t = list(zip(aspected_planet_t, t_angle, trines))
#             # print(aspect_table_t)
#
#             print(f'{event_one_pp[i][1], event_one_pp[i][3]} - {event_two_pp[k][1], event_two_pp[k][3]} = '
#                   f'{abs(round(aspect, 2))} \n')
#         if 85 <= aspect <= 95: #sqaure
#             planet_ax.plot(pl_one, pl_two, color='red', lw=3.5)
#
#             aspected_planet_s.append((event_one_pp[i][0]))
#             sq_angle.append(f'{round(aspect,2)}°')
#             squares.append(event_two_pp[k][0])
#             aspect_table_s = zip(aspected_planet_s, sq_angle, squares)
#             print(list(aspect_table_s))
#             print(f'{event_one_pp[i][1], event_one_pp[i][3]} - {event_two_pp[k][1], event_two_pp[k][3]} = '
#                   f'{abs(round(aspect, 2))} \n', )
#
#         if 175 <= aspect <= 185:
#             planet_ax.plot(pl_one, pl_two, color='orange', lw=3.5)
#             print(f'{event_one_pp[i][1], event_one_pp[i][3]} - {event_two_pp[k][1], event_two_pp[k][3]} = '
#                   f'{abs(round(aspect, 2))} \n', )
#         if 0 <= aspect <= 7:
#             planet_ax.plot(pl_one, pl_two, color='pink', lw=3.5)
#             # print(f'{event_one_pp[i][1], event_one_pp[i][3]} - {event_two_pp[k][1], event_two_pp[k][3]} = '
#             #       f'{abs(round(aspect, 2))} \n', )
#
#
#  plt.show()



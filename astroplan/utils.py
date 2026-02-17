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

from astroknow import settings

matplotlib.rcParams['axes.edgecolor'] = '#ffd700'
matplotlib.rcParams['axes.linewidth'] = 1.5


flags = swe.FLG_SIDEREAL

sectors = {"♊︎": 30, "♉︎": 30, "♈︎": 30,
           "♓︎": 30, "♒︎": 30, "♑︎": 30,
           "♐︎": 30, "♏︎": 30, "♎︎": 30,
           "♍︎": 30, "♌︎": 30, "♋︎": 30,
           }

circos = Circos(sectors)


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


planet_symbols = ['☼', '☾', '☿', '♀', '♂', '♃', '♄', '♅', '♆', '♇',' ⯓']

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
font_size = 26
color = ''

PLANET_METADATA = {

    0: ['☼', 'yellow', marker_size, font_size],
    1: ['○', 'aliceblue', marker_size, font_size],
    2: ['☿', 'grey', marker_size, font_size],
    3: ['♀', 'sienna', marker_size, font_size],
    4: ['♂', 'red', marker_size, font_size],
    5: ['♃', '#16CBBC', marker_size, font_size],
    6: ['♄', '#052443', marker_size, font_size],
    7: ['♅', 'chartreuse', marker_size, font_size],
    8: ['♆', 'indigo', marker_size, font_size],
    9: ['♇', 'darkmagenta', marker_size, font_size]
}
signs = []
sign = ''
def get_planet_data(jd, ch_mode, chart=None):

    pd = {}
    chart_mode = int(ch_mode)

    for pl_number, meta in PLANET_METADATA.items():

        planet_name = swe.get_planet_name(pl_number)

        ecliptic_latitude = swe.calc_ut(jd, pl_number, chart_mode)[0][0]
        ecliptic_longitude = swe.calc_ut(jd, pl_number, chart_mode)[0][1]

        pd[planet_name] = [meta[0], meta[1], meta[2], meta[3],ecliptic_latitude, ecliptic_longitude]
    return pd


def zip_ad(pl_one_pos, angle_data, pl_two_pos, aspect_angle, po_list, pt_list):
    po_list.append(pl_one_pos)
    angle_data.append(aspect_angle)
    pt_list.append(pl_two_pos)
    return zip(po_list, angle_data, pt_list)


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
    deg_form = [str(n).replace('.', '°') + "'" for n in deg_list_thirty]
    sign_table = zip(name_list, deg_form, signs)
    return list(sign_table)


def draw_chart(fig_name, planet_ax = None, house_ax=None,
               ha_color = None, ha_lab_cl = None, ha_lbl_size=None,
               ha_lw=None, houses_data=None, chart_path=None):
    hl = ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII']
    fig_name = plt.figure(figsize=(870 * px, 870 * px))
    fig_name.patch.set_alpha(0.0)

    if chart_path is None:
        img = mpi.imread('astroplan/static/images/zr_final_tr.png')
        ax_img = fig_name.add_axes((0.05, 0.05, 0.9, 0.9))
        ax_img.imshow(img)
        ax_img.axis('off')

    if chart_path:
        img = mpi.imread(chart_path)
        ax_img = fig_name.add_axes((0.05, 0.05, 0.9, 0.9))
        ax_img.imshow(img)
        ax_img.axis('off')

    planet_ax = fig_name.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
    planet_ax.set_theta_direction('counterclockwise')
    planet_ax.set_rlim(-130, 100)
    planet_ax.set_rticks([])
    planet_ax.set_axis_off()
    planet_ax.imshow(img)
    planet_ax.patch.set_alpha(0)


    if house_ax is not None:

        house_ax = fig_name.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
        house_ax.patch.set_alpha(0.0)
        house_ax.set_rlim(-130, 100)
        house_ax.set_theta_direction(1)
        house_ax.set_rticks([])
        house_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1,
                                 labelfontfamily='monospace',
                                 labelcolor='aliceblue')

        house_ax.set_thetagrids(houses_data,hl)

        if ha_color and ha_lab_cl:
            house_ax.tick_params(labelsize=ha_lbl_size, grid_color=ha_color,
                                 grid_linewidth=ha_lw,
                                 labelfontfamily='monospace',
                                 labelcolor=ha_lab_cl)


    return (fig_name, planet_ax, house_ax, ha_color, ha_lab_cl,
            ha_lbl_size, ha_lw, chart_path,houses_data)



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

    set_zr_ax(event_one_ax)
    set_zr_ax(event_two_ax)

    if event_one_ha is not None:

        set_zr_ax(event_one_ax)
        event_one_ha= set_ha(event_one_ax, angles=event_one_houses, labels=hl)

    if event_two_ha is not None:
        set_zr_ax(event_two_ax)
        event_two_ha = set_ha(event_two_ax, angles=event_two_houses, labels=hl)

    return tr_fig, event_one_ax, event_two_ax, event_one_ha, event_two_ha

def build_aspects(ax_name, planet_data, marker_clr=None, symbol_clr=None,
                  pl_marker_size=None, symbol_size=None):

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


    for key, value in planet_data.items():
        event_data.append((key, value[4], value[5], value[0], value[1], value[2], value[3]))

    for value in range(len(event_data)):

        if symbol_size is None and symbol_clr is None:
            t_one = ax_name.text(np.deg2rad(event_data[value][1]), event_data[value][2],
                                 event_data[value][3], color='aliceblue',
                                 fontsize=event_data[value][6])
            event_one_td.append(t_one)
        if symbol_clr and symbol_size:
            t_one = ax_name.text(np.deg2rad(event_data[value][1]), event_data[value][2],
                                 event_data[value][3], color=symbol_clr,
                                 fontsize=symbol_size)
            if event_one_td:
                event_one_td.clear()
                event_one_td.append(t_one)


    for value in range(len(event_data) - 1):
        for pl in range(0, 10):

            if event_data[pl][1] != event_data[value + 1][1]:

                    aspect = abs(event_data[pl][1] - event_data[value + 1][1])

                    pl_one = np.array(
                                [np.deg2rad(event_data[pl][1]), np.deg2rad(event_data[value + 1][1])])
                    pl_two = np.array(
                                [np.deg2rad(event_data[pl][2]), np.deg2rad(event_data[value + 1][2])])

                    ax_name.plot(np.deg2rad(event_data[pl][1]), event_data[pl][2], 'o',
                                          mfc=planet_data[swe.get_planet_name(pl)][1],
                                          ms=planet_data[swe.get_planet_name(pl)][2])
                    if marker_clr and pl_marker_size:
                        ax_name.plot(np.deg2rad(event_data[pl][1]), event_data[pl][2], 'o',
                                     mfc=marker_clr,
                                     ms=pl_marker_size)

                    color = None
                    line_width = None

                    round_aspect = f'{round(aspect, 2)}'
                    ready_aspect = str(round_aspect).replace('.', '°') + "'"

                    if 0 <= aspect <= 7:

                        color = 'pink'
                        line_width = 1

                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_c.append(event_data[pl][3])
                        c_angle.append(ready_aspect)
                        conjunctions.append(event_data[value + 1][3])
                        aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

                    if 119 <= aspect <= 121:

                        color = '#01ff00'
                        line_width = 3.5

                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)
                        aspected_planet_t.append(event_data[pl][3])
                        t_angle.append(ready_aspect)
                        trines.append(event_data[value + 1][3])
                        aspect_table_t = zip(aspected_planet_t, t_angle, trines)


                    elif 122 <= aspect <= 123:

                        color = '#01ff00'
                        line_width = 2.0

                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)
                        aspected_planet_t.append(event_data[pl][3])
                        t_angle.append(ready_aspect)
                        trines.append(event_data[value + 1][3])
                        aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                    elif 123 <= aspect <= 125:

                        color = '#01ff00'
                        line_width = 1.8
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_t.append(event_data[pl][3])
                        t_angle.append(ready_aspect)
                        trines.append(event_data[value + 1][3])
                        aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                    if 89 < aspect < 91:
                        color = '#e20000'
                        line_width = 3.5

                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_s.append(event_data[pl][3])
                        sq_angle.append(ready_aspect)
                        squares.append(event_data[value + 1][3])
                        aspect_table_s = zip(aspected_planet_s, sq_angle, squares)

                    elif 91 < aspect < 93:
                        color = '#e20000'
                        line_width = 2.3
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_s.append(event_data[pl][3])
                        sq_angle.append(ready_aspect)
                        squares.append(event_data[value + 1][3])
                        aspect_table_s = zip(aspected_planet_s, sq_angle, squares)

                    elif 93 < aspect < 95:
                        color = '#e20000'
                        line_width = 1.8
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_s.append(event_data[pl][3])
                        sq_angle.append(ready_aspect)
                        squares.append(event_data[value + 1][3])
                        aspect_table_s = zip(aspected_planet_s, sq_angle, squares)


                    if 179 <= aspect <= 181:
                        color = '#0400ff'
                        line_width = 3.5
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_op.append(event_data[pl][3])
                        op_angle.append(ready_aspect)
                        oppositions.append(event_data[value + 1][3])
                        aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)


                    elif 181 <= aspect <= 184:
                        color = '#0400ff'
                        line_width = 2.0
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_op.append(event_data[pl][3])
                        op_angle.append(ready_aspect)
                        oppositions.append(event_data[value + 1][3])
                        aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)



                    elif 183 <= aspect <= 186:
                        color = '#0400ff'
                        line_width = 1.8
                        ax_name.plot(pl_one, pl_two, color=color, lw=line_width)

                        aspected_planet_op.append(event_data[pl][3])
                        op_angle.append(ready_aspect)
                        oppositions.append(event_data[value + 1][3])
                        aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)


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
    return chart_path


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


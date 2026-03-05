import datetime
import matplotlib

import swisseph as swe
import julian as jl

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from astroknow import settings
from datetime import datetime as dt
from geopy.geocoders import Nominatim
from .models import FullChart, TransitFullChart, OneColorZodiacRingMF
from .forms import (ShowChart, TransitForm, OneColorZodiacRing,
                    HOUSE_SYSTEM_CHOICES, MODE_CHOICES)
from .utils import (draw_zodiac_one_color, get_planet_data,
                    build_aspects, draw_chart, get_graph, build_transit_aspects,
                    draw_transit_chart, set_signs)
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo

matplotlib.use('Agg')

swe.set_ephe_path('/home/gaia/Документы/eph files')

planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter',
                'Saturn', 'Uranus', 'Neptune', 'Pluto']

tr_planet_names = ['tr_Sun', 'tr_Moon', 'tr_Mercury', 'tr_Venus', 'tr_Mars',
                   'tr_Jupiter', 'tr_Saturn', 'tr_Uranus', 'tr_Neptune', 'tr_Pluto']

house_names = ['ASC', 'II', 'III', 'IC', 'V', 'VI',
               'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII']

tf = TimezoneFinder()
loc = Nominatim(user_agent="GetLoc")


def show_td_chart(request):
    jd = jl.to_jd(dt.now(), fmt='jd')

    flags = swe.FLG_SIDEREAL | swe.SIDM_LAHIRI

    planet_data = get_planet_data(jd, flags)
    planet_data_values = list(planet_data.values())

    fig_form, planet_ax, _, _, _, _, _, _, _ = (
        draw_chart(fig_name='fig_form', planet_ax='planet_ax'))

    aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, = \
        build_aspects(planet_data=planet_data, ax_name=planet_ax)

    graph, _ = get_graph(fig_form)

    swe.close()

    context = {'planet_data': set_signs(planet_names,
                                        [p[4] for p in planet_data_values]),
               'ats': aspect_table_s, 'ato': aspect_table_ops,
               'att': aspect_table_t, 'atc': aspect_table_c,
               'date': dt.now().strftime('%B, %d, %A, %H:%M'),
               'planet_names': planet_names, 'graph': graph}

    return render(request, 'main_astro.html', context)


def chart_for_any_date(request):
    chart_form = ShowChart(request.POST or None, request.FILES or None)

    if chart_form.is_valid():

        city = chart_form.cleaned_data['city']
        if city.isdigit():
            chart_form.add_error('city', 'Type "city" in letters')
            return render(request, 'chart_for_any_date.html',
                          {'chart_form': chart_form})

        country = chart_form.cleaned_data['country']
        if country.isdigit():
            chart_form.add_error('country', 'Type "country "in letters')
            return render(request, 'chart_for_any_date.html',
                          {'chart_form': chart_form})

        chart_dt = chart_form.cleaned_data['chart_date']
        mode = int(chart_form.cleaned_data['mode'])
        house_system = chart_form.cleaned_data['house_system']
        hs_name = HOUSE_SYSTEM_CHOICES.get(house_system)
        mode_name = MODE_CHOICES.get(mode)

        get_loc = loc.geocode(f'{city, country}', timeout=7000)

        if get_loc is None:
            (chart_form.add_error
             ('city', f'"{city}" is not found, try again'))
            (chart_form.add_error
             ('country', f'"{country}" is not found, try again'))
            return render(request, 'chart_for_any_date.html',
                          {'chart_form': chart_form})

        loc_tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
        local_dt = chart_dt.replace(tzinfo=ZoneInfo(loc_tz))

        utc_dt = local_dt.astimezone(datetime.timezone.utc)
        jd = jl.to_jd(utc_dt, fmt='jd')

        hs_bytes = house_system.encode('utf-8')

        planet_data = get_planet_data(jd, mode)
        planet_data_values = list(planet_data.values())

        if house_system != 'Without houses':
            houses = swe.houses_ex(jd, get_loc.latitude,
                                   get_loc.longitude, hs_bytes, (int(mode)))

            fig_form, planet_ax, house_ax, _, _, _, _, _, _ = (
                draw_chart(fig_name='fig_form', planet_ax='planet_ax',
                           house_ax='house_ax', houses_data=houses[0]))

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, = \
                build_aspects(ax_name=planet_ax, planet_data=planet_data)

            graph, _ = get_graph(fig_form)

            swe.close()

            return render(request, 'show_by_date.html',
                          {'planet_data': set_signs(planet_names,
                                                    [p[4] for p in planet_data_values]),
                           'house_data': set_signs(house_names, list(houses[0])),
                           'ats': aspect_table_s, 'ato': aspect_table_ops,
                           'att': aspect_table_t, 'atc': aspect_table_c,
                           'date': chart_dt.strftime("%B %d, %Y, %H:%M:%S, %A"),
                           'country': country, 'city': city,
                           'latitude': get_loc.latitude,
                           'longitude': get_loc.longitude,
                           'mode_name': mode_name, 'hs_name': hs_name,
                           'graph': graph, 'tz': loc_tz})

        elif house_system == 'Without houses':

            fig_form, planet_ax, _, _, _, _, _, _, _ = (
                draw_chart(fig_name='fig_form', planet_ax='planet_ax'))

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, = \
                build_aspects(planet_data=planet_data, ax_name=planet_ax)
            graph, _ = get_graph(fig_form)
            swe.close()

            return render(request, 'show_by_date_wh.html',
                          {'planet_data': set_signs(planet_names,
                           [p[4] for p in planet_data_values]),
                           'ats': aspect_table_s, 'ato': aspect_table_ops,
                           'attt': aspect_table_t, 'atc': aspect_table_c,
                           'date': chart_dt.strftime("%B %d, %Y, %H:%M:%S, %A"),
                           'city': city, 'country': country,'tz': loc_tz,
                           'latitude': get_loc.latitude, 'hs_name': hs_name,
                           'longitude': get_loc.longitude, 'mode_name': mode_name,
                           'graph': graph})

    return render(request, 'chart_for_any_date.html',
                  {'chart_form': chart_form})


def build_transit_chart(request):
    tr_form = TransitForm(request.POST or None, request.FILES or None)

    if tr_form.is_valid():

        event_date = tr_form.cleaned_data['event_date']
        event_city = tr_form.cleaned_data['event_city']
        event_country = tr_form.cleaned_data['event_country']
        ev_mode = tr_form.cleaned_data['ev_mode']
        ev_hs = tr_form.cleaned_data['ev_house_system']
        ev_hs_name = HOUSE_SYSTEM_CHOICES.get(ev_hs)
        ev_hs_bytes = ev_hs.encode('utf-8')
        ev_m = MODE_CHOICES.get(ev_mode)

        transit_date = tr_form.cleaned_data['transit_date']
        transit_country = tr_form.cleaned_data['transit_city']
        transit_city = tr_form.cleaned_data['transit_country']
        tr_mode = tr_form.cleaned_data['tr_mode']
        tr_hs = tr_form.cleaned_data['tr_house_system']
        tr_hs_name = HOUSE_SYSTEM_CHOICES.get(tr_hs)
        tr_hs_bytes = tr_hs.encode('utf-8')
        tr_m = MODE_CHOICES.get(tr_mode)

        ev_get_loc = loc.geocode(f'{event_city, event_country}', timeout=7000)
        ev_loc_tz = tf.timezone_at(lng=ev_get_loc.longitude, lat=ev_get_loc.latitude)
        ev_local_dt = event_date.replace(tzinfo=ZoneInfo(ev_loc_tz))
        ev_utc_dt = ev_local_dt.astimezone(datetime.timezone.utc)
        jd_ev = jl.to_jd(ev_utc_dt, fmt='jd')

        tr_get_loc = loc.geocode(f'{transit_city, transit_country}', timeout=7000)
        tr_loc_tz = tf.timezone_at(lng=tr_get_loc.longitude, lat=tr_get_loc.latitude)
        tr_local_dt = transit_date.replace(tzinfo=ZoneInfo(tr_loc_tz))
        tr_utc_dt = tr_local_dt.astimezone(datetime.timezone.utc)
        jd_tr = jl.to_jd(tr_utc_dt, fmt='jd')

        event_data = get_planet_data(jd_ev, ev_mode)
        transit_data = get_planet_data(jd_tr, tr_mode)

        if ev_hs == 'Without houses' and tr_hs == 'Without houses':

            tr_fig, event_one_ax, event_two_ax, _, _ = (
                draw_transit_chart('event_one_ax',
                                   'event_two_ax'))

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, \
                event_one_pp, event_two_pp = (
                build_transit_aspects(event_one_data=event_data,
                                      event_two_data=transit_data,
                                      event_one_ax=event_one_ax,
                                      event_two_ax=event_two_ax,
                                      fig=tr_fig))

            swe.close()

            graph, _ = get_graph(tr_fig)

            context = {'planet_data': set_signs([item[0] for item in event_one_pp
                        if isinstance(item, (list, tuple))],
                       [item[1] for item in event_one_pp
                        if isinstance(item, (list, tuple))]),
                       'ats': aspect_table_s, 'ato': aspect_table_ops,
                       'att': aspect_table_t, 'graph': graph, 'event_date': event_date,
                       'atc': aspect_table_c, 'tr_mode': tr_m, 'ev_mode': ev_m,
                       'tr_planet_data': set_signs([item[0] for item in event_two_pp
                        if isinstance(item, (list, tuple))],
                        [item[1] for item in event_two_pp if
                        isinstance(item, (list, tuple))]),
                       'event_city': event_city, 'event_country': event_country,
                       'tr_date': transit_date, 'tr_city': transit_city,
                       'tr_country': transit_country, 'ev_hs_name': ev_hs_name,
                       'tr_hs_name': tr_hs_name}

            return render(request, 'transit_chart_wh.html', context)

        elif ev_hs != 'Without houses' and tr_hs != 'Without houses':

            houses = swe.houses_ex(jd_ev, ev_get_loc.latitude,
                                   ev_get_loc.longitude, ev_hs_bytes, int(ev_mode))
            tr_houses = swe.houses_ex(jd_tr, tr_get_loc.latitude,
                                      tr_get_loc.longitude, tr_hs_bytes, int(tr_mode))

            tr_fig, event_one_ax, event_two_ax, event_one_ha, event_two_ha = (
                draw_transit_chart(event_one_ax='event_one_ax',
                                   event_two_ax='event_two_ax',
                                   event_one_ha='event_one_ha',
                                   event_two_ha='event_two_ha',
                                   event_one_houses=houses[0],
                                   event_two_houses=tr_houses[0]))

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, \
                event_one_pp, event_two_pp = (
                build_transit_aspects(event_one_data=event_data,
                                      event_two_data=transit_data,
                                      event_one_ax=event_one_ax,
                                      event_two_ax=event_two_ax,
                                      fig=tr_fig))

            graph, _ = get_graph(tr_fig)
            context = {'planet_data': set_signs([item[0] for item in event_one_pp
                                                 if isinstance(item, (list, tuple))],
                                                [item[1] for item in event_one_pp
                                                 if isinstance(item, (list, tuple))]),
                       'ats': aspect_table_s, 'ato': aspect_table_ops,
                       'att': aspect_table_t, 'atc': aspect_table_c,
                       'tr_planet_data': set_signs([item[0] for item in event_two_pp
                                                    if isinstance(item, (list, tuple))],
                                                   [item[1] for item in event_two_pp if
                                                    isinstance(item, (list, tuple))]),
                       'event_date': event_date, 'event_city': event_city,
                       'event_country': event_country, 'ev_mode': ev_m,
                       'tr_date': transit_date, 'tr_city': transit_city,
                       'tr_country': transit_country, 'tr_hs_name': tr_hs_name,
                       'ev_hs_name': ev_hs_name, 'tr_mode': tr_m, 'graph': graph,
                       'house_data': set_signs(house_names, list(houses[0])),
                       'tr_house_data': set_signs(house_names, list(tr_houses[0]))
                       }

            swe.close()

            return render(request, 'transit_chart.html', context)

        elif ev_hs == 'Without houses' and tr_hs != 'Without houses':  #event_two_ha work

            tr_houses = swe.houses_ex(jd_tr, tr_get_loc.latitude,
                                      tr_get_loc.longitude, tr_hs_bytes, int(tr_mode))

            tr_fig, event_one_ax, event_two_ax, _, event_two_ha = (
                draw_transit_chart(event_one_ax='event_one_ax',
                                   event_two_ax='event_two_ax',
                                   event_two_ha='event_two_ha',
                                   event_two_houses=tr_houses[0]))

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, \
                event_one_pp, event_two_pp = (
                build_transit_aspects(event_one_data=event_data,
                                      event_two_data=transit_data,
                                      event_one_ax=event_one_ax,
                                      event_two_ax=event_two_ax,
                                      fig=tr_fig))

            swe.close()

            graph, _ = get_graph(tr_fig)

            context = {'planet_data': set_signs([item[1] for item in event_one_pp
                                                 if isinstance(item, (list, tuple))],
                                                [item[0] for item in event_one_pp
                                                 if isinstance(item, (list, tuple))]),
                       'ats': aspect_table_s, 'ato': aspect_table_ops,
                       'att': aspect_table_t,
                       'atc': aspect_table_c, 'graph': graph,
                       'tr_planet_data': set_signs([item[1] for item in event_two_pp
                                                    if isinstance(item, (list, tuple))],
                                                   [item[0] for item in event_two_pp if
                                                    isinstance(item, (list, tuple))]),
                       'event_date': event_date, 'event_city': event_city,
                       'event_country': event_country, 'tr_country': transit_country,
                       'tr_date': transit_date, 'tr_city': transit_city,
                       'ev_hs_name': ev_hs_name, 'tr_hs_name': tr_hs_name,
                       'tr_mode': tr_m, 'ev_mode': ev_m,
                       'tr_house_data': set_signs(list(tr_houses[0]), house_names)
                       }

            return render(request, 'transit_chart_tr_hs.html', context)

        elif ev_hs != 'Without houses' and tr_hs == 'Without houses':  #event_one_ha dont work

            houses = swe.houses_ex(jd_ev, ev_get_loc.latitude,
                                   ev_get_loc.longitude, ev_hs_bytes, int(ev_mode))

            tr_fig, event_one_ax, event_two_ax, event_one_ha, _ = (
                draw_transit_chart(event_one_ax='event_one_ax',
                                   event_two_ax='event_two_ax',
                                   event_one_ha='event_one_ha',
                                   event_one_houses=houses[0],
                                   ))

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, \
                event_one_pp, event_two_pp = (
                build_transit_aspects(event_one_data=event_data,
                                      event_two_data=transit_data,
                                      event_one_ax=event_one_ax,
                                      event_two_ax=event_two_ax,
                                      fig=tr_fig))

            graph, _ = get_graph(tr_fig)

            swe.close()

            context = {'planet_data': set_signs([item[1] for item in event_one_pp
                                                 if isinstance(item, (list, tuple))],
                                                [item[0] for item in event_one_pp if
                                                 isinstance(item, (list, tuple))]),
                       'ats': aspect_table_s, 'ato': aspect_table_ops,
                       'atc': aspect_table_c, 'att': aspect_table_t,
                       'tr_planet_data': set_signs([item[1] for item in event_two_pp
                                                    if isinstance(item, (list, tuple))],
                                                   [item[0] for item in event_two_pp if
                                                    isinstance(item, (list, tuple))]), 'graph': graph,
                       'event_date': event_date, 'event_city': event_city,
                       'event_country': event_country, 'ev_mode': ev_m,
                       'tr_date': transit_date, 'tr_city': transit_city,
                       'ev_hs_name': ev_hs_name, 'tr_hs_name': tr_hs_name,
                       'house_data': set_signs(list(houses[0]), house_names),
                       'tr_mode': tr_m, 'tr_country': transit_country}

            return render(request, 'transit_chart_ev_hs.html', context)

    return render(request, 'transit_form.html',
                  context={'tr_form': tr_form})


def one_color_chart(request):
    zodiac_oc_form = OneColorZodiacRing(request.POST or None)

    if zodiac_oc_form.is_valid():

        zf_city = zodiac_oc_form.cleaned_data['oc_chart_city']
        zf_country = zodiac_oc_form.cleaned_data['oc_chart_country']
        zf_date = zodiac_oc_form.cleaned_data['oc_chart_date']
        zf_mode = int(zodiac_oc_form.cleaned_data['one_clr_zr_chart_mode'])
        zf_hs = zodiac_oc_form.cleaned_data['one_clr_zr_chart_hs']
        clr_ch_hs_name = HOUSE_SYSTEM_CHOICES.get(zf_hs)
        mode_choice = MODE_CHOICES.get(zf_mode)
        hs_en = zf_hs.encode('utf-8')

        get_loc = loc.geocode(f'{zf_city, zf_country}', timeout=7000)

        loc_tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
        local_dt = zf_date.replace(tzinfo=ZoneInfo(loc_tz))
        utc_dt = local_dt.astimezone(datetime.timezone.utc)
        jd = jl.to_jd(utc_dt, fmt='jd')

        zf_face_color = zodiac_oc_form.cleaned_data['face_color']
        zf_edge_color = zodiac_oc_form.cleaned_data['edge_color']
        zf_text_color = zodiac_oc_form.cleaned_data['text_color']
        zf_tick_color = zodiac_oc_form.cleaned_data['tick_color']
        zf_deg_color = zodiac_oc_form.cleaned_data['deg_color']
        zf_font_size = zodiac_oc_form.cleaned_data['font_size']
        zf_line_width = zodiac_oc_form.cleaned_data['line_width']

        zf_marker_color = zodiac_oc_form.cleaned_data['marker_color']  #build_aspects
        zf_symbol_color = zodiac_oc_form.cleaned_data['symbol_color']
        zf_marker_size = zodiac_oc_form.cleaned_data['marker_size']
        zf_symbol_size = zodiac_oc_form.cleaned_data['symbol_size']

        zf_house_ax_color = zodiac_oc_form.cleaned_data['house_ax_color']  #tick params draw_chart
        zf_house_num_color = zodiac_oc_form.cleaned_data['house_number_color']  #tick params
        zf_house_ax_lw = zodiac_oc_form.cleaned_data['house_ax_lw']
        zf_house_num_fs = zodiac_oc_form.cleaned_data['house_num_fs']

        zf_house_track_lw = zodiac_oc_form.cleaned_data['house_track_lw']
        zf_house_track_color = zodiac_oc_form.cleaned_data['house_track_color']

        img = draw_zodiac_one_color(zf_face_color, zf_edge_color,
                                    zf_text_color, zf_tick_color,
                                    zf_deg_color, zf_font_size, zf_line_width)

        matplotlib.rcParams['axes.edgecolor'] = zf_house_track_color
        matplotlib.rcParams['axes.linewidth'] = zf_house_track_lw

        planet_data = get_planet_data(jd, zf_mode)
        coords_value = list(planet_data.values())

        if zf_hs != 'Without houses':
            houses = swe.houses_ex(jd, get_loc.latitude,
                                   get_loc.longitude, hs_en, int(zf_mode))
            fig_form, planet_ax, house_ax, _, _, _, _, _, _ = \
                draw_chart(fig_name='fig_form',
                           planet_ax='planet_ax',
                           house_ax='house_ax',
                           ha_color=zf_house_ax_color,
                           ha_lbl_size=zf_house_num_fs,
                           ha_lw=zf_house_ax_lw,
                           ha_lab_cl=zf_house_num_color,
                           chart_path=img,
                           houses_data=houses[0])

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, = \
                build_aspects(planet_data=planet_data, ax_name=planet_ax,
                              marker_clr=zf_marker_color,
                              pl_marker_size=zf_marker_size,
                              symbol_size=zf_symbol_size,
                              symbol_clr=zf_symbol_color)

            swe.close()

            graph, _ = get_graph(fig_form)

            return render(request, 'designed_oc_chart.html',
                          context={'planet_data': set_signs(planet_names,
                                                            [p[4] for p in coords_value]),
                                   'house_data': set_signs(house_names, list(houses[0])),
                                   'ats': aspect_table_s, 'ato': aspect_table_ops,
                                   'att': aspect_table_t, 'atc': aspect_table_c,
                                   'date': zf_date.strftime("%B %d, %Y, %H:%M:%S, %A"),
                                   'planet_names': planet_names, 'mode': mode_choice,
                                   'hs_name': clr_ch_hs_name, 'graph': graph,
                                   'city': zf_city, 'country': zf_country})

        elif zf_hs == 'Without houses':

            fig_form, planet_ax, _, _, _, _, _, _, _ = (
                draw_chart(fig_name='fig_form',
                           planet_ax='planet_ax',
                           ha_color=zf_house_ax_color,
                           ha_lbl_size=zf_house_num_fs,
                           ha_lw=zf_house_ax_lw,
                           ha_lab_cl=zf_house_num_color,
                           chart_path=img))

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, = \
                build_aspects(planet_data=planet_data, ax_name=planet_ax)

            swe.close()

            graph, _ = get_graph(fig_form)

            return render(request, 'designed_oc_chart_wh.html',
                          context={'planet_data': set_signs(planet_names,
                                                            [p[4] for p in coords_value]),
                                   'ats': aspect_table_s, 'ato': aspect_table_ops,
                                   'att': aspect_table_t, 'atc': aspect_table_c,
                                   'date': zf_date.strftime("%B %d, %Y, %H:%M:%S, %A"),
                                   'planet_names': planet_names, 'mode': mode_choice,
                                   'hs_name': clr_ch_hs_name, 'graph': graph,
                                   'city': zf_city, 'country': zf_country, })

    return render(request, 'design_one_clr_ch.html', {'z_form': zodiac_oc_form})


def chart_detail(request, id):
    chart = get_object_or_404(FullChart, id=id)
    username = request.user.username

    if request.method == 'POST':
        chart.delete()
        messages.success(request, 'Chart deleted')
        return redirect('user lounge', username=username)

    context = {'chart': chart}

    if chart.house_system == 'Without houses':
        return render(request, 'user_chart_db_dtl_wh.html', context)

    return render(request, 'user_chart_db_detail.html', context)


def tr_chart_detail(request, id):
    tr_chart_db_dtl = TransitFullChart.objects.get(id=id)

    eo_hs = HOUSE_SYSTEM_CHOICES.get(tr_chart_db_dtl.ev_house_system)
    et_hs = HOUSE_SYSTEM_CHOICES.get(tr_chart_db_dtl.tr_house_system)

    username = request.user.username

    if request.method == 'POST':
        tr_chart_db_dtl.delete()
        messages.success(request, 'Chart deleted')
        return redirect('user lounge', username=username)

    context = {'tr_chart': tr_chart_db_dtl,
               'eo_hs': eo_hs, 'et_hs': et_hs}

    if (tr_chart_db_dtl.ev_house_system == 'Without houses'
        and tr_chart_db_dtl.tr_house_system == 'Without houses'):
        return render(request, 'transit_chart_db_detail_nh.html', context)
    elif (tr_chart_db_dtl.ev_house_system == 'Without houses'
          and tr_chart_db_dtl.tr_house_system != 'Without houses'):
        return render(request, 'transit_chart_db_detail_th.html', context)
    elif (tr_chart_db_dtl.ev_house_system != 'Without houses'
          and tr_chart_db_dtl.tr_house_system == 'Without houses'):
        return render(request, 'transit_chart_db_detail_eh.html', context)
    else:
        return render(request, 'transit_chart_db_detail.html', context)


def clr_chart_detail(request, id):
    clr_chart_dtl = get_object_or_404(OneColorZodiacRingMF, id=id)
    hs = HOUSE_SYSTEM_CHOICES.get(clr_chart_dtl.chart_house_system)

    if request.method == 'POST':
        clr_chart_dtl.delete()
        messages.success(request, 'Chart deleted')
        return redirect('user lounge', username=request.user.username)

    context = {'clr_chart': clr_chart_dtl, 'hs': hs}

    if clr_chart_dtl.chart_house_system == 'Without houses':
        return render(request, 'user_clr_chart_db_dtl_wh.html', context)
    return render(request, 'user_clr_chart_db_dtl.html', context)


def user_chart_lists(request):
    my_charts = (
        FullChart.objects.filter(drawer__id=request.user.id))
    my_tr_charts = (
        TransitFullChart.objects.filter(drawer__id=request.user.id))
    my_clr_charts = (
        OneColorZodiacRingMF.objects.filter(drawer__id=request.user.id))

    return render(request, 'user_chart_lists.html',
                  {'my_charts': my_charts,
                   'my_tr_charts': my_tr_charts,
                   'my_clr_charts': my_clr_charts})

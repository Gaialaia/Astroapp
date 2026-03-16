import io, os
import boto3, uuid


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout, authenticate
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm
from .decorators import user_not_auth

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import swisseph as swe
import julian as jl


from geopy.geocoders import Nominatim

from astroplan.models import (Chart, TransitChart, FullChart,
                              TransitFullChart, OneColorZodiacRingMF,
                              HOUSE_SYSTEM_CHOICES, MODE_CHOICES)

from astroplan.forms import (FullChartForm, TransitFullChartForm,
                             OneColorZodiacRingFM)

from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo

from .utils import draw_zodiac_one_color, get_s3_client, upload_to_storage
from astroplan.utils import (get_planet_data,
                    build_aspects, draw_chart, get_graph, build_transit_aspects,
                    draw_transit_chart, set_signs)

from astroknow import settings
import datetime

flags =  swe.FLG_SIDEREAL | swe.SIDM_LAHIRI

planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter',
                'Saturn', 'Uranus', 'Neptune', 'Pluto']

tr_planet_names = ['tr_Sun','tr_Moon', 'tr_Mercury', 'tr_Venus', 'tr_Mars',
                   'tr_Jupiter', 'tr_Saturn', 'tr_Uranus', 'tr_Neptune', 'tr_Pluto']

house_names = ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII']

tf = TimezoneFinder()
loc = Nominatim(user_agent="GetLoc")


swe.set_ephe_path('/home/gaia/Документы/eph files')


def activate(request, uidb64, token):

    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        (messages.success
         (request, "E-mail's been confirmed. Please, log in."))
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('showed chart')


def activate_email(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

@user_not_auth
def register(request):
    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save(commit=False)
            user.is_active = False
            user.save()
            # login(request, user)
            activate_email(request, user, reg_form.cleaned_data.get('email'))
            messages.success(request, f"New account created: {user.username}")
            return redirect('showed chart')
        else:
            for error in list(reg_form.errors.values()):
                messages.error(request, error)

    else:
        reg_form = UserRegistrationForm()

    return render(request,"register.html",{"reg_form":reg_form})


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, 'You have logged out')
    return redirect('showed chart')

@user_not_auth
def custom_login(request):

    if request.method == 'POST':
        auth_form = UserLoginForm(request=request, data=request.POST)
        if auth_form.is_valid():
            user = authenticate(
                username=auth_form.cleaned_data['username'],
                password=auth_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f' Welcome, {user.username}')
                return redirect('user lounge',user.username)


        else:
            for error in list(auth_form.errors.values()):
                messages.error(request, error)
        # auth_form.clean()
    auth_form = UserLoginForm()

    return render(request,'login.html', {'auth_form': auth_form})



def user_chart_for_date_form(request):

    username = request.user.username

    user_chart_form = FullChartForm(request.POST or None, request.FILES or None)

    if user_chart_form.is_valid():

        chart = user_chart_form.save(commit=False)
        get_loc = loc.geocode(f'{chart.city, chart.country}', timeout=7000)
        d = chart.chart_date
        us_hs = chart.house_system.encode('utf-8')
        house_system = HOUSE_SYSTEM_CHOICES.get(chart.house_system)
        mode = MODE_CHOICES.get(chart.chart_mode)

        chart.drawer = get_object_or_404(get_user_model(),username=username)
        loc_tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
        local_dt = d.replace(tzinfo=ZoneInfo(loc_tz))

        utc_dt = local_dt.astimezone(datetime.timezone.utc)
        jd = jl.to_jd(utc_dt, fmt='jd')

        planet_data = get_planet_data(jd, chart.chart_mode)
        planet_data_values = list(planet_data.values())

        planet_data_for_db = [(set_signs(planet_names, [p[4] for p in planet_data_values]))]

        chart.Sun_deg = planet_data_for_db[0][0][1]
        chart.Sun_sign = f' {planet_data_for_db[0][0][2]}'

        chart.Moon_deg = f'{planet_data_for_db[0][1][1]}'
        chart.Moon_sign = planet_data_for_db[0][1][2]

        chart.Mercury_deg = f'{planet_data_for_db[0][2][1]}'
        chart.Mercury_sign = planet_data_for_db[0][2][2]

        chart.Venus_deg = f'{planet_data_for_db[0][3][1]}'
        chart.Venus_sign = planet_data_for_db[0][3][2]

        chart.Mars_deg = planet_data_for_db[0][4][1]
        chart.Mars_sign = planet_data_for_db[0][4][2]

        chart.Jupiter_deg = f'{planet_data_for_db[0][5][1]}'
        chart.Jupiter_sign = planet_data_for_db[0][5][2]

        chart.Saturn_deg = f'{planet_data_for_db[0][6][1]}'
        chart.Saturn_sign = planet_data_for_db[0][6][2]

        chart.Uranus_sign = f'{planet_data_for_db[0][7][1]}'
        chart.Uranus_deg = planet_data_for_db[0][7][2]

        chart.Neptune_deg = f'{planet_data_for_db[0][8][1]}'
        chart.Neptune_sign = planet_data_for_db[0][8][2]

        chart.Pluto_deg = f'{planet_data_for_db[0][9][1]}'
        chart.Pluto_sign = planet_data_for_db[0][9][2]

        if chart.house_system != 'Without houses':

            houses = swe.houses_ex(jd, get_loc.latitude, get_loc.longitude, us_hs, (int(chart.chart_mode)))

            fig_form, planet_ax, house_ax, _, _, _, _, _,_ = draw_chart(fig_name='fig_form', planet_ax='planet_ax',
                                                                         house_ax='house_ax', houses_data=houses[0])

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, = \
                build_aspects(ax_name=planet_ax, planet_data=planet_data)

            graph, buffer = get_graph(fig_form)
            plot_name = f'{chart.drawer}_{d}.png'
            chart.chart_image.save(plot_name, ContentFile(buffer.getvalue()), save=True)
            buffer.close()
            user_chart_form.save()

            swe.close()

            hc_data_for_db = [set_signs(house_names, list(houses[0]))]

            chart.first_house = hc_data_for_db[0][0][0]
            chart.asc_deg = hc_data_for_db[0][0][1]
            chart.asc_sign = hc_data_for_db[0][0][2]

            chart.second_house = hc_data_for_db[0][1][0]
            chart.resource_deg = hc_data_for_db[0][1][1]
            chart.resource_sign = hc_data_for_db[0][1][2]

            chart.third_house = hc_data_for_db[0][2][0]
            chart.mental_deg = hc_data_for_db[0][2][1]
            chart.mental_sign = hc_data_for_db[0][2][2]

            chart.forth_house = hc_data_for_db[0][3][0]
            chart.home_deg = hc_data_for_db[0][3][1]
            chart.home_sign = hc_data_for_db[0][3][2]

            chart.fifth_house = hc_data_for_db[0][4][0]
            chart.game_deg = hc_data_for_db[0][4][1]
            chart.game_sign = hc_data_for_db[0][4][2]

            chart.sixth_house = hc_data_for_db[0][5][0]
            chart.work_deg = hc_data_for_db[0][5][1]
            chart.work_sign = hc_data_for_db[0][5][2]

            chart.seventh_house = hc_data_for_db[0][6][0]
            chart.rel_deg = hc_data_for_db[0][6][1]
            chart.rel_sign = hc_data_for_db[0][6][2]

            chart.eighth_house = hc_data_for_db[0][7][0]
            chart.magic_deg = hc_data_for_db[0][7][1]
            chart.magic_sign = hc_data_for_db[0][7][2]

            chart.nineth_house = hc_data_for_db[0][8][0]
            chart.esoteric_deg = hc_data_for_db[0][8][1]
            chart.esoteric_sign = hc_data_for_db[0][8][2]

            chart.tenth_house = hc_data_for_db[0][9][0]
            chart.status_deg = hc_data_for_db[0][9][1]
            chart.status_sign = hc_data_for_db[0][9][2]

            chart.eleventh_house = hc_data_for_db[0][10][0]
            chart.interests_deg = hc_data_for_db[0][10][1]
            chart.interests_sign = hc_data_for_db[0][10][2]

            chart.twelfth_house = hc_data_for_db[0][11][0]
            chart.benefits_deg = hc_data_for_db[0][11][1]
            chart.benefits_sign = hc_data_for_db[0][11][2]

            chart.save()

            return render(request, 'user_chart.html', { 'planet_data': set_signs(planet_names,
                                                  [p[4] for p in planet_data_values]),
                                                 'house_data': set_signs(house_names, list(houses[0])),
                                                 'ats': aspect_table_s, 'ato': aspect_table_ops,
                                                 'att': aspect_table_t, 'atc': aspect_table_c, 'date': d,
                                                  'chart':chart, 'house_system': house_system,
                                                  'mode': mode, 'graph':graph})

        else:
            fig_form, planet_ax, _, _, _, _, _, _, _ = draw_chart(fig_name='fig_form', planet_ax='planet_ax')

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, = \
                build_aspects(planet_data=planet_data, ax_name=planet_ax)

            swe.close()

            graph, buffer = get_graph(fig_form)
            plot_name = f'{chart.drawer}_{d}.png'
            chart.chart_image.save(plot_name, ContentFile(buffer.getvalue()), save=True)
            buffer.close()

            user_chart_form.save()

            return render(request, 'user_chart_nh.html', {'planet_data': set_signs(planet_names, [p[4] for p in planet_data_values]),
                                                       'ats': aspect_table_s, 'ato': aspect_table_ops,
                                                       'att': aspect_table_t, 'atc': aspect_table_c, 'date': d,
                                                        'chart': chart, 'house_system': house_system,
                                                        'mode': mode, 'graph': graph})

    return render(request, 'user_chart_for_date_form.html', {'user_chart_form': user_chart_form })


def user_lounge(request, username):

    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form.username}, Your profile has been updated!')
            return redirect('user lounge', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()

    if user:
        form = UserUpdateForm(instance=user)
        form.fields['description'].widget.attrs = {'rows': 1}
        return render(request, 'user_lounge.html', context={'form': form})

    return render(request, 'user_lounge.html')


def user_transit_chart_form(request):

    username = request.user.username
    tr_form = TransitFullChartForm(request.POST or None, request.FILES or None)

    if tr_form.is_valid():

        tr_form.save()

        tr_user_chart = TransitFullChart.objects.last()

        ev_d = tr_user_chart.event_date
        tr_uc_ev_hs = tr_user_chart.ev_house_system.encode('utf-8')
        eo_hs = HOUSE_SYSTEM_CHOICES.get(tr_user_chart.ev_house_system)
        tr_mode = MODE_CHOICES.get(tr_user_chart.tr_chart_mode)

        tr_d = tr_user_chart.transit_date
        tr_uc_tr_hs = tr_user_chart.tr_house_system.encode('utf-8')
        et_hs = HOUSE_SYSTEM_CHOICES.get(tr_user_chart.tr_house_system)
        ev_mode = MODE_CHOICES.get(tr_user_chart.ev_chart_mode)

        ev_get_loc = loc.geocode(f'{tr_user_chart.event_city, tr_user_chart.event_country}', timeout=7000)
        ev_loc_tz = tf.timezone_at(lng=ev_get_loc.longitude, lat=ev_get_loc.latitude)
        ev_local_dt = ev_d.replace(tzinfo=ZoneInfo(ev_loc_tz))
        ev_utc_dt = ev_local_dt.astimezone(datetime.timezone.utc)
        jd_ev = jl.to_jd(ev_utc_dt, fmt='jd')

        tr_get_loc = loc.geocode(f'{tr_user_chart.transit_city, tr_user_chart.transit_country}', timeout=7000)
        tr_loc_tz = tf.timezone_at(lng=tr_get_loc.longitude, lat=tr_get_loc.latitude)
        tr_local_dt = tr_d.replace(tzinfo=ZoneInfo(tr_loc_tz))
        tr_utc_dt = tr_local_dt.astimezone(datetime.timezone.utc)
        jd_tr = jl.to_jd(tr_utc_dt, fmt='jd')

        tr_user_chart.drawer = get_object_or_404(get_user_model(), username=username)

        event_data = get_planet_data(jd_ev, tr_user_chart.ev_chart_mode)
        transit_data = get_planet_data(jd_tr, tr_user_chart.tr_chart_mode)

        ev_d_val = list(event_data.values())
        tr_d_val = list(transit_data.values())



        planet_data_for_db = [(set_signs(planet_names, [p[4] for p in ev_d_val]))]

        tr_user_chart.Sun_deg = planet_data_for_db[0][0][1]
        tr_user_chart.Sun_sign = f' {planet_data_for_db[0][0][2]}'

        tr_user_chart.Moon_deg = f'{planet_data_for_db[0][1][1]}'
        tr_user_chart.Moon_sign = planet_data_for_db[0][1][2]

        tr_user_chart.Mercury_deg = f'{planet_data_for_db[0][2][1]}'
        tr_user_chart.Mercury_sign = planet_data_for_db[0][2][2]

        tr_user_chart.Venus_deg = f'{planet_data_for_db[0][3][1]}'
        tr_user_chart.Venus_sign = planet_data_for_db[0][3][2]

        tr_user_chart.Mars_deg = planet_data_for_db[0][4][1]
        tr_user_chart.Mars_sign = planet_data_for_db[0][4][2]

        tr_user_chart.Jupiter_deg = f'{planet_data_for_db[0][5][1]}'
        tr_user_chart.Jupiter_sign = planet_data_for_db[0][5][2]

        tr_user_chart.Saturn_deg = f'{planet_data_for_db[0][6][1]}'
        tr_user_chart.Saturn_sign = planet_data_for_db[0][6][2]

        tr_user_chart.Uranus_sign = f'{planet_data_for_db[0][7][1]}'
        tr_user_chart.Uranus_deg = planet_data_for_db[0][7][2]

        tr_user_chart.Neptune_deg = f'{planet_data_for_db[0][8][1]}'
        tr_user_chart.Neptune_sign = planet_data_for_db[0][8][2]

        tr_user_chart.Pluto_deg = f'{planet_data_for_db[0][9][1]}'
        tr_user_chart.Pluto_sign = planet_data_for_db[0][9][2]

        tr_planet_data_for_db = [(set_signs(planet_names, [p[4] for p in tr_d_val]))]

        tr_user_chart.tr_Sun_deg = tr_planet_data_for_db[0][0][1]
        tr_user_chart.tr_Sun_sign = tr_planet_data_for_db[0][0][2]

        tr_user_chart.tr_Moon_deg = tr_planet_data_for_db[0][1][1]
        tr_user_chart.tr_Moon_sign = tr_planet_data_for_db[0][1][2]

        tr_user_chart.tr_Mercury_deg = tr_planet_data_for_db[0][2][1]
        tr_user_chart.tr_Mercury_sign = tr_planet_data_for_db[0][2][2]

        tr_user_chart.tr_Venus_deg = tr_planet_data_for_db[0][3][1]
        tr_user_chart.tr_Venus_sign = tr_planet_data_for_db[0][3][2]

        tr_user_chart.tr_Mars_deg = tr_planet_data_for_db[0][4][1]
        tr_user_chart.tr_Mars_sign = tr_planet_data_for_db[0][4][2]

        tr_user_chart.tr_Jupiter_deg = tr_planet_data_for_db[0][5][1]
        tr_user_chart.tr_Jupiter_sign = tr_planet_data_for_db[0][5][2]

        tr_user_chart.tr_Saturn_deg = tr_planet_data_for_db[0][6][1]
        tr_user_chart.tr_Saturn_sign = tr_planet_data_for_db[0][6][2]

        tr_user_chart.tr_Uranus_deg = tr_planet_data_for_db[0][7][1]
        tr_user_chart.tr_Uranus_sign = tr_planet_data_for_db[0][7][2]

        tr_user_chart.tr_Neptune_deg = tr_planet_data_for_db[0][8][1]
        tr_user_chart.tr_Neptune_sign = tr_planet_data_for_db[0][8][2]

        tr_user_chart.tr_Pluto_deg = tr_planet_data_for_db[0][9][1]
        tr_user_chart.tr_Pluto_sign = tr_planet_data_for_db[0][9][1]

        if tr_user_chart.ev_house_system == 'Without houses' and tr_user_chart.tr_house_system == 'Without houses':
            tr_fig, event_one_ax, event_two_ax, _, _ = (
                draw_transit_chart('event_one_ax', 'event_two_ax'))

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, \
                event_one_pp, event_two_pp = (
                build_transit_aspects(event_one_data=event_data, event_two_data=transit_data,
                                      event_one_ax=event_one_ax, event_two_ax=event_two_ax,
                                      fig=tr_fig))


            graph, buffer = get_graph(tr_fig)
            plot_name = f'{tr_user_chart.drawer}_{ev_d}.png'
            tr_user_chart.tr_chart_image.save(plot_name, ContentFile(buffer.getvalue()), save=True)
            buffer.close()
            tr_user_chart.save()

            context = {'planet_data': set_signs(planet_names, [p[4] for p in ev_d_val]),
                       'ats': aspect_table_s, 'ato': aspect_table_ops,
                       'att': aspect_table_t, 'atc': aspect_table_c,
                       'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_d_val]),
                       'event_date': ev_d,
                       'event_city': tr_user_chart.event_city,
                       'event_country': tr_user_chart.event_country,
                       'tr_date': tr_d, 'tr_city': tr_user_chart.transit_city,
                       'tr_country': tr_user_chart.transit_country,
                       'tr_uc_tr_name': tr_user_chart.event_name,
                       'tr_uc_ev_name': tr_user_chart.transit_name,
                       'tr_mode': tr_mode, 'ev_mode': ev_mode,
                       'graph': graph}


            return render(request, 'tr_user_chart_dtl_wh.html', context)


        if tr_user_chart.ev_house_system != 'Without houses' and tr_user_chart.tr_house_system != 'Without houses':

            houses = swe.houses_ex(jd_ev, ev_get_loc.latitude, ev_get_loc.longitude, tr_uc_ev_hs,
                                   int(tr_user_chart.ev_chart_mode))

            tr_houses = swe.houses_ex(jd_tr, tr_get_loc.latitude, tr_get_loc.longitude, tr_uc_tr_hs,
                                      int(tr_user_chart.tr_chart_mode))

            tr_fig, event_one_ax, event_two_ax, event_one_ha, event_two_ha = (
                draw_transit_chart(event_one_ax='event_one_ax',
                                   event_two_ax='event_two_ax',
                                   event_one_ha='event_one_ha',
                                   event_two_ha='event_two_ha',
                                   event_one_houses=houses[0],
                                   event_two_houses=tr_houses[0]))

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, \
                event_one_pp, event_two_pp = build_transit_aspects(event_one_data=event_data,
                                                                   event_two_data=transit_data,
                                                                   event_one_ax=event_one_ax,
                                                                   event_two_ax=event_two_ax,
                                                                   fig=tr_fig)
            graph, buffer = get_graph(tr_fig)
            plot_name = f'{tr_user_chart.drawer}_{ev_d}.png'
            tr_user_chart.tr_chart_image.save(plot_name, ContentFile(buffer.getvalue()), save=True)
            buffer.close()
            tr_user_chart.save()

            hc_data_for_db = [set_signs(house_names, list(houses[0]))]

            tr_user_chart.first_house = hc_data_for_db[0][0][0]
            tr_user_chart.asc_deg = hc_data_for_db[0][0][1]
            tr_user_chart.asc_sign = hc_data_for_db[0][0][2]

            tr_user_chart.second_house = hc_data_for_db[0][1][0]
            tr_user_chart.resource_deg = hc_data_for_db[0][1][1]
            tr_user_chart.resource_sign = hc_data_for_db[0][1][2]

            tr_user_chart.third_house = hc_data_for_db[0][2][0]
            tr_user_chart.mental_deg = hc_data_for_db[0][2][1]
            tr_user_chart.mental_sign = hc_data_for_db[0][2][2]

            tr_user_chart.forth_house = hc_data_for_db[0][3][0]
            tr_user_chart.home_deg = hc_data_for_db[0][3][1]
            tr_user_chart.home_sign = hc_data_for_db[0][3][2]

            tr_user_chart.fifth_house = hc_data_for_db[0][4][0]
            tr_user_chart.game_deg = hc_data_for_db[0][4][1]
            tr_user_chart.game_sign = hc_data_for_db[0][4][2]

            tr_user_chart.sixth_house = hc_data_for_db[0][5][0]
            tr_user_chart.work_deg = hc_data_for_db[0][5][1]
            tr_user_chart.work_sign = hc_data_for_db[0][5][2]

            tr_user_chart.seventh_house = hc_data_for_db[0][6][0]
            tr_user_chart.rel_deg = hc_data_for_db[0][6][1]
            tr_user_chart.rel_sign = hc_data_for_db[0][6][2]

            tr_user_chart.eighth_house = hc_data_for_db[0][7][0]
            tr_user_chart.magic_deg = hc_data_for_db[0][7][1]
            tr_user_chart.magic_sign = hc_data_for_db[0][7][2]

            tr_user_chart.nineth_house = hc_data_for_db[0][8][0]
            tr_user_chart.esoteric_deg = hc_data_for_db[0][8][1]
            tr_user_chart.esoteric_sign = hc_data_for_db[0][8][2]

            tr_user_chart.tenth_house = hc_data_for_db[0][9][0]
            tr_user_chart.status_deg = hc_data_for_db[0][9][1]
            tr_user_chart.status_sign = hc_data_for_db[0][9][2]

            tr_user_chart.eleventh_house = hc_data_for_db[0][10][0]
            tr_user_chart.interests_deg = hc_data_for_db[0][10][1]
            tr_user_chart.interests_sign = hc_data_for_db[0][10][2]

            tr_user_chart.twelfth_house = hc_data_for_db[0][11][0]
            tr_user_chart.benefits_deg = hc_data_for_db[0][11][1]
            tr_user_chart.benefits_sign = hc_data_for_db[0][11][2]

            tr_hc_data_for_db = [set_signs(house_names, list(tr_houses[0]))]

            tr_user_chart.tr_first_house = tr_hc_data_for_db[0][0][0]
            tr_user_chart.tr_asc_deg = tr_hc_data_for_db[0][1][1]
            tr_user_chart.tr_asc_sign = tr_hc_data_for_db[0][1][2]

            tr_user_chart.tr_second_house = tr_hc_data_for_db[0][1][0]
            tr_user_chart.tr_resource_deg = tr_hc_data_for_db[0][1][1]
            tr_user_chart.tr_resource_sign = tr_hc_data_for_db[0][1][2]

            tr_user_chart.tr_third_house = tr_hc_data_for_db[0][2][0]
            tr_user_chart.tr_mental_deg = tr_hc_data_for_db[0][2][1]
            tr_user_chart.tr_mental_sign = tr_hc_data_for_db[0][2][2]

            tr_user_chart.tr_forth_house = tr_hc_data_for_db[0][3][0]
            tr_user_chart.tr_home_deg = tr_hc_data_for_db[0][3][1]
            tr_user_chart.tr_home_sign = tr_hc_data_for_db[0][3][2]

            tr_user_chart.tr_fifth_house = tr_hc_data_for_db[0][4][0]
            tr_user_chart.tr_game_deg = tr_hc_data_for_db[0][4][1]
            tr_user_chart.tr_game_sign = tr_hc_data_for_db[0][4][2]

            tr_user_chart.tr_sixth_house = tr_hc_data_for_db[0][5][0]
            tr_user_chart.tr_work_deg = tr_hc_data_for_db[0][5][1]
            tr_user_chart.tr_work_sign = tr_hc_data_for_db[0][5][2]

            tr_user_chart.tr_seventh_house = tr_hc_data_for_db[0][6][0]
            tr_user_chart.tr_rel_deg = tr_hc_data_for_db[0][6][1]
            tr_user_chart.tr_rel_sign = tr_hc_data_for_db[0][6][2]

            tr_user_chart.tr_eighth_house = tr_hc_data_for_db[0][7][0]
            tr_user_chart.tr_magic_deg = tr_hc_data_for_db[0][7][1]
            tr_user_chart.tr_magic_sign = tr_hc_data_for_db[0][7][2]

            tr_user_chart.tr_nineth_house = tr_hc_data_for_db[0][8][0]
            tr_user_chart.tr_esoteric_deg = tr_hc_data_for_db[0][8][1]
            tr_user_chart.tr_esoteric_sign = tr_hc_data_for_db[0][8][2]

            tr_user_chart.tr_tenth_house = tr_hc_data_for_db[0][9][0]
            tr_user_chart.tr_status_deg = tr_hc_data_for_db[0][9][1]
            tr_user_chart.tr_status_sign = tr_hc_data_for_db[0][9][2]

            tr_user_chart.tr_eleventh_house = tr_hc_data_for_db[0][10][0]
            tr_user_chart.tr_interests_deg = tr_hc_data_for_db[0][10][1]
            tr_user_chart.tr_interests_sign = tr_hc_data_for_db[0][10][2]

            tr_user_chart.tr_twelfth_house = tr_hc_data_for_db[0][11][0]
            tr_user_chart.tr_benefits_deg = tr_hc_data_for_db[0][11][1]
            tr_user_chart.tr_benefits_sign = tr_hc_data_for_db[0][11][2]

            tr_user_chart.save()

            context = {'planet_data': set_signs(planet_names, [p[4] for p in ev_d_val]),
                       'house_data': set_signs(house_names, list(houses[0])),
                       'tr_house_data': set_signs(house_names, list(tr_houses[0])),
                       'ats': aspect_table_s, 'ato': aspect_table_ops,
                       'att': aspect_table_t, 'atc': aspect_table_c,
                       'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_d_val]),
                       'event_date': ev_d, 'tr_date': tr_d,
                       'event_city': tr_user_chart.event_city,
                       'event_country': tr_user_chart.event_country,
                       'tr_city': tr_user_chart.transit_city,
                       'tr_country': tr_user_chart.transit_country,
                       'tr_uc_tr_name': tr_user_chart.event_name,
                       'tr_uc_ev_name': tr_user_chart.transit_name,
                       'tr_mode': tr_mode, 'ev_mode': ev_mode,
                       'graph': graph, 'ev_one_hs': eo_hs, 'ev_two_hs': et_hs }

            return render(request, 'tr_user_chart_dtl.html', context)

        elif tr_user_chart.ev_house_system == 'Without houses' and tr_user_chart.tr_house_system:

            tr_houses = swe.houses_ex(jd_tr, tr_get_loc.latitude, tr_get_loc.longitude, tr_uc_tr_hs,
                                      int(tr_user_chart.tr_chart_mode))

            tr_hc_data_for_db = [set_signs(house_names, list(tr_houses[0]))]

            tr_user_chart.tr_first_house = tr_hc_data_for_db[0][0][0]
            tr_user_chart.tr_asc_deg = tr_hc_data_for_db[0][1][1]
            tr_user_chart.tr_asc_sign = tr_hc_data_for_db[0][1][2]

            tr_user_chart.tr_second_house = tr_hc_data_for_db[0][1][0]
            tr_user_chart.tr_resource_deg = tr_hc_data_for_db[0][1][1]
            tr_user_chart.tr_resource_sign = tr_hc_data_for_db[0][1][2]

            tr_user_chart.tr_third_house = tr_hc_data_for_db[0][2][0]
            tr_user_chart.tr_mental_deg = tr_hc_data_for_db[0][2][1]
            tr_user_chart.tr_mental_sign = tr_hc_data_for_db[0][2][2]

            tr_user_chart.tr_forth_house = tr_hc_data_for_db[0][3][0]
            tr_user_chart.tr_home_deg = tr_hc_data_for_db[0][3][1]
            tr_user_chart.tr_home_sign = tr_hc_data_for_db[0][3][2]

            tr_user_chart.tr_fifth_house = tr_hc_data_for_db[0][4][0]
            tr_user_chart.tr_game_deg = tr_hc_data_for_db[0][4][1]
            tr_user_chart.tr_game_sign = tr_hc_data_for_db[0][4][2]

            tr_user_chart.tr_sixth_house = tr_hc_data_for_db[0][5][0]
            tr_user_chart.tr_work_deg = tr_hc_data_for_db[0][5][1]
            tr_user_chart.tr_work_sign = tr_hc_data_for_db[0][5][2]

            tr_user_chart.tr_seventh_house = tr_hc_data_for_db[0][6][0]
            tr_user_chart.tr_rel_deg = tr_hc_data_for_db[0][6][1]
            tr_user_chart.tr_rel_sign = tr_hc_data_for_db[0][6][2]

            tr_user_chart.tr_eighth_house = tr_hc_data_for_db[0][7][0]
            tr_user_chart.tr_magic_deg = tr_hc_data_for_db[0][7][1]
            tr_user_chart.tr_magic_sign = tr_hc_data_for_db[0][7][2]

            tr_user_chart.tr_nineth_house = tr_hc_data_for_db[0][8][0]
            tr_user_chart.tr_esoteric_deg = tr_hc_data_for_db[0][8][1]
            tr_user_chart.tr_esoteric_sign = tr_hc_data_for_db[0][8][2]

            tr_user_chart.tr_tenth_house = tr_hc_data_for_db[0][9][0]
            tr_user_chart.tr_status_deg = tr_hc_data_for_db[0][9][1]
            tr_user_chart.tr_status_sign = tr_hc_data_for_db[0][9][2]

            tr_user_chart.tr_eleventh_house = tr_hc_data_for_db[0][10][0]
            tr_user_chart.tr_interests_deg = tr_hc_data_for_db[0][10][1]
            tr_user_chart.tr_interests_sign = tr_hc_data_for_db[0][10][2]

            tr_user_chart.tr_twelfth_house = tr_hc_data_for_db[0][11][0]
            tr_user_chart.tr_benefits_deg = tr_hc_data_for_db[0][11][1]
            tr_user_chart.tr_benefits_sign = tr_hc_data_for_db[0][11][2]

            tr_fig, event_one_ax, event_two_ax, _, event_two_ha = (
                draw_transit_chart(event_one_ax='event_one_ax',
                                   event_two_ax='event_two_ax',
                                   event_two_ha='event_two_ha',
                                   event_two_houses=tr_houses[0]))

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, \
                event_one_pp, event_two_pp = build_transit_aspects(event_one_data=event_data,
                                                                   event_two_data=transit_data,
                                                                   event_one_ax=event_one_ax,
                                                                   event_two_ax=event_two_ax,
                                                                   fig=tr_fig)

            graph, buffer = get_graph(tr_fig)
            plot_name = f'{tr_user_chart.drawer}_{ev_d}.png'
            tr_user_chart.tr_chart_image.save(plot_name, ContentFile(buffer.getvalue()), save=True)
            buffer.close()
            tr_user_chart.save()

            context = {'planet_data': set_signs(planet_names, [p[4] for p in ev_d_val]),
                       'tr_house_data': set_signs(house_names, list(tr_houses[0])),
                       'ats': aspect_table_s, 'ato': aspect_table_ops,
                       'att': aspect_table_t, 'atc': aspect_table_c,
                       'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_d_val]),
                       'event_date': ev_d, 'tr_date': tr_d,
                       'event_city': tr_user_chart.event_city,
                       'event_country': tr_user_chart.event_country,
                       'tr_city': tr_user_chart.transit_city,
                       'tr_country': tr_user_chart.transit_country,
                       'tr_uc_tr_name': tr_user_chart.event_name,
                       'tr_uc_ev_name': tr_user_chart.transit_name,
                       'tr_mode': tr_mode, 'ev_mode': ev_mode,
                       'graph': graph, 'ev_two_hs': et_hs }

            return render(request, 'tr_user_chart_dtl_th.html', context)



        elif tr_user_chart.tr_house_system == 'Without houses' and tr_user_chart.ev_house_system:

            houses = swe.houses_ex(jd_ev, ev_get_loc.latitude, ev_get_loc.longitude, tr_uc_ev_hs,
                                   int(tr_user_chart.ev_chart_mode))

            hc_data_for_db = [set_signs(house_names, list(houses[0]))]

            tr_user_chart.first_house = hc_data_for_db[0][0][0]
            tr_user_chart.asc_deg = hc_data_for_db[0][0][1]
            tr_user_chart.asc_sign = hc_data_for_db[0][0][2]

            tr_user_chart.second_house = hc_data_for_db[0][1][0]
            tr_user_chart.resource_deg = hc_data_for_db[0][1][1]
            tr_user_chart.resource_sign = hc_data_for_db[0][1][2]

            tr_user_chart.third_house = hc_data_for_db[0][2][0]
            tr_user_chart.mental_deg = hc_data_for_db[0][2][1]
            tr_user_chart.mental_sign = hc_data_for_db[0][2][2]

            tr_user_chart.forth_house = hc_data_for_db[0][3][0]
            tr_user_chart.home_deg = hc_data_for_db[0][3][1]
            tr_user_chart.home_sign = hc_data_for_db[0][3][2]

            tr_user_chart.fifth_house = hc_data_for_db[0][4][0]
            tr_user_chart.game_deg = hc_data_for_db[0][4][1]
            tr_user_chart.game_sign = hc_data_for_db[0][4][2]

            tr_user_chart.sixth_house = hc_data_for_db[0][5][0]
            tr_user_chart.work_deg = hc_data_for_db[0][5][1]
            tr_user_chart.work_sign = hc_data_for_db[0][5][2]

            tr_user_chart.seventh_house = hc_data_for_db[0][6][0]
            tr_user_chart.rel_deg = hc_data_for_db[0][6][1]
            tr_user_chart.rel_sign = hc_data_for_db[0][6][2]

            tr_user_chart.eighth_house = hc_data_for_db[0][7][0]
            tr_user_chart.magic_deg = hc_data_for_db[0][7][1]
            tr_user_chart.magic_sign = hc_data_for_db[0][7][2]

            tr_user_chart.nineth_house = hc_data_for_db[0][8][0]
            tr_user_chart.esoteric_deg = hc_data_for_db[0][8][1]
            tr_user_chart.esoteric_sign = hc_data_for_db[0][8][2]

            tr_user_chart.tenth_house = hc_data_for_db[0][9][0]
            tr_user_chart.status_deg = hc_data_for_db[0][9][1]
            tr_user_chart.status_sign = hc_data_for_db[0][9][2]

            tr_user_chart.eleventh_house = hc_data_for_db[0][10][0]
            tr_user_chart.interests_deg = hc_data_for_db[0][10][1]
            tr_user_chart.interests_sign = hc_data_for_db[0][10][2]

            tr_user_chart.twelfth_house = hc_data_for_db[0][11][0]
            tr_user_chart.benefits_deg = hc_data_for_db[0][11][1]
            tr_user_chart.benefits_sign = hc_data_for_db[0][11][2]

            tr_fig, event_one_ax, event_two_ax, event_one_ha, _ = (
                draw_transit_chart(event_one_ax='event_one_ax',
                                   event_two_ax='event_two_ax',
                                   event_one_ha='event_one_ha',
                                   event_one_houses=houses[0],
                                   ))

            aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, \
                event_one_pp, event_two_pp = build_transit_aspects(event_one_data=event_data,
                                                                   event_two_data=transit_data,
                                                                   event_one_ax=event_one_ax,
                                                                   event_two_ax=event_two_ax,
                                                                   fig=tr_fig)


            swe.close()

            graph, buffer = get_graph(tr_fig)
            plot_name = f'{tr_user_chart.drawer}_{ev_d}.png'
            tr_user_chart.tr_chart_image.save(plot_name, ContentFile(buffer.getvalue()), save=True)
            buffer.close()
            tr_user_chart.save()

            context = {'planet_data': set_signs(planet_names, [p[4] for p in ev_d_val]),
                       'house_data': set_signs(house_names, list(houses[0])),
                       'ats': aspect_table_s, 'ato': aspect_table_ops,
                       'att': aspect_table_t, 'atc': aspect_table_c,
                       'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_d_val]),
                       'event_date': ev_d, 'tr_date': tr_d,
                       'event_city': tr_user_chart.event_city,
                       'event_country': tr_user_chart.event_country,
                       'tr_city': tr_user_chart.transit_city,
                       'tr_country': tr_user_chart.transit_country,
                       'tr_uc_tr_name': tr_user_chart.event_name,
                       'tr_uc_ev_name': tr_user_chart.transit_name,
                       'tr_mode': tr_mode, 'ev_mode': ev_mode,
                       'graph': graph, 'ev_one_hs': eo_hs }

            return render(request, 'tr_user_chart_dtl_eh.html', context)

    return render(request, 'user_transit_chart_form.html', {'tr_form':tr_form})


def user_color_chart_form(request):

    if request.method == 'POST':

        color_form = OneColorZodiacRingFM(request.POST, request.FILES)

        if color_form.is_valid():

            color_chart = color_form.save(commit=False)
            color_chart.save()

            get_loc = loc.geocode(f'{color_chart.chart_city, color_chart.chart_country}', timeout=7000)
            us_hs = color_chart.chart_house_system.encode('utf-8')
            ev_cc_hs = HOUSE_SYSTEM_CHOICES.get(color_chart.chart_house_system)
            ev_cc_cm = MODE_CHOICES.get(color_chart.chart_mode)
            cc_city = color_chart.chart_city
            cc_country =  color_chart.chart_country
            cc_date = color_chart.chart_date

            loc_tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
            local_dt = color_chart.chart_date.replace(tzinfo=ZoneInfo(loc_tz))
            utc_dt = local_dt.astimezone(datetime.timezone.utc)
            jd = jl.to_jd(utc_dt, fmt='jd')

            username = request.user.username
            color_chart.drawer = get_object_or_404(get_user_model(), username=username)

            img = draw_zodiac_one_color(color_chart.face_color, color_chart.edge_color, color_chart.text_color,
                                  color_chart.tick_color, color_chart.deg_color, color_chart.font_size,
                                  color_chart.line_width)

            matplotlib.rcParams['axes.edgecolor'] = color_chart.house_track_color
            matplotlib.rcParams['axes.linewidth'] = color_chart.house_track_lw

            planet_data = get_planet_data(jd, color_chart. chart_mode)
            pd_val = list(planet_data.values())

            planet_data_for_db = [(set_signs(planet_names, [p[4] for p in pd_val]))]

            color_chart.Sun_deg = planet_data_for_db[0][0][1]
            color_chart.Sun_sign = f'{planet_data_for_db[0][0][2]}'

            color_chart.Moon_deg = f'{planet_data_for_db[0][1][1]}'
            color_chart.Moon_sign = planet_data_for_db[0][1][2]

            color_chart.Mercury_deg = f'{planet_data_for_db[0][2][1]}'
            color_chart.Mercury_sign = planet_data_for_db[0][2][2]

            color_chart.Venus_deg = f'{planet_data_for_db[0][3][1]}'
            color_chart.Venus_sign = planet_data_for_db[0][3][2]

            color_chart.Mars_deg = planet_data_for_db[0][4][1]
            color_chart.Mars_sign = planet_data_for_db[0][4][2]

            color_chart.Jupiter_deg = f'{planet_data_for_db[0][5][1]}'
            color_chart.Jupiter_sign = planet_data_for_db[0][5][2]

            color_chart.Saturn_deg = f'{planet_data_for_db[0][6][1]}'
            color_chart.Saturn_sign = planet_data_for_db[0][6][2]

            color_chart.Uranus_sign = f'{planet_data_for_db[0][7][1]}'
            color_chart.Uranus_deg = planet_data_for_db[0][7][2]

            color_chart.Neptune_deg = f'{planet_data_for_db[0][8][1]}'
            color_chart.Neptune_sign = planet_data_for_db[0][8][2]

            color_chart.Pluto_deg = f'{planet_data_for_db[0][9][1]}'
            color_chart.Pluto_sign = planet_data_for_db[0][9][2]

            if color_chart.chart_house_system != 'Without houses':

                houses = swe.houses_ex(jd, get_loc.latitude, get_loc.longitude, us_hs, int(color_chart.chart_mode))

                hc_data_for_db = [set_signs(house_names, list(houses[0]))]

                color_chart.first_house = hc_data_for_db[0][0][0]
                color_chart.asc_deg = hc_data_for_db[0][0][1]
                color_chart.asc_sign = hc_data_for_db[0][0][2]

                color_chart.second_house = hc_data_for_db[0][1][0]
                color_chart.resource_deg = hc_data_for_db[0][1][1]
                color_chart.resource_sign = hc_data_for_db[0][1][2]

                color_chart.third_house = hc_data_for_db[0][2][0]
                color_chart.mental_deg = hc_data_for_db[0][2][1]
                color_chart.mental_sign = hc_data_for_db[0][2][2]

                color_chart.forth_house = hc_data_for_db[0][3][0]
                color_chart.home_deg = hc_data_for_db[0][3][1]
                color_chart.home_sign = hc_data_for_db[0][3][2]

                color_chart.fifth_house = hc_data_for_db[0][4][0]
                color_chart.game_deg = hc_data_for_db[0][4][1]
                color_chart.game_sign = hc_data_for_db[0][4][2]

                color_chart.sixth_house = hc_data_for_db[0][5][0]
                color_chart.work_deg = hc_data_for_db[0][5][1]
                color_chart.work_sign = hc_data_for_db[0][5][2]

                color_chart.seventh_house = hc_data_for_db[0][6][0]
                color_chart.rel_deg = hc_data_for_db[0][6][1]
                color_chart.rel_sign = hc_data_for_db[0][6][2]

                color_chart.eighth_house = hc_data_for_db[0][7][0]
                color_chart.magic_deg = hc_data_for_db[0][7][1]
                color_chart.magic_sign = hc_data_for_db[0][7][2]

                color_chart.nineth_house = hc_data_for_db[0][8][0]
                color_chart.esoteric_deg = hc_data_for_db[0][8][1]
                color_chart.esoteric_sign = hc_data_for_db[0][8][2]

                color_chart.tenth_house = hc_data_for_db[0][9][0]
                color_chart.status_deg = hc_data_for_db[0][9][1]
                color_chart.status_sign = hc_data_for_db[0][9][2]

                color_chart.eleventh_house = hc_data_for_db[0][10][0]
                color_chart.interests_deg = hc_data_for_db[0][10][1]
                color_chart.interests_sign = hc_data_for_db[0][10][2]

                color_chart.twelfth_house = hc_data_for_db[0][11][0]
                color_chart.benefits_deg = hc_data_for_db[0][11][1]
                color_chart.benefits_sign = hc_data_for_db[0][11][2]

                fig_form, planet_ax, house_ax, _, _, _, _, _, _ = draw_chart(fig_name='fig_form',
                                                                             planet_ax='planet_ax',
                                                                             house_ax='house_ax',
                                                                             ha_color=color_chart.house_ax_color,
                                                                             ha_lbl_size=color_chart.house_num_fs,
                                                                             ha_lw=color_chart.house_ax_lw,
                                                                             ha_lab_cl=color_chart.house_number_color,
                                                                             chart_path=img,
                                                                             houses_data=houses[0])

                aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, = \
                    build_aspects(planet_data=planet_data, ax_name=planet_ax, marker_clr=color_chart.marker_color,
                                  pl_marker_size=color_chart.marker_size, symbol_size=color_chart.symbol_size,
                                  symbol_clr=color_chart.symbol_color)

                swe.close()

                get_s3_client()
                graph, buffer = get_graph(fig_form)
                plot_name = f'{color_chart.drawer}{color_chart.id}.png'
                color_chart.chart_image = upload_to_storage(buffer, plot_name, 'chart_plots/colored_charts_nh/')

                color_chart.save()

                return render(request, 'user_color_chart.html',
                              {'planet_data': set_signs(planet_names, [p[4] for p in pd_val]),
                               'house_data': set_signs(house_names,list(houses[0])),
                               'ats': aspect_table_s, 'ato': aspect_table_ops,
                               'att': aspect_table_t, 'atc': aspect_table_c, 'date': color_chart.chart_date,
                               'color_chart': color_chart, 'graph':graph,
                               'cc_hs': ev_cc_hs, 'cc_mode': ev_cc_cm,
                               'cc_city': cc_city, 'cc_country': cc_country,
                               'cc_date': cc_date.strftime("%B %d, %Y, %H:%M:%S, %A"),})

            else:

                fig_form, planet_ax, _, _, _, _, _, _, _ = draw_chart(fig_name='fig_form',
                                                                      planet_ax='planet_ax',
                                                                      chart_path=img)

                aspect_table_s, aspect_table_ops, aspect_table_t, aspect_table_c, = \
                    build_aspects(planet_data=planet_data, ax_name=planet_ax)

                get_s3_client()
                graph, buffer = get_graph(fig_form)
                plot_name = f'{color_chart.drawer}{color_chart.id}.png'
                color_chart.chart_image = upload_to_storage(buffer, plot_name, 'chart_plots/colored_charts_nh/')

                buffer.close()

                color_chart.save()

                return render(request, 'user_color_chart_nh.html',
                              {'planet_data': set_signs(planet_names, [p[4] for p in pd_val]),
                               'ats': aspect_table_s, 'ato': aspect_table_ops,
                               'att': aspect_table_t, 'atc': aspect_table_c,
                               'color_chart': color_chart, 'graph': graph,
                               'cc_hs': ev_cc_hs, 'cc_mode': ev_cc_cm,
                               'cc_city': cc_city, 'cc_country': cc_country,
                               'cc_date': cc_date.strftime("%B %d, %Y, %H:%M:%S, %A"),})

    else:
        color_form = OneColorZodiacRingFM(request.POST, request.FILES)

    return render(request, 'user_color_chart_form.html', {'color_form':color_form})

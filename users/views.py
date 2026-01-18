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
from pycirclize import Circos
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.image as mpi

import numpy as np

import swisseph as swe

import julian as jl


from geopy.geocoders import Nominatim

from astroplan.models import (Chart, TransitChart, ZodiacInColors, FullChart,
                              TransitFullChart, OneColorZodiacRingMF,
                              HOUSE_SYSTEM_CHOICES, MODE_CHOICES)

from astroplan.forms import (FullChartForm, TransitFullChartForm,
                             ZodiacInColorForm, OneColorZodiacRingFM)

from timezonefinder import TimezoneFinder

from .utils import draw_zodiac_one_color
from PIL import Image
from astroknow import settings

flags =  swe.FLG_SIDEREAL | swe.SIDM_LAHIRI

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
            'Saturn', 'Uranus', 'Neptune', 'Pluto','tr_Sun',
             'tr_Moon', 'tr_Mercury', 'tr_Venus', 'tr_Mars', 'tr_Jupiter',
            'tr_Saturn', 'tr_Uranus', 'tr_Neptune', 'tr_Pluto']

tr_planet_names = ['tr_Sun','tr_Moon', 'tr_Mercury', 'tr_Venus', 'tr_Mars',
                   'tr_Jupiter', 'tr_Saturn', 'tr_Uranus', 'tr_Neptune', 'tr_Pluto']

cur_tr_coords = []

cur_tr_aspects =[]
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


swe.set_ephe_path('/home/gaia/Документы/eph files')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

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
                return redirect('showed chart')


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
        tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
        d = chart.chart_date
        us_hs = chart.house_system.encode('utf-8')
        house_system = HOUSE_SYSTEM_CHOICES.get(us_hs)
        mode = MODE_CHOICES.get(chart.chart_mode)

        jd = jl.to_jd(d, fmt='jd')
        chart.drawer = get_object_or_404(get_user_model(),username=username)

        pd = {swe.get_planet_name(0): ['☼', 'yellow', 5, 17, swe.calc_ut(jd, 0, chart.chart_mode)[0][0],
                                       swe.calc_ut(jd, 0, chart.chart_mode)[0][0]],
              swe.get_planet_name(1): ['☾', 'blue', 5, 17, swe.calc_ut(jd, 1, chart.chart_mode)[0][0],
                                       swe.calc_ut(jd, 1, chart.chart_mode)[0][1]],
              swe.get_planet_name(2): ['☿', 'grey', 5, 17, swe.calc_ut(jd, 2, chart.chart_mode)[0][0],
                                       swe.calc_ut(jd, 1, chart.chart_mode)[0][1]],
              swe.get_planet_name(3): ['♀', 'sienna', 5, 17, swe.calc_ut(jd, 3, chart.chart_mode)[0][0],
                                       swe.calc_ut(jd, 1, chart.chart_mode)[0][1]],
              swe.get_planet_name(4): ['♂', 'red', 5, 17, swe.calc_ut(jd, 4, chart.chart_mode)[0][0],
                                       swe.calc_ut(jd, 1, chart.chart_mode)[0][1]],
              swe.get_planet_name(5): ['♃', 'teal', 5, 17, swe.calc_ut(jd, 5, chart.chart_mode)[0][0],
                                       swe.calc_ut(jd, 1, chart.chart_mode)[0][1]],
              swe.get_planet_name(6): ['♄', 'slategrey', 5, 17, swe.calc_ut(jd, 6, chart.chart_mode)[0][0],
                                       swe.calc_ut(jd, 1, chart.chart_mode)[0][1]],
              swe.get_planet_name(7): ['♅', 'chartreuse', 5, 17, swe.calc_ut(jd, 7, chart.chart_mode)[0][0],
                                       swe.calc_ut(jd, 1, chart.chart_mode)[0][1]],
              swe.get_planet_name(8): ['♆', 'indigo', 5, 17, swe.calc_ut(jd, 8, chart.chart_mode)[0][0],
                                       swe.calc_ut(jd, 1, chart.chart_mode)[0][1]],
              swe.get_planet_name(9): ['♇', 'darkmagenta', 5, 17, swe.calc_ut(jd, 9, chart.chart_mode)[0][0],
                                       swe.calc_ut(jd, 1, chart.chart_mode)[0][1]]}

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

        planet_data_for_db = [(set_signs(planet_names, [p[4] for p in form_coords_value]))]

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

            img = mpi.imread('astroplan/static/images/tr_zr_1.png')
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

            houses = swe.houses_ex(jd, get_loc.latitude, get_loc.longitude, us_hs, chart.chart_mode)
            house_ax.set_rlim(-130, 100)
            house_ax.set_theta_direction(1)
            house_ax.set_rticks([])
            house_ax.set_thetagrids(houses[0],
                                    ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
            house_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=1, labelfontfamily='monospace',
                                 labelcolor='aliceblue')

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

            swe.close()

            # user_chart_path = '/astro_app/astroknow/astroplan/static/plots/user_chart.png'
            # directory = os.path.dirname(user_chart_path)
            #
            # if not os.path.exists(directory):
            #     os.makedirs(directory, exist_ok=True)
            # plt.savefig(user_chart_path)
            #
            # img_path = 'astroplan/media/astroplan/images/'
            # fn_path = os.path.join(img_path, f'{d}.png')
            # plt.savefig(fn_path)
            #
            # plt.close(fig_form)
            #
            # with open(fn_path, 'rb') as f:
            #     chart.chart_image.save(f'{d}.png', f)
            #     chart.save()

            buffer = io.BytesIO()
            fig_form.savefig(buffer, format='png')

            plot_name = f'{chart.drawer}_{d}.png'
            chart.chart_image.save(plot_name, ContentFile(buffer.getvalue()), save=True)
            user_chart_form.save()

            buffer.close()
            plt.close(fig_form)

            return render(request, 'user_chart.html', { 'planet_data': set_signs(planet_names,
                                                  [p[4] for p in form_coords_value]),
                                                 'house_data': set_signs(house_names, list(houses[0])),
                                                 'ats': aspect_table_s, 'ato': aspect_table_ops,
                                                 'att': aspect_table_t, 'atc': aspect_table_c, 'date': d,
                                                  'chart':chart, 'house_system': house_system,
                                                  'mode': mode})

        else:

            img = mpi.imread('astroplan/static/images/tr_zr_1.png')
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

            swe.close()
            # user_chart_path = '/astro_app/astroknow/astroplan/static/plots/user_chart.png'
            # directory = os.path.dirname(user_chart_path)
            #
            # if not os.path.exists(directory):
            #     os.makedirs(directory, exist_ok=True)
            # plt.savefig(user_chart_path)
            #
            # img_path = 'astroplan/media/astroplan/images/'
            # fn_path = os.path.join(img_path, f'{d}.png')
            # plt.savefig(fn_path)
            #
            # plt.close(fig_form)
            #
            # with open(fn_path, 'rb') as f:
            #     chart.chart_image.save(f'{d}.png', f)
            #     chart.save()

            buffer = io.BytesIO()
            fig_form.savefig(buffer, format='png')

            plot_name = f'{chart.drawer}_{d}.png'
            chart.chart_image.save(plot_name, ContentFile(buffer.getvalue()), save=True)
            user_chart_form.save()

            buffer.close()
            plt.close(fig_form)

            return render(request, 'user_chart_nh.html', {'planet_data': set_signs(planet_names, [p[4] for p in form_coords_value]),
                                                       'ats': aspect_table_s, 'ato': aspect_table_ops,
                                                       'att': aspect_table_t, 'atc': aspect_table_c, 'date': d,
                                                        'chart': chart, 'house_system': house_system,
                                                        'mode': mode})

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

        ev_get_loc = loc.geocode(f'{tr_user_chart.event_city, tr_user_chart.event_country}', timeout=7000)
        tz = tf.timezone_at(lng=ev_get_loc.longitude, lat=ev_get_loc.latitude)
        ev_d = tr_user_chart.event_date
        tr_uc_ev_hs = tr_user_chart.ev_house_system.encode('utf-8')
        tr_house_system = HOUSE_SYSTEM_CHOICES.get(tr_uc_ev_hs)
        tr_mode = MODE_CHOICES.get(tr_user_chart.tr_chart_mode)
        jd_ev = jl.to_jd(ev_d, fmt='jd')

        tr_get_loc = loc.geocode(f'{tr_user_chart.transit_city, tr_user_chart.transit_country}', timeout=7000)
        tz = tf.timezone_at(lng=tr_get_loc.longitude, lat=tr_get_loc.latitude)
        tr_d = tr_user_chart.transit_date
        tr_uc_tr_hs = tr_user_chart.tr_house_system.encode('utf-8')
        jd_tr = jl.to_jd(tr_d, fmt='jd')
        tr_ev_house_system = HOUSE_SYSTEM_CHOICES.get(tr_uc_tr_hs)
        ev_mode = MODE_CHOICES.get(tr_user_chart.ev_chart_mode)

        tr_user_chart.drawer = get_object_or_404(get_user_model(), username=username)

        pd_cr = {swe.get_planet_name(0): ['☼', 'yellow', 5, 17,
                                          swe.calc_ut(jd_ev, 0, int(tr_user_chart.ev_chart_mode))[0][0],
                                          swe.calc_ut(jd_ev, 0, int(tr_user_chart.ev_chart_mode))[0][1], 10],
                 swe.get_planet_name(1): ['☾', 'blue', 5, 17,
                                          swe.calc_ut(jd_ev, 1, int(tr_user_chart.ev_chart_mode))[0][0],
                                          swe.calc_ut(jd_ev, 1, int(tr_user_chart.ev_chart_mode))[0][1], -25],
                 swe.get_planet_name(2): ['☿', 'grey', 5, 17,
                                          swe.calc_ut(jd_ev, 2, int(tr_user_chart.ev_chart_mode))[0][0],
                                          swe.calc_ut(jd_ev, 2, int(tr_user_chart.ev_chart_mode))[0][1], -25],
                 swe.get_planet_name(3): ['♀', 'sienna', 5, 17,
                                          swe.calc_ut(jd_ev, 3, int(tr_user_chart.ev_chart_mode))[0][0],
                                          swe.calc_ut(jd_ev, 3, int(tr_user_chart.ev_chart_mode))[0][1], 25],
                 swe.get_planet_name(4): ['♂', 'red', 5, 17,
                                          swe.calc_ut(jd_ev, 4, int(tr_user_chart.ev_chart_mode))[0][0],
                                          swe.calc_ut(jd_ev, 4, int(tr_user_chart.ev_chart_mode))[0][1], -10],
                 swe.get_planet_name(5): ['♃', 'teal', 5, 17,
                                          swe.calc_ut(jd_ev, 5, int(tr_user_chart.ev_chart_mode))[0][0],
                                          swe.calc_ut(jd_ev, 5, int(tr_user_chart.ev_chart_mode))[0][1], 0],
                 swe.get_planet_name(6): ['♄', 'slategrey', 5, 17,
                                          swe.calc_ut(jd_ev, 6, int(tr_user_chart.ev_chart_mode))[0][0],
                                          swe.calc_ut(jd_ev, 6, int(tr_user_chart.ev_chart_mode))[0][1], -25],
                 swe.get_planet_name(7): ['♅', 'chartreuse', 5, 17,
                                          swe.calc_ut(jd_ev, 7, int(tr_user_chart.ev_chart_mode))[0][0],
                                          swe.calc_ut(jd_ev, 7, int(tr_user_chart.ev_chart_mode))[0][1], 0],
                 swe.get_planet_name(8): ['♆', 'indigo', 5, 17,
                                          swe.calc_ut(jd_ev, 8, int(tr_user_chart.ev_chart_mode))[0][0],
                                          swe.calc_ut(jd_ev, 8, int(tr_user_chart.ev_chart_mode))[0][1], 0],
                 swe.get_planet_name(9): ['♇', 'darkmagenta', 5, 17,
                                          swe.calc_ut(jd_ev, 9, int(tr_user_chart.ev_chart_mode))[0][0],
                                          swe.calc_ut(jd_ev, 9, int(tr_user_chart.ev_chart_mode))[0][1], 0]}

        cr_form_coords_value = list(pd_cr.values())

        pd = {swe.get_planet_name(0): ['☼ᵀᴿ', 'yellow', 5, 17, swe.calc_ut(jd_tr, 0,
                                                                           int(tr_user_chart.tr_chart_mode))[0][0],
                                       swe.calc_ut(jd_tr, 0,
                                                   int(tr_user_chart.tr_chart_mode))[0][1], 10],

              swe.get_planet_name(1): ['☾ᵀᴿ', 'blue', 5, 17, swe.calc_ut(jd_tr, 1,
                                                                         int(tr_user_chart.tr_chart_mode))[0][0],
                                       swe.calc_ut(jd_tr, 1,
                                                   int(tr_user_chart.tr_chart_mode))[0][1], -25],

              swe.get_planet_name(2): ['☿ᵀᴿ', 'grey', 5, 17,
                                       swe.calc_ut(jd_tr, 2, int(tr_user_chart.tr_chart_mode))[0][0],
                                       swe.calc_ut(jd_tr, 2, int(tr_user_chart.tr_chart_mode))[0][1], -25],

              swe.get_planet_name(3): ['♀ᵀᴿ', 'sienna', 5, 17,
                                       swe.calc_ut(jd_tr, 3, int(tr_user_chart.tr_chart_mode))[0][0],
                                       swe.calc_ut(jd_tr, 3, int(tr_user_chart.tr_chart_mode))[0][1], 25],
              swe.get_planet_name(4): ['♂ᵀᴿ', 'red', 5, 17,
                                       swe.calc_ut(jd_tr, 4, int(tr_user_chart.tr_chart_mode))[0][0],
                                       swe.calc_ut(jd_tr, 4, int(tr_user_chart.tr_chart_mode))[0][1], -10],
              swe.get_planet_name(5): ['♃ᵀᴿ', 'teal', 5, 17,
                                       swe.calc_ut(jd_tr, 5, int(tr_user_chart.tr_chart_mode))[0][0],
                                       swe.calc_ut(jd_tr, 5, int(tr_user_chart.tr_chart_mode))[0][1], 0],
              swe.get_planet_name(6): ['♄ᵀᴿ', 'slategrey', 5, 17,
                                       swe.calc_ut(jd_tr, 6, int(tr_user_chart.tr_chart_mode))[0][0],
                                       swe.calc_ut(jd_tr, 6, int(tr_user_chart.tr_chart_mode))[0][1], -25],

              swe.get_planet_name(7): ['♅ᵀᴿ', 'chartreuse', 5, 17,
                                       swe.calc_ut(jd_tr, 7, int(tr_user_chart.tr_chart_mode))[0][0],
                                       swe.calc_ut(jd_tr, 7, int(tr_user_chart.tr_chart_mode))[0][1], 0],

              swe.get_planet_name(8): ['♆ᵀᴿ', 'indigo', 5, 17,
                                       swe.calc_ut(jd_tr, 8, int(tr_user_chart.tr_chart_mode))[0][0],
                                       swe.calc_ut(jd_tr, 8, int(tr_user_chart.tr_chart_mode))[0][1], 0],
              swe.get_planet_name(9): ['♇ᵀᴿ', 'darkmagenta', 5, 17,
                                       swe.calc_ut(jd_tr, 9, int(tr_user_chart.tr_chart_mode))[0][0],
                                       swe.calc_ut(jd_tr, 9, int(tr_user_chart.tr_chart_mode))[0][1], 0]}

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

        both_chart_apd.extend(cr_form_coords_value)
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

        planet_data_for_db = [(set_signs(planet_names, [p[4] for p in cr_form_coords_value]))]

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

        tr_planet_data_for_db = [(set_signs(planet_names, [p[4] for p in tr_form_coords_value]))]

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

            img = mpi.imread('astroplan/static/images/zr_final_dp_pp.png')
            fig = plt.figure(figsize=(870 * px, 870 * px))
            fig.patch.set_alpha(0.0)

            ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
            ax_img.imshow(img)
            ax_img.axis('off')

            planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            planet_ax.set_theta_direction('counterclockwise')
            planet_ax.set_rlim(-180, 100)
            planet_ax.set_rticks([])
            planet_ax.set_axis_off()

            transit_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
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
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#34b806', lw=0.8)

                        aspected_planet_t.append(both_chart_apd[pl][0])
                        t_angle.append(f'{aspect}°')
                        trines.append(both_chart_apd[value + 1][0])
                        aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                    if aspect in opposition and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                        pl_one = np.array([np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                        pl_two = np.array([np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#fffe03', lw=0.8)

                        aspected_planet_op.append(both_chart_apd[pl][0])
                        op_angle.append(f'{aspect}°')
                        oppositions.append(both_chart_apd[value + 1][0])
                        aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                    if aspect in square and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                        pl_one = np.array(
                            [np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                        pl_two = np.array(
                            [np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#ff1a00', lw=0.8)

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

                    planet_ax.plot(np.deg2rad(cr_form_coords_value[pl][4]), cr_form_coords_value[pl][5], 'o',
                                   mfc=pd_cr[swe.get_planet_name(pl)][1],
                                   ms=pd_cr[swe.get_planet_name(pl)][2])
                    planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(pd_cr[swe.get_planet_name(pl)][6], 3),
                                       xycoords='data',
                                       xy=(np.deg2rad(cr_form_coords_value[pl][4]), cr_form_coords_value[pl][5]),
                                       fontsize=pd_cr[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    transit_ax.plot(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5], 'o',
                                    mfc=pd[swe.get_planet_name(pl)][1],
                                    ms=pd[swe.get_planet_name(pl)][2])
                    transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                        xytext=(pd[swe.get_planet_name(pl)][6], 3),
                                        xycoords='data',
                                        xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                        fontsize=pd[swe.get_planet_name(pl)][3],
                                        color='chartreuse',
                                        arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

            swe.close()
            tr_user_chart_path = '/astro_app/astroknow/astroplan/static/plots/tr_user_chart.png'
            directory = os.path.dirname(tr_user_chart_path)

            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            plt.savefig(tr_user_chart_path)

            img_path = 'astroplan/media/astroplan/images/'
            fn_path = os.path.join(img_path, f'{ev_d}.png')
            plt.savefig(fn_path)
            plt.close(fig)

            with open(fn_path, 'rb') as f:
                tr_user_chart.tr_chart_image.save(f'{tr_d}.png', f)
                tr_user_chart.save()


            return render(request, 'tr_user_chart_dtl_wh.html',
                          context={'planet_data': set_signs(planet_names, [p[4] for p in cr_form_coords_value]),
                                   'ats': aspect_table_s, 'ato': aspect_table_ops,
                                   'att': aspect_table_t, 'atc': aspect_table_c,
                                   'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_form_coords_value]),
                                   'event_date': ev_d,
                                   'event_city': tr_user_chart.event_city, 'event_country': tr_user_chart.event_country,
                                   'tr_date': tr_d, 'tr_city': tr_user_chart.transit_city,
                                   'tr_country': tr_user_chart.transit_country,
                                   'tr_uc_tr_name':tr_user_chart.event_name,
                                   'tr_uc_ev_name' : tr_user_chart.transit_name,
                                   'tr_mode': tr_mode, 'ev_mode': ev_mode})

        if tr_user_chart.ev_house_system != 'Without houses' and tr_user_chart.tr_house_system != 'Without houses':

            img = mpi.imread('astroplan/static/images/zr_final_dp_pp.png')
            fig = plt.figure(figsize=(870 * px, 870 * px))
            fig.patch.set_alpha(0.0)

            ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
            ax_img.imshow(img)
            ax_img.axis('off')

            planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            planet_ax.set_theta_direction('counterclockwise')

            planet_ax.set_rticks([])
            planet_ax.set_axis_off()
            planet_ax.set_rlim(-180, 100)

            transit_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
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

            houses = swe.houses_ex(jd_ev, ev_get_loc.latitude, ev_get_loc.longitude, tr_uc_ev_hs,
                                   int(tr_user_chart.ev_chart_mode))
            hc_data_for_db = [set_signs(house_names, list(houses[0]))]

            house_ax.set_thetagrids(houses[0],
                                    ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
            house_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=0.5,
                                 labelfontfamily='monospace', labelcolor='aliceblue')
            house_ax.set_theta_offset(np.pi)

            tr_house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            tr_house_ax.patch.set_alpha(0.0)
            tr_house_ax.set_rlim(-130, 100)
            tr_house_ax.set_theta_direction(1)
            tr_house_ax.set_rticks([])

            tr_houses = swe.houses_ex(jd_tr, tr_get_loc.latitude, tr_get_loc.longitude, tr_uc_tr_hs,
                                      int(tr_user_chart.tr_chart_mode))

            tr_house_ax.set_thetagrids(tr_houses[0],
                                       ['TR ASC', 'TR II', 'TR III', 'TR IC', 'TR V', 'TR VI', 'TR DSC',
                                        'TR VIII', 'TR IX', 'TR MC', 'TR XI', 'TR XII'])
            tr_house_ax.tick_params(labelsize=20, grid_color='chartreuse', grid_linewidth=0.5,
                                    labelfontfamily='monospace', pad=23.0, labelcolor='chartreuse')
            tr_house_ax.set_theta_offset(np.pi)

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

            for value in range(len(both_chart_apd) - 1):
                for pl in range(0, 10):
                    aspect = abs(round(both_chart_apd[pl][4]) - round(both_chart_apd[value + 1][4]))

                    if aspect in trine and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                        pl_one = np.array(
                            [np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                        pl_two = np.array(
                            [np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#34b806', lw=0.8)

                        aspected_planet_t.append(both_chart_apd[pl][0])
                        t_angle.append(f'{aspect}°')
                        trines.append(both_chart_apd[value + 1][0])
                        aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                    if aspect in opposition and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                        pl_one = np.array([np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                        pl_two = np.array([np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#fffe03', lw=0.8)

                        aspected_planet_op.append(both_chart_apd[pl][0])
                        op_angle.append(f'{aspect}°')
                        oppositions.append(both_chart_apd[value + 1][0])
                        aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                    if aspect in square and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                        pl_one = np.array(
                            [np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                        pl_two = np.array(
                            [np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#ff1a00', lw=0.8)

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

                    planet_ax.plot(np.deg2rad(cr_form_coords_value[pl][4]), cr_form_coords_value[pl][5], 'o',
                                   mfc=pd_cr[swe.get_planet_name(pl)][1],
                                   ms=pd_cr[swe.get_planet_name(pl)][2])
                    planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(pd_cr[swe.get_planet_name(pl)][6], 3),
                                       xycoords='data',
                                       xy=(np.deg2rad(cr_form_coords_value[pl][4]), cr_form_coords_value[pl][5]),
                                       fontsize=pd_cr[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    transit_ax.plot(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5], 'o',
                                    mfc=pd[swe.get_planet_name(pl)][1],
                                    ms=pd[swe.get_planet_name(pl)][2])
                    transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                        xytext=(pd[swe.get_planet_name(pl)][6], 3),
                                        xycoords='data',
                                        xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                        fontsize=pd[swe.get_planet_name(pl)][3],
                                        color='chartreuse',
                                        arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

            swe.close()
            tr_user_chart_path = '/astro_app/astroknow/astroplan/static/plots/tr_user_chart.png'
            directory = os.path.dirname(tr_user_chart_path)

            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            plt.savefig(tr_user_chart_path)

            img_path = 'astroplan/media/astroplan/images/'
            fn_path = os.path.join(img_path, f'{ev_d}.png')
            plt.savefig(fn_path)
            plt.close()

            with open(fn_path, 'rb') as f:
                tr_user_chart.tr_chart_image.save(f'{tr_d}.png', f)
                tr_user_chart.save()


            return render(request, 'tr_user_chart_dtl.html',
                          context={'planet_data': set_signs(planet_names, [p[4] for p in cr_form_coords_value]),
                                   'house_data': set_signs(house_names, list(houses[0])),
                                   'ats': aspect_table_s, 'ato': aspect_table_ops,
                                   'att': aspect_table_t, 'atc': aspect_table_c,
                                   'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_form_coords_value]),
                                   'tr_house_data': set_signs(house_names, list(tr_houses[0])), 'event_date': ev_d,
                                   'event_city': tr_user_chart.event_city, 'event_country': tr_user_chart.event_country,
                                   'tr_date': tr_d, 'tr_city': tr_user_chart.transit_city,
                                   'tr_country': tr_user_chart.transit_country,
                                   'tr_uc_tr_name': tr_user_chart.event_name,
                                   'tr_uc_ev_name': tr_user_chart.transit_name,
                                   'tr_hs': tr_house_system, 'tr_mode': tr_mode,
                                   'tr_ev_hs': tr_ev_house_system, 'ev_mode': ev_mode})

        elif tr_user_chart.ev_house_system == 'Without houses' and tr_user_chart.tr_house_system:

            img = mpi.imread('astroplan/static/images/zr_final_dp_pp.png')
            fig = plt.figure(figsize=(870 * px, 870 * px))
            fig.patch.set_alpha(0.0)

            ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
            ax_img.imshow(img)
            ax_img.axis('off')

            planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            planet_ax.set_rlim(-180,100)
            planet_ax.set_theta_direction('counterclockwise')
            planet_ax.set_rticks([])
            planet_ax.set_axis_off()

            transit_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
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

            tr_house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            tr_house_ax.patch.set_alpha(0.0)
            tr_house_ax.set_rlim(-130, 100)
            tr_house_ax.set_theta_direction(1)
            tr_house_ax.set_rticks([])

            tr_house_ax.set_thetagrids(tr_houses[0],
                                       ['TR ASC', 'TR II', 'TR III', 'TR IC', 'TR V', 'TR VI', 'TR DSC',
                                        'TR VIII', 'TR IX', 'TR MC', 'TR XI', 'TR XII'])
            tr_house_ax.tick_params(labelsize=20, grid_color='chartreuse', grid_linewidth=0.5,
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
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#34b806', lw=0.8)

                        aspected_planet_t.append(both_chart_apd[pl][0])
                        t_angle.append(f'{aspect}°')
                        trines.append(both_chart_apd[value + 1][0])
                        aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                    if aspect in opposition and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                        pl_one = np.array([np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                        pl_two = np.array([np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#fffe03', lw=0.8)

                        aspected_planet_op.append(both_chart_apd[pl][0])
                        op_angle.append(f'{aspect}°')
                        oppositions.append(both_chart_apd[value + 1][0])
                        aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                    if aspect in square and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                        pl_one = np.array(
                            [np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                        pl_two = np.array(
                            [np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#ff1a00', lw=0.8)

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

                    planet_ax.plot(np.deg2rad(cr_form_coords_value[pl][4]), cr_form_coords_value[pl][5], 'o',
                                   mfc=pd_cr[swe.get_planet_name(pl)][1],
                                   ms=pd_cr[swe.get_planet_name(pl)][2])
                    planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(pd_cr[swe.get_planet_name(pl)][6], 3),
                                       xycoords='data',
                                       xy=(np.deg2rad(cr_form_coords_value[pl][4]), cr_form_coords_value[pl][5]),
                                       fontsize=pd_cr[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    transit_ax.plot(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5], 'o',
                                    mfc=pd[swe.get_planet_name(pl)][1],
                                    ms=pd[swe.get_planet_name(pl)][2])
                    transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                        xytext=(pd[swe.get_planet_name(pl)][6], 3),
                                        xycoords='data',
                                        xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                        fontsize=pd[swe.get_planet_name(pl)][3],
                                        color='chartreuse',
                                        arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

            swe.close()
            tr_user_chart_path = '/astro_app/astroknow/astroplan/static/plots/tr_user_chart.png'
            directory = os.path.dirname(tr_user_chart_path)

            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            plt.savefig(tr_user_chart_path)

            img_path = 'astroplan/media/astroplan/images/'
            fn_path = os.path.join(img_path, f'{ev_d}.png')
            plt.savefig(fn_path)
            plt.close(fig)

            with open(fn_path, 'rb') as f:
                tr_user_chart.tr_chart_image.save(f'{tr_d}.png', f)
                tr_user_chart.save()


            return render(request, 'tr_user_chart_dtl_th.html',
                          context={'planet_data': set_signs(planet_names, [p[4] for p in cr_form_coords_value]),
                                   'ats': aspect_table_s, 'ato': aspect_table_ops,
                                   'att': aspect_table_t, 'atc': aspect_table_c,
                                   'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_form_coords_value]),
                                   'tr_house_data': set_signs(house_names, list(tr_houses[0])), 'event_date': ev_d,
                                   'event_city': tr_user_chart.event_city, 'event_country': tr_user_chart.event_country,
                                   'tr_date': tr_d, 'tr_city': tr_user_chart.transit_city,
                                   'tr_country': tr_user_chart.transit_country,
                                   'tr_uc_tr_name': tr_user_chart.event_name,
                                   'tr_uc_ev_name': tr_user_chart.transit_name,
                                   'tr_hs': tr_house_system, 'tr_mode': tr_mode,
                                   'tr_ev_hs': tr_ev_house_system, 'ev_mode': ev_mode})


        elif tr_user_chart.tr_house_system == 'Without houses' and tr_user_chart.ev_house_system:

            img = mpi.imread('astroplan/static/images/zr_final_dp_pp.png')
            fig = plt.figure(figsize=(870 * px, 870 * px))
            fig.patch.set_alpha(0.0)

            ax_img = fig.add_axes((0.05, 0.05, 0.9, 0.9))
            ax_img.imshow(img)
            ax_img.axis('off')

            planet_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            planet_ax.set_rlim(-180,100)
            planet_ax.set_theta_direction('counterclockwise')
            planet_ax.set_rticks([])
            planet_ax.set_axis_off()

            transit_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
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

            house_ax = fig.add_axes((0.05, 0.05, 0.9, 0.9), projection='polar')
            house_ax.patch.set_alpha(0.0)
            house_ax.set_rlim(-130, 100)
            house_ax.set_theta_direction(1)
            house_ax.set_rticks([])
            house_ax.set_thetagrids(houses[0],
                                    ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
            house_ax.tick_params(labelsize=20, grid_color='aliceblue', grid_linewidth=0.5,
                                 labelfontfamily='monospace', labelcolor='aliceblue')
            house_ax.set_theta_offset(np.pi)

            for value in range(len(both_chart_apd) - 1):
                for pl in range(0, 10):
                    aspect = abs(round(both_chart_apd[pl][4]) - round(both_chart_apd[value + 1][4]))

                    if aspect in trine and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                        pl_one = np.array(
                            [np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                        pl_two = np.array(
                            [np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#34b806', lw=0.8)

                        aspected_planet_t.append(both_chart_apd[pl][0])
                        t_angle.append(f'{aspect}°')
                        trines.append(both_chart_apd[value + 1][0])
                        aspect_table_t = zip(aspected_planet_t, t_angle, trines)

                    if aspect in opposition and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                        pl_one = np.array([np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                        pl_two = np.array([np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#fffe03', lw=0.8)

                        aspected_planet_op.append(both_chart_apd[pl][0])
                        op_angle.append(f'{aspect}°')
                        oppositions.append(both_chart_apd[value + 1][0])
                        aspect_table_ops = zip(aspected_planet_op, op_angle, oppositions)

                    if aspect in square and both_chart_apd[pl][4] != both_chart_apd[value + 1][4]:
                        pl_one = np.array(
                            [np.deg2rad(both_chart_apd[pl][4]), np.deg2rad(both_chart_apd[value + 1][4])])
                        pl_two = np.array(
                            [np.deg2rad(both_chart_apd[pl][5]), np.deg2rad(both_chart_apd[value + 1][5])])
                        tr_cr_aspects_ax.plot(pl_one, pl_two, color='#ff1a00', lw=0.8)

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

                    planet_ax.plot(np.deg2rad(cr_form_coords_value[pl][4]), cr_form_coords_value[pl][5], 'o',
                                   mfc=pd_cr[swe.get_planet_name(pl)][1],
                                   ms=pd_cr[swe.get_planet_name(pl)][2])
                    planet_ax.annotate(f'{pd_cr[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                       xytext=(pd_cr[swe.get_planet_name(pl)][6], 3),
                                       xycoords='data',
                                       xy=(np.deg2rad(cr_form_coords_value[pl][4]), cr_form_coords_value[pl][5]),
                                       fontsize=pd_cr[swe.get_planet_name(pl)][3],
                                       color='aliceblue',
                                       arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                    transit_ax.plot(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5], 'o',
                                    mfc=pd[swe.get_planet_name(pl)][1],
                                    ms=pd[swe.get_planet_name(pl)][2])
                    transit_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                        xytext=(pd[swe.get_planet_name(pl)][6], 3),
                                        xycoords='data',
                                        xy=(np.deg2rad(tr_form_coords_value[pl][4]), tr_form_coords_value[pl][5]),
                                        fontsize=pd[swe.get_planet_name(pl)][3],
                                        color='chartreuse',
                                        arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

            swe.close()
            tr_user_chart_path = '/astro_app/astroknow/astroplan/static/plots/tr_user_chart.png'
            directory = os.path.dirname(tr_user_chart_path)

            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            plt.savefig(tr_user_chart_path)

            img_path = 'astroplan/media/astroplan/images/'
            fn_path = os.path.join(img_path, f'{ev_d}.png')
            plt.savefig(fn_path)
            plt.close(fig)

            with open(fn_path, 'rb') as f:
                tr_user_chart.tr_chart_image.save(f'{tr_d}.png', f)
                tr_user_chart.save()


            return render(request, 'tr_user_chart_dtl_eh.html',
                          context={'planet_data': set_signs(planet_names, [p[4] for p in cr_form_coords_value]),
                                   'ats': aspect_table_s, 'ato': aspect_table_ops,
                                   'att': aspect_table_t, 'atc': aspect_table_c,
                                   'tr_planet_data': set_signs(tr_planet_names, [p[4] for p in tr_form_coords_value]),
                                   'event_date': ev_d,
                                   'event_city': tr_user_chart.event_city, 'event_country': tr_user_chart.event_country,
                                   'tr_date': tr_d, 'tr_city': tr_user_chart.transit_city,
                                   'tr_country': tr_user_chart.transit_country,
                                   'house_data': set_signs(house_names, list(houses[0])),
                                   'tr_uc_tr_name': tr_user_chart.event_name,
                                   'tr_uc_ev_name': tr_user_chart.transit_name,
                                   'tr_hs': tr_house_system, 'tr_mode': tr_mode,
                                   'tr_ev_hs': tr_ev_house_system, 'ev_mode': ev_mode
                                   })


    return render(request, 'user_transit_chart_form.html', {'tr_form':tr_form})

def user_color_chart_form(request):

    if request.method == 'POST':

        color_form = OneColorZodiacRingFM(request.POST, request.FILES)

        if color_form.is_valid():

            color_chart = color_form.save(commit=False)

            # color_chart = OneColorZodiacRingMF.objects.last()
            get_loc = loc.geocode(f'{color_chart.chart_city, color_chart.chart_country}', timeout=7000)
            tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
            d = color_chart.chart_date
            us_hs = color_chart.chart_house_system.encode('utf-8')
            jd = jl.to_jd(d, fmt='jd')
            username = request.user.username
            color_chart.drawer = get_object_or_404(get_user_model(), username=username)

            draw_zodiac_one_color(color_chart.face_color, color_chart.edge_color, color_chart.text_color,
                                  color_chart.tick_color, color_chart.deg_color, color_chart.font_size,
                                  color_chart.line_width)

            matplotlib.rcParams['axes.edgecolor'] = color_chart.house_track_color
            matplotlib.rcParams['axes.linewidth'] = color_chart.house_track_lw

            pd = {swe.get_planet_name(0): ['☼', color_chart.marker_color, color_chart.symbol_size, color_chart.marker_size,
                                           color_chart.symbol_color,
                                           swe.calc_ut(jd, 0, color_chart.chart_mode)[0][0],
                                           swe.calc_ut(jd, 0, color_chart.chart_mode)[0][0]],

                  swe.get_planet_name(1): ['☾', color_chart.marker_color, color_chart.symbol_size, color_chart.marker_size,
                                           color_chart.symbol_color,
                                           swe.calc_ut(jd, 1, color_chart.chart_mode)[0][0],
                                           swe.calc_ut(jd, 1, color_chart.chart_mode)[0][1]],

                  swe.get_planet_name(2): ['☿', color_chart.marker_color, color_chart.symbol_size, color_chart.marker_size,
                                           color_chart.symbol_color,
                                           swe.calc_ut(jd, 2, color_chart.chart_mode)[0][0],
                                           swe.calc_ut(jd, 2, color_chart.chart_mode)[0][1]],

                  swe.get_planet_name(3): ['♀', color_chart.marker_color, color_chart.symbol_size, color_chart.marker_size,
                                           color_chart.symbol_color,
                                           swe.calc_ut(jd, 3, color_chart.chart_mode)[0][0],
                                           swe.calc_ut(jd, 3, color_chart.chart_mode)[0][1]],

                  swe.get_planet_name(4): ['♂', color_chart.marker_color, color_chart.symbol_size, color_chart.marker_size,
                                           color_chart.symbol_color,
                                           swe.calc_ut(jd, 4, color_chart.chart_mode)[0][0],
                                           swe.calc_ut(jd, 4, color_chart.chart_mode)[0][1]],

                  swe.get_planet_name(5): ['♃', color_chart.marker_color, color_chart.symbol_size, color_chart.marker_size,
                                           color_chart.symbol_color,
                                           swe.calc_ut(jd, 5, color_chart.chart_mode)[0][0],
                                           swe.calc_ut(jd, 5, color_chart.chart_mode)[0][1]],

                  swe.get_planet_name(6): ['♄', color_chart.marker_color, color_chart.symbol_size, color_chart.marker_size,
                                           color_chart.symbol_color,
                                           swe.calc_ut(jd, 6, color_chart.chart_mode)[0][0],
                                           swe.calc_ut(jd, 6, color_chart.chart_mode)[0][1]],

                  swe.get_planet_name(7): ['♅', color_chart.marker_color, color_chart.symbol_size, color_chart.marker_size,
                                           color_chart.symbol_color,
                                           swe.calc_ut(jd, 7, color_chart.chart_mode)[0][0],
                                           swe.calc_ut(jd, 7, color_chart.chart_mode)[0][1]],

                  swe.get_planet_name(8): ['♆', color_chart.marker_color, color_chart.symbol_size, color_chart.marker_size,
                                           color_chart.symbol_color,
                                           swe.calc_ut(jd, 8, color_chart.chart_mode)[0][0],
                                           swe.calc_ut(jd, 8, color_chart.chart_mode)[0][1]],

                  swe.get_planet_name(9): ['♇', color_chart.marker_color, color_chart.symbol_size, color_chart.marker_size,
                                           color_chart.symbol_color,
                                           swe.calc_ut(jd, 9, color_chart.chart_mode)[0][0],
                                           swe.calc_ut(jd, 9, color_chart.chart_mode)[0][1]]}

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

            planet_data_for_db = [(set_signs(planet_names, [p[5] for p in form_coords_value]))]

            color_chart.Sun_deg = planet_data_for_db[0][0][1]
            color_chart.Sun_sign = f' {planet_data_for_db[0][0][2]}'

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

                img = np.array(Image.open(os.path.join(settings.MEDIA_ROOT, 'color_chart_zodiac_ring//zodiac_ring_background.png')))
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

                houses = swe.houses_ex(jd, get_loc.latitude, get_loc.longitude, us_hs, color_chart.chart_mode)
                house_ax.set_rlim(-130, 100)
                house_ax.set_theta_direction(1)
                house_ax.set_rticks([])
                house_ax.set_thetagrids(houses[0],
                                        ['ASC', 'II', 'III', 'IC', 'V', 'VI', 'DSC', 'VIII', 'IX', 'MC', 'XI', 'XII'])
                house_ax.tick_params(labelsize=color_chart.house_num_fs,
                                     grid_color=color_chart.house_ax_color,
                                     grid_linewidth=color_chart.house_ax_lw,
                                     labelfontfamily='monospace',
                                     labelcolor=color_chart.house_number_color, pad=13.0)

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
                color_chart.save()

                for value in range(len(form_coords_value) - 1):
                    for pl in range(0, 10):
                        aspect = abs(round(form_coords_value[pl][5]) - round(form_coords_value[value + 1][5]))

                        if aspect in trine and form_coords_value[pl][5] != form_coords_value[value + 1][5]:
                            pl_one = np.array(
                                [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
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

                        if aspect in opposition and form_coords_value[pl][5] != form_coords_value[value + 1][5]:
                            pl_one = np.array(
                                [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
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

                        if aspect in square and form_coords_value[pl][5] != form_coords_value[value + 1][5]:
                            pl_one = np.array(
                                [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
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

                        if aspect in conjunction and form_coords_value[pl][5] != form_coords_value[value + 1][5]:
                            pl_one = np.array(
                                [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
                            pl_two = np.array(
                                [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
                            planet_ax.plot(pl_one, pl_two, color='green', lw=0.8)

                            aspected_planet_c.append(form_coords_value[pl][0])
                            c_angle.append(f'{aspect}°')
                            conjunctions.append(form_coords_value[value + 1][0])
                            aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

                        planet_ax.plot(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6], 'o',
                                       mfc=pd[swe.get_planet_name(pl)][1],
                                       ms=pd[swe.get_planet_name(pl)][3])

                        if form_coords_value[pl][5] == 0 or form_coords_value[pl][5] < 45:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(-20, -8),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                        elif 45 < form_coords_value[pl][5] < 135:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(-5, -25),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                        elif 135 < form_coords_value[pl][5] < 180:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(3, 13),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                        elif 180 < form_coords_value[pl][5] < 225:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(0, 25),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                        elif 225 < form_coords_value[pl][5] < 270:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(-25, -5),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                        elif 270 < form_coords_value[pl][5] < 315:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(-25, -5),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                        elif 315 < form_coords_value[pl][5] < 360:
                            if form_coords_value[pl][0] == '♆':
                                planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                                   xytext=(3, -10),
                                                   xycoords='data',
                                                   xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                                   fontsize=pd[swe.get_planet_name(pl)][3],
                                                   color='aliceblue',
                                                   arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                            else:
                                planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                                   xytext=(-25, -5),
                                                   xycoords='data',
                                                   xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                                   fontsize=pd[swe.get_planet_name(pl)][3],
                                                   color='aliceblue',
                                                   arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                swe.close()
                # color_user_chart_dir = '/astro_app/astroknow/astroplan/static/plots/'

                # color_user_chart_dir = '/astro_app/astroknow/media/chart_plots/'
                # clr_user_chart_path = os.path.join(color_user_chart_dir, f'{color_chart.drawer}_{d}.png')
                #
                # if not os.path.exists(color_user_chart_dir):
                #     os.makedirs(color_user_chart_dir, exist_ok=True)
                #
                # plt.savefig(clr_user_chart_path)
                #
                # with open(clr_user_chart_path, 'rb') as f:
                #     color_form.chart_image.save(clr_user_chart_path)
                #     color_form.save()
                #
                # plt.close(fig_form)

                buffer = io.BytesIO()
                fig_form.savefig(buffer, format='png')
                buffer.seek(0)

                plot_name = f'{color_chart.drawer}_{d}.png'

                # color_chart.chart_image.save(plot_name, ContentFile(buffer.getvalue()), save=True)
                # color_form.save()

                session = boto3.Session(
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name="ru-central1")
                s3 = session.client("s3", endpoint_url="https://storage.yandexcloud.net")
                plot_name = f'{color_chart.drawer}_{d}.png'
                s3_key = f"graphs/{plot_name}"
                bucket_name = os.getenv('BUCKET_NAME')
                s3.put_object(Bucket = bucket_name, Key=plot_name, Body = buffer, ContentType = 'image/png')

                plot_url = f"https://{bucket_name}.storage.yandexcloud.net/{s3_key}"
                color_chart.chart_image = plot_url
                color_chart.save()

                buffer.close()
                plt.close(fig_form)
                plt.close('all')

                return render(request, 'user_color_chart.html', {'planet_data': set_signs(planet_names,
                                                                                          [p[5] for p in
                                                                                           form_coords_value]),
                                                                 'house_data': set_signs(house_names, list(houses[0])),
                                                                 'ats': aspect_table_s, 'ato': aspect_table_ops,
                                                                 'att': aspect_table_t, 'atc': aspect_table_c, 'date': d,
                                                                 'plot_name': plot_name, 'color_chart': color_chart})

            else:

                img = np.array(Image.open(os.path.join(settings.MEDIA_ROOT, 'color_chart_zodiac_ring//zodiac_ring_background.png')))
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
                        aspect = abs(round(form_coords_value[pl][5]) - round(form_coords_value[value + 1][5]))

                        if aspect in trine and form_coords_value[pl][5] != form_coords_value[value + 1][5]:
                            pl_one = np.array(
                                [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
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

                        if aspect in opposition and form_coords_value[pl][5] != form_coords_value[value + 1][5]:
                            pl_one = np.array(
                                [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
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

                        if aspect in square and form_coords_value[pl][5] != form_coords_value[value + 1][5]:
                            pl_one = np.array(
                                [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
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

                        if aspect in conjunction and form_coords_value[pl][5] != form_coords_value[value + 1][5]:
                            pl_one = np.array(
                                [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
                            pl_two = np.array(
                                [np.deg2rad(form_coords_value[pl][5]), np.deg2rad(form_coords_value[value + 1][5])])
                            planet_ax.plot(pl_one, pl_two, color='green', lw=0.8)

                            aspected_planet_c.append(form_coords_value[pl][0])
                            c_angle.append(f'{aspect}°')
                            conjunctions.append(form_coords_value[value + 1][0])
                            aspect_table_c = zip(aspected_planet_c, c_angle, conjunctions)

                        planet_ax.plot(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6], 'o',
                                       mfc=pd[swe.get_planet_name(pl)][1],
                                       ms=pd[swe.get_planet_name(pl)][3])

                        if form_coords_value[pl][5] == 0 or form_coords_value[pl][5] < 45:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(-20, -8),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))


                        elif 55 < form_coords_value[pl][5] < 135:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(-5, -25),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

                        elif 135 < form_coords_value[pl][5] < 180:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(3, 13),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][5]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='red'))

                        elif 180 < form_coords_value[pl][5] < 225:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(0, 25),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                        elif 225 < form_coords_value[pl][5] < 270:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(-25, -5),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                        elif 270 < form_coords_value[pl][5] < 315:
                            planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                               xytext=(-25, -5),
                                               xycoords='data',
                                               xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                               fontsize=pd[swe.get_planet_name(pl)][3],
                                               color='aliceblue',
                                               arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                        elif 315 < form_coords_value[pl][5] < 360:
                            if form_coords_value[pl][0] == '♆':
                                planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                                   xytext=(3, -10),
                                                   xycoords='data',
                                                   xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                                   fontsize=pd[swe.get_planet_name(pl)][3],
                                                   color='aliceblue',
                                                   arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))
                            else:
                                planet_ax.annotate(f'{pd[swe.get_planet_name(pl)][0]}', textcoords='offset points',
                                                   xytext=(-25, -5),
                                                   xycoords='data',
                                                   xy=(np.deg2rad(form_coords_value[pl][5]), form_coords_value[pl][6]),
                                                   fontsize=pd[swe.get_planet_name(pl)][3],
                                                   color='aliceblue',
                                                   arrowprops=dict(facecolor='red', arrowstyle='-', edgecolor='hotpink'))

                # color_user_chart_dir = '/astro_app/astroknow/astroplan/static/plots/'
                # clr_user_chart_path = os.path.join(color_user_chart_dir, f'{color_chart.drawer}_{d}.png')
                #
                # if not os.path.exists(color_user_chart_dir):
                #     os.makedirs(color_user_chart_dir, exist_ok=True)
                #
                # plt.savefig(clr_user_chart_path)
                #
                # img_path = '/media/chart_plots/'
                # if not os.path.exists(img_path):
                #     os.makedirs(img_path, exist_ok=True)
                # fn_path = os.path.join(img_path, f'{color_chart.drawer}_{d}.png')
                #
                # plt.savefig(fn_path)
                # plt.close(fig_form)

                buffer = io.BytesIO()
                fig_form.savefig(buffer, format='png')

                plot_name = f'{color_chart.drawer}_{d}.png'
                color_chart.chart_image.save(plot_name, ContentFile(buffer.getvalue()), save=True)
                color_form.save()

                buffer.close()
                plt.close(fig_form)

                return render(request, 'user_color_chart_nh.html',
                              {'planet_data': set_signs(planet_names, [p[5] for p in form_coords_value]),
                               'ats': aspect_table_s, 'ato': aspect_table_ops,
                               'att': aspect_table_t, 'atc': aspect_table_c, 'date': d,
                               'color_chart': color_chart})

    else:
        color_form = OneColorZodiacRingFM(request.POST, request.FILES)

    return render(request, 'user_color_chart_form.html', {'color_form':color_form})

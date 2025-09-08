from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
import matplotlib.pyplot as plt
import matplotlib.image as mpi

import numpy as np

from datetime import datetime as dt

import swisseph as swe

import julian as jl


from geopy.geocoders import Nominatim
from pytz import timezone

from astroplan.models import Chart, TransitChart, ZodiacInColors, FullChart
from astroplan.forms import FullChartForm, TransitChartForm, ZodiacInColorForm
import os

from timezonefinder import TimezoneFinder

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

def activate_email(request, user, to_email):
    messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
        received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')

@user_not_auth
def register(request):
    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save(commit=False)
            # user.is_active = False
            user.save()
            login(request, user)
            # activate_email(request, user, reg_form.cleaned_data.get('email'))
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


def activateEmail(request, user, to_email):
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


def activate(request, uidb64, token):
    return redirect('showed chart')



def my_chart(request, username):

    chart_form = FullChartForm(request.POST or None, request.FILES or None)

    if chart_form.is_valid():
        chart_form.save()
        chart = FullChart.objects.last()
        get_loc = loc.geocode(f'{chart.city, chart.country}', timeout=7000)
        tz = tf.timezone_at(lng=get_loc.longitude, lat=get_loc.latitude)
        d = chart.chart_date
        # d = dt.strptime(chart.chart_date, '%Y-%m-%d %H:%m:%s')
        jd = jl.to_jd(d, fmt='jd')
        chart.drawer = get_object_or_404(get_user_model(),username=username)

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

        houses = swe.houses_ex(jd, get_loc.latitude, get_loc.longitude, b'R', flags=swe.FLG_SIDEREAL)
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

        houses = swe.houses_ex(jd, get_loc.latitude, get_loc.longitude, b'R', flags=swe.FLG_SIDEREAL)

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

        plt.savefig('astroplan/static/plots/user_chart.png')

        img_path = 'astroplan/media/astroplan/images/'
        fn_path = os.path.join(img_path, f'{d}.png')
        plt.savefig(fn_path)

        with open(fn_path, 'rb') as f:
            chart.chart_image.save(f'{d}.png', f)
            chart.save()
        swe.close()

        return render(request, 'user_chart.html', {
                                                 'planet_data': set_signs(planet_names,
                                                                          [p[4] for p in form_coords_value]),
                                                 'house_data': set_signs(house_names, list(houses[0])),
                                                 'ats': aspect_table_s, 'ato': aspect_table_ops,
                                                 'att': aspect_table_t, 'atc': aspect_table_c, 'date': d})





    if request.method == 'POST':
            user = request.user
            form = UserUpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                user_form = form.save()

                messages.success(request, f'{user_form}, Your profile has been updated!')
                return redirect('my chart', user_form.username)

            for error in list(form.errors.values()):
                messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    userid = request.user.id
    my_charts = FullChart.objects.filter(drawer__id=userid)
    if user:
        form = UserUpdateForm(instance=user)
        form.fields['description'].widget.attrs = {'rows': 1}
        return render(request, 'my_chart.html', context={'form': form, 'chart_form':chart_form,
                                                         'my_charts':my_charts})

    return redirect("showed chart")



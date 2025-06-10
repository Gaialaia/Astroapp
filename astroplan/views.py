from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import matplotlib.pyplot as plt

import numpy as np

from datetime import datetime as dt

import swisseph as swe

import julian as jl
from geopy.geocoders import Nominatim
from pytz import timezone


swe.set_ephe_path('/home/gaia/Документы/eph files')

planet_list = ['sun','mercury','venus', 'moon', 'mars',
                 'jupiter','saturn', 'uranus', 'neptune','pluto']


now = dt.now(tz=timezone('Asia/Yekaterinburg'))

date = dt(1986, 2,17, 22,20 )
jd_date = jl.to_jd(date,fmt='jd')

jd = jl.to_jd(now, fmt='jd')
flags =  swe.FLG_SIDEREAL

sun = swe.calc_ut(jd, 0, flags)
moon = swe.calc_ut(jd, 1, flags)

mercury = swe.calc_ut(jd,2, flags)
venus = swe.calc_ut(jd, 3, flags)
mars = swe.calc_ut(jd, 4, flags)

jupiter = swe.calc_ut(jd, 5, flags)
saturn =  swe.calc_ut(jd, 6,flags)

uranus =  swe.calc_ut(jd, 7,flags)
neptune = swe.calc_ut(jd, 8, flags)
pluto = swe.calc_ut(jd, 9, flags)

loc = Nominatim(user_agent="GetLoc")
getLoc = loc.geocode("Ufa, Russia", timeout=1000000)
# houses = swe.houses(jd, getLoc.latitude, getLoc.longitude, b'P')
houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'P', flags=swe.FLG_SIDEREAL)

def chart(request):
    template = loader.get_template('test_template.html')
    return HttpResponse(template.render())

# planet_list = ['sun','mercury','venus', 'moon', 'mars',
#                  'jupiter','saturn', 'uranus', 'neptune','pluto']


def show_td_chart(request):

    px = 1/plt.rcParams['figure.dpi']
    fig = plt.figure(figsize=(870*px, 870*px), facecolor='violet', edgecolor='black')
    fig.suptitle(f'Planet chart today,{now.strftime('%B, %d, %H:%M')}', size=17 )
    fig.patch.set_alpha(0.0)
   
    left = 0.05
    bottom = 0.05 
    width = 0.9
    height = 0.9
    ax1 = fig.add_axes([left, bottom, width, height], projection='polar') #center plot
    # ax1.set_theta_offset()

    ax1.set_rlim(-130,100)
    ax1.set_theta_direction('counterclockwise')
    ax1.set_rticks([])
    ax1.set_axis_off() #'theta ax' is off and grid off
    ax1.set_thetagrids(range(0, 360, 30))
    #ax1.grid()  #wont work because the axis is off

    ax1.plot(np.deg2rad(venus[0][0]), venus[0][1], marker='o', label='venus', ms=5, mfc='deeppink')
    ax1.annotate('♀', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(venus[0][0]), venus[0][1]), fontsize=15, color='blueviolet',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    ax1.plot(np.deg2rad(moon[0][0]), moon[0][1], marker='o', label='moon', mfc='forestgreen', ms=5)
    ax1.annotate('☾', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(moon[0][0]), moon[0][1]), fontsize=15, color='slateblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    ax1.plot(np.deg2rad(sun[0][0]), sun[0][1], marker='o', label='sun', ms=8, mfc='gold')
    ax1.annotate('☼', textcoords='offset points', xytext=(20, 5), xycoords='data',
                 xy=(np.deg2rad(sun[0][0]), sun[0][1]), fontsize=15, color='midnightblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    ax1.plot(np.deg2rad(mercury[0][0]), mercury[0][1], 'o:b', label='merc', ms=5)
    ax1.annotate('☿', textcoords='offset points', xytext=(20, 5), xycoords='data',
                 xy=(np.deg2rad(mercury[0][0]), mercury[0][1]), fontsize=15, color='orange',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    ax1.plot(np.deg2rad(mars[0][0]), mars[0][1], marker='o', label='mars', ms=5, mfc='red')
    ax1.annotate('♂', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(mars[0][0]), mars[0][1]), fontsize=15, color='slateblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    ax1.plot(np.deg2rad(jupiter[0][0]), jupiter[0][1], 'o', label='jupiter', ms=7, mfc='steelblue')
    ax1.annotate('♃', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(jupiter[0][0]), jupiter[0][1]), fontsize=17, color='slateblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    ax1.annotate(f'{round(jupiter[0][0])}°', textcoords='offset points', xytext=(-20, 5), xycoords='data',
                 xy=(np.deg2rad(jupiter[0][0]), jupiter[0][1]), fontsize=8, color='navy',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    ax1.plot(np.deg2rad(saturn[0][0]), saturn[0][1], 'o:k', label='saturn', ms=6)
    ax1.annotate('♄', textcoords='offset points', xytext=(20, -20), xycoords='data',
                 xy=(np.deg2rad(saturn[0][0]), saturn[0][1]), fontsize=15,
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    ax1.plot(np.deg2rad(uranus[0][0]), uranus[0][1], marker='o', mfc='chartreuse', label='uranus', ms=6)
    ax1.annotate('♅', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(uranus[0][0]), uranus[0][1]), fontsize=15, color='rebeccapurple',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    ax1.plot(np.deg2rad(neptune[0][0]), neptune[0][1], marker='o', label='neptune', ms=5, mfc='deepskyblue')
    ax1.annotate('♆', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(neptune[0][0]), neptune[0][1]), fontsize=20, color='indigo',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    ax1.plot(np.deg2rad(pluto[0][0]), pluto[0][1], 'o:k', mfc='red', label='pluto', ms=5)
    ax1.annotate('♇', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(pluto[0][0]), pluto[0][1]), fontsize=15, color='darkgoldenrod',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    plt.grid()

    # ax2.set_thetagrids(range(0,360,30), ('')) #each sector 24deg

    plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/today_chart.png')  #aplha setting isn't applied if a plot saved to jpg
    swe.close()
    return render (request,'planets.html')


def show_chart_houses(request):

    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.figure(figsize=(870 * px, 870 * px), facecolor='violet', edgecolor='black')
    # fig.suptitle(f'Planet chart today,{now.strftime('%B, %d, %H:%M')}', size=17)
    fig.patch.set_alpha(0.0)

    left = 0.05
    bottom = 0.05
    width = 0.9
    height = 0.9
    ax1 = fig.add_axes([left, bottom, width, height], projection='polar')  # center plot
    # ax1.set_theta_offset()

    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode("Ufa, Russia", timeout=7000)
    houses = swe.houses_ex(jd, getLoc.latitude, getLoc.longitude, b'R', flags=swe.FLG_SIDEREAL)

    ax1.set_alpha(0.0)
    ax1.set_rlim(-130, 100)
    ax1.set_theta_direction(1)
    ax1.set_rticks([])
    # ax1.set_axis_off()  # 'theta ax' is off
    ax1.set_thetagrids(houses[0], ['8', '9', 'MC', '11', '12', 'ASC', '2', '3', 'IC', '5', '6', 'DSC'])
    ax1.tick_params(labelsize=20, grid_color='red', grid_linewidth=1, labelfontfamily='monospace')


    # ax1.set_thetagrids(range(0,360,30))
    ax1.set_theta_offset(np.pi)
    ax1.grid(color= '#178270', linewidth=1)
    ax1.set_alpha(0.0)

    plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/house_chart.png')  # aplha setting isn't applied if a plot saved to jpg
    # swe.close()
    return render(request, 'house_chart.html')

def show_birth_chart(request):
    sun = swe.calc_ut(jd_date, 0, flags)
    moon = swe.calc_ut(jd_date, 1, flags)

    mercury = swe.calc_ut(jd_date, 2, flags)
    venus = swe.calc_ut(jd_date, 3, flags)
    mars = swe.calc_ut(jd_date, 4, flags)

    jupiter = swe.calc_ut(jd_date, 5, flags)
    saturn = swe.calc_ut(jd_date, 6, flags)

    uranus = swe.calc_ut(jd_date, 7, flags)
    neptune = swe.calc_ut(jd_date, 8, flags)
    pluto = swe.calc_ut(jd_date, 9, flags)

    planet_list = [sun, moon, mercury, venus, mars, jupiter,
                   saturn, uranus, neptune, pluto]
    planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter',
                'Saturn', 'Uranus', 'Neptune', 'Pluto']
    planet_symbols = ['☼', '☾', '☿', '♀', '♂', '♃','♄', '♅', '♆', '♇']

    pl_names_and_sym = {name: symbol for name, symbol in zip(planet_names, planet_symbols)}

    r_deg = [round(p[0][0],2) for p in planet_list]
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

    houses_list = [round(d, 2) for d in houses[0]]
    conv_h_deg = [str(n).replace('.', '°').replace(',', '′,') for n in houses_list]
    thirty_r_h_deg = [round(d, 2) % 30 for d in houses_list]  # convert from start point 360 to 30X12
    h_r_result = [round(d, 2) for d in thirty_r_h_deg]  # round divided into 30 result
    conv_h_r_result = [str(n).replace('.', '°').replace(',', '′,') for n in h_r_result]
    cusps_deg = zip(conv_h_deg, house_names)


    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.figure(figsize=(870 * px, 870 * px), facecolor='violet', edgecolor='black')
    fig.suptitle(f'Birth chart,{date.strftime('%B, %d, %H:%M')}', size=17)
    fig.patch.set_alpha(0.0)

    left = 0.05
    bottom = 0.05
    width = 0.9
    height = 0.9
    ax1 = fig.add_axes([left, bottom, width, height], projection='polar')  # center plot
    # ax1.set_theta_offset()

    ax1.set_rlim(-100, 130)
    ax1.set_theta_direction('counterclockwise')
    ax1.set_rticks([])
    ax1.set_axis_off()  # 'theta ax' is off
    ax1.set_thetagrids(range(0, 360, 30))

    opposition = np.arange(175.0, 185.0)
    trine = np.arange(115.0, 125.0)
    square = np.arange(85.0, 95.0)

    ops = []

    names_and_coords = list(zip(planet_names, planet_list))

    def aspect(planet_number):
        # for i in range(len(planet_list) - 1):
        #     z = abs(round(planet_list[planet_number][0][0]) - round(planet_list[i + 1][0][0]))
        #     if z in trine:
        #         p1 = np.array([np.deg2rad(planet_list[planet_number][0][0]), np.deg2rad(planet_list[i + 1][0][0])])
        #         p2 = np.array([planet_list[planet_number][0][1], planet_list[i + 1][0][1]])
        #         ax1.plot(p1, p2, lw=0.5, color='springgreen')

                # tr.append(planet_numbers[planet_number])
                # tr.append(planet_numbers[i])

        for i in range(len(names_and_coords) - 1):

            z = abs(round(names_and_coords[planet_number][1][0][0]) - round(pp[i + 1][1][0][0]))
            if z in square:
                p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
                               np.deg2rad(names_and_coords[i + 1][1][0][0])])
                p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
                ax1.plot(p1, p2, lw=0.5, color='firebrick')

                ops.append(names_and_coords[planet_number][0])
                ops.append(names_and_coords[i+1][0])

            if z in opposition:
                p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
                               np.deg2rad(names_and_coords[i + 1][1][0][0])])
                p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
                ax1.plot(p1, p2, lw=0.5, color='dimgrey')

            if z in trine:
                p1 = np.array([np.deg2rad(names_and_coords[planet_number][1][0][0]),
                               np.deg2rad(names_and_coords[i + 1][1][0][0])])
                p2 = np.array([names_and_coords[planet_number][1][0][1], names_and_coords[i + 1][1][0][1]])
                ax1.plot(p1, p2, lw=0.5, color='dimgrey')



    planet_numbers = {0: 'Sun', 1: 'Moon', 2: 'Mercury', 3: 'Venus',
                      4: 'Mars', 5: 'Jupiter', 6: 'Saturn', 7: 'Uranus',
                      8: 'Neptune', 9:'Pluto'}
    ax1.plot(np.deg2rad(planet_list[3][0][0]), planet_list[3][0][1], marker='o', label='venus', ms=5, mfc='deeppink')
    ax1.annotate('♀', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(planet_list[3][0][0]), planet_list[3][0][1]), fontsize=15, color='blueviolet',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
    aspect(3)

    ax1.plot(np.deg2rad(moon[0][0]), moon[0][1], marker='o', label='moon', mfc='forestgreen', ms=5)
    ax1.annotate('☾', textcoords='offset points', xytext=(20, 3), xycoords='data',
                 xy=(np.deg2rad(moon[0][0]), moon[0][1]), fontsize=15, color='slateblue',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))

    aspect(2)

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

    ax1.annotate(f'{round(jupiter[0][0])}°', textcoords='offset points', xytext=(-20, 5), xycoords='data',
                 xy=(np.deg2rad(jupiter[0][0]), jupiter[0][1]), fontsize=8, color='navy',
                 arrowprops=dict(facecolor='purple', arrowstyle='-', edgecolor='purple'))
    aspect(5)

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

    # x = np.array([np.deg2rad(mars[0][0]),np.deg2rad(venus[0][0])])
    # y = np.array([mars[0][1], venus[0][1]])
    # ax1.plot(x, y)
    # ax1.plot([np.deg2rad(mars[0][1])])

    ax1.grid(False)
    plt.grid(False)

    plt.savefig(
        '/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/birth_plot.png')  # aplha setting isn't applied if a plot saved to jpg
    swe.close()

    return render(request, 'birth_chart.html',
                  context={'planet_deg':planet_deg,'cusps_deg':cusps_deg, 'ops':ops} )

planet_numbers = {0:'Sun' , 1:'Moon', 2:'Mercury', 3:'Venus',
                  4:'Mars',5:'Jupiter', 6:'Saturn', 7:'Uranus',
                  8:'Neptune','Pluto':9}



sun = swe.calc_ut(jd_date, 0, flags)
moon = swe.calc_ut(jd_date, 1, flags)

mercury = swe.calc_ut(jd_date, 2, flags)
venus = swe.calc_ut(jd_date, 3, flags)
mars = swe.calc_ut(jd_date, 4, flags)

jupiter = swe.calc_ut(jd_date, 5, flags)
saturn = swe.calc_ut(jd_date, 6, flags)

uranus = swe.calc_ut(jd_date, 7, flags)
neptune = swe.calc_ut(jd_date, 8, flags)
pluto = swe.calc_ut(jd_date, 9, flags)

planet_list = [sun, moon, mercury, venus, mars, jupiter,
                   saturn, uranus, neptune, pluto]
planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter',
                'Saturn', 'Uranus', 'Neptune', 'Pluto']


pp = list(zip(planet_names, planet_list))
print(pp[1][1][0][1])
print(pp[[1][0]])


# # planet_deg = [i[0][0] for i in planet_list]
# # orbis = 5

opposition = np.arange(175.0, 185.0)
op = np.arange(175.0,185.0)
trine = np.arange(115.0,125.0)
square = np.arange(85.0, 95.0)
# aspects = (np.any(175.0, 185.0),  np.any(175.0,185.0),np.any(85.0, 95.0)) do not work


aspect_list = []
for i in range(len(pp)-1):

    z = abs(round(pp[3][1][0][0]) - round(pp[i+1][1][0][0]))


    if z in square:
        aspect_list.append(pp[3][0])
        aspect_list.append(pp[i+1][0])
        aspect_list.

        # print(z,pp[3][0],pp[i+1][0])
        print(aspect_list)

# print(planet_list[])

# for p in planet_numbers.values():
#     c = swe.calc_ut(jd_date, p, flags)
#     print(c,p)
#planet_numbers = {'Sun': 0, 'Moon':1, 'Mercury':2, 'Venus':3,
#                   'Mars':4,'Jupiter': 5, 'Saturn':6, 'Uranus':7,
#                   'Neptune':8,'Pluto':9}
# for number, name in planet_numbers.items():
#     planet_coords = swe.calc_ut(jd_date, name, flags)
#     print(planet_coords[0][0], planet_coords[0][1],name,number)




    # if z in trine:
    #     print(z)
    # if z in square:
    #     print(z)
    # if z in opposition:
    #     print(z)
#







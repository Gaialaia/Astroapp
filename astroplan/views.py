from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import matplotlib.pyplot as plt

import numpy as np

from datetime import datetime as dt

import swisseph as swe

import julian as jl

swe.set_ephe_path('/home/gaia/Документы/eph files')

planet_list = ['sun','mercury','venus', 'moon', 'mars',
                 'jupiter','saturn', 'uranus', 'neptune','pluto']

now = dt.now()
date = dt(1986, 2,17, 22,20 )
jd_date = jl.to_jd(date,fmt='jd')

jd = jl.to_jd(now, fmt='jd')
flags =  swe.FLG_SIDEREAL | swe.SIDM_DELUCE 

sun = swe.calc_ut(jd, 0, flags)
print(sun[0][0])


moon = swe.calc_ut(jd, 1, flags)



mercury = swe.calc_ut(jd,2, flags)
venus = swe.calc_ut(jd, 3, flags)
mars = swe.calc_ut(jd, 4, flags)


jupiter = swe.calc_ut(jd, 5, flags)
saturn =  swe.calc_ut(jd, 6,flags)

uranus =  swe.calc_ut(jd, 7,flags)
neptune = swe.calc_ut(jd, 8, flags)
pluto = swe.calc_ut(jd, 9, flags)


def chart(request):
    template = loader.get_template('test_template.html')
    return HttpResponse(template.render())

# planet_list = ['sun','mercury','venus', 'moon', 'mars',
#                  'jupiter','saturn', 'uranus', 'neptune','pluto']


def show_chart(request):
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
    ax1.set_axis_off() #'theta ax' is off
    ax1.set_thetagrids(range(0, 360, 30))
  

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

    ax1.grid(False)
    # ax2.set_thetagrids(range(0,360,30), ('')) #each sector 24deg
    plt.grid(False)

    plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/chart.png')  #aplha setting isn't applied if a plot saved to jpg
    swe.close()
    return render (request,'planets.html')

def show_transit_chart(request):

    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.figure(figsize=(870 * px, 870 * px), facecolor='violet', edgecolor='black')
    fig.suptitle(f'Transit chart,{now.strftime('%B, %d, %H:%M')}', size=17)
    fig.patch.set_alpha(0.0)

    left = 0.05
    bottom = 0.05
    width = 0.9
    height = 0.9
    ax1 = fig.add_axes([left, bottom, width, height], projection='polar')  # center plot
    # ax1.set_theta_offset()

    ax1.set_rlim(-130, 100)
    ax1.set_theta_direction('counterclockwise')
    ax1.set_rticks([])
    ax1.set_axis_off()  # 'theta ax' is off
    ax1.set_thetagrids(range(0, 360, 30))

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

    ax1.grid(False)
    plt.grid(False)


    plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/transit_plot.png')  # aplha setting isn't applied if a plot saved to jpg
    swe.close()

    return render(request, 'transit_chart.html')



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

    r_deg = [round(p[0][0],2) for p in planet_list]
    p = str(r_deg).replace('.', '°').replace(',', '′,')

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

    ax1.grid(False)
    # ax2.set_thetagrids(range(0,360,30), ('')) #each sector 24deg

    # plt.legend(loc='lower right')

    # plt.grid(True, color='pink') grid on

    plt.grid(False)
    mplcursors.cursor(hover=True)

    plt.savefig(
        '/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/birth_plot.png')  # aplha setting isn't applied if a plot saved to jpg
    swe.close()

    return render(request, 'birth_chart.html', context={'r_deg':r_deg, 'p':p})

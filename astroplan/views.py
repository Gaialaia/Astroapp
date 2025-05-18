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
jd = jl.to_jd(now, fmt='jd')



flags =  swe.FLG_SIDEREAL | swe.SIDM_DELUCE 

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
    ax1.set_theta_offset(np.pi) 
    ax1.set_rlim(-180,100)
    ax1.set_theta_direction(-1)
    ax1.set_rticks([])
    ax1.set_axis_off() #'theta ax' is off 
  
    # ax2 = plt.subplot(1, 1, 1, projection='polar')
    # ax2.set_theta_offset(np.pi) 
    # ax2.set_rlim(-180,100)
    # ax2.set_theta_direction(-1)
    # ax2.set_rticks([])

    ax1.plot(np.deg2rad(venus[0][0]), venus[0][1], 'o:m', label='venus', ms=2)
    ax1.plot(np.deg2rad(moon[0][0]), moon[0][1], 'o:g', label='moon')
    # ax1.annotate(round(venus[0][0]), xy=(np.deg2rad(venus[0][0]), venus[0][1]))
    # ax1.plot( venus[0][0], venus[0][1], zorder=2, color='silver', linestyle=':')
    ax1.plot(np.deg2rad(sun[0][0]), sun[0][1], marker='$☼$', label='sun', ms=30, mfc='gold')
    # ax1.annotate('☉', xy=(np.deg2rad(sun[0][0]), sun[0][1]))
    ax1.plot(np.deg2rad(mercury[0][0]), mercury[0][1], 'o:b', label='merc', ms=2)
    ax1.plot(np.deg2rad(mars[0][0]), mars[0][1], marker='$♂$', label='mars', ms=13)
    ax1.plot(np.deg2rad(jupiter[0][0]), jupiter[0][1], 'o:c', label='jupiter', ms=9)
    ax1.plot(np.deg2rad(saturn[0][0]), saturn[0][1], 'o:k', label='saturn', ms=2)
    ax1.plot(np.deg2rad(uranus[0][0]), uranus[0][1], marker='$♅$',mfc='chartreuse', label='uranus', ms=20)
    ax1.plot(np.deg2rad(neptune[0][0]), neptune[0][1], marker='$♆$', mfc='m', label='neptune', ms=20)
    ax1.plot(np.deg2rad(pluto[0][0]), pluto[0][1], 'o:k', mfc='red', label='pluto')

   
    ax1.set_thetagrids(range(0,360,30), (''))
   
    ax1.grid(False)
    # ax2.set_thetagrids(range(0,360,30), ('')) #each sector 24deg

    # plt.legend(loc='lower right')

    # plt.grid(True, color='pink') grid on

    plt.grid(False)


    plt.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/plots/chart.png')  #aplha setting isn't applied if a plot saved to jpg
    swe.close()

 
    return render (request,'planets.html')



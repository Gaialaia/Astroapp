from django.forms import DateInput, ModelForm
from django_flatpickr.widgets import DatePickerInput, DateTimePickerInput

from .models import Chart, TransitChart, ZodiacInColors
import datetime


from django import forms


class ChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = '__all__'
        labels = {'chart_date': 'Enter date',
                  'city': 'Enter city',
                  'country': 'Enter country'
                  }
        widgets = {
            'chart_date': DateTimePickerInput()}

        class Media:
            css = {
                'all': ['/static/styles/form_style.css']
            }


class TransitChartForm(forms.ModelForm):

    class Meta:
        model = TransitChart
        fields = '__all__'

        class Media:
            css = {
                'all': ['/static/styles/form_style.css']
            }
        widgets = {'event_date': DateTimePickerInput(),
                   'transit_date': DateTimePickerInput()
                   }
        labels = {'event_date': 'Enter an event date',
                  'event_city': 'Enter city',
                  'event_country': 'Enter country',
                  'transit_date': 'Enter transit date',
                  'transit_city':  'Enter city',
                  'transit_country': 'Enter country',
                  }

class ZodiacInColorForm(forms.ModelForm):
    
    class Meta:
        model = ZodiacInColors
        fields = '__all__'
        
        widgets = {'chart_date': DateTimePickerInput()}
        
        labels = {'track_aries_axis_fc': 'Aries axis face color',
                  'track_aries_axis_ec' :'Aries axis ed:Ge color',
                  'track_aries_axis_tc' : 'Aries text color',

                  'track_leo_axis_fc': 'Leo axis face color',
                  'track_leo_axis_ec': 'Leo axis ed:Ge color',
                  'track_leo_axis_tc': 'Leo text color',

                  'track_sag_axis_fc' : 'Sagittarius axis face color',
                  'track_sag_axis_ec': 'Sagittarius axis ed:Ge color',
                  'track_sag_axis_tc': 'Sagittarius text color',
                  
                  'track_aqua_axis_fc': 'Aquarius axis face color',
                  'track_aqua_axis_ec': 'Aquarius axis ed:Ge color',
                  'track_aqua_axis_tc': 'Aquarius text color',
                  
                  'track_gemini_axis_fc': 'Gemini axis face color',
                  'track_gemini_axis_ec':'Gemini axis ed:Ge color',
                  'track_gemini_axis_tc': 'Gemini text color',

                  'track_libra_axis_fc':'Libra axis face color',
                  'track_libra_axis_ec': 'Libra axis edge color',
                  'track_libra_axis_tc':'Libra text color',

                  'track_scorpio_axis_fc': 'Scorpio axis face color',
                  'track_scorpio_axis_ec': 'Scorpio axis edge color',
                  'track_scorpio_axis_tc': 'Scorpio text color',
                  
                  'track_cancer_axis_fc': 'Cancer axis face color',
                  'track_cancer_axis_ec': 'Cancer axis ed:Ge color',
                  'track_cancer_axis_tc': 'Cancer text color',

                  'track_pisces_axis_fc' : 'Pisces axis face color',
                  'track_pisces_axis_ec': 'Pisces axis edge color',
                  'track_pisces_axis_tc': 'Pisces text color',                  # 
                  
                  'track_taurus_axis_fc': 'Taurus axis face color',
                  'track_taurus_axis_ec': 'Taurus axis edge color',
                  'track_taurus_axis_tc': 'Taurus text color',
                  
                  'track_virgo_axis_fc' : 'Virgo axis face color',
                  'track_virgo_axis_ec': 'Virgo axis edge color',
                  'track_virgo_axis_tc': 'Virgo text color',
                  
                  'track_capricorn_axis_fc': 'Capricorn axis face color',
                  'track_capricorn_axis_ec':'Capricorn axis ed:Ge color',
                  'track_capricorn_axis_tc':'Capricorn text color',
                  
                  'degrees_track_ec' : 'Degrees track face color',
                  'degrees_ticks_color' : 'Degrees tick color',
                  
                   
                  'sun_symbol_c': 'Sun symbol color',
                  'sun_symbol_s' : 'Sun symbol size',
                  'sun_marker_c': 'Sun marker color',

                  'moon_symbol_c' : 'Moon symbol color',
                  'moon_symbol_s' : 'Moon symbol size',
                  'moon_marker_c' : 'Moon marker color',

                  'mercury_symbol_c': 'Mercury symbol color',
                  'mercury_symbol_s' : 'Mercury symbol size',
                  'mercury_marker_c' :'Mercury symbol color',

                  'venus_symbol_c': 'Venus symbol color',
                  'venus_symbol_s' :'Venus symbol size',
                  'marker_cVenus' : 'marker color',

                  'mars_symbol_c': 'Mars symbol color',
                  'mars_symbol_s' : 'Mars symbol size',
                  'mars_marker_c': 'Mars marker color',


                  'jupiter_symbol_c':'Jupiter symbol color',
                  'jup_symbol_s' :'Jupiter symbol size',
                  'jup_marker_c' : 'Jupiter marker color',

                  'saturn_symbol_c': 'Saturn symbol color',
                  'saturn_symbol_s' :'Saturn symbol size',
                  'saturn_marker_c': 'Saturn marker color',

                  'uranus_symbol_c': 'Uranus symbol color',
                  'uranus_symbol_s' :'Uranus symbol size',
                  'uranus_marker_c':'Uranus marker color',

                  'neptune_symbol_c':'Neptune symbol color',
                  'neptune_symbol_s' : 'Neptune symbol size',
                  'neptune_marker_c':'Neptune marker color',


                  'pluto_symbol_c' : 'Pluto symbol color',
                  'pluto_symbol_s' : 'Pluto symbol size',
                  'pluto_marker_c': 'Pluto marker color',

                  }

    class Media:
            css = {
            ' all': ['/static/styles/form_style.css']}
        
                
                
                
        

   
   
    
   
  









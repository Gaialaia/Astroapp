from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from astroplan.models import FullChart, TransitFullChart, OneColorZodiacRingMF
from astroplan.forms import (FullChartForm, TransitFullChartForm,
                             OneColorZodiacRingFM)
from datetime import datetime as dt
from django.utils import timezone


User = get_user_model()


class TestAstroViews(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='astrouser', password = 'password')
        self.client.login(username='astrouser', password = 'password')

        self.full_chart = FullChart.objects.create(chart_name='Write Tests',
                                                   chart_date=dt(2026,1,12,15,00),
                                                   city = 'Izhevsk', country='Russia',
                                                   chart_mode = 0, house_system='Equal')

        self.transit_chart = (
            TransitFullChart.objects.create(event_name = 'My birthdate',
                                                             event_date = dt(1986,2,17,10,20),
                                                             event_city = 'Ufa', event_country = 'Russia',
                                                             ev_chart_mode = 65536, ev_house_system='Regiomontanus',
                                                             transit_name = 'Flight to Pluto',
                                                             transit_date = dt(2032, 2,17,13,44,56),
                                                             transit_city = 'Kabakovo', transit_country = 'Russia',
                                                             tr_chart_mode = 65536, tr_house_system='Without houses'))

        self.color_chart = OneColorZodiacRingMF.objects.create(chart_name = 'Became a general',
                                                               chart_date = dt(1564, 5,20, 5,23),
                                                               chart_city = 'Paris',chart_country = 'France',
                                                               chart_mode = 8,
                                                               chart_house_system='Regiomontanus',
                                                               face_color = '#3f0332', edge_color='#b9d11b',
                                                               text_color = '#b2713e', tick_color='#88f047',
                                                               deg_color='#749a81', marker_color='#a82e0c',
                                                               symbol_color = '#b2713e', house_ax_color='#6f5f97',
                                                               house_number_color='#cb7a14', house_track_color='#164f64',
                                                               marker_size = 21, symbol_size=17,
                                                               font_size = 45, line_width = 3,
                                                               house_ax_lw = 3,house_num_fs = 25,
                                                               house_track_lw = 3)

        self.url = reverse('ad user chart')
        self.url_t = reverse('user tc f')
        self.url_c = reverse('user c ch f')

    def test_view_displays_form(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.context['user_chart_form'], FullChartForm)
        self.assertTemplateUsed(response,'user_chart_for_date_form.html')

        response = self.client.get(self.url_t)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['tr_form'], TransitFullChartForm)
        self.assertTemplateUsed(response, 'user_transit_chart_form.html')

        response = self.client.get(self.url_c)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['color_form'], OneColorZodiacRingFM)
        self.assertTemplateUsed(response, 'user_color_chart_form.html')

    def test_valid_form_submission_creates_object(self):

        chart_data = {  'chart_name': 'Write Tests',
                        'chart_date': timezone.make_aware(dt(2026, 1, 12, 15, 0)),
                        'city': 'Izhevsk',
                        'country': 'Russia',
                        'chart_mode': 0,
                        'house_system': 'Without houses',
                        'drawer': self.user.id,
                    }
        response = self.client.post(self.url, data=chart_data)
        print(response.context['user_chart_form'].errors)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FullChart.objects.filter(name='Write Tests').exists()
)


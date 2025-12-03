from pycirclize import Circos

sectors_reverse = {"IX": 30,  "VIII" : 30,  "VII" : 30,
            "VI": 30,"V": 30,  "IV": 30,
            "III": 30,  "II": 30, "I" : 40,
            "XII︎": 30,  "XI" : 30, "X︎": 30,
           }

sectors = {"♊︎": 30, "♉︎": 30, "♈︎": 30,
           "♓︎": 30, "♒︎": 30, "♑︎": 30,
           "♐︎": 30, "♏︎": 30, "♎︎": 30,
           "♍︎": 30, "♌︎": 30, "♋︎": 30,
           }

circos_rev = Circos(sectors_reverse)


zs = ['♈','︎♉︎','♊︎','♋︎','♌︎','♍','♎︎','♏︎','︎♐︎','♑︎','♒︎','♓︎' ]


zr_purple = '#331386'
light_color = '#dddbf8'
for sector in circos_rev.sectors:
    sign_track = sector.add_track((30, 75))
    sign_track.axis(ec='aliceblue', lw=3)
    house_track = sector.add_track((80,100))
    house_track.axis(ec='aliceblue', lw=3)
    house_track.text(f'{sector.name}', size=40, color='aliceblue')


# i_house = circos_rev.get_sector('I')
# sign_track = i_house.add_track((30, 75))
# i_house.axis(ec='aliceblue', lw=3)
# house_track = i_house.add_track((75,100))
# house_track.axis(ec='aliceblue', lw=3)




# fh = circos_rev.get_sector('I')
# fh.add_track((50,75))
# fh.axis(ec='#867777', lw=5)
# fh.text(f"{'♈'}")









fig = circos_rev.plotfig(figsize=(5,5))

fig.patch.set_alpha(0.0)

fig.savefig('ah.png', pad_inches=0.0)



from pycirclize import Circos

sectors_reverse = {"♐︎": 30,  "♎︎" : 30,  "♏︎" : 30,
            "♍︎": 30,"♌︎": 30,  "♋︎": 30,
            "♊︎": 30,  "♉︎": 30, "♈︎" : 30,
            "♓︎": 30,  "♒︎" : 30, "♑︎": 30,
           }


circos_rev = Circos(sectors_reverse)

for sector in circos_rev.sectors:
    track = sector.add_track((50,90))
    track.axis(ec='purple', lw=5)
    track.text(f'{sector.name}', size=40)



# sector_aries = circos_rev.get_sector("♈︎")
# # sector_aries.axis()
# track_aries = sector_aries.add_track((70, 100 ))
# # second_track = sector_aries.add_track((80,100))
# # third_track = sector_aries.add_track((90,100))
# track_aries.axis(ec='#ff1a00', lw=7)
# # second_track.axis(fc='red')
# # third_track.axis(fc='yellow')
# # second_track.text('♉︎ ♊︎ ♋︎ ♌︎ ♍︎ ♎︎ ♏︎ ♐︎ ♑︎ ♒︎ ♓︎')
# # second_track.text(f'{'FIRST HOUSE'}', size=20)
# # third_track.text(f'{'ARIES HOUSE'}', size=20)
# track_aries.text(f'{"I"}', size=50, color="#3300cc")
#
# sector_leo = circos_rev.get_sector("♌︎")
# # sector_leo.axis()
# track_leo = sector_leo.add_track((70,100))
# track_leo.axis(fc="#9933ff", ec='aliceblue')
# track_leo.text(f'{"♌︎"}', size=50, color='#ff1a00')
#
# sector_sag = circos_rev.get_sector("♐︎")
# # sector_sag.axis()
# track_sag = sector_sag.add_track((70,100))
# track_sag.axis(fc="#6600ff", ec='aliceblue')
# track_sag.text(f'{"♐︎"}', size=40, color='#ff1a00')
#
# sector_aqua = circos_rev.get_sector("♒︎")
# # sector_aqua.axis()
# track_aqua = sector_aqua.add_track((70,100))
# track_aqua.axis(fc="#9933ff", ec='aliceblue')
# track_aqua.text(f'{"♒︎"}', size=40, color='#ffd700')
#
# sector_gemini = circos_rev.get_sector("♊︎")
# # sector_gemini.axis()
# track_gemini = sector_gemini.add_track((70,100))
# track_gemini.axis(fc="#6600ff", ec='aliceblue')
# track_gemini.text(f'{"♊︎"}', size=40, color='#ffd700')
#
# sector_libra = circos_rev.get_sector("♎︎")
# # sector_libra.axis()
# track_libra = sector_libra.add_track((70,100))
# track_libra.axis(fc="#3300cc", ec='aliceblue')
# track_libra.text(f'{"♎︎"}', size=40, color='#ffd700')
#
# sector_taurus = circos_rev.get_sector("♉︎")
# # sector_taurus.axis()
# track_taurus = sector_taurus.add_track((70,100))
# track_taurus.axis(fc="#9933ff", ec='aliceblue', lw=3 )
# track_taurus.text(f'{"♉︎"}', size=40, color='#99FF33')
#
# sector_virgo = circos_rev.get_sector("♍︎")
# # sector_virgo.axis()
# track_virgo = sector_virgo.add_track((70,100))
# track_virgo.axis(fc="#6600ff", ec='aliceblue')
# track_virgo.text(f'{"♍︎"}', size=40, color='#99FF33')
#
# sector_capricon = circos_rev.get_sector("♑︎")
# # sector_capricon.axis()
# track_capricon = sector_capricon.add_track((70,100))
# track_capricon.axis(fc="#3300cc", ec='aliceblue')
# track_capricon.text(f'{"♑︎"}', size=40, color='#99FF33')
#
# sector_cancer = circos_rev.get_sector("♋︎")
# # sector_cancer.axis()
# track_cancer = sector_cancer.add_track((70,100))
# track_cancer.axis(fc="#3300cc", ec='aliceblue')
# track_cancer.text(f'{"♋︎"}', size=40, color='#34b806')
#
# sector_scorpio = circos_rev.get_sector("♏︎")
# # sector_scorpio.axis()
# track_scorpio = sector_scorpio.add_track((70,100))
# track_scorpio.axis(fc="#9933ff", ec='aliceblue')
# track_scorpio.text(f'{"♏︎"}', size=40, color='#34b806')
#
# sector_pisces = circos_rev.get_sector("♓︎")
# # sector_pisces.axis()
# track_pisces = sector_pisces.add_track((70,100))
# track_pisces.axis(fc="#6600ff", ec='aliceblue')
# track_pisces.text(f'{"♓︎"}', size=40, color='#34b806')






fig = circos_rev.plotfig()
fig.patch.set_alpha(0.0)
fig.savefig('astrohouses.png', pad_inches=0.0)
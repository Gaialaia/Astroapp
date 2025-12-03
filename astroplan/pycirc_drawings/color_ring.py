from pycirclize import Circos


sectors = {"♐︎": 30,  "♎︎" : 30,  "♏︎" : 30,
            "♍︎": 30,"♌︎": 30,  "♋︎": 30,
            "♊︎": 30,  "♉︎": 30, "♈︎" : 30,
            "♓︎": 30,  "♒︎" : 30, "♑︎": 30,
           }



circos = Circos(sectors)

sector_aries = circos.get_sector("♈︎")
track_aries = sector_aries.add_track((20, 100))
track_aries.axis(fc="red", ec="aliceblue")


sector_leo = circos.get_sector("♌︎")
track_leo = sector_leo.add_track((20,100))
track_leo.axis(fc="yellow", ec='aliceblue')


sector_sag = circos.get_sector("♐︎")
track_sag = sector_sag.add_track((20,100))
track_sag.axis(fc="steelblue", ec='aliceblue')


sector_aqua = circos.get_sector("♒︎")
track_aqua = sector_aqua.add_track((20,100))
track_aqua.axis(fc="blueviolet", ec='aliceblue')


sector_gemini = circos.get_sector("♊︎")
track_gemini = sector_gemini.add_track((20,100))
track_gemini.axis(fc="orange", ec='aliceblue')


sector_libra = circos.get_sector("♎︎")
track_libra = sector_libra.add_track((20,100))
track_libra.axis(fc="lightseagreen", ec='aliceblue')


sector_taurus = circos.get_sector("♉︎")
track_taurus = sector_taurus.add_track((20,100))
track_taurus.axis(fc="orangered", ec='aliceblue')


sector_virgo = circos.get_sector("♍︎")
track_virgo = sector_virgo.add_track((20,100))
track_virgo.axis(fc="yellowgreen", ec='aliceblue')


sector_capricon = circos.get_sector("♑︎")
track_capricon = sector_capricon.add_track((20,100))
track_capricon.axis(fc="slateblue", ec='aliceblue')


sector_cancer = circos.get_sector("♋︎")
track_cancer = sector_cancer.add_track((20,100))
track_cancer.axis(fc="#FFAA33", ec='aliceblue')


sector_scorpio = circos.get_sector("♏︎")
track_scorpio = sector_scorpio.add_track((20,100))
track_scorpio.axis(fc="#00BFFF", ec='aliceblue')


sector_pisces = circos.get_sector("♓︎")
track_pisces = sector_pisces.add_track((20,100))
track_pisces.axis(fc="indigo", ec='aliceblue')


fig = circos.plotfig()
fig.patch.set_alpha(0.0)
fig.savefig('zr_in_colors.png', pad_inches=0.0)




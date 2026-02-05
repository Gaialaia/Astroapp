from pycirclize import Circos

sectors = {"♊︎": 30, "♉︎": 30, "♈︎": 30,
           "♓︎": 30, "♒︎": 30, "♑︎": 30,
           "♐︎": 30, "♏︎": 30, "♎︎": 30,
           "♍︎": 30, "♌︎": 30, "♋︎": 30,
           }

circos = Circos(sectors)

sector_aries = circos.get_sector("♈︎")
track_aries = sector_aries.add_track((70, 95))
track_aries.axis(ec='aliceblue', lw=1)
track_aries.axis(fc="#3300cc", alpha=0.3)
track_aries.text(f'{"♈︎"}', size=50, color='#ff1a00')

sector_leo = circos.get_sector("♌︎")
# sector_leo.axis()
track_leo = sector_leo.add_track((70,95))
track_leo.axis(ec='aliceblue', lw=1)
track_leo.axis(fc="#9933ff",alpha=0.3 )
track_leo.text(f'{"♌︎"}', size=50, color='#ff1a00')

sector_sag = circos.get_sector("♐︎")
# sector_sag.axis()
track_sag = sector_sag.add_track((70,95))
track_sag.axis(ec='aliceblue', lw=1)
track_sag.axis(fc="#6700ff", alpha=0.3)
track_sag.text(f'{"♐︎"}', size=50, color='#ff1a00')

sector_aqua = circos.get_sector("♒︎")
# sector_aqua.axis()
track_aqua = sector_aqua.add_track((70,95))
track_aqua.axis(ec='aliceblue', lw=1)
track_aqua.axis(fc="#9933ff", alpha=0.3)
track_aqua.text(f'{"♒︎"}', size=50, color='#ffd700')

sector_gemini = circos.get_sector("♊︎")
# sector_gemini.axis()
track_gemini = sector_gemini.add_track((70,95))
track_gemini.axis(ec='aliceblue', lw=1)
track_gemini.axis(fc="#6700ff", alpha=0.3)
track_gemini.text(f'{"♊︎"}', size=50, color='#ffd700')

sector_libra = circos.get_sector("♎︎")
# sector_libra.axis()
track_libra = sector_libra.add_track((70,95))
track_libra.axis(ec='aliceblue', lw=1)
track_libra.axis(fc="#3300cc", alpha=0.3)
track_libra.text(f'{"♎︎"}', size=50, color='#ffd700')

sector_taurus = circos.get_sector("♉︎")
track_taurus = sector_taurus.add_track((70,95))
track_taurus.axis(ec='aliceblue', lw=1)
track_taurus.axis(ec='aliceblue')
track_taurus.axis(fc="#9933ff", alpha=0.3)
track_taurus.text(f'{"♉︎"}', size=50, color='#99FF33')

sector_virgo = circos.get_sector("♍︎")
# sector_virgo.axis()
track_virgo = sector_virgo.add_track((70,95))
track_virgo.axis(ec='aliceblue', lw=1)
track_virgo.axis(fc="#6700ff", alpha=0.3)
track_virgo.text(f'{"♍︎"}', size=50, color='#99FF33')

sector_capricon = circos.get_sector("♑︎")
# sector_capricon.axis()
track_capricon = sector_capricon.add_track((70,95))
track_capricon.axis(ec='aliceblue', lw=1)
track_capricon.axis(fc="#3300cc", alpha=0.3)
track_capricon.text(f'{"♑︎"}', size=50, color='#99FF33')

sector_cancer = circos.get_sector("♋︎")
# sector_cancer.axis()
track_cancer = sector_cancer.add_track((70,95))
track_cancer.axis(ec='aliceblue', lw=1)
track_cancer.axis(fc="#3300cc", alpha=0.3)
track_cancer.text(f'{"♋︎"}', size=50, color='#34b806')

sector_scorpio = circos.get_sector("♏︎")
# sector_scorpio.axis()
track_scorpio = sector_scorpio.add_track((70,95))
track_scorpio.axis(ec='aliceblue', lw=1)
track_scorpio.axis(fc="#9933ff", alpha=0.3)
track_scorpio.text(f'{"♏︎"}', size=50, color='#34b806')

sector_pisces = circos.get_sector("♓︎")

track_pisces = sector_pisces.add_track((70,95))
track_pisces.axis(ec='aliceblue')
track_pisces.axis(ec='aliceblue', lw=1)
track_pisces.axis(fc="#6600ff", alpha=0.3)
track_pisces.text(f'{"♓︎"}', size=50, color='#34b806')

for sector in circos.sectors:
    # sector.axis(lw=1, ec="thistle")  # turn off sector line (axis)

    track_deg = sector.add_track((95,100 ))
    track_deg.axis(ec='aliceblue', lw=0.8)
    track_deg.grid(y_grid_num=None, x_grid_interval=1, color='chartreuse')

fig = circos.plotfig()
fig.patch.set_alpha(0.0)

fig.savefig('drawings/zr_final_tr.png', pad_inches=0.0)
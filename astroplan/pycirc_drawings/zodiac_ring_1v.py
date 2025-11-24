from pycirclize import Circos

sectors = {"♊︎": 30, "♉︎": 30, "♈︎": 30,
           "♓︎": 30, "♒︎": 30, "♑︎": 30,
           "♐︎": 30, "♏︎": 30, "♎︎": 30,
           "♍︎": 30, "♌︎": 30, "♋︎": 30,
           }

circos = Circos(sectors)

sector_aries = circos.get_sector("♈︎")
track_aries = sector_aries.add_track((95, 80))
track_aries.axis(fc="#3300cc", ec="aliceblue")
track_aries.text(f'{"♈︎"}', size=27, color='#ff1a00')

sector_leo = circos.get_sector("♌︎")
track_leo = sector_leo.add_track((95, 80))
track_leo.axis(fc="#9933ff", ec='aliceblue')
track_leo.text(f'{"♌︎"}', size=27, color='#ff1a00')

sector_sag = circos.get_sector("♐︎")
track_sag = sector_sag.add_track((95, 80))
track_sag.axis(fc="#6600ff", ec='aliceblue')
track_sag.text(f'{"♐︎"}', size=27, color='#ff1a00')

sector_aqua = circos.get_sector("♒︎")
track_aqua = sector_aqua.add_track((95, 80))
track_aqua.axis(fc="#9933ff", ec='aliceblue')
track_aqua.text(f'{"♒︎"}', size=27, color='#ffd700')

sector_gemini = circos.get_sector("♊︎")
track_gemini = sector_gemini.add_track((95, 80))
track_gemini.axis(fc="#6600ff", ec='aliceblue')
track_gemini.text(f'{"♊︎"}', size=27, color='#ffd700')

sector_libra = circos.get_sector("♎︎")
track_libra = sector_libra.add_track((95, 80))
track_libra.axis(fc="#3300cc", ec='aliceblue')
track_libra.text(f'{"♎︎"}', size=27, color='#ffd700')

sector_taurus = circos.get_sector("♉︎")
track_taurus = sector_taurus.add_track((95, 80))
track_taurus.axis(fc="#9933ff", ec='aliceblue')
track_taurus.text(f'{"♉︎"}', size=27, color='#99FF33')

sector_virgo = circos.get_sector("♍︎")
track_virgo = sector_virgo.add_track((95, 80))
track_virgo.axis(fc="#6600ff", ec='aliceblue')
track_virgo.text(f'{"♍︎"}', size=27, color='#99FF33')

sector_capricon = circos.get_sector("♑︎")
track_capricon = sector_capricon.add_track((95, 80))
track_capricon.axis(fc="#3300cc", ec='aliceblue')
track_capricon.text(f'{"♑︎"}', size=27, color='#99FF33')

sector_cancer = circos.get_sector("♋︎")
track_cancer = sector_cancer.add_track((95, 80))
track_cancer.axis(fc="#3300cc", ec='aliceblue')
track_cancer.text(f'{"♋︎"}', size=27, color='#34b806')

sector_scorpio = circos.get_sector("♏︎")
track_scorpio = sector_scorpio.add_track((95, 80))
track_scorpio.axis(fc="#9933ff", ec='aliceblue')
track_scorpio.text(f'{"♏︎"}', size=27, color='#34b806')

sector_pisces = circos.get_sector("♓︎")
track_pisces = sector_pisces.add_track((95, 80))
track_pisces.axis(fc="#6600ff", ec='aliceblue')
track_pisces.text(f'{"♓︎"}', size=27, color='#34b806')

# for sector in circos.sectors:
#     # sector.axis(lw=1, ec="thistle")  # turn off sector line (axis)
#
#     track_deg = sector.add_track((95, 100))
#     track_deg.axis(ec='pink')
#     track_deg.grid(y_grid_num=None, x_grid_interval=1, color='blue')

fig = circos.plotfig()
fig.patch.set_alpha(0.0)
fig.savefig('zr_original.png', pad_inches=0.0)






#######################################################################

#
# color = '#330033'
#
# sector_aries = circos.get_sector("♈︎")
# # sector_aries.axis()
# track_aries = sector_aries.add_track((95, 80))
# track_aries.axis(fc="#ff3300", ec=color, lw=2)
# track_aries.text(f'{"♈︎"}', size=27, color='#6699cc')
#
# sector_leo = circos.get_sector("♌︎")
# # sector_leo.axis()
# track_leo = sector_leo.add_track((95, 80))
# track_leo.axis(fc="#ff6600", ec='#330033',lw=2)
# track_leo.text(f'{"♌︎"}', size=27, color='#6699ff')
#
# sector_sag = circos.get_sector("♐︎")
# # sector_sag.axis()
# track_sag = sector_sag.add_track((95, 80))
# track_sag.axis(fc="#ff0000", ec='#330033',lw=2)
# track_sag.text(f'{"♐︎"}', size=27, color='#669999')
#
# sector_aqua = circos.get_sector("♒︎")
# # sector_aqua.axis()
# track_aqua = sector_aqua.add_track((95, 80))
# track_aqua.axis(fc="#6699ff", ec='#330033',lw=2)
# track_aqua.text(f'{"♒︎"}', size=27, color='#ffd700')
#
# sector_gemini = circos.get_sector("♊︎")
# # sector_gemini.axis()
# track_gemini = sector_gemini.add_track((95, 80))
# track_gemini.axis(fc="#669999", ec='#330033', lw=2)
# track_gemini.text(f'{"♊︎"}', size=27, color='#ffff00')
#
# sector_libra = circos.get_sector("♎︎")
# # sector_libra.axis()
# track_libra = sector_libra.add_track((95, 80))
# track_libra.axis(fc="#6699cc", ec='#330033', lw=2)
# track_libra.text(f'{"♎︎"}', size=27, color='#ffd700')
#
# sector_taurus = circos.get_sector("♉︎")
# # sector_taurus.axis()
# track_taurus = sector_taurus.add_track((95, 80))
# track_taurus.axis(fc="#993300", ec='#330033', lw=2)
# track_taurus.text(f'{"♉︎"}', size=27, color='#99FF33')
#
# sector_virgo = circos.get_sector("♍︎")
# # sector_virgo.axis()
# track_virgo = sector_virgo.add_track((95, 80))
# track_virgo.axis(fc="#663300",  ec='#330033', lw=2)
# track_virgo.text(f'{"♍︎"}', size=27, color='#99FF33')
#
# sector_capricon = circos.get_sector("♑︎")
# # sector_capricon.axis()
# track_capricon = sector_capricon.add_track((95, 80))
# track_capricon.axis(fc="#330000",  ec='#330033', lw=2)
# track_capricon.text(f'{"♑︎"}', size=27, color='#99FF33')
#
# sector_cancer = circos.get_sector("♋︎")
# # sector_cancer.axis()
# track_cancer = sector_cancer.add_track((95, 80))
# track_cancer.axis(fc="#666666",  ec='#330033', lw=2)
# track_cancer.text(f'{"♋︎"}', size=27, color='#34b806')
#
# sector_scorpio = circos.get_sector("♏︎")
# # sector_scorpio.axis()
# track_scorpio = sector_scorpio.add_track((95, 80))
# track_scorpio.axis(fc="#666600",  ec='#330033', lw=2)
# track_scorpio.text(f'{"♏︎"}', size=27, color='#34b806')
#
# sector_pisces = circos.get_sector("♓︎")
# # sector_pisces.axis()
# track_pisces = sector_pisces.add_track((95, 80))
# track_pisces.axis(fc="#666699",  ec='#330033', lw=2)
# track_pisces.text(f'{"♓︎"}', size=27, color='#34b806')
#
# for sector in circos.sectors:
#     # sector.axis(lw=1, ec="thistle")  # turn off sector line (axis)
#
#     track_deg = sector.add_track((95, 100))
#     track_deg.axis(ec='#660033')
#     track_deg.grid(y_grid_num=None, x_grid_interval=1, color='blue')
#
# fig = circos.plotfig()
# fig.patch.set_alpha(0.0)
# fig.savefig('tr_zr_df.png')


edge_color_list = []
text_color_list =[]

def draw_zodiac_one_color(face_color, edge_color, text_color, font_size, line_width, tick_clr, deg_clr):
    for s in sectors.keys():
        zodiac_sector = circos.get_sector(s)
        zodiac_track = zodiac_sector.add_track((70,95))
        zodiac_track.axis(fc=face_color, ec=edge_color, lw=line_width)
        zodiac_track.text(f'{s}',size=font_size,color=text_color)

        for sector in circos.sectors:
            # sector.axis(lw=1, ec="thistle")  # turn off sector line (axis)

            track_deg = sector.add_track((95, 100))
            track_deg.axis(ec=tick_clr)
            track_deg.grid(y_grid_num=None, x_grid_interval=1, color=deg_clr)


    fig = circos.plotfig()
    fig.patch.set_alpha(0.0)
    fig.savefig('zr_dark.png')


# draw_zodiac_one_color('#A800D8','aliceblue','#2BC200', 30,3)


import random, string
face_color_list = []
choice_list = list(string.hexdigits)

def get_random_colors(list_name):
    for c in range(0, 12):
        random_color = random.choices(choice_list, k=6)
        rnd_c_str = '#' + ''.join(random_color)
        list_name.append(rnd_c_str)


get_random_colors(face_color_list)
get_random_colors(edge_color_list)
get_random_colors(text_color_list)

sign_colors_z = zip(sectors.keys(), face_color_list, edge_color_list, text_color_list)
sign_colors = list(sign_colors_z)


def draw_zodiac_df_color(list_name):
    for t in list_name:
        zodiac_sector = circos.get_sector(t[0])
        zodiac_track = zodiac_sector.add_track((80, 100))
        zodiac_track.axis(fc=t[1], ec=t[2], lw=2)
        zodiac_track.text(f'{t[0]}', size=27, color=t[3])

    fig = circos.plotfig(figsize=(8.3,8.3))
    fig.patch.set_alpha(0.0)
    fig.savefig('tr_for8.png', pad_inches=0.0, figsize=(6,6))

# draw_zodiac_df_color(sign_colors)

#
#
# draw_zodiac_one_color('#2d2b31','#e7e3f5','#e7e3f5',45,3, '#2d2b31','#2d2b31')

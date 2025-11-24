from pycirclize import Circos

sectors = {"♊︎": 30, "♉︎": 30, "♈︎": 30,
           "♓︎": 30, "♒︎": 30, "♑︎": 30,
           "♐︎": 30, "♏︎": 30, "♎︎": 30,
           "♍︎": 30, "♌︎": 30, "♋︎": 30,
           }

circos = Circos(sectors)

def draw_zodiac_one_color(face_color, edge_color, text_color, tick_clr, deg_clr, font_size, line_width):
    for s in sectors.keys():
        zodiac_sector = circos.get_sector(s)
        zodiac_track = zodiac_sector.add_track((70,94))
        zodiac_track.axis(fc=face_color, ec=edge_color, lw=line_width)
        zodiac_track.text(f'{s}',size=font_size,color=text_color)

        for sector in circos.sectors:
            track_deg = sector.add_track((94, 100))
            track_deg.axis(ec=tick_clr)
            track_deg.grid(y_grid_num=None, x_grid_interval=1, color=deg_clr)


    fig = circos.plotfig()
    fig.patch.set_alpha(0.0)
    fig.savefig('/home/gaia/PythonProject/astroapp/astroknow/astroplan/static/images/zr_one_clr.png',
                    pad_inches=0.0)



import os

# directory_path = '/home/gaia/PythonProject/astroapp/astroknow/media/chart_plots'
def remove_all_files_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Removed file: {file_path}")

remove_all_files_in_directory('/home/gaia/PythonProject/astroapp/astroknow/media/chart_plots')
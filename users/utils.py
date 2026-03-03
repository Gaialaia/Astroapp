import boto3
import os

from pycirclize import Circos
from astroknow import settings

sectors = {"♊︎": 30, "♉︎": 30, "♈︎": 30,
           "♓︎": 30, "♒︎": 30, "♑︎": 30,
           "♐︎": 30, "♏︎": 30, "♎︎": 30,
           "♍︎": 30, "♌︎": 30, "♋︎": 30,
           }

circos = Circos(sectors)


def draw_zodiac_one_color(face_color, edge_color, text_color, tick_clr,
                          deg_clr, font_size, line_width):

    for s in sectors.keys():
        zodiac_sector = circos.get_sector(s)
        zodiac_track = zodiac_sector.add_track((70, 94))
        zodiac_track.axis(fc=face_color, ec=edge_color, lw=line_width)
        zodiac_track.text(f'{s}', size=font_size, color=text_color)

        for sector in circos.sectors:
            track_deg = sector.add_track((94, 100))
            track_deg.axis(ec=tick_clr)
            track_deg.grid(y_grid_num=None, x_grid_interval=1, color=deg_clr)

    fig = circos.plotfig()
    fig.patch.set_alpha(0.0)

    chart_path = (os.path.join(settings.MEDIA_ROOT, 'color_chart_zodiac_ring/'
                                                    'zodiac_ring_background.png'))
    directory = os.path.dirname(chart_path)

    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    fig.savefig(chart_path, pad_inches=0.0)


def get_s3_client():

    session = boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name="ru-central1")
    return session.client("s3",
                          endpoint_url="https://storage.yandexcloud.net")


def upload_to_storage(buffer, plot_name, path):

    s3 = get_s3_client()
    bucket_name = os.getenv('BUCKET_NAME')
    s3_key = f"{path}{plot_name}"
    s3.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=buffer,
        ContentType='image/png',
        ACL='public-read'
    )
    return f"https://{bucket_name}.storage.yandexcloud.net/{s3_key}"


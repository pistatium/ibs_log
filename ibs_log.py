import csv
from time import sleep
from typing import NamedTuple, List
from datetime import datetime, timezone
from logging import getLogger

import click
import requests

logger = getLogger('ibs_log')

ENDPOINT = 'https://ibispaint.com/artistArtworkList.jsp'


class Artwork(NamedTuple):
    publish_date: datetime
    pv: int
    worktime: int

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            publish_date=parse_ts(d['publishDateLong']),
            pv=d['totalPV'],
            worktime=d['workTimeLong']
        )


def parse_ts(ts: int) -> datetime:
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc)


def fetch_artworks(page: int, artist_id: str, service_id: str) -> List[Artwork]:
    logger.debug(f'Fetching page={page} artist_id={artist_id} service_id={service_id}')
    params = {
        'page': page,
        'artistID': artist_id,
        'serviceID': service_id,
        'art': 'illust',
        'sort': 'new'
    }
    res = requests.get(ENDPOINT, params)
    res.raise_for_status()
    return [Artwork.from_dict(a) for a in res.json()['artworkList']]


def format_to_csv(artworks: List[Artwork]) -> str:
    output = 'publish_date, pv, worktime\n'
    for aw in artworks:
        output += f'{aw.publish_date.isoformat()}, {aw.pv}, {aw.worktime}\n'
    return output


@click.command()
@click.argument('artist-id')
@click.option('--service-id', '-s', default='twitter')
@click.option('--fetch-interval', '-i', default=1, type=int)
@click.option('--format', '-f', 'output_format', type=click.Choice(['csv', ]), default='csv')
def cmd(artist_id, service_id, fetch_interval, output_format):
    page = 0
    artworks = []

    while True:
        page += 1
        aws = fetch_artworks(page, artist_id, service_id)
        if not aws:
            break
        artworks.extend(aws)
        sleep(fetch_interval)
    if output_format == 'csv':
        click.echo(format_to_csv(artworks))


def main():
    cmd()


if __name__ == '__main__':
    main()
import click
from settings import BaseConfig
from flask.cli import with_appcontext
from models import Sitemap, SitemapTaskStatus
from models import session
from bs4 import BeautifulSoup
from decimal import Decimal
import datetime
import urllib.parse
import requests


class URL(click.ParamType):
    name = "url"

    def convert(self, value, param, ctx):
        if not isinstance(value, tuple):
            parse_result = urllib.parse.urlparse(value)
            if parse_result.scheme not in ("http", "https"):
                self.fail(
                    f"invalid URL scheme ({parse_result.scheme}). Only HTTP URLs are allowed",
                    param,
                    ctx,
                )
        return {"value": value,
                "parse_result": parse_result}


def strptime(date_text):
    try:
        return datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
    except:
        ValueError
    return datetime.datetime.strptime(date_text, '%Y-%m-%d')


@click.command('save_sitemap', help="Save the sitemap given as an url argument in the database")
@click.argument('url_object', type=URL())
@with_appcontext
def save_sitemap(url_object):
    url = url_object.get("value")
    headers = {'User-Agent': BaseConfig.UA}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    urls = soup.find_all("url")
    for url in urls:
        if not url.loc:
            raise ValueError("url.loc is None...")

        parse_result = urllib.parse.urlparse(url.loc.text)
        sitemap = session.query(Sitemap).filter(Sitemap.loc == urllib.parse.unquote(url.loc.text)).first()

        if sitemap is None:
            sitemap = Sitemap()
            sitemap.loc = urllib.parse.unquote(url.loc.text)
            sitemap.lastmod = strptime(url.lastmod.text) if url.lastmod else None
            sitemap.change_freq = url.changefreq.text if url.changefreq else None
            sitemap.priority = Decimal(url.priority.text) if url.priority else None
            sitemap.domain = parse_result.netloc
            sitemap.path = urllib.parse.unquote(parse_result.path)
            sitemap.status = SitemapTaskStatus.before_html_stats
            sitemap.add(sitemap)
        elif sitemap.lastmod is None or sitemap.lastmod > strptime(url.lastmod.text) if url.lastmod else None :
            sitemap.lastmod = strptime(url.lastmod.text) if url.lastmod else None
            sitemap.status = SitemapTaskStatus.before_html_stats
            session.merge(sitemap)
        session.flush()

    session.commit()

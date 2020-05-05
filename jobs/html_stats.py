import click
from settings import BaseConfig
from flask.cli import with_appcontext
from models import Sitemap, SitemapTaskStatus, HtmlStats
from models import session
from bs4 import BeautifulSoup
import datetime
import urllib.parse
import requests


@click.command('html_stats', help="Save html stats in the database")
@with_appcontext
def html_stats():

    sitemaps = Sitemap.get_by_status(SitemapTaskStatus.before_html_stats)
    for sitemap in sitemaps:

        headers = {'User-Agent': BaseConfig.UA}
        r = requests.get(urllib.parse.quote(sitemap.loc, safe=':/'), headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        text = ''.join(soup.findAll(text=True))
        html_stats = HtmlStats()
        html_stats.loc = sitemap.loc
        html_stats.domain = sitemap.domain
        html_stats.path = sitemap.path
        html_stats.word_count = len(text)
        html_stats.number_of_punctuation_marks = (text.count("、") + text.count("。"))
        html_stats.number_of_h1 = len(soup.find_all('h1'))
        html_stats.number_of_h2 = len(soup.find_all('h2'))
        html_stats.number_of_h3 = len(soup.find_all('h3'))
        html_stats.number_of_h4 = len(soup.find_all('h4'))
        html_stats.number_of_h5 = len(soup.find_all('h5'))
        html_stats.number_of_h6 = len(soup.find_all('h6'))
        html_stats.number_of_table = len(soup.find_all('table'))
        html_stats.number_of_li = len(soup.find_all('li'))
        html_stats.number_of_dl = len(soup.find_all('dl'))
        html_stats.number_of_image = len(soup.find_all('img'))
        html_stats.number_of_a = len(soup.find_all('a'))
        html_stats.number_of_iframe = len(soup.find_all('iframe'))
        html_stats.update_at = datetime.datetime.now()
        sitemap.status = SitemapTaskStatus.task_done
        session.merge(html_stats)
        session.flush()

    session.commit()

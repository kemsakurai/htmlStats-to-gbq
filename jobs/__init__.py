from flask.cli import AppGroup
from jobs.save_sitemap import save_sitemap
from jobs.html_stats import html_stats
from jobs.save_to_gbq import save_to_gbq

job = AppGroup('job')
job.add_command(save_sitemap)
job.add_command(html_stats)
job.add_command(save_to_gbq)

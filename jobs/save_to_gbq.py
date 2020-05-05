import os

import click
import datetime
import json
from flask.cli import with_appcontext
from google.cloud import bigquery

import gbq_conf
from models import HtmlStats

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gbq_conf.CREDENTIALS_JSON

schema = [
    bigquery.SchemaField('loc', 'STRING', mode='REQUIRED', description='url'),
    bigquery.SchemaField('domain', 'STRING', mode='REQUIRED', description='domain'),
    bigquery.SchemaField('path', 'STRING', mode='REQUIRED', description='path'),
    bigquery.SchemaField('create_at', 'DATETIME', mode='REQUIRED', description='create_at'),
    bigquery.SchemaField('update_at', 'DATETIME', mode='REQUIRED', description='update_at'),
    bigquery.SchemaField('word_count', 'INT64', mode='REQUIRED', description='Word count of HTML'),
    bigquery.SchemaField('number_of_punctuation_marks', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('number_of_h1', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('number_of_h2', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('number_of_h3', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('number_of_h4', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('number_of_h5', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('number_of_h6', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('number_of_table', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('number_of_li', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('number_of_dl', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('number_of_image', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('number_of_a', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('number_of_iframe', 'INT64', mode='REQUIRED'),
]


def support_datetime_default(o):
    if isinstance(o, datetime.datetime):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")


@click.command('save_to_gbq', help="Save html statistics in the google big query")
@with_appcontext
def save_to_gbq():
    html_stats = HtmlStats.get_all()
    insert_rows = []
    for html_stat in html_stats:
        dictionary = html_stat.__dict__
        del dictionary['_sa_instance_state']
        dictionary = json.loads(json.dumps(dictionary, default=support_datetime_default))
        insert_rows.append(dictionary)

    bigquery_client = bigquery.Client(project=gbq_conf.PROJECT)
    table_id = "{0}.{1}.{2}".format(gbq_conf.PROJECT, gbq_conf.DATASET, gbq_conf.TABLE)
    bigquery_client.delete_table(table_id, not_found_ok=True)
    dataset_ref = bigquery_client.get_dataset(gbq_conf.DATASET)
    table_ref = dataset_ref.table(gbq_conf.TABLE)
    table = bigquery.Table(table_ref, schema=schema)
    table = bigquery_client.create_table(table, exists_ok=False)
    bigquery_client.insert_rows_json(table, insert_rows)

import datetime
import enum

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import BaseConfig

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    Migrate(app, db)


engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()


class SitemapTaskStatus(enum.Enum):
    before_html_stats = 1
    failed_html_stats = 2
    task_done = 99


class Sitemap(db.Model):
    __tablename__ = 't_sitemap'

    loc = db.Column(db.String(length=2083), primary_key=True, nullable=False)
    domain = db.Column(db.String(length=2083), nullable=False)
    path = db.Column(db.String(length=2083), nullable=False)
    lastmod = db.Column(db.DATETIME(), nullable=True)
    change_freq = db.Column(db.String(length=10), nullable=True)
    priority = db.Column(db.String(length=5), nullable=True)
    status = db.Column(db.Enum(SitemapTaskStatus))

    @classmethod
    def create(cls, domain, loc, path, lastmod, change_freq, priority):
        obj = cls(domain=domain, loc=loc, lastmod=lastmod, path=path, change_freq=change_freq, priority=priority,
                  status=SitemapTaskStatus.before_html_stats)
        db.session.add(obj)
        return obj

    @classmethod
    def get_by_status(cls, status):
        return db.session.query(cls).filter(cls.status == status).all();

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()


class HtmlStats(db.Model):
    loc = db.Column(db.String(length=2083), primary_key=True, nullable=False)
    domain = db.Column(db.String(length=2083), nullable=False)
    path = db.Column(db.String(length=2083), nullable=False)
    create_at = db.Column(db.DATETIME(), nullable=False, default=datetime.datetime.now())
    update_at = db.Column(db.DATETIME(), nullable=False)
    word_count = db.Column(db.INTEGER, nullable=False)
    number_of_punctuation_marks = db.Column(db.INTEGER, nullable=False)
    number_of_h1 = db.Column(db.INTEGER, nullable=False)
    number_of_h2 = db.Column(db.INTEGER, nullable=False)
    number_of_h3 = db.Column(db.INTEGER, nullable=False)
    number_of_h4 = db.Column(db.INTEGER, nullable=False)
    number_of_h5 = db.Column(db.INTEGER, nullable=False)
    number_of_h6 = db.Column(db.INTEGER, nullable=False)
    number_of_table = db.Column(db.INTEGER, nullable=False)
    number_of_li = db.Column(db.INTEGER, nullable=False)
    number_of_dl = db.Column(db.INTEGER, nullable=False)
    number_of_image = db.Column(db.INTEGER, nullable=False)
    number_of_a = db.Column(db.INTEGER, nullable=False)
    number_of_iframe = db.Column(db.INTEGER, nullable=False)
    
    @classmethod
    def get_by_loc(cls, loc):
        return db.session.query(cls).filter(cls.loc == loc).first()

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

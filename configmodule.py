# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash


class Config(object):
	DATABASE = '/tmp/flaskr.db'
	SECRET_KEY = 'development key'
	USERNAME = 'admin'
	PASSWORD = 'default'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
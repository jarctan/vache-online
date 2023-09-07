"""Configuration for the app."""

from os import environ

class Config:
    """ Flask configuration. """
    SECRET_KEY = environ.get('SECRET_KEY')

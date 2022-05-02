import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or\
                 """9bbf38a8a2e021054285a22077787417bd1cfa81c04e712a360e3aa091371a86f7b8ace538d07f389d62fd9bfaf8c0aa0872ceb76aaf0b86615914d1bfe921bf"""

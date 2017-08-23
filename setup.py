import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "gmail_parser",
    version = "0.0.1",
    author = "Shoval Sadde",
    author_email = "shoval_sade@walla.co.il",
    description = ("stores messages from gmail in SQL for further parsing Edit."),
    license = "MIT",
    keywords = "gmail SQL parsing",
    url = "https://github.com/shovalsa/gmail_parser",
    packages=['gmail_parser'],
    long_description=read('README.md'),
)
import csv
import requests
from collections import namedtuple
import attr
from zipfile import ZipFile
from io import BytesIO, TextIOWrapper, StringIO
import io
import sys
from tempfile import TemporaryFile
import codecs
from six import text_type

NACE_COLUMNS = (
    "order",
    "level",
    "code",
    "parent",
    "description",
    "includes",
    "also_includes",
    "rulings",
    "excludes",
    "reference_to_ISIC_Rev_4"
)


@attr.s
class NACE_URL(object):
    url = attr.ib()
    lang = attr.ib()


@attr.s
class NACE_ROW(object):
    order = attr.ib()
    level = attr.ib()
    code = attr.ib()
    parent = attr.ib()
    description = attr.ib()
    includes = attr.ib()
    also_includes = attr.ib()
    rulings = attr.ib()
    excludes = attr.ib()
    reference_to_ISIC_rev_4 = attr.ib()

    def astuple(self):
        return attr.astuple(self)

    def __str__(self):
        return '{}: {}'.format(self.code, self.description)


class NACEDB(object):
    def __init__(self, db=[]):
        self._db = db
        self.original_columns = self._db.pop(0)
        self.columns = NACE_COLUMNS

    @classmethod
    def load_from_url(cls, csv_file_url):
        csv = cls._load_from_url(csv_file_url)
        return cls.from_chunk(csv)

    @classmethod
    def from_chunk(cls, chunk):
        db = list(csv.reader(chunk.splitlines()))
        return cls(db)

    @classmethod
    def from_file(cls, file):
        db = list(csv.reader(file))
        return cls(db)

    def include_only_codes(self, code_list=[]):
        """
        Return a NACE object with only matching business activity from the provided
        code list.
        """
        filtered_codes = filter(lambda row: row[2] in code_list, self._db)
        return [self._row_as_namedtuple(row) for row in filtered_codes]
    
    @staticmethod
    def _row_as_namedtuple(row):
        return NACE_ROW(*row)

    def all(self):
        return [self._row_as_namedtuple(row) for row in self._db]


class NACECodesService(object):
    def __init__(self, **kwargs):
        self._cached_dbs = {}
        self._files_urls = kwargs

    @classmethod
    def get_contents_from_url(cls, url):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        content_decoded = response.content.decode('utf8')
        return content_decoded

    def get_db_by_lang(self, language):
        if language in self._cached_dbs.keys():
            return self._cached_dbs[language]
        language_url = self._files_urls[language]
        localised_nace_db = self.load_from_url(language_url)
        self._cached_dbs[language] = localised_nace_db
        return localised_nace_db

    @classmethod
    def load_from_url(cls, url):
        content = cls.get_contents_from_url(url)
        return NACEDB.from_chunk(content)


ZIP_URL = 'https://github.com/MuhistheHolvi/nace_codes/raw/main/NACE_EN_FI_DE.zip'
URL_GERMAN = 'https://gist.githubusercontent.com/MuhistheHolvi/b4f5eb662cb2a1af5ba1eca7e75d7c27/raw/5c1e3eeadd5d407f759be8507b2106b7dd597a95/NACE_V2_EN.csv'
URL_ENGLISH = "https://gist.githubusercontent.com/MuhistheHolvi/7df41fe9232d0d6d69b5118aed63f1b1/raw/ce3a1b104b28989b2b3ede810f4879828ac5da7c/NACE_V2_EN.csv"
# db = NACEDB.load_from_url(csv_file_url=URL_ENGLISH)
# dbb= db.include_only_codes(['01', 'A'])
URLS = {
    'EN': URL_ENGLISH,
    'DE': URL_GERMAN,
}
service = NACECodesService(**URLS)
import ipdb; ipdb.set_trace()
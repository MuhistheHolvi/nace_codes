import csv
import requests
from collections import namedtuple
import attr
from zipfile import ZipFile


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
        self.original_columns = self._db.pop()
        self.columns = NACE_COLUMNS

    @classmethod
    def load_from_url(cls, csv_file_url):
        csv = cls._load_from_url(csv_file_url)
        return cls.from_chunk(csv)

    @classmethod
    def from_chunk(cls, chunk):
        db = list(csv.reader(chunk.splitlines()))
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
    @classmethod
    def download_file(cls, url):
        response = requests.get(url)
        response.raise_for_status()
        decoded_content = response.content.decode('utf-8')
        return decoded_content

    @classmethod
    def extract_files(cls, zip_file_contents):
        zip_file = ZipFile(zip_file_contents)
        extracted_files = [
            (cls.extract_language_from_file_name(file_name), zip_file.read(file_name)) for file_name in zip_file.namelist()
        ]
        return tuple(extracted_files)

    @staticmethod
    def extract_language_from_file_name(cls, file_name):
        language = file_name[-6, -4]
        if not(file_name.endswith('.csv') and language.isupper()):
            raise ValueError('File name must end with XX.csv where XX is capitalized language code')
        return language

    @classmethod
    def load_file_from_local(cls, file_name):
        pass

    def load_nace_databases(self, zip_url, on_desk=False, languages=['EN']):
        pass
    
    @staticmethod
    def db_for_lang(self, language):
        pass


URL_GERMAN = 'https://gist.githubusercontent.com/MuhistheHolvi/b4f5eb662cb2a1af5ba1eca7e75d7c27/raw/5c1e3eeadd5d407f759be8507b2106b7dd597a95/NACE_V2_EN.csv'
URL_ENGLISH = "https://gist.githubusercontent.com/MuhistheHolvi/7df41fe9232d0d6d69b5118aed63f1b1/raw/ce3a1b104b28989b2b3ede810f4879828ac5da7c/NACE_V2_EN.csv"
db = NACEDB.load_from_url(csv_file_url=URL_ENGLISH)
dbb= db.include_only_codes(['01', 'A'])
print(dbb)
import ipdb; ipdb.set_trace()
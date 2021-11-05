import csv342 as csv
import requests
from pynace.models import NACERow
import pkgutil
import os
from six import text_type
from typing import Dict, Tuple  # noqa


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


class NACEDB(object):
    """Database for NACE codes.
    The database provide an api to interact with NACE codes. CSV files
    from EU Ramon are deserialized into python objects.
    Row tuples from csv (row of strings) can be accessed using
    `_data` property.
    """
    def __init__(self, db=[]):
        self._db = db
        self.original_columns = self._db.pop(0)
        self.columns = NACE_COLUMNS

    @classmethod
    def from_chunk(cls, chunk):
        db = list(csv.reader(chunk.splitlines()))
        return cls(db)

    @classmethod
    def from_file(cls, file):
        db = list(csv.reader(file))
        return cls(db)

    def filter_codes_in(self, *args):
        # type Tuple[str] -> [NACERow]
        """Return a NACE object with only matching business activity from the
        provided code list.

        Returns:
            List[NACERow]: List of NACERow matching codes provided to filter.
        """
        code_list = args
        filtered_codes = filter(lambda row: row[2] in code_list, self._db)
        return [self._row_as_namedtuple(row) for row in filtered_codes]

    @staticmethod
    def _row_as_namedtuple(row):
        return NACERow(*row)

    def all(self):
        return [self._row_as_namedtuple(row) for row in self._db]


class NACECodes(object):
    BUILTIN_LANGUAGES = ['EN', 'FI', "DE"]

    def __init__(self, **kwargs):
        self._cached_dbs = {}  # type: Dict[str, NACEDB]
        self._files_urls = kwargs

    @classmethod
    def get_contents_from_url(cls, url):
        # type: (str) -> str
        response = requests.get(url, stream=True)
        response.raise_for_status()
        content_decoded = response.content.decode('utf8')
        return content_decoded

    def get_db_by_lang(self, language):
        # type: (str) -> NACEDB
        if language in self._cached_dbs.keys():
            return self._cached_dbs[language]
        localised_nace_db = self._load_db(language=language)
        self._cached_dbs[language] = localised_nace_db
        return localised_nace_db

    def _load_db(self, language):
        if self._files_urls:
            language_url = self._files_urls[language]
            return self.load_from_url(language_url)
        return self.load_db_from_local(language=language)

    @classmethod
    def load_from_url(cls, url):
        content = cls.get_contents_from_url(url)
        return NACEDB.from_chunk(content)

    @classmethod
    def load_db_from_local(cls, language):
        if language not in cls.BUILTIN_LANGUAGES:
            raise NotImplementedError(
                'Language is not supported, please load with url instead.'
            )
        csv_file = cls._load_lang_csv_file(language)
        return NACEDB.from_chunk(csv_file)

    @classmethod
    def _load_lang_csv_file(cls, language):
        file_name = cls._construct_file_name_for_language(language)
        full_path = os.path.join('db', file_name)
        return text_type(
            pkgutil.get_data(__name__, full_path), encoding='utf8'
        )

    @staticmethod
    def _construct_file_name_for_language(language):
        return 'NACE_REV2_{}.csv'.format(language)

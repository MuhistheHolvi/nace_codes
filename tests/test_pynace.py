from pynace import __version__
from pynace import interface


def test_version():
    assert __version__ == '0.1.0'


def test_nace_service():
    db = interface.NACECodes().get_db_by_lang('EN')
    assert len(db.all()) == 996
    selected_rows = db.filter_codes_in('A', '01', '01.1')
    assert [row.code for row in selected_rows] == ['A', '01', '01.1']

from pathlib import Path

from cheese import SubtitleParser
from cheese import SrtParser
import constants
import app


def test_srt_extract_meaning():
    with app.app.app_context():
        con_db = app.get_db()
        cursor = con_db.cursor()
        cursor.execute("USE cheese_project")
        srt_parser = SrtParser(constants.PATH_SRT / Path("lionking.srt"), con_db)  # noqa
        sentences = srt_parser.extract_sentences()
        words = srt_parser.extract_words(sentences)
        meanings = srt_parser.dict_parser.search_dict(words, con_db)
        answers = {
            'day': '1.날, 2.하루, 3.낮, 4.데이, 5.시절',
            'arrive': '1.도착하다, 2.오다, 3.가다, 4.도래하다, 5.도달하다',
            'planet': '1.행성, 2.혹성, 3.유성',
            'blinking': '1.깜박이는, 2.가물거리는, 3.지독한',
            'step': '1.단계, 2.조치, 3.걸음, 4.계단, 5.스텝',
            'sun': '1.태양, 2.해, 3.햇볕',
            'see': '1.보다, 2.알다, 3.만나다, 4.발견하다, 5.이해하다',
        }
        assert meanings == answers


def test_srt_extract_words():
    with app.app.app_context():
        con_db = app.get_db()
        srt_parser = SrtParser(constants.PATH_SRT / Path("lionking.srt"), con_db)  # noqa
        sentences = srt_parser.extract_sentences()
        words = srt_parser.extract_words(sentences)
        assert words == {
            "day": 1, "arrive": 1,
            "planet": 1, "blinking": 1,
            "see": 1, "step": 1, "sun": 1,
        }


def test_srt_extract_sentence():
    with app.app.app_context():
        con_db = app.get_db()
        srt_parser = SrtParser(constants.PATH_SRT / Path("lionking.srt"), con_db)  # noqa
        sentences = srt_parser.extract_sentences()
        assert sentences == [
            " from the day we arrive ",
            " on the planet ",
            " and blinking step into the sun ",
            " there more to see ",
        ]


def test_remove_tag():
    sub = SubtitleParser()
    sub_line = sub.remove_tag("<i>There's more to see</i>")
    assert sub_line == " There's more to see "

    sub_line = sub.remove_tag("<i>There's more to see</i>")
    assert sub_line == " There's more to see "

    sub_line = sub.remove_tag("<p>There's more to see</p>")
    assert sub_line == " There's more to see "

    sub_line = sub.remove_tag("<p>There's more to see</p>")
    assert sub_line == " There's more to see "

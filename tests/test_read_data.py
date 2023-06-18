from dotenv import load_dotenv, dotenv_values


config = dotenv_values()
path = config.get('PATH_TO_FILE')


def test_read_foo():
    assert True

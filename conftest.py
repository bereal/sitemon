import pytest

#  https://stackoverflow.com/a/47567535/770830
def pytest_addoption(parser):
    parser.addoption('--integrated', action='store_true')

def pytest_runtest_setup(item):
    if 'integrated' in item.keywords and not item.config.getoption("--integrated"):
        pytest.skip("skipping integrated test without --integrated")
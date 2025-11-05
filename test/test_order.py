import logging

import pytest
from lib import get_head

from backend.models import Category


def test_smth(session):
    logging.error(get_head(session, Category))
    assert 1 == 0

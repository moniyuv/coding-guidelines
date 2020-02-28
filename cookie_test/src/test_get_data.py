import pytest
import pandas as pd

from get_data import get_data


def test_get_data_is_inst():
    value = get_data()
    assert isinstance(value, type(pd.DataFrame()))


def test_get_data_dim():
    value = get_data().shape
    assert value[0] > 0
    assert value[1] > 0

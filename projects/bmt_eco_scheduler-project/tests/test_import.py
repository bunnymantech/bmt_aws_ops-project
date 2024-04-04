# -*- coding: utf-8 -*-

import os
import pytest
import bmt_eco_scheduler


def test_import():
    _ = bmt_eco_scheduler


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])

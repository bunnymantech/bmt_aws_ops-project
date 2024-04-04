# -*- coding: utf-8 -*-

from bmt_eco_scheduler.logger import logger
from bmt_eco_scheduler.lbd.hello import low_level_api


def _test_low_level_api():
    # invoke api
    response = low_level_api(name="alice")
    # validate response
    assert response["message"] == "hello alice"


def test_low_level_api():
    with logger.disabled(
        disable=True,
        # disable=False,
    ):
        _test_low_level_api()


if __name__ == "__main__":
    from bmt_eco_scheduler.tests import run_cov_test

    run_cov_test(__file__, "bmt_eco_scheduler.lbd.hello", preview=False)

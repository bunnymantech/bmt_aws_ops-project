# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from bmt_eco_scheduler.cron_helper import should_trigger_event


def test_should_trigger_event():
    assert (
        should_trigger_event("*/5 * * * *", datetime(2010, 1, 25, 4, 46), delta=120)
        is True
    )
    assert (
        should_trigger_event("*/5 * * * *", datetime(2010, 1, 25, 4, 48), delta=120)
        is False
    )


if __name__ == "__main__":
    from bmt_eco_scheduler.tests import run_cov_test

    run_cov_test(__file__, "bmt_eco_scheduler.cron_helper", preview=False)

# -*- coding: utf-8 -*-

from bmt_eco_scheduler.runtime import runtime


def test():
    _ = runtime


if __name__ == "__main__":
    from bmt_eco_scheduler.tests import run_cov_test

    run_cov_test(__file__, "bmt_eco_scheduler.runtime", preview=False)

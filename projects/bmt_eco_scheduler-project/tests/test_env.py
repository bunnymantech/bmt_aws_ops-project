# -*- coding: utf-8 -*-

from bmt_eco_scheduler.env import EnvNameEnum, detect_current_env


def test():
    _ = detect_current_env()


if __name__ == "__main__":
    from bmt_eco_scheduler.tests import run_cov_test

    run_cov_test(__file__, "bmt_eco_scheduler.env", preview=False)

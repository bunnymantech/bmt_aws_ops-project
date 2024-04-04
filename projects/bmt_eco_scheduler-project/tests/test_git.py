# -*- coding: utf-8 -*-

from bmt_eco_scheduler.git import git_repo


def test():
    _ = git_repo.git_branch_name
    _ = git_repo.semantic_branch_name


if __name__ == "__main__":
    from bmt_eco_scheduler.tests import run_cov_test

    run_cov_test(__file__, "bmt_eco_scheduler.git", preview=False)

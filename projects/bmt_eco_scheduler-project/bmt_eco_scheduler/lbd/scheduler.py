# -*- coding: utf-8 -*-

"""
"""

import typing as T

from ..logger import logger
from ..boto_ses import bsm
from ..config.load import config
from ..controllers.api import (
    Base,
    Ec2Instance,
    RdsInstance,
    RedshiftCluster,
)


@logger.pretty_log()
def low_level_api() -> dict:
    delta = config.env.delta
    params = [
        (Ec2Instance, bsm.ec2_client, delta),
        (RdsInstance, bsm.rds_client, delta),
        (RedshiftCluster, bsm.redshift_client, delta),
    ]
    response = dict()
    klass: T.Type[Base]
    for klass, client, delta in params:
        resource_ids_to_start, resource_ids_to_stop = klass().run(
            client=client, delta=delta
        )
        response[klass.__name__] = {
            "resource_ids_to_start": resource_ids_to_start,
            "resource_ids_to_stop": resource_ids_to_stop,
        }
    return response


def lambda_handler(event: dict, context):  # pragma: no cover
    return low_level_api()

# -*- coding: utf-8 -*-

from datetime import datetime

import moto
from rich import print as rprint

from bmt_eco_scheduler.logger import logger
from bmt_eco_scheduler.constants import TAG_START_AT, TAG_STOP_AT
from bmt_eco_scheduler.tests.mock_test import BaseMockTest
from bmt_eco_scheduler.lbd.scheduler import low_level_api


now = datetime.utcnow()


class Test(BaseMockTest):
    mock_list = [
        moto.mock_ec2,
        moto.mock_rds,
        moto.mock_redshift,
    ]

    @classmethod
    def setup_ec2_instance(cls):
        image_id = cls.bsm.ec2_client.describe_images()["Images"][0]["ImageId"]

        kwargs = dict(
            MinCount=1,
            MaxCount=1,
            ImageId=image_id,
        )

        def run_instance(tags: dict[str, str]) -> str:
            if not tags:
                tags = {}
            more_kwargs = dict(
                TagSpecifications=[
                    dict(
                        ResourceType="instance",
                        Tags=[dict(Key=k, Value=v) for k, v in tags.items()],
                    )
                ],
            )
            res = cls.bsm.ec2_client.run_instances(**kwargs | more_kwargs)
            instance_id = res["Instances"][0]["InstanceId"]
            return instance_id

        cls.ec2_inst_id_1 = run_instance(
            tags={"Name": "ec2-1", TAG_START_AT: f"{now.minute} {now.hour} * * *"}
        )
        cls.ec2_inst_id_2 = run_instance(
            tags={"Name": "ec2-2", TAG_STOP_AT: f"{now.minute} {now.hour} * * *"}
        )

        cls.bsm.ec2_client.stop_instances(InstanceIds=[cls.ec2_inst_id_1])

    @classmethod
    def setup_rds_db_instance(cls):
        def create_instance(id: str, tags: dict[str, str]) -> str:
            if not tags:
                tags = {}
            cls.bsm.rds_client.create_db_instance(
                DBInstanceIdentifier=id,
                DBInstanceClass="db.t2",
                Engine="postgres",
                Tags=[dict(Key=k, Value=v) for k, v in tags.items()],
            )
            return id

        cls.rds_db_inst_id_1 = create_instance(
            id="rds-inst-1",
            tags={TAG_START_AT: f"{now.minute} {now.hour} * * *"},
        )
        cls.rds_db_inst_id_2 = create_instance(
            id="rds-inst-2",
            tags={TAG_STOP_AT: f"{now.minute} {now.hour} * * *"},
        )
        cls.bsm.rds_client.stop_db_instance(DBInstanceIdentifier=cls.rds_db_inst_id_1)

    @classmethod
    def setup_redshift_cluster(cls):
        def create_cluster(id: str, tags: dict[str, str]) -> str:
            if not tags:
                tags = {}
            cls.bsm.redshift_client.create_cluster(
                ClusterIdentifier=id,
                NodeType="ds2.xlarge",
                MasterUsername="admin",
                Tags=[dict(Key=k, Value=v) for k, v in tags.items()],
            )
            return id

        cls.rs_cluster_id_1 = create_cluster(
            id="rs-1",
            tags={TAG_START_AT: f"{now.minute} {now.hour} * * *"},
        )
        cls.rs_cluster_id_2 = create_cluster(
            id="rs-2",
            tags={TAG_STOP_AT: f"{now.minute} {now.hour} * * *"},
        )

        cls.bsm.redshift_client.pause_cluster(ClusterIdentifier=cls.rs_cluster_id_1)

    @classmethod
    def setup_class_post_hook(cls):
        cls.setup_ec2_instance()
        cls.setup_rds_db_instance()
        cls.setup_redshift_cluster()

    def _test_low_level_api(self):
        res = low_level_api()
        # rprint(res)  # for debug only
        assert res["Ec2Instance"]["resource_ids_to_start"] == [self.ec2_inst_id_1]
        assert res["Ec2Instance"]["resource_ids_to_stop"] == [self.ec2_inst_id_2]
        assert res["RedshiftCluster"]["resource_ids_to_start"] == [self.rs_cluster_id_1]
        assert res["RedshiftCluster"]["resource_ids_to_stop"] == [self.rs_cluster_id_2]
        assert res["RdsInstance"]["resource_ids_to_start"] == [self.rds_db_inst_id_1]
        assert res["RdsInstance"]["resource_ids_to_stop"] == [self.rds_db_inst_id_2]

    def test_low_level_api(self):
        with logger.disabled(
            disable=True,
            # disable=False,
        ):
            self._test_low_level_api()


if __name__ == "__main__":
    from bmt_eco_scheduler.tests import run_cov_test

    run_cov_test(__file__, "bmt_eco_scheduler.lbd.scheduler", preview=False)

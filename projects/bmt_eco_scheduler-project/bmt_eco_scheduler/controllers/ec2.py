# -*- coding: utf-8 -*-

from .base import Base, T_ID, T_STATUS


class Ec2InstanceStateEnum:
    pending = "pending"
    running = "running"
    shutting_down = "shutting-down"
    terminated = "terminated"
    stopping = "stopping"
    stopped = "stopped"


class Ec2Instance(Base):
    def list_resources(self, client, **kwargs) -> list[tuple[T_ID, T_STATUS]]:
        paginator = client.get_paginator("describe_instance_status")
        tuples = list()
        for res in paginator.paginate(
            IncludeAllInstances=True,
        ):
            for dct in res.get("InstanceStatuses", []):
                tuples.append((dct["InstanceId"], dct["InstanceState"]["Name"]))
        return tuples

    def is_ready_to_start(self, status: T_STATUS) -> bool:
        return status in [
            Ec2InstanceStateEnum.stopped,
        ]

    def is_ready_to_stop(self, status: T_STATUS) -> bool:
        return status in [
            Ec2InstanceStateEnum.running,
        ]

    def start_many(self, client, id_list: list[T_ID]):
        client.start_instances(InstanceIds=id_list)

    def stop_many(self, client, id_list: list[T_ID]):
        client.stop_instances(InstanceIds=id_list)

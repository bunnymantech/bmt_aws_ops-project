# -*- coding: utf-8 -*-

import typing as T

from ..constants import TAG_START_AT, TAG_STOP_AT
from .base import Base, T_ID, T_STATUS, Resource


class Ec2InstanceStateEnum:
    pending = "pending"
    running = "running"
    shutting_down = "shutting-down"
    terminated = "terminated"
    stopping = "stopping"
    stopped = "stopped"


class Ec2Instance(Base):
    def list_resources(self, client, **kwargs) -> list[Resource]:
        paginator = client.get_paginator("describe_instances")
        resources = list()
        for res in paginator.paginate(
            Filters=[dict(Name="tag-key", Values=[TAG_START_AT, TAG_STOP_AT])],
        ):
            for dct1 in res.get("Reservations", []):
                for dct2 in dct1.get("Instances", []):
                    tags = {kv["Key"]: kv["Value"] for kv in dct2.get("Tags", [])}
                    start_at, stop_at = self.get_start_stop_at(tags)
                    resource = Resource(
                        id=dct2["InstanceId"],
                        status=dct2["State"]["Name"],
                        start_at=start_at,
                        stop_at=stop_at,
                    )
                    resources.append(resource)
        return resources

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

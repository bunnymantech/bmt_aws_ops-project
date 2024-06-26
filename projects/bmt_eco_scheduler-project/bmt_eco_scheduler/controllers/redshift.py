# -*- coding: utf-8 -*-

from .base import Base, T_ID, T_STATUS, Resource


class RedshiftClusterStatusEnum:
    available = "available"
    available_prep_for_resize = "available, prep-for-resize"
    available_resize_cleanup = "available, resize-cleanup"
    cancelling_resize = "cancelling-resize"
    creating = "creating"
    deleting = "deleting"
    final_snapshot = "final-snapshot"
    hardware_failure = "hardware-failure"
    incompatible_hsm = "incompatible-hsm"
    incompatible_network = "incompatible-network"
    incompatible_parameters = "incompatible-parameters"
    incompatible_restore = "incompatible-restore"
    modifying = "modifying"
    paused = "paused"
    rebooting = "rebooting"
    renaming = "renaming"
    resizing = "resizing"
    rotating_keys = "rotating-keys"
    storage_full = "storage-full"
    updating_hsm = "updating-hsm"


class RedshiftCluster(Base):
    def list_resources(self, client, **kwargs) -> list[Resource]:
        paginator = client.get_paginator("describe_clusters")
        resources = list()
        for res in paginator.paginate():
            for dct in res.get("Clusters", []):
                tags = {kv["Key"]: kv["Value"] for kv in dct.get("Tags", [])}
                start_at, stop_at = self.get_start_stop_at(tags)
                resource = Resource(
                    id=dct["ClusterIdentifier"],
                    status=dct["ClusterStatus"],
                    start_at=start_at,
                    stop_at=stop_at,
                )
                # print(resource)  # for debug only
                resources.append(resource)
        return resources

    def is_ready_to_start(self, status: T_STATUS) -> bool:
        return status in [
            RedshiftClusterStatusEnum.paused,
        ]

    def is_ready_to_stop(self, status: T_STATUS) -> bool:
        return status in [
            RedshiftClusterStatusEnum.available,
        ]

    def start_many(self, client, id_list: list[T_ID]):
        for id in id_list:
            client.resume_cluster(ClusterIdentifier=id)

    def stop_many(self, client, id_list: list[T_ID]):
        for id in id_list:
            client.pause_cluster(ClusterIdentifier=id)

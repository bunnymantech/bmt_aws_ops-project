# -*- coding: utf-8 -*-

from .base import Base, T_ID, T_STATUS


class RdsDBInstanceStatusEnum:
    # fmt: off
    available = "available"
    backing_up = "backing-up"
    configuring_enhanced_monitoring = "configuring-enhanced-monitoring"
    configuring_iam_database_auth = "configuring-iam-database-auth"
    configuring_log_exports = "configuring-log-exports"
    converting_to_vpc = "converting-to-vpc"
    creating = "creating"
    delete_precheck = "delete-precheck"
    deleting = "deleting"
    failed = "failed"
    inaccessible_encryption_credentials = "inaccessible-encryption-credentials"
    inaccessible_encryption_credentials_recoverable = "inaccessible-encryption-credentials-recoverable"
    incompatible_network = "incompatible-network"
    incompatible_option_group = "incompatible-option-group"
    incompatible_parameters = "incompatible-parameters"
    incompatible_restore = "incompatible-restore"
    insufficient_capacity = "insufficient-capacity"
    maintenance = "maintenance"
    modifying = "modifying"
    moving_to_vpc = "moving-to-vpc"
    rebooting = "rebooting"
    resetting_master_credentials = "resetting-master-credentials"
    renaming = "renaming"
    restore_error = "restore-error"
    starting = "starting"
    stopped = "stopped"
    stopping = "stopping"
    storage_full = "storage-full"
    storage_optimization = "storage-optimization"
    upgrading = "upgrading"
    # fmt: on


class RdsInstance(Base):
    def list_resources(self, client, **kwargs) -> list[tuple[T_ID, T_STATUS]]:
        paginator = client.get_paginator("describe_db_instances")
        tuples = list()
        for res in paginator.paginate():
            for dct in res.get("DBInstances", []):
                tuples.append((dct["DBInstanceIdentifier"], dct["DBInstanceStatus"]))
        return tuples

    def is_ready_to_start(self, status: T_STATUS) -> bool:
        return status in [RdsDBInstanceStatusEnum.stopped]

    def is_ready_to_stop(self, status: T_STATUS) -> bool:
        return status in [
            RdsDBInstanceStatusEnum.available,
        ]

    def start_many(self, client, id_list: list[T_ID]):
        for id in id_list:
            client.start_db_instance(DBInstanceIdentifier=id)

    def stop_many(self, client, id_list: list[T_ID]):
        for id in id_list:
            client.stop_db_instance(DBInstanceIdentifier=id)

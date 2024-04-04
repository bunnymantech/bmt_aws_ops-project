# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from datetime import datetime

from ..constants import TAG_START_AT, TAG_STOP_AT
from ..cron_helper import should_trigger_event

T_ID = str
T_STATUS = T.Any


@dataclasses.dataclass
class Resource:
    id: T_ID
    status: T_STATUS
    start_at: list[str]
    stop_at: list[str]


class Base:
    @staticmethod
    def get_start_stop_at(tags: dict[str, str]) -> tuple[list[str], list[str]]:
        start_at: T.Union[list[str], str] = tags.get(TAG_START_AT, [])
        stop_at: T.Union[list[str], str] = tags.get(TAG_STOP_AT, [])
        if start_at:
            start_at = start_at.split(";")
        if stop_at:
            stop_at = stop_at.split(";")
        return start_at, stop_at

    def list_resources(self, client, **kwargs) -> list[Resource]:
        """
        List all resources, Return list[tuple[identifier, state]]
        """
        raise NotImplementedError

    def is_ready_to_start(self, status: T_STATUS) -> bool:
        raise NotImplementedError

    def is_ready_to_stop(self, status: T_STATUS) -> bool:
        raise NotImplementedError

    def start_many(
        self,
        client,
        id_list: list[T_ID],
    ):
        raise NotImplementedError

    def stop_many(
        self,
        client,
        id_list: list[T_ID],
    ):
        raise NotImplementedError

    def run(
        self,
        client,
        delta: int,
    ) -> tuple[list[T_ID], list[T_ID]]:
        resources = self.list_resources(client)
        now = datetime.utcnow()

        resource_ids_to_start = list()
        resource_ids_to_stop = list()

        def func(resource: Resource):
            # for each resource, only the first match will be considered
            for cron in resource.start_at:
                if should_trigger_event(cron, now, delta):
                    if self.is_ready_to_start(resource.status):
                        resource_ids_to_start.append(resource.id)
                        return

            for cron in resource.stop_at:
                if should_trigger_event(cron, now, delta):
                    if self.is_ready_to_stop(resource.status):
                        resource_ids_to_stop.append(resource.id)
                        return

        for resource in resources:
            func(resource)

        if resource_ids_to_start:
            self.start_many(client, resource_ids_to_start)
        if resource_ids_to_stop:
            self.stop_many(client, resource_ids_to_stop)

        return resource_ids_to_start, resource_ids_to_stop

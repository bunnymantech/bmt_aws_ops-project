# -*- coding: utf-8 -*-

import typing as T


T_ID = str
T_STATUS = T.Any


class Base:
    def list_resources(self, client, **kwargs) -> list[tuple[T_ID, T_STATUS]]:
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

    @staticmethod
    def stop_many(
        client,
        id_list: list[T_ID],
    ):
        raise NotImplementedError

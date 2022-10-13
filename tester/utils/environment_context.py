# -*- coding: utf-8 -*-

from copy import deepcopy
from os import environ
from typing import Dict, Optional


def exchange_env(key: str, exchange: Optional[str]) -> Optional[str]:
    original = environ.get(key)
    if original is not None:
        environ.pop(key)
    if exchange is not None:
        environ[key] = exchange
    return original


class EnvironmentContext:

    _originals: Dict[str, Optional[str]]
    _exchanges: Dict[str, Optional[str]]

    def __init__(self, **kwargs: Optional[str]):
        self._exchanges = kwargs
        self._originals = dict()

    def open(self) -> Dict[str, Optional[str]]:
        originals = dict()
        for key, value in self._exchanges.items():
            originals[key] = exchange_env(key, value)
            assert environ.get(key) == value
        self._originals = originals
        return deepcopy(self._originals)

    def close(self) -> None:
        for key, value in self._originals.items():
            exchange_env(key, value)

    def __enter__(self) -> Dict[str, Optional[str]]:
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import TypeVar

AnyNamespace = TypeVar("AnyNamespace", bound=Namespace)


def strip_none_attributes(namespace: AnyNamespace) -> AnyNamespace:
    keys = list(vars(namespace).keys())
    for key in keys:
        if getattr(namespace, key) is None:
            delattr(namespace, key)
    return namespace

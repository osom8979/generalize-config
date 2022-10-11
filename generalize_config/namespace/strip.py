# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import TypeVar

AnyNamespace = TypeVar("AnyNamespace", bound=Namespace)


def strip_none_attributes(namespace: AnyNamespace) -> AnyNamespace:
    immutable_keys = list(vars(namespace).keys())
    for key in immutable_keys:
        assert hasattr(namespace, key)
        if getattr(namespace, key) is None:
            delattr(namespace, key)
    return namespace

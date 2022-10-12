# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Optional

from generalize_config.namespace.types import AnyNamespace


def mergeable_attribute(ns: Namespace, key: str, none_is_exist: bool) -> bool:
    if not hasattr(ns, key):
        return True
    if getattr(ns, key) is not None:
        return False
    return not none_is_exist


def merge_left_first(
    *namespaces: Optional[AnyNamespace],
    left_none_is_exist=False,
) -> AnyNamespace:
    """
    Insert if the attribute in the **left** namespace does not exist or is None.
    """

    if len(namespaces) == 0:
        raise IndexError("At least one argument is required")

    left = namespaces[0]
    for ns in namespaces[1:]:
        if not ns:
            continue

        if left is None:
            assert isinstance(ns, Namespace)
            left = ns
            continue

        for key, value in vars(ns).items():
            if mergeable_attribute(left, key, left_none_is_exist):
                setattr(left, key, value)

    if left is None:
        raise ValueError("At least one argument must not be None")

    return left


def merge_right_first(
    *namespaces: Optional[AnyNamespace],
    right_none_is_exist=False,
) -> AnyNamespace:
    """
    Insert if the attribute in the **right** namespace does not exist or is None.
    """

    if len(namespaces) == 0:
        raise IndexError("At least one argument is required")

    nss = list(namespaces)
    nss.reverse()
    return merge_left_first(*nss, left_none_is_exist=right_none_is_exist)

# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Any, Dict, Optional, Union

from generalize_config.inspect.member import get_public_instance_attributes


def parse_dict(
    obj: Union[Dict[str, Any], Any],
    *subsection: Optional[str],
) -> Namespace:
    if subsection:
        key = str(subsection[0])
        if isinstance(obj, dict):
            if key not in obj:
                raise KeyError(f"A `{key}` key not in the dictionary.")
            return parse_dict(obj[key], *subsection[1:])
        else:
            if not hasattr(obj, key):
                raise KeyError(f"A `{key}` key not in the object.")
            return parse_dict(getattr(obj, key), *subsection[1:])

    # The final depth of the recursion.
    return Namespace(**{k: v for k, v in get_public_instance_attributes(obj)})

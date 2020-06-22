# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import json
from pathlib import Path
from jsonom.pronom_data import PronomData
from typing import Dict, Any, Callable, Union

# -----------------------------------------------------------------------------
# Auxiliary functions
# -----------------------------------------------------------------------------


def recurse_dict(func: Callable, value: Union[dict, list]) -> None:
    if isinstance(value, dict):
        func(value)
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                func(item)


def fix_keys(in_dict: Dict[str, Any]) -> Dict[str, Any]:
    keys = list(in_dict.keys())
    for key in keys:
        value = in_dict[key]
        recurse_dict(fix_keys, value)
        new_key = key.strip("#@")
        in_dict[new_key] = in_dict.pop(key)
    return in_dict


def fix_byte_sequence(in_dict: Dict[str, Any]) -> Dict[str, Any]:
    keys = list(in_dict.keys())
    for key in keys:
        value = in_dict[key]
        recurse_dict(fix_byte_sequence, value)
        if "ByteSequence" in key and isinstance(value, dict):
            in_dict[key] = [value]
    return in_dict


def keys_to_lower(in_dict: Dict[str, Any]) -> Dict[str, Any]:
    keys = list(in_dict.keys())
    for key in keys:
        value = in_dict[key]
        recurse_dict(keys_to_lower, value)
        in_dict[key.lower()] = in_dict.pop(key)
    return in_dict


def json_dump(data: dict, file: Path) -> None:
    json.dump(
        data, file.open("w", encoding="utf-8"), indent=2, ensure_ascii=False
    )


# -----------------------------------------------------------------------------
# Data parsing
# -----------------------------------------------------------------------------

pronom_data = PronomData()
signature_file = pronom_data.latest_file("signature")
json_dump(signature_file, Path("D:\\data\\signature_file.json"))

container_file = pronom_data.latest_file("container")

fixed_signature_file = keys_to_lower(
    fix_byte_sequence(fix_keys(signature_file))
)
json_dump(fixed_signature_file, Path("D:\\data\\fixed_signature_file.json"))

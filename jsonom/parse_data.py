# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import re
import json
from pathlib import Path
from jsonom.pronom_data import PronomData
from typing import Dict, Any

# -----------------------------------------------------------------------------
# Auxiliary functions
# -----------------------------------------------------------------------------


def recurse_fix(in_dict: Dict[str, Any]) -> Dict[str, Any]:
    new_dict = dict()
    for key, value in in_dict.items():
        if isinstance(value, dict):
            return recurse_fix(value)
        if isinstance(value, list):
            for item in value:
                recurse_fix(item)
        new_key = key.strip("#@")
        new_dict[new_key] = value
    print(new_dict)
    return new_dict


def fix_keys(in_dict: Dict[str, Any]) -> Dict[str, Any]:
    keys = list(in_dict.keys())
    for key in keys:
        if re.match(r"@|#", key):
            print("Found key")
            new_key = key.strip("@#")
            in_dict[new_key] = in_dict.pop(key)
    return in_dict


def json_dump(data: dict, file: Path) -> None:
    json.dump(
        data, file.open("w", encoding="utf-8"), indent=2, ensure_ascii=False
    )


# -----------------------------------------------------------------------------
# Data parsing
# -----------------------------------------------------------------------------

pronom_data = PronomData()
signature_file = recurse_fix(pronom_data.latest_file("signature"))
container_file = pronom_data.latest_file("container")

json_dump(signature_file, Path("D:\\data\\signature_file.json"))

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import json
import re
from pathlib import Path
from jsonom.pronom_data import PronomData, FileFormat
from pydantic import parse_obj_as
from typing import Dict, Any, Callable, Union, List

# -----------------------------------------------------------------------------
# Auxiliary functions
# -----------------------------------------------------------------------------


def camel_case_split(in_str: str) -> Any:
    return re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", in_str)


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
        new_key = "".join(word.title() for word in camel_case_split(new_key))
        in_dict[new_key] = in_dict.pop(key)
    return in_dict


def fix_lists(in_dict: Dict[str, Any]) -> Dict[str, Any]:
    keys = list(in_dict.keys())
    for key in keys:
        value = in_dict[key]
        recurse_dict(fix_lists, value)
        if key in [
            "ByteSequence",
            "Extension",
            "HasPriorityOverFileFormatId",
            "InternalSignatureId",
        ] and not isinstance(value, list):
            in_dict[key] = [value]
    return in_dict


def json_dump(data: Any, file: Path) -> None:
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
fixed_signature_file = fix_lists(fix_keys(signature_file))
test_file_formats = parse_obj_as(
    List[FileFormat],
    fixed_signature_file["FfSignatureFile"]["FileFormatCollection"][
        "FileFormat"
    ],
)
json_dump(
    [file_format.dict() for file_format in test_file_formats],
    Path("D:\\data\\file_formats.json"),
)
json_dump(fixed_signature_file, Path("D:\\data\\fixed_signature_file.json"))

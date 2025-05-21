import json
from typing import Any


def convert_value(value: Any) -> Any:
    """
    Convert a JSON value to a format compatible with Nextflow.

    Attempts to convert string representations of numbers into int or float.
    Returns the original value if no conversion is possible.
    """
    if isinstance(value, str):
        try:
            float_value = float(value)
            return int(float_value) if float_value.is_integer() else float_value
        except ValueError:
            return value
    return str(value)


def format_quote(value: Any) -> str:
    """
    Format a value with appropriate quotes for Nextflow configuration syntax.

    - Adds quotes for strings unless they are valid numbers or boolean/null literals.
    - Removes inline comments (`//`) from values.
    """
    if isinstance(value, (int, float)):
        return str(value)

    if isinstance(value, str):
        value = value.split(" //")[0].strip()  # remove inline comment if any

        if value in {"true", "false", "null"}:
            return value

        # replace the ' to be "
        if "'" in value:
            value = value.replace("'", '"')

        # avoid adding extra quotes if already quoted
        if '"' not in value:
            try:
                float(value)  # attempt to convert, for safety
                return value
            except ValueError:
                pass
            return f'"{value}"'

    return str(value)


def json_to_nextflow_config(json_file: str, nf_config_file: str) -> None:
    """
    Converts a JSON file containing parameters into a Nextflow-compatible config block.

    Args:
        json_file: Path to the input JSON file.
        nf_config_file: Path to the output Nextflow config file.

    Raises:
        ValueError: If the JSON file does not contain a 'params' field.
    """
    with open(json_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}")

    params = data.get("params")
    if not params:
        raise ValueError("Missing 'params' section in JSON.")

    lines = ["params {"]
    for key, value in params.items():
        formatted_value = format_quote(convert_value(value))
        lines.append(f"    {key} = {formatted_value}")
    lines.append("}")

    with open(nf_config_file, "w") as f:
        f.write("\n".join(lines) + "\n")

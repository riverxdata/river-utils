import json


def convert_value(value):
    """Convert JSON values to Nextflow-compatible syntax."""
    if isinstance(value, str):
        try:
            float_value = float(value)
            return int(float_value) if float_value.is_integer() else float_value
        except ValueError:
            return value
    return str(value)


def format_quote(value: str):
    # format quotes so nextflow can read config
    if " //" in value:
        value = value.split(" //")[0].strip()
    if value in {"true", "false", "null"}:
        return value
    if '"' not in value and "'" not in value:
        value = f'"{value}"'
    return value


def json_to_nextflow_config(json_file, nf_config_file):
    """Convert JSON to Nextflow params format."""
    with open(json_file, "r") as f:
        data = json.load(f)
        clean_data = data.get("params", False)
        if not clean_data:
            raise ValueError("nf_config is missing")

    nextflow_params = "params {\n"
    for key, value in clean_data.items():
        nextflow_params += f"    {key} = {format_quote(convert_value(value))}\n"
    nextflow_params += "}"

    with open(nf_config_file, "w") as f:
        f.write(
            nextflow_params,
        )

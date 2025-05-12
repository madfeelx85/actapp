def expand_data_for_template(data: dict, max_length: int = 40) -> dict:
    result = {}

    for key, value in data.items():
        if isinstance(value, str) and len(value) > max_length:
            # разбиваем длинную строку на части
            lines = [value[i:i + max_length] for i in range(0, len(value), max_length)]
            for idx, line in enumerate(lines, start=1):
                result[f"{key}_line_{idx}"] = line
        else:
            result[key] = value

    return result

# utils.py
import sys


def is_integer_dtype(dtype):
    """Check if dtype represents an integer type."""
    return dtype in {"int8", "int16", "int32", "int64"}


def is_string_dtype(dtype):
    """Check if dtype represents a string type."""
    return dtype == "string"


def check_value_within_dtype_range(value, dtype):
    """Check if an integer value fits within the specified dtype's range."""
    size = int(dtype[3:]) // 8  # Calculate byte size from dtype (e.g., 8, 16, 32, 64)
    if -2 ** (8 * size - 1) <= value < 2 ** (8 * size - 1):
        return True
    return False


def validate_data_for_encoding(data, dtype):
    """Pre-validate data to check if it's compatible with the specified dtype."""
    incompatible_items = []
    for item in data:
        if is_integer_dtype(dtype):
            try:
                int_value = int(item)
                if not check_value_within_dtype_range(int_value, dtype):
                    incompatible_items.append(item)
            except (ValueError, TypeError):
                incompatible_items.append(item)
        elif is_string_dtype(dtype) and not isinstance(item, str):
            incompatible_items.append(item)

    if incompatible_items:
        print(f"Warning: Skipping incompatible items for dtype '{dtype}': {incompatible_items}", file=sys.stderr)
        return False  # Data is incompatible with dtype
    return True

#!/usr/bin/env python3
"""Task 0 Module"""
from typing import List
import re


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """returns log message"""
    for field in fields:
        pattern = f'{field}=.*?{separator}'
        replacement = f"{field}={redaction}{separator}"
        message = (pattern, replacement, message)
    return message

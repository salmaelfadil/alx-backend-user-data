#!/usr/bin/env python3
"""Task 0 Module"""
import logging
from typing import List
import re


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str):
    """returns log message"""
    for field in fields:
        message = (field+'=.*?'+separator,
                   field+'='+redaction+separator, message)
    return message

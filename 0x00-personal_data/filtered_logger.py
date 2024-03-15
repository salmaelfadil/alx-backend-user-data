#!/usr/bin/env python3
"""Task 0 Module"""
from typing import List
import re
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'ip')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """hides sensitive data"""
    for f in fields:
        message = re.sub(f+'=.*?'+separator,
                         f+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """intilization function"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """"format function"""
        rec = super(RedactingFormatter, self).format(record)
        mess = filter_datum(self.fields, self.REDACTION,
                            rec, self.SEPARATOR)
        return mess


def get_logger() -> logging.Logger:
    """gettter function for logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger

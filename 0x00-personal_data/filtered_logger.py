#!/usr/bin/env python3
"""Task 0 Module"""
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """gets the database to connect to"""

    user = os.getenv("PERSONAL_DATA_DB_USERNAME") or "root"
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD") or ""
    host = os.getenv("PERSONAL_DATA_DB_HOST") or "localhost"
    database = os.getenv("PERSONAL_DATA_DB_NAME") or ""

    conn = mysql.connector.connect(user=user, password=password,
                                   host=host, database=database)
    return conn


def main() -> None:
    """main function for reading and filtering data"""
    conn = get_db()
    cursor = conn.cursor()
    query = ("SELECT * FROM users;")
    cursor.execute(query)
    fields = cursor.column_names
    for row in cursor:
        parts = []
        for key, value in zip(fields, row):
            parts.append("{}={}".format(key, value))
        mess = "".join(parts)
        logger.info(mess.strip())
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()

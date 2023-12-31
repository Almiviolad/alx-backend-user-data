#!/usr/bin/env python3
"""Write a function called filter_datum that returns
the log message obfuscated:"""
import re
from typing import List

import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated:

    Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field
will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating
all fields in the log line (message)"""
    for field in fields:
        message = re.sub(f'{field}.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Implement the format method to filter values
in incoming log records using filter_datum. Values
for fields in fields should be filtered."""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)

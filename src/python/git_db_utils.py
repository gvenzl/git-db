#!/usr/bin/env python
#
# Since: June, 2018
# Author: gvenzl
# Name: git_db_utils.py
# Description: Utility functions for Git DB
#
# Copyright 2018 Gerald Venzl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from enum import Enum


def pretty_print_result(col_names, result, color=None):
    widths = []
    column_names = []
    row_values = []
    tavnit = '|'
    separator = '+'

    for idx, name in enumerate(col_names):
        # Preserve length of column name
        widths.append({"name": name, "length": len(name)})
        column_names.append(name)

    for row in result:
        row_vals = []
        for idx, column in enumerate(row):
            if column is not None:
                for line in column.split("\n"):
                    widths[idx]["length"] = max(len(line), widths[idx]["length"])
                row_vals.append(format_change(column))
            else:
                row_vals.append(" ")
        row_values.append(row_vals)

    for w in widths:
        col_length = w["length"]
        tavnit += " %-" + "%ss |" % col_length
        separator += '-' * col_length + '--+'

    # Set color if set
    if color is not None:
        print(color.value, end='')
    print(separator)
    print(tavnit % tuple(column_names))
    print(separator)
    for row in row_values:
        print(tavnit % tuple(row))
    print(separator)
    if color is not None:
        print(Color.RESET.value, end='')


def format_change(change):
    return change.lstrip("\n").replace("\x00", ";")


def print_error(msg, err):
    print(msg)
    for err_msg in err.args:
        print(err_msg)


class Color(Enum):
    GREEN = "\x1b[32m"
    RED = "\x1b[31m"
    RESET = "\x1b[0m"


#!/usr/bin/env python3
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

import subprocess
from enum import Enum


def pretty_print_result(col_names, result, color=None):
    widths = []
    column_names = []
    row_values = []
    tavnit = '|'
    separator = '+'
    change_col_idx = -1
    change_indention = 0
    change_length = 0

    # Store column name lengths
    for idx, name in enumerate(col_names):
        # Preserve length of column name
        widths.append({"name": name, "length": len(name)})
        if name == "CHANGE":
            change_col_idx = idx
        column_names.append(name)

    # Iterate over all rows to determine column width.
    # If the value is short, the column needs to have the length of the column name
    # If the value is long, the column needs to have the length of the value itself
    for row in result:
        row_vals = []
        for idx, column in enumerate(row):
            # No value in column  (privileges, etc)
            if column is not None:
                for line in column.split("\n"):
                    widths[idx]["length"] = max(len(line), widths[idx]["length"])
                row_vals.append(column)
            else:
                row_vals.append(" ")
        row_values.append(row_vals)

    for w in widths:
        # Record how many spaces new lines for a change need
        if w["name"] == "CHANGE":
            change_indention = len(separator)
            change_length = w["length"]
        col_length = w["length"]
        tavnit += " %-" + "%ss |" % col_length
        separator += '-' * col_length + '--+'

    # Replace new lines in change with indented new lines
    for row in row_values:
        row[change_col_idx] = format_change_and_indent(row[change_col_idx], "|", change_indention, change_length)

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
    return change.lstrip("\n").replace("\x00", ";").replace(";;", ";")


def format_change_and_indent(change, border_marker, indention, length):
    change = format_change(change)
    if change.find("\n") != -1:
        lines = change.splitlines()
        for idx, line in enumerate(lines):
            lines[idx] = border_marker + (" " * indention) + line + (" " * (length-len(line)+1) + border_marker)
        change = "\n".join(lines)
        # Remove leading spaces of first line
        change = change.lstrip(border_marker).lstrip()
        # Remove trailing border marker and space of last line
        change = change[:-2]
    return change


def print_error(msg, err):
    print(Color.RED.value, end='')
    print(msg)
    for err_msg in err.args:
        print(err_msg)
    print(Color.RESET.value, end='')


def print_warning(msg):
    print(Color.YELLOW.value, end='')
    print(msg)
    print(Color.RESET.value, end='')


def get_git_commit_id():
    """Return git commit log"""
    p = subprocess.run(["git", "log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf-8"))
    output = p.stdout.decode("utf-8")
    return output.split()[1:2][0]


class Color(Enum):
    GREEN = "\x1b[32m"
    RED = "\x1b[31m"
    YELLOW = "\x1b[33m"
    RESET = "\x1b[0m"


#!/usr/bin/env bash
#
# Since: June, 2018
# Author: gvenzl
# Name: git-db-install.sh
# Description: Git DB make-less installer for *nix systems.
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

if [ -z "$INSTALL_PREFIX" ]; then
    INSTALL_PREFIX="/usr/local/bin"
fi

if [ -z "$GITDB_REPO_HOME" ]; then
    GITDB_REPO_HOME="https://github.com/gvenzl/git-db"
fi

EXEC_FILE="git-db"
GITDB_DIR="git-db"
GITDB_BIN="git-db-bin"
SCRIPT_FILES="git_db_configuration.py git_db_database.py git_db_init.py"
DB_TYPE="oracle"
SQL_FILES="setup_table.sql setup_trigger.sql"

function getGitPath() {
    GIT_PATH=$(which git)

    if [ -z "$GIT_PATH" ]; then
        echo "git is not installed or in the PATH";
        echo "Please install git first!";
        exit 1;
    fi;

    echo "$GIT_PATH";
}


########################
######### MAIN #########
########################

echo "### Git DB installer ###"

case "$1" in
    uninstall)
        echo "Uninstalling Git DB from $INSTALL_PREFIX"
        if [ -d "$INSTALL_PREFIX" ] ; then
            # Removing git-db-bin directory
            echo "rm -vf $INSTALL_PREFIX/$GITDB_BIN"
            rm -vrf "$INSTALL_PREFIX/$GITDB_BIN"

            # Removing git-db binary"
            echo "rm -vf $INSTALL_PREFIX/$EXEC_FILE"
            rm -vf "$INSTALL_PREFIX/$EXEC_FILE"
        else
            echo "The '$INSTALL_PREFIX' directory does not exist!"
            echo "Do you need to set 'INSTALL_PREFIX'?"
        fi
        exit
        ;;
    help)
        echo "Usage: [environment] git-db-install.sh [install|uninstall]"
        echo "Environment:"
        echo "   INSTALL_PREFIX=$INSTALL_PREFIX"
        echo "   GITDB_REPO_HOME=$GITDB_REPO_HOME"
        exit
        ;;
    *)
        echo "Installing Git DB"
        echo "Git path: $(getGitPath)"
        echo "Git version: $(git --version)"

		if [ -d "$GITDB_DIR" -a -d "$GITDB_DIR/.git" ] ; then
			echo "Using existing repo: $GITDB_DIR"
		else
			echo "Cloning repo from GitHub to $GITDB_DIR"
			git clone "$GITDB_REPO_HOME" "$GITDB_DIR"
		fi

        install -v -d -m 0755 "$INSTALL_PREFIX/$GITDB_BIN"
        install -v    -m 0755 "$GITDB_DIR/src/$EXEC_FILE" "$INSTALL_PREFIX"

        install -v -d  -m 0755 "$INSTALL_PREFIX/$GITDB_BIN/python"
        for script_file in $SCRIPT_FILES ; do
            install -v -m 0755 "$GITDB_DIR/src/python/$script_file" "$INSTALL_PREFIX/$GITDB_BIN/python"
        done

        install -v -d  -m 0755 "$INSTALL_PREFIX/$GITDB_BIN/sql/$DB_TYPE"
        for sql_file in $SQL_FILES ; do
            install -v -m 0755 "$GITDB_DIR/src/sql/$DB_TYPE/$sql_file" "$INSTALL_PREFIX/$GITDB_BIN/sql/$DB_TYPE"
        done

        exit
        ;;
esac

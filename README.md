# Git DB

Git DB is a Git plugin for tracking database schema changes.
It tracks DDL changes performed in a database schema or the entire database.
Git DB uses system triggers to keep track of DDL changes happening.

Following databases are currently supported: `Oracle`

## Usage

    git db [--version] [--help] <command> [<args>]

    These are common Git DB commands used in various situations:

    start a working area
       init       Create an empty Git DB repository or reinitialize an existing one

    work on the current change
       add        Add a DDL change to the index
       reset      Reset current HEAD to the specified state
       squash     Squash changes on a given object into a single file

    examine the history and state
       log        Show commit logs
       show       Show various types of objects
       status     Show the working tree status

    grow, mark and tweak your common history
       commit     Record changes to the repository
       tag        Tag a commit  

# License
    Copyright 2018 Gerald Venzl
 
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
 
        http://www.apache.org/licenses/LICENSE-2.0
 
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

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
       
    destroy a working area
       deinit     Destroy the Git DB repository

### git db init
`git db init` enables a given database schema, or the entire database via the `--all` flag, for DDL change tracking.
It initializes an empty `git` repository in the current working directory where `git db init` has been called.
The database credentials passed on to `git db init` are stored in the `.git/git-db` folder within the current working directory.
Subsequent `git db` commands will acquire the credentials from the `.git/git-db` folder and do not require credentials to be passed on anymore.

    usage: git db init [-h] --user USER --password PASSWORD --host HOST --port
                       PORT --dbname DBNAME [--role ROLE] [--all]
    
    Initialize git repo and database tracking
    
    optional arguments:
      -h, --help           show this help message and exit
      --user USER          The database schema to track
      --password PASSWORD  The database schema password
      --host HOST          The host name on which the database is running on
      --port PORT          The port on which the database is listening
      --dbname DBNAME      The name of the database
      --role ROLE          The database user role (SYSDBA, SYSOPER, ...)
      --all                Track all database changes. If set, the database user
                           must have rights to create a database wide trigger.
### git db status
`git db status` displays the not yet tracked database changes.

    usage: git db status
    
    gvenzl-mac:schema1 gvenzl$ git db status
    Uncommitted database changes:
    
    +-----+---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    | TAG | CHANGE_TMS          | CHANGE_USER | OBJECT_NAME | OBJECT_TYPE | CHANGE                                                                 |
    +-----+---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    |     | 2018-07-01 05:07:23 | TEST        | PEOPLE      | TABLE       | create table people (first_name varchar2(25), last_name varchar2(25)); |
    |     | 2018-07-01 05:07:36 | TEST        | PEOPLE      | TABLE       | alter table people add (middle_name varchar2(25));                     |
    +-----+---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    
    On branch master
    
    No commits yet
    
    nothing to commit (create/copy files and use "git add" to track)

### git db add
`git db add` adds database changes to git.

    usage: git db add [-h] [--user] [--owner] [--object] User|Owner|Object|.
    
    Adds database changes to the git repo
    
    positional arguments:
      User|Owner|Object|.  The change(s) to add
    
    optional arguments:
      -h, --help           show this help message and exit
      --user               add all changes made by the following user
      --owner              add all changes made for the following object owner
      --object             add all changes for the following object
    
    Use '.' to add all changes or specify change type parameter and value.
    For example:
    
    To add all changes made by user "GERALD" run "git add --user GERALD"
    To add all changes made on objects owned by owner "MYSCHEMA" run "git add --owner MYSCHEMA"
    To add all changes made on a specific object, e.g. the table "ORDERS" run  "git add --object ORDERS"
    To add all changes that have happened run "git add ."
    
A sample output adding all changes:

    gvenzl-mac:schema1 gvenzl$ git db status
    Uncommitted database changes:
    
    +-----+---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    | TAG | CHANGE_TMS          | CHANGE_USER | OBJECT_NAME | OBJECT_TYPE | CHANGE                                                                 |
    +-----+---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    |     | 2018-07-01 05:07:23 | TEST        | PEOPLE      | TABLE       | create table people (first_name varchar2(25), last_name varchar2(25)); |
    |     | 2018-07-01 05:07:36 | TEST        | PEOPLE      | TABLE       | alter table people add (middle_name varchar2(25));                     |
    +-----+---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    
    On branch master
    
    No commits yet
    
    nothing to commit (create/copy files and use "git add" to track)
    gvenzl-mac:schema1 gvenzl$ git db add .
    gvenzl-mac:schema1 gvenzl$ git db status
    Uncommitted database changes:
    
    +-----+------------+-------------+-------------+-------------+--------+
    | TAG | CHANGE_TMS | CHANGE_USER | OBJECT_NAME | OBJECT_TYPE | CHANGE |
    +-----+------------+-------------+-------------+-------------+--------+
    +-----+------------+-------------+-------------+-------------+--------+
    
    On branch master
    
    No commits yet
    
    Changes to be committed:
      (use "git rm --cached <file>..." to unstage)
    
    	new file:   PEOPLE.sql
    
    gvenzl-mac:schema1 gvenzl$ cat PEOPLE.sql
    create table people (first_name varchar2(25), last_name varchar2(25));
    alter table people add (middle_name varchar2(25));
    gvenzl-mac:schema1 gvenzl$

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

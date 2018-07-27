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
    
    +---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    | CHANGE_TMS          | CHANGE_USER | OBJECT_NAME | OBJECT_TYPE | CHANGE                                                                 |
    +---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    | 2018-07-01 05:07:23 | TEST        | PEOPLE      | TABLE       | create table people (first_name varchar2(25), last_name varchar2(25)); |
    | 2018-07-01 05:07:36 | TEST        | PEOPLE      | TABLE       | alter table people add (middle_name varchar2(25));                     |
    +---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    
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
    
    +---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    | CHANGE_TMS          | CHANGE_USER | OBJECT_NAME | OBJECT_TYPE | CHANGE                                                                 |
    +---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    | 2018-07-01 05:07:23 | TEST        | PEOPLE      | TABLE       | create table people (first_name varchar2(25), last_name varchar2(25)); |
    | 2018-07-01 05:07:36 | TEST        | PEOPLE      | TABLE       | alter table people add (middle_name varchar2(25));                     |
    +---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    
    On branch master
    
    No commits yet
    
    nothing to commit (create/copy files and use "git add" to track)
    gvenzl-mac:schema1 gvenzl$ git db add .
    gvenzl-mac:schema1 gvenzl$ git db status
    Changes to be committed:
    
    +---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    | CHANGE_TMS          | CHANGE_USER | OBJECT_NAME | OBJECT_TYPE | CHANGE                                                                 |
    +---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    | 2018-07-01 05:07:23 | TEST        | PEOPLE      | TABLE       | create table people (first_name varchar2(25), last_name varchar2(25)); |
    | 2018-07-01 05:07:36 | TEST        | PEOPLE      | TABLE       | alter table people add (middle_name varchar2(25));                     |
    +---------------------+-------------+-------------+-------------+------------------------------------------------------------------------+
    
    On branch master
    
    No commits yet
    
    Changes to be committed:
      (use "git rm --cached <file>..." to unstage)
    
    	new file:   PEOPLE.sql
    
    gvenzl-mac:schema1 gvenzl$ cat PEOPLE.sql
    create table people (first_name varchar2(25), last_name varchar2(25));
    alter table people add (middle_name varchar2(25));
    gvenzl-mac:schema1 gvenzl$

### git db commit
`git db commit` commits changes to the git repository.

    gvenzl-mac:schema1 gvenzl$ git db status
    Changes to be committed:
    
    +---------------------+-------------+--------------+-------------+----------------------------------------------------------------------------------+
    | CHANGE_TMS          | CHANGE_USER | OBJECT_NAME  | OBJECT_TYPE | CHANGE                                                                           |
    +---------------------+-------------+--------------+-------------+----------------------------------------------------------------------------------+
    | 2018-07-16 03:11:41 | TEST        | PEOPLE       | TABLE       | CREATE TABLE PEOPLE (first_name VARCHAR2(25), last_name VARCHAR2(25), dob DATE); |
    | 2018-07-16 03:11:43 | TEST        | PEOPLE_IDX01 | INDEX       | CREATE INDEX PEOPLE_IDX01 ON PEOPLE (first_name);                                |
    +---------------------+-------------+--------------+-------------+----------------------------------------------------------------------------------+
    
    On branch master
    
    No commits yet
    
    Changes to be committed:
      (use "git rm --cached <file>..." to unstage)
    
    	new file:   PEOPLE.sql
    	new file:   PEOPLE_IDX01.sql
    
    gvenzl-mac:schema1 gvenzl$ git db commit -m "My first commit"
    [master (root-commit) c5a5697] My first commit
     2 files changed, 2 insertions(+)
     create mode 100644 PEOPLE.sql
     create mode 100644 PEOPLE_IDX01.sql
    gvenzl-mac:schema1 gvenzl$ git db status
    On branch master
    nothing to commit, working tree clean
    gvenzl-mac:schema1 gvenzl$ git log -p
    commit c5a5697adde43279c368c6ae069b2283640544bd (HEAD -> master)
    Author: Gerald Venzl
    Date:   Sun Jul 15 20:12:23 2018 -0700
    
        My first commit
    
    diff --git a/PEOPLE.sql b/PEOPLE.sql
    new file mode 100644
    index 0000000..8c69712
    --- /dev/null
    +++ b/PEOPLE.sql
    @@ -0,0 +1 @@
    +CREATE TABLE PEOPLE (first_name VARCHAR2(25), last_name VARCHAR2(25), dob DATE);
    diff --git a/PEOPLE_IDX01.sql b/PEOPLE_IDX01.sql
    new file mode 100644
    index 0000000..70a6dfb
    --- /dev/null
    +++ b/PEOPLE_IDX01.sql
    @@ -0,0 +1 @@
    +CREATE INDEX PEOPLE_IDX01 ON PEOPLE (first_name);

### git db tag
`git db tag` tags a given commit:

    gvenzl-mac:schema1 gvenzl$ git db commit -m "First commit" --signoff
    [master (root-commit) 64d3ae1] First commit
     2 files changed, 2 insertions(+)
     create mode 100644 PEOPLE.sql
     create mode 100644 PEOPLE_IDX01.sql
    
    gvenzl-mac:schema1 gvenzl$ git db log
    +---------+---------------------+-------------+--------------+----------------------------------------------------------------------------------+
    | ID      | CHANGE_TMS          | CHANGE_USER | OBJECT_NAME  | CHANGE                                                                           |
    +---------+---------------------+-------------+--------------+----------------------------------------------------------------------------------+
    | 64d3ae1 | 2018-07-27 03:21:56 | TEST        | PEOPLE_IDX01 | CREATE INDEX PEOPLE_IDX01 ON PEOPLE (first_name);                                |
    | 64d3ae1 | 2018-07-27 03:21:54 | TEST        | PEOPLE       | CREATE TABLE PEOPLE (first_name VARCHAR2(25), last_name VARCHAR2(25), dob DATE); |
    +---------+---------------------+-------------+--------------+----------------------------------------------------------------------------------+
    
    gvenzl-mac:schema1 gvenzl$ git db tag "v1" 64d3ae1
    
    gvenzl-mac:schema1 gvenzl$ git db log -v
    +------------------------------------------+---------------------+-------------+-----+--------------+-------------+----------------------------------------------------------------------------------+
    | ID                                       | CHANGE_TMS          | CHANGE_USER | TAG | OBJECT_NAME  | OBJECT_TYPE | CHANGE                                                                           |
    +------------------------------------------+---------------------+-------------+-----+--------------+-------------+----------------------------------------------------------------------------------+
    | 64d3ae1e92a39f42e60a317cf746520d5fd0ef99 | 2018-07-27 03:21:56 | TEST        | v1  | PEOPLE_IDX01 | INDEX       | CREATE INDEX PEOPLE_IDX01 ON PEOPLE (first_name);                                |
    | 64d3ae1e92a39f42e60a317cf746520d5fd0ef99 | 2018-07-27 03:21:54 | TEST        | v1  | PEOPLE       | TABLE       | CREATE TABLE PEOPLE (first_name VARCHAR2(25), last_name VARCHAR2(25), dob DATE); |
    +------------------------------------------+---------------------+-------------+-----+--------------+-------------+----------------------------------------------------------------------------------+
    
`git db tag` supports abbreviated and full commit ids.
If you pass on the 7 characters short commit id, `git db tag` will
tag every change that has a commit that starts with these 7 characters.  
If you pass on the full 40 characters commit id, `git db tag` will
tag every change with that exact commit id.  
`git db tag` will not perform a `git tag` operation.
If the user desires to tag the file objects in `git` as well,
he or she will have to run `git tag` manually.

### git db log
`git db log` shows the commit log.

    gvenzl-mac:schema1 gvenzl$ git db log
    +---------+---------------------+-------------+--------------+----------------------------------------------------------------------------------+
    | ID      | CHANGE_TMS          | CHANGE_USER | OBJECT_NAME  | CHANGE                                                                           |
    +---------+---------------------+-------------+--------------+----------------------------------------------------------------------------------+
    | 64d3ae1 | 2018-07-27 03:21:56 | TEST        | PEOPLE_IDX01 | CREATE INDEX PEOPLE_IDX01 ON PEOPLE (first_name);                                |
    | 64d3ae1 | 2018-07-27 03:21:54 | TEST        | PEOPLE       | CREATE TABLE PEOPLE (first_name VARCHAR2(25), last_name VARCHAR2(25), dob DATE); |
    +---------+---------------------+-------------+--------------+----------------------------------------------------------------------------------+
    
The `-v | --verbose` option will print verbose output, such as the full commit id and tags:
    
    gvenzl-mac:schema1 gvenzl$ git db log -v
    +------------------------------------------+---------------------+-------------+-----+--------------+-------------+----------------------------------------------------------------------------------+
    | ID                                       | CHANGE_TMS          | CHANGE_USER | TAG | OBJECT_NAME  | OBJECT_TYPE | CHANGE                                                                           |
    +------------------------------------------+---------------------+-------------+-----+--------------+-------------+----------------------------------------------------------------------------------+
    | 64d3ae1e92a39f42e60a317cf746520d5fd0ef99 | 2018-07-27 03:21:56 | TEST        |     | PEOPLE_IDX01 | INDEX       | CREATE INDEX PEOPLE_IDX01 ON PEOPLE (first_name);                                |
    | 64d3ae1e92a39f42e60a317cf746520d5fd0ef99 | 2018-07-27 03:21:54 | TEST        |     | PEOPLE       | TABLE       | CREATE TABLE PEOPLE (first_name VARCHAR2(25), last_name VARCHAR2(25), dob DATE); |
    +------------------------------------------+---------------------+-------------+-----+--------------+-------------+----------------------------------------------------------------------------------+

### git db deinit
`git db deinit` will remove the change tracking from the databases. The local git repository will remain intact:

    gvenzl-mac:schema1 gvenzl$ git db deinit
    Removed change tracking
    gvenzl-mac:schema1 gvenzl$ ls -al
    total 0
    drwxr-xr-x   3 gvenzl  staff   96 Jul  9 22:44 .
    drwxr-xr-x   7 gvenzl  staff  224 Jul  9 22:41 ..
    drwxr-xr-x  10 gvenzl  staff  320 Jul  9 22:44 .git

Pass on the `--all` option to remove the change tracking from the database and the local git repository:

    gvenzl-mac:schema1 gvenzl$ git db deinit --all
    Removed change tracking
    Removed local git repository
    gvenzl-mac:schema1 gvenzl$ ls -al
    total 0
    drwxr-xr-x  2 gvenzl  staff   64 Jul  9 22:45 .
    drwxr-xr-x  7 gvenzl  staff  224 Jul  9 22:41 ..

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

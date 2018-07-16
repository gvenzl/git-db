### git db commit
`git db commit` commits changes to the git repository.

    gvenzl-mac:schema1 gvenzl$ git db status
    Changes to be committed:
    
    +-----+---------------------+-------------+--------------+-------------+----------------------------------------------------------------------------------+
    | TAG | CHANGE_TMS          | CHANGE_USER | OBJECT_NAME  | OBJECT_TYPE | CHANGE                                                                           |
    +-----+---------------------+-------------+--------------+-------------+----------------------------------------------------------------------------------+
    |     | 2018-07-16 03:11:41 | TEST        | PEOPLE       | TABLE       | CREATE TABLE PEOPLE (first_name VARCHAR2(25), last_name VARCHAR2(25), dob DATE); |
    |     | 2018-07-16 03:11:43 | TEST        | PEOPLE_IDX01 | INDEX       | CREATE INDEX PEOPLE_IDX01 ON PEOPLE (first_name);                                |
    +-----+---------------------+-------------+--------------+-------------+----------------------------------------------------------------------------------+
    
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

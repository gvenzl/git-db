--
-- Since: May, 2018
-- Author: gvenzl
-- Name: setup_table.py
-- Description: Sets up the tracking table for Git DB
--
-- Copyright 2018 Gerald Venzl
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
--

CREATE TABLE GITDB_CHANGES
(
    COMMIT_ID      INTEGER,
    CHANGE_TMS     DATE NOT NULL,
    CHANGE_USER    VARCHAR2(255) NOT NULL,
    TAG            VARCHAR2(255),
    CHANGE         CLOB NOT NULL,
    OBJECT_NAME    VARCHAR2(128),
    OBJECT_TYPE    VARCHAR2(23),
    OBJECT_OWNER   VARCHAR2(128)
);
/

COMMENT ON TABLE GITDB_CHANGES IS 'v0.1.0';
/
Following credentials are using during the tests:

* Admin user: "system"
* Admin user password: "LetsDocker"
* Admin user role: "sysdba" (just used to verify credential storage tests)
* Test user: "unit_test"
* Test user password": "unittest"
* Database host: "localhost"
* Database port: "1521"
* Database name/service: "ORCLPDB1",

The above credentials must be valid for the unit tests to work.
If you want to use other ones, change them in `test_utils.py`!
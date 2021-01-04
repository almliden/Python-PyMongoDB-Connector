# Python-PyMongoDB-Connector

Connect to a MongoDB over ssh.

## Example usage

```python 
from databaseConnection import DatabaseConnection, DatabaseConfigurator

dbcontext = DatabaseConnection(DatabaseConfigurator('config.ini').Config())
db = dbcontext.connect()

mycollection = 'some-name' 
db.[mycollection].find_one({})
```

The connection needs the following configuration values:

 - `REMOTE_HOST`
 - `REMOTE_BIND_ADDRESS`
 - `REMOTE_BIND_PORT`
 - `SSH_USER`
 - `SSH_PASS`
 - `MONGO_DB` (*optional, but must then be passed in as an argument to* `dbcontext.connect()`)
 - `MONGO_USER` (*optional, only needed if authorization is enabled*)
 - `MONGO_PASS` (*optional, only needed if authorization is enabled*)

These can be stored in the default `databaseConnectionConfig.ini`-file, or in another config-file which can be passed in. Another option would be to omit the configuration file entirely and instead send in an object to the `DatabaseConfig.CustomConfigSource()`.

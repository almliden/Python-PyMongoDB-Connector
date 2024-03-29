from sshtunnel import SSHTunnelForwarder
import pymongo
import configparser
import os.path

class DatabaseConnectorConfig:
  REMOTE_HOST=None
  REMOTE_BIND_ADDRESS=None
  REMOTE_BIND_PORT=None
  SSH_USER=None
  SSH_PASS=None
  MONGO_DB=None
  MONGO_USER=None
  MONGO_PASS=None

class DatabaseConnector:
  client=None
  db=None
  database_config=DatabaseConnectorConfig

  def __init__(self, database_config:DatabaseConnectorConfig):
    self.database_config=database_config
    self.server = SSHTunnelForwarder(
      ssh_address_or_host=self.database_config.REMOTE_HOST,
      ssh_username=self.database_config.SSH_USER,
      ssh_password=self.database_config.SSH_PASS,
      remote_bind_address=(self.database_config.REMOTE_BIND_ADDRESS, self.database_config.REMOTE_BIND_PORT)
    )
  
  def connect(self, database=None):
    self.server.start()
    self.client = pymongo.MongoClient(self.database_config.REMOTE_BIND_ADDRESS, self.server.local_bind_port)
    database = database if database != None else self.database_config.MONGO_DB
    if (database == None):
      raise Exception("You must provide a database name")
    self.db = self.client[database]
    try:
      self.db.authenticate(self.database_config.MONGO_USER, self.database_config.MONGO_PASS)
    except (pymongo.errors.OperationFailure):
      print("Could not authenticate against %s", database)
    return self.db

  def __del__(self):
    self.disconnect()

  def disconnect(self):
    if (self.client != None):
      try:
        self.client.disconnect()
      except:
        print("Disconnect failed.")
        pass
      try:
        if (self.server != None):
          self.server.close()
          self.server.stop(force=True)
      except:
        pass

class DatabaseConfigurator:
  conf = DatabaseConnectorConfig
  configName = None

  def __init__(self, configName='databaseConnectionConfig.ini'):
    self.configName = configName

  def Config(self):
    if not os.path.isfile(self.configName):
      raise FileExistsError("Config file not found")
    parser=configparser.ConfigParser()
    parser.read(self.configName)
    self.conf.REMOTE_HOST=parser.get('SSH Credentials', 'REMOTE_HOST')
    self.conf.REMOTE_BIND_ADDRESS=parser.get('SSH Credentials', 'REMOTE_BIND_ADDRESS')
    self.conf.REMOTE_BIND_PORT=int(parser.get('SSH Credentials', 'REMOTE_BIND_PORT'))
    self.conf.SSH_USER=parser.get('SSH Credentials', 'SSH_USER')
    self.conf.SSH_PASS=parser.get('SSH Credentials', 'SSH_PASS')
    self.conf.MONGO_DB=parser.get('MongoDB Credentials', 'MONGO_DB', fallback=None)
    self.conf.MONGO_USER=parser.get('MongoDB Credentials', 'MONGO_USER', fallback=None)
    self.conf.MONGO_PASS=parser.get('MongoDB Credentials', 'MONGO_PASS', fallback=None)
    return self.conf

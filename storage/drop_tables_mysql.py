import mysql.connector
import yaml 

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())


conn = mysql.connector.connect(host=app_config["datastore"]["hostname"], user=app_config["datastore"]["user"], password=app_config["datastore"]["password"], database=app_config["datastore"]["db"])


c = conn.cursor()
c.execute('''
          DROP TABLE mask, sanitizer
          ''')
conn.commit()
conn.close()

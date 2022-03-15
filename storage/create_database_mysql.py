import mysql.connector 
import yaml

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

conn = mysql.connector.connect(host=app_config["datastore"]["hostname"], user=app_config["datastore"]["user"], password=app_config["datastore"]["password"], database=app_config["datastore"]["db"])

c = conn.cursor()
c.execute('''
          CREATE TABLE sanitizer
          (id INT NOT NULL AUTO_INCREMENT, 
           transaction_id VARCHAR(250) NOT NULL,
           scent VARCHAR(250) NOT NULL,
           volume INTEGER NOT NULL,
           quantity INTEGER NOT NULL,
           price INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           CONSTRAINT sanitizer_pk PRIMARY KEY (id))
          ''')

c.execute('''
          CREATE TABLE mask
          (id INT NOT NULL AUTO_INCREMENT, 
           transaction_id VARCHAR(250) NOT NULL,
           color VARCHAR(250) NOT NULL,
           size VARCHAR(50) NOT NULL,
           quantity INTEGER NOT NULL,
           price INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           CONSTRAINT mask_pk PRIMARY KEY (id))
          ''')

conn.commit()
conn.close()

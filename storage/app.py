import connexion 
from connexion import NoContent 
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from sanitizer import Sanitizer
from mask import Mask
import datetime
import yaml
import logging.config
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

engine = f'mysql+pymysql://{app_config["datastore"]["user"]}:'\
         f'{app_config["datastore"]["password"]}@{app_config["datastore"]["hostname"]}:'\
         f'{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}'
DB_ENGINE = create_engine(engine)
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


# Your functions here 
MAX_EVENT = 10
EVENT_FILE = "events.json"

def get_sanitizer(timestamp): 
    """ Gets sanitizer transaction after the timestamp """ 
 
    session = DB_SESSION() 
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S") 
    
 
    readings = session.query(Sanitizer).filter(Sanitizer.date_created >=   
                                                  timestamp_datetime) 
    results_list = [] 
    for reading in readings: 
        results_list.append(reading.to_dict()) 
 
    session.close() 
     
    logger.info("Query for sanitizer transactions after %s returns %d results" %  
                (timestamp, len(results_list))) 
 
    return results_list, 200

def get_mask(timestamp): 
    """ Gets mask transaction after the timestamp """ 
 
    session = DB_SESSION() 
    print(timestamp)
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S") 
   
 
    readings = session.query(Mask).filter(Mask.date_created >=   
                                                  timestamp_datetime) 
    results_list = [] 
    for reading in readings: 
        results_list.append(reading.to_dict()) 
 
    session.close() 
     
    logger.info("Query for mask transactions after %s returns %d results" %  
                (timestamp, len(results_list))) 
 
    return results_list, 200

def logoutput(trace_id, event_name):
    msg = f'Stored event {event_name} request with a trace id of {trace_id}'
    logger.debug(msg)

def db_logoutput():
    logger.info(f'Connecting to DB. Hostname: {app_config["datastore"]["hostname"]}, Port: {app_config["datastore"]["port"]}')

def process_messages(): 
    """ Process event messages """ 
    hostname = "%s:%d" % (app_config["events"]["hostname"],   
                          app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
     
    # Create a consume on a consumer group, that only reads new messages  
    # (uncommitted messages) when the service re-starts (i.e., it doesn't  
    # read all the old messages from the history in the message queue). 
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', 
                                         reset_offset_on_start=False, 
                                         auto_offset_reset=OffsetType.LATEST) 
 
    # This is blocking - it will wait for a new message 
    for msg in consumer: 
        msg_str = msg.value.decode('utf-8') 
        msg = json.loads(msg_str) 
        logger.info("Message: %s" % msg) 
 
        payload = json.loads(msg["payload"]) 
 
        if msg["type"] == "sanitizer": # Change this to your event type 
            # Store the event1 (i.e., the payload) to the DB 
            session = DB_SESSION()

            bp = Sanitizer(payload['transaction_id'],
                            payload['scent'],
                            payload['volume'],
                            payload['quantity'],
                            payload['price'],
                            payload['trace_id'])

            session.add(bp)
            session.commit()
            session.close()

            logoutput(payload['trace_id'], "sanitizer transctioin")
        elif msg["type"] == "mask": # Change this to your event type 
            # Store the event2 (i.e., the payload) to the DB 
            session = DB_SESSION()

            bp = Mask(payload['transaction_id'],
                            payload['color'],
                            payload['size'],
                            payload['quantity'],
                            payload['price'],
                            payload['trace_id'])

            session.add(bp)

            session.commit()
            session.close()
            logoutput(payload['trace_id'], "mask transctioin")
 
        # Commit the new message as being read 
        consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='') 
app.add_api("openapi.yaml",
            strict_validation=True,
            validate_responses=True) 
 
if __name__ == "__main__": 
    t1 = Thread(target=process_messages) 
    t1.setDaemon(True) 
    t1.start() 
    app.run(port=8090)
import connexion 
from connexion import NoContent 
import json
import yaml
import logging
import logging.config
from pykafka import KafkaClient
from flask_cors import CORS, cross_origin

HEADER = {'content-type': 'application/json'}

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

logger = logging.getLogger('basicLogger')

def get_sanitizer(index): 
    """ Get BP Reading in History """ 
    hostname = "%s:%d" % (app_config["events"]["hostname"],  
                          app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
 
    # Here we reset the offset on start so that we retrieve 
    # messages at the beginning of the message queue.  
    # To prevent the for loop from blocking, we set the timeout to 
    # 100ms. There is a risk that this loop never stops if the 
    # index is large and messages are constantly being received! 
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,  
                                         consumer_timeout_ms=1000) 
 
    logger.info("Retrieving sanitizer at index %d" % index) 
    try: 
        for num, msg in enumerate(consumer):
            if num == index: 
                
                msg_str = msg.value.decode('utf-8') 
                print(msg_str)
                msg = json.loads(msg_str)
                result = json.loads(msg['payload'])
                return result, 200 
 
            # Find the event at the index you want and  
            # return code 200 
            # i.e., return event, 200 
    except: 
        logger.error("No more messages found") 
     
    logger.error("Could not find sanitizer at index %d" % index) 
    return { "message": "Not Found"}, 404

def get_mask(index): 
    """ Get BP Reading in History """ 
    hostname = "%s:%d" % (app_config["events"]["hostname"],  
                          app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
 
    # Here we reset the offset on start so that we retrieve 
    # messages at the beginning of the message queue.  
    # To prevent the for loop from blocking, we set the timeout to 
    # 100ms. There is a risk that this loop never stops if the 
    # index is large and messages are constantly being received! 
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,  
                                         consumer_timeout_ms=1000) 
 
    logger.info("Retrieving mask at index %d" % index) 
    try: 
        for num, msg in enumerate(consumer):
            if num == index: 
                msg_str = msg.value.decode('utf-8') 
                msg = json.loads(msg_str)
                result = json.loads(msg['payload'])
                return result, 200  
 
            # Find the event at the index you want and  
            # return code 200 
            # i.e., return event, 200 
    except: 
        logger.error("No more messages found") 
     
    logger.error("Could not find mask at index %d" % index) 
    return { "message": "Not Found"}, 404

app = connexion.FlaskApp(__name__, specification_dir='') 
CORS(app.app) 
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml",
            strict_validation=True,
            validate_responses=True) 

if __name__ == "__main__": 
    app.run(port=8110)

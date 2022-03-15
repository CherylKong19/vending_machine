from inspect import trace
import connexion 
from connexion import NoContent 
import json
import datetime
import yaml
import logging.config
import uuid
from pykafka import KafkaClient

HEADER = {'content-type': 'application/json'}

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config)
    
logger = logging.getLogger('basicLogger')

def sanitizer_transaction(body): 
    """ Receives a hand sanitizer transaction """ 
    trace_id = str(uuid.uuid4())
    body['trace_id'] = trace_id
    reading = json.dumps(body)
    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}") 
    topic = client.topics[str.encode(app_config['events']['topic'])] 
    producer = topic.get_sync_producer() 
    
    msg = { "type": "sanitizer",  
            "datetime" :    
            datetime.datetime.now().strftime( 
                "%Y-%m-%dT%H:%M:%S"),  
            "payload": reading } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))

    return NoContent, 201
 
 
def mask_transaction(body): 
    """ Receives a mask transaction """ 
    trace_id = str(uuid.uuid4())
    body['trace_id'] = trace_id
    reading = json.dumps(body)
    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}") 
    topic = client.topics[str.encode(app_config['events']['topic'])] 
    producer = topic.get_sync_producer() 
    
    msg = { "type": "mask",  
            "datetime" :    
            datetime.datetime.now().strftime( 
                "%Y-%m-%dT%H:%M:%S"),  
            "payload": reading } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))
    return NoContent, 201

def logoutput(trace_id, event_name):
    msg = f'Returned event {event_name} response (ID: {trace_id}) with status 201'
    logger.info(msg)
    
app = connexion.FlaskApp(__name__, specification_dir='') 
app.add_api("openapi.yaml",
            strict_validation=True,
            validate_responses=True) 
 
if __name__ == "__main__": 
    app.run(port=8080) 
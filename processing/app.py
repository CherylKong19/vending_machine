import connexion 
from connexion import NoContent 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from stats import Stats
import datetime
import yaml
import logging.config
import logging
import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import uuid
from flask_cors import CORS, cross_origin

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine(f'sqlite:///{app_config["datastore"]["filename"]}') 
Base.metadata.bind = DB_ENGINE 
DB_SESSION = sessionmaker(bind=DB_ENGINE)


# Your functions here 

def get_stats(): 
    """ Receives stats """
    trace_id = str(uuid.uuid4())
    logger.info("Start Getting Statistics (ID: {trace_id})")
    session = DB_SESSION()
    record = session.query(Stats).order_by(Stats.last_updated.desc()).first()
    session.close()

    if record == None:
        logger.error(f"Statistics do not exist (ID: {trace_id})")
        return {"message": "Statistics do not exist"}, 404

    result = record.to_dict()
    logger.debug(f"Statistics {result} (ID: {trace_id})")
    logger.info(f"Complete Getting Statistics (ID: {trace_id})") 
    return result, 200

def populate_stats(): 
    """ Periodically update stats """ 
    trace_id = str(uuid.uuid4())
    logger.info(f'Start Periodic Processing (ID: {trace_id}')

    stats = get_latest_processing_stats()
    
    received_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    print(received_timestamp)
    if "last_updated" in stats.keys():
        last_updated = stats["last_updated"]
    else:
        last_updated = received_timestamp
    
    rm = requests.get(app_config['mask']['url']+'?timestamp='+last_updated)
    rs = requests.get(app_config['sanitizer']['url']+'?timestamp='+last_updated)

    if rm.status_code == 200 and rs.status_code == 200:
        count_mask = len(rm.json())
        count_sanitizer = len(rs.json())

        if count_mask > 0:
            stats["mask_quantity"] += count_mask
            for record in rm.json():
                stats["mask_price"] += record["price"]
        
        if count_sanitizer > 0:
            print(stats)
            print(count_sanitizer)
            stats["sanitizer_quantity"] += count_sanitizer
            for record in rs.json():
                stats["sanitizer_price"] += record["price"]
        
        if count_mask == 0 and count_sanitizer == 0:
            logger.info(f"No Data Updated (ID: {trace_id})")
        else:
            #stats["last_updated"] = received_timestamp

            new_stats = Stats(stats["sanitizer_quantity"],
                            stats["sanitizer_price"],
                            stats["mask_quantity"],
                            stats["mask_price"],
                            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

            session = DB_SESSION()
            session.add(new_stats)
            session.commit()
            session.close()

            logger.info(f"Finish Periodic Processing Successfully (ID: {trace_id})")

    else:
        logger.info(f"Periodic Processing Not Working (ID: {trace_id})")
    

def get_latest_processing_stats():
    """ Get the latest stats object, or None if there isn't one """
    session = DB_SESSION()

    results = session.query(Stats).order_by(Stats.last_updated.desc())
    
    session.close()

    if len(results.all()) > 0:
        return results.first().to_dict()
    
    return {"sanitizer_quantity": 0,
            "sanitizer_price": 0,
            "mask_quantity": 0,
            "mask_price": 0,
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}

def init_scheduler(): 
    sched = BackgroundScheduler(daemon=True) 
    sched.add_job(populate_stats,    
                  'interval', 
                  seconds=app_config['scheduler']['period_sec']) 
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='') 
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml",
            strict_validation=True,
            validate_responses=True) 
if __name__ == "__main__":
    init_scheduler() 
    app.run(port=8100, use_reloader=False) 

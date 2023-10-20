import os
import logging
from datetime import date
from super_admin_1 import db
from super_admin_1.models.alternative import Database
from super_admin_1.models.product_logs import ProductLogs

if os.path.isdir('logs') is False:
    os.mkdir('logs')

log_file_name=f'logs/product_log_report_{date.today().strftime("%Y_%m_%d")}.log'

# Configure the logging module
logging.basicConfig(
    filename=f'logs/server_logs_{date.today().strftime("%Y_%m_%d")}.log',
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

def generate_log_file():
    """Generate a log file"""
    try:
        all_logs = db.session.execute(db.select(ProductLogs)).scalars().all()
        for log in all_logs:
            log_message = f"Admin '{log.user_id}' performed action: '{log.action}'\
                on product with Id '{log.product_id}' time: {log.log_date}"
            logging.info(log_message)
        return log_file_name
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error} - stacktrace: {os.getcwd()}")
        return None


def register_action(user_id, action, product_id):
    """log the admin action"""
    try:
        log = ProductLogs(user_id=user_id, action=action, product_id=product_id)
        log.insert()
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error} - stacktrace: {os.getcwd()}")


def generate_log_file_d():
    """Generate a log file using pure sql queries"""
    try:
        query = """
            SELECT * FROM product_logs;
        """
        with Database() as cursor:
            cursor.execute(query)
            all_logs = cursor.fetchall()
            if len(all_logs) <= 0:
                return False
            if os.path.isfile(log_file_name):
                os.remove(log_file_name)
            for log in all_logs:
                # print(f"type: {type(log)}")
                _ , user_id, action, product_id, log_date = log
                log_message = f"Admin '{user_id}' performed action: '{action}' on product with Id '{product_id}' at time: '{log_date}'\n"
                try:
                    with open(log_file_name, 'a') as log_file:
                        log_file.write(log_message)
                except Exception as error:
                    logger.error(f"{type(error).__name__}: {error} - stacktrace: {os.getcwd()}")
                    return None
        return log_file_name
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error} - stacktrace: {os.getcwd()}")
        return None


def register_action_d(user_id, action, product_id, reason = None):
    """log the admin action using raw queries"""
    try:
        query = """
            INSERT INTO product_logs (user_id, action, product_id)
            VALUES (%s, %s, %s);
        """
        with Database() as cursor:
            cursor.execute(query, (user_id, action, product_id))
        if reason is not None:
            pass
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error} - stacktrace: {os.getcwd()}")
        return None

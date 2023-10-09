import os
import logging
from datetime import date
from super_admin_1 import db
from super_admin_1.models.alternative import Database
from super_admin_1.models.product_logs import ProductLogs

log_file_name=f'product_log_report_{date.today().strftime("%Y_%m_%d")}.log'
# Configure the logging module
logging.basicConfig(
    filename=f'server_logs_{date.today().strftime("%Y_%m_%d")}.log',
    level=logging.FATAL,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def generate_log_file():
    """Generate a log file"""
    for log in all_logs:
        all_logs = db.session.execute(db.select(ProductLogs)).scalars().all()
        log_message = f"Admin '{log.user_id}' performed action: '{log.action}'\
              on product with Id '{log.product_id}' time: {log.log_date}"
        logging.info(log_message)
    return log_file_name


def register_action(user_id, action, product_id):
    """log the admin action"""
    log = ProductLogs(user_id=user_id, action=action, product_id=product_id)
    log.insert()


def generate_log_file_d():
    """Generate a log file using pure sql queries"""
    try:
        query = """
            SELECT * FROM product_logs LIMIT 50;
        """
        with Database() as cursor:
            cursor.execute(query)
            all_logs = cursor.fetchall()
            if all_logs == None:
                return False
            if os.path.isfile(log_file_name):
                os.remove(log_file_name)
            for log in all_logs:
                # print(f"type: {type(log)}")
                # log = id , user_id, action, product_id
                log_message = f" Admin '{log[1]}' performed action: '{log[2]}' on product with Id '{log[3]}'\n"
                try:
                    with open(log_file_name, 'a') as log_file:
                        log_file.write(log_message)
                except Exception:
                    return False
                # logging.info(log_message)
        return log_file_name
    except Exception as error:
        print(f"{type(error).__name__}: {error}")


def register_action_d(user_id, action, product_id):
    """log the admin action using raw queries"""
    try:
        query = """
            INSERT INTO product_logs (user_id, action, product_id)
            VALUES (%s, %s, %s);
        """
        with Database() as cursor:
            cursor.execute(query, (user_id, action, product_id))
    except Exception as error:
        print(f"{type(error).__name__}: {error}")

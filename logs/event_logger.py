import logging
from datetime import date

# Configure the logging module
logging.basicConfig(
    filename=f'admin_actions_{date.today().strftime("%Y_%m_%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Event:
    def __init__(self, username, action, product):
        self.username = username
        self.action = action
        self.product = product
        # self.timestamp = time.time()

    def log_action(self):
        log_message = f"Admin '{self.username}' performed action: '{self.action}' on product with Id '{self.product}'"
        logging.info(log_message)

# Usage
if __name__ == "__main__":
    my_event = Event("Wonderful", "Approved", "Product_2")

    my_event.log_action()



# import queue
# import threading

# class PubSub:
#     def __init__(self):
#         self.subscribers = {}
#         self.lock = threading.Lock()

#     def subscribe(self, topic, callback):
#         with self.lock:
#             if topic not in self.subscribers:
#                 self.subscribers[topic] = queue.Queue()
#             self.subscribers[topic].put(callback)

#     def publish(self, topic, message):
#         with self.lock:
#             if topic in self.subscribers:
#                 while not self.subscribers[topic].empty():
#                     callback = self.subscribers[topic].get()
#                     callback(message)

# # Example usage
# def subscriber1(message):
#     print(f"Subscriber 1 received: {message}")

# def subscriber2(message):
#     print(f"Subscriber 2 received: {message}")

# pubsub = PubSub()

# pubsub.subscribe("topic1", subscriber1)
# pubsub.subscribe("topic2", subscriber2)

# pubsub.publish("topic1", "Hello, topic1 subscribers!")
# pubsub.publish("topic2", "Hi, topic2 subscribers!")
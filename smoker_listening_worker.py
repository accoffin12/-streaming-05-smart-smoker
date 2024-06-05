"""
*** UNDER DEVELOPEMENT ****

    This program listens for work messages contiously. 
    Start multiple versions to add more workers.  

    Author: Alex Coffin
    Date: January 15, 2023

"""

import pika
import sys
import time
from utils.util_logger import setup_logger
import struct
from datetime import datetime
from collections import deque


# Configuring the Logger:
logger, logname = setup_logger(__file__)


# Define Program functions
#--------------------------------------------------------------------------

# Create deques to hold windows of data for the sensor smoker. 
# Each reading is 30 secs apart, each deque has maxlen = 2 * windowminutes.
# 5/2 = 2.5 minute window
smoker_deque = deque(maxlen = 5)
# 20/2 = 10 minute window
#foodA_deque = deque(maxlen = 20)
#foodB_deque = deque(maxlen = 20)

# Define a function to calculate the different between values at the beginning and end of a window.
# Allowing us to examine the change in value over time, this is recieved from a collection.

def calculate_window_delta(collection):
    """
    Calculates the differences between the last and first items in a collection.
    Args: collection (list): A list of numerical values, smoker_temps
    Returns: float: The difference between the last and first items.
    """
    return collection[-1] - collection[0]

# define a callback function for each sensor that will be called when message is recieved.
def smoker_callback(ch, method, properties, body):
    """ 
    Define behavior on getting a message from the smoker_queue.
    This process involves unpacking the encoded string from the Producer and logging the action.
    It unpacts the struct and decodes the timestamp for the log.
    The produces an alert for the temperature drop
    """
    # Unpacking the struct by the temp_ProducerV2.py
    # Timestamps for logging ONLY
    timestamp, temp = struct.unpack('!df', body)
    # Convert the timestamp back to original:
    timestamp_str = datetime.fromtimestamp(timestamp).strftime("%m/%d/%y %H:%M:%S")
    logger.info(f'[01-smoker Reading]: {timestamp_str}: {temp} deg. F')
    print(f" [x] Received [01-smoker Reading]: {timestamp_str}: {temp} deg. F")
    
    # Append smoker_deque, new temp:
    smoker_deque.append(temp)
    
    # check if deque is full, check temp for a drop:
    if len(smoker_deque) == smoker_deque.maxlen:
        if calculate_window_delta(smoker_deque) <= -15:
            logger.info( f'''
                    ************* [ALERT!] ****************
                    SMOKER TEMP HAS DROPPED 15 deg. F!
                    * {timestamp_str}
                    * Current temp: {temp}
                    * INCREASE TEMPEATURE IMEDIATLY.
                    ***************************************\n''')
        
    # Add completed task to log:
    logger.info("[x] Done: 01-smoker reading")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)


# define a main function to run the program
def main(hn: str):
    """ Continuously listen for task messages on a named queue."""

    # when a statement can go wrong, use a try-except block
    try:
        # try this code, if it works, keep going
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        logger.error(f"ERROR: connection to RabbitMQ server failed. The error is {e}.")
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        ch = connection.channel()

        # Declare queues for each column
        queues = ["01-smoker", "02-food-A", "03-food-B"]
        # Delete the queue if it already exists, and then create a new Durable Queue 
        for queue_name in queues:
             ch.queue_delete(queue=queue_name)
             ch.queue_declare(queue=queue_name, durable=True)

        # Set the prefetch count to one to limit the number of messages
        # being consumed and processed concurrently.
        # prefetch_count = Per consumer limit of unaknowledged messages      
        ch.basic_qos(prefetch_count=1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        ch.basic_consume(queue='01-smoker', on_message_callback=smoker_callback)
        ch.basic_consume(queue='02-food-A', on_message_callback=foodA_callback)
        ch.basic_consume(queue='02-food-B', on_message_callback=foodB_callback)

        # print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")
        logger.info(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        ch.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        logger.error(f"Error: Something whent wrong. Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        logger.info("KeyboardInterrupt. Stopping the Program")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        logger.info("\nclosing connection. Goodby\n")
        connection.close()


# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    host = "localhost"
    main(host)

"""
   temp_producerV2

   **** Streamlined UNDER DEVELOPEMENT ***

   Program will read in temepratures provided in 'smoker-temps.csv'.
   Will send temperatures to respective consumers based on what we are reading the temperature of (smoker, food_A, food_B).
   Addition of Struct library to use C structures during the process.

   Author: Alex Coffin
   Date: June, 2024

   Modified to accomidate windowing and closer to assignement requirements with tuples for M6 Requirements.
"""

import pika
import sys
import webbrowser
import csv
from datetime import datetime
import pika.exceptions
from utils.util_logger import setup_logger
import time
import struct

# Configuring the Logger:
logger, logname = setup_logger(__file__)

# Variables:
host = 'localhost'
input_file_name = "smoker-temps.csv"


# Define Program functions
#--------------------------------------------------------------------------

def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()



def main(host: str, queue_name: str, message: str):
    """
    publish the message the the desired queue.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queues (str): 01-smoker, 02-food-A, 03-food-B queues created to publish messages to queues.

    """
    try:
        """Connect to RabbitMQ Server, return the connection and channel.
            Creating multiple queues to handle the required data.
            Queues are durable to ensure messages are delivered in order and queue will restart if disconnected."""
        # Creating a connection to the RabbitMQ Server:
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # Use the connection to create a communication channel
        ch = conn.channel()
        
        # Delete existing queues and declares them anew to clear previous queue information.
        # use the channel to declare a durable queue for each of the queues.
        queues = ["01-smoker", "02-food-A", "03-food-B"]
        for queue_name in queues:
             ch.queue_delete(queue=queue_name)
             ch.queue_declare(queue=queue_name, durable=True)
        
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
    except KeyboardInterrupt:
         logger.info("KeyboardInterrupt. Stopping the program.")
    except pika.exceptions.AMQPChannelError as e:
        print(f"Error: Connections to RabbitMQ server failed: {e}")
        logger.info(f"Error: Connections to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # Close the connection to the server
        conn.close()    

def send_message(host: str, queue_name: str, message: str):       
        """
        Open a CSV and iterate through each row of the CSV.
        Seperate three processes by column and send the individual messages to the corresponding queue, 
        by calling send_message function.
        """
try:    
        # Processing the CSV     
    with open(input_file_name, 'r', newline='', encoding='utf-8-sig') as input_file:
        reader = csv.reader(input_file)
        next(reader)
        # reading rows from csv
        for row in reader:
            timestamp_str = row[0]
            smoker_temp = row[1]
            food_A_temp = row[2]
            food_B_temp = row[3]

            # Convert dates into Unix date timestamp that can be added to struct later.
            timestamp = datetime.strptime(timestamp_str, "%m/%d/%y %H:%M:%S").timestamp()

            """
            Created for smoker_temp, using struct which conversts python values and C structs represented as Python bytes.
            This is done to compat formate strings that will be converted to and from Python Values.
            Format strings descirbe the data layout when packing and unpacking the data, 
            this is controled by format characters that specifiy the type of data being pack/unpacked. 
            This process heavily relies on the use of C types in the machines native format and byte order.

            Original segments of code prior to adding struct are commented out to show developement.
            """
            if smoker_temp:
                #smoker_temp = float(smoker_temp)
                #message = (timestamp, smoker_temp)
                message = struct.pack('!df', timestamp, float(smoker_temp))
                send_message(host, "01-smoker", message)
                logger.info(f"[x] Sent Message to {host} in '01-smoker', {message}")
            # Created message for food_A_temp
            if food_A_temp:
                #message = (timestamp, food_A_temp)
                message = struct.pack('!df', timestamp, float(food_A_temp))
                send_message(host, "02-food-A", message)
                logger.info(f"[x] Sent Message to {host} in '02-food-B', {message}")
                # Created a message for food_B_temp
            if food_B_temp:
                #message = (timestamp, food_B_temp)
                message = struct.pack('!df', timestamp, float(food_B_temp))
                send_message(host, "03-food-B", message)
                logger.info(f"[x] Sent Message to {host} in '03-food-B', {message}")
                # Set sleep for 30 seconds before reading the next row:
                time.sleep(30)
except FileNotFoundError:
    logger.error("CSV file not found")
    sys.exit(1)
except ValueError as e:
    logger.error(f"An unecpected error has occured: {e}")
    sys.exit(1)  
except pika.exceptions.AMQPChannelError as e:
    print(f"Error: Connections to RabbitMQ server failed: {e}")
    logger.info(f"Error: Connections to RabbitMQ server failed: {e}")
    sys.exit(1)


# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    
    host = 'localhost'
    input_file_name = "smoker-temps.csv"
    queues = ["01-smoker", "02-food-A", "03-food-B"]
    offer_rabbitmq_admin_site()
    send_message(host,queues, input_file_name)
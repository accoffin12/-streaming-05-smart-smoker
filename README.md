# streaming-05-smart-smoker
> Created by: A. C. Coffin | Completed: 2024 May | NW Missouri State University | CSIS: 44671-80| Dr. Case | Developing a Producer for RabbitMQ

# Overview
Developing a Producer to read the temperature of a Smart Smoker based on specific events. This will be done through simulating temerature readings from the smart smoker of two foods. Create a producer to send these temeprature readings to RabbitMQ and then three consumer processes, each on monitoring one of the temperature streams. Within each consumer it must perform calculations to determine if a significant event has occured. This is the first half, where the focus is on the developement of a Producer. 

# Screen Shot
![R3ProducerV1SendMessage.PNG](/ScreenShots/R3ProducerV1SendMessage.PNG)

# Table of Contents
1. [File List](File_List)
2. [Machine Specs & Terminal Information](Machine_Specs_&_Terminal_Information)
3. [Prerequisites](Prerequisites)
4. [Before you Begin](Before_you_Begin)
5. [Creating Enviroment & Installs](Creating_Enviroment_&_Installs)
6. [Data & Project Specifics](Data_&_Project_Specifics)
7. [Developing Producer](Developing_Producer)
8. [Running Producer](Running_Producer)
9. [Results](Results)
10. [References](References)

# 1. File List
| File Name | Repo Location | File Type |
| ----- | ----- | ----- |
| util_about.py | utils folder | python script |
| util_aboutenv.py | utils folder | python script |
| util_logger.py | utils folder | python script |
| aboutenv.txt | util_outputs | text |
| util_about.tst | util_outputs | text |
| Data_smoker-temps.csv | main repo | csv |
| requirements.txt | main repo | text |
| v2_emitter_of_tasks.py | BaseCode_Samples folder | python script |
| temp_producerV1.py | main repo | python script |
| R1ProducerV1SendMessage.PNG | ScreenShots folder | PNG |
| R2Producerv1SendMessage.PNG | ScreenShots folder | PNG |
| RabbitMQDashProducerV1.PNG | ScreenShots folder | PNG |

# 2. Machine Specs & Terminal Information
This project was completed using a Windows OS computer with the following specs. These are not required to run this repository. For further details see util_about.txt and aboutenv.txt in the utils_outputs located in the utils folder.
* Date and Time: 2024-05-26 at 02:13 PM
* Operating System: nt Windows 10
* System Architecture: 64bit
* Number of CPUs: 12
* Machine Type: AMD64
* Python Version: 3.12.3
* Python Build Date and Compiler: main with Apr 15 2024 18:20:11
* Python Implementation: CPython
* Terminal Environment:        VS Code
* Terminal Type:               cmd.exe
* Preferred command:           python
# 3. Prerequisites
1. Git
2. Python 3.7+ (3.11+ preferred)
3. VS Code Editor
4. VS Code Extension: Python (by Microsoft)
5. RabbitMQ Server Installed and Running Locally
6. Anaconda Installed

# 4. Before you Begin
1. Fork this starter repo into your GitHub.
2. Clone your repo down to your machine.
3. View / Command Palette - then Python: Select Interpreter
4. Select your conda environment.

# 5. Creating Enviroment & Installs
To create a local Python virtual environment to isolate our project's third-party dependencies from other projects. Use the following commands to create an environment, when prompted in VS Code set the .venv to a workspace folder and select yes.

```
python - m venv .venv # Creates a new environment
.venv\Scripts\activate # Activates the new environment
```
Once the environment is created install the following:
```
python -m pip install -r requirements.txt
```

# 6. Data & Project Specifics
The Data was provided by NW Missouri State University as part of the Module 5 Assignment by Dr. Case. The specific requirements for the module are as follows:

We want to stream information from a smart smoker. Read one value every half minute. (sleep_secs = 30)

smoker-temps.csv has 4 columns:

[0] Time = Date-time stamp for the sensor reading
[1] Channel1 = Smoker Temp --> send to message queue "01-smoker"
[2] Channel2 = Food A Temp --> send to message queue "02-food-A"
[3] Channel3 = Food B Temp --> send to message queue "03-food-B"
## 6a. Required Approach
* Use your Module 4 projects (Version 2 and Version 3) as examples.
* Remember: No prior coding experience is required to take this course. Rely heavily on the working examples from earlier modules. 
* The more similar your code looks to the examples - the more credit earned.
* Vastly different approaches can be expected to earn less credit not more.
* This project should clearly build on skills and code we've already mastered. If not, let me know and more help will be provided. 
* The primary difference should be going from 1 to 3 queue_names and from 1 to 3 callbacks. 
* Part of the challenge is to implement analytics using the tools and approach provided (don't significantly refactor the codebase during your first week of work!) 
* AFTER earning credit for the assignment, THEN create and share additional custom projects. 
It's important to note that this project only developes a Producer, which means that we will be hevaily relying on the RabbitMQ Admin Panel and logs. The logs for this project have been included in the repository as a way to show that the message is being sent to the queue. 

# 7. Developing Producer
The Producer for this project is based on a Base Code provided by Dr. Case called v2_emitter_of_tasks from the streaming-04-multiple-consumers. Samples of the v2_emitter_of_tasks.py can be found in the BaseCode_Samples folder, as well as two variations on a Consumer. The entire base code was kept, with some sections modified to meet the requriements of the assignment. The original code included a path to the RabbitMQ Admin Website seen in lines 44 to 51. 

## 7a. send_message Function
The focus of this particular Producer was developing a Producer that would stream data to 3 seperate queues, smoker_queue, foodA_queue, foodB_queue. In order to do this the variables were declared upfront. There were complications when the variables were placed under the entry point, so they were moved to the top under the Imported Libraries. 

```
# Declaring variables:
host = 'localhost'
input_file_name = 'smoker-temps.csv'
smoker_queue = "01-smoker"
foodA_queue = "02-food-A"
foodB_queue = "03-food-B"
```

With each of the three queues, an emphasis was placed on making them durable if RabbitMQ crashed, but also addressed the issue of messages accumulating without a consumer to retrieve them. This was done by using `queue_delete` prior to `queue_declare`. 

```
# Delete existing queues and declares them anew to clear previous queue information.
        # use the channel to declare a durable queue for each of the queues.
        ch.queue_delete(smoker_queue)
        ch.queue_delete(foodA_queue)
        ch.queue_delete(foodB_queue)

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(smoker_queue, durable=True)
        ch.queue_declare(foodA_queue, durable=True)
        ch.queue_declare(foodB_queue, durable=True)
```
We set the messages to publish to a specific exchange, routing_key and message. Once established error handling was added, in case the connection to the server either failed, or couldn't be established. Finally we designed the script ot close when the stream of data was complete. This proccess can take a very long time, so an exceptionw was added for a keyboard escape:

```
except KeyboardInterrupt:
         logger.info("KeyboardInterrupt. Stopping the program.")
```

## 7b. main function
This portion was designed to open a CSV and iterate through each of the rows based on the column infromation to the corresponding queue. There are a total of 4 columns in the CSV, however only 3 need queues of their own. 

When creating the read function, it is important to note that we utilize row numbers in correspondence with the information in each row.

```
for row in reader:
                timestamp = row[0]
                smoker_temp = row[1]
                food_A_temp = row[2]
                food_B_temp = row[3]
```
A time and date split was performed as the data could not be transformed into a Unix format, it did not contain seconds which is required to use this format. Next each of the three queues were given specific messages to recieve. Each message contains the following information and a logger to track the message.

```
 # Created for smoker_temp, using encode which encodes the data as a binary output
                if smoker_temp:
                    smoker_temp = float(smoker_temp)
                    # Using an f string to send data with timestamp
                    message = (f"{smoker_queue} Reading = Date: {date_split}, Time: {time_split}; temp: {smoker_temp} deg F.").encode()
                    send_message(host, "01-smoker", message)
```
Another exception handler was added in case the CSV file could not be found, or there was a value error. 

# 8. Running Producer
To run the Producer open a terminal in VS Code, in this case we won't have to worry about a Consumer, so don't panic when we only see the print messages. **Before Running Producer, make sure RabbitMQ is running, it will not work if it isn't.**

Once in the terminal type command:
`python temp_producerV1.py`

Once active, it will inquire as to if you want to open RabbitMQ's Admin Panel, answer as you like, a y = yes and n = no. When the code is transmitting the boxes in RabbitMQ will change to green and say running. 

![RabbitMQDashProducerV1.PNG](/ScreenShots/RabbitMQDashProducerV1.PNG)

After the question is answered the script will run. Watch the terminal carefully, you should see the log message for each of the three columns flash through eventually. The sleep time was set to 30 seconds so it may take some time to run through the entire CSV. 

The terminal when running should look like this prior to adding the variable messages to each of the logging statements. 
![R1ProducerV1SendMessages.PNG](/ScreenShots/R1ProducerV1SendMessage.PNG)

# 9. Results
This is the final output, complete with message added to the logging data.

![R2ProducerV1SendMessage.PNG](/ScreenShots/R2Producerv1SendMessage.PNG)

1 = Producer Code Being Run,
2 = Activer Terminal Processing Data,
3 = Log 
# 10. References


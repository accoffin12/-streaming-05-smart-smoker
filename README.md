# streaming-05-smart-smoker
> Created by: A. C. Coffin | Completed: 2024 May | NW Missouri State University | CSIS: 44671-80| Dr. Case | Developing a Producer for RabbitMQ

# Overview
Developing a Producer to read the temperature of a Smart Smoker based on specific events. This will be done through simulating temerature readings from the smart smoker of two foods. Create a producer to send these temeprature readings to RabbitMQ and then three consumer processes, each on monitoring one of the temperature streams. Within each consumer it must perform calculations to determine if a significant event has occured.

# Screen Shot

# Table of Contents
1. [File List](File_List)
2. [Machine Specs & Terminal Information](Machine_Specs_&_Terminal_Information)
3. [Prerequisites](Prerequisites)
4. [Before you Begin](Before_you_Begin)
5. [Creating Enviroment & Installs](Creating_Enviroment_&_Installs)
6. [Data & Project Specifics](Data_&_Project_Specifics)
7. [Developing Producer](Developing_Producer)
8. [Developing Consumers](Developing_Consumers)
9. [Running Producer/Consumers](Running_Producer/Consumers)
10. [Final Output](Final_Output)
11. [Results](Results)
12. [References](References)

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
Before beginning this project two environments were made, one as a VS Code environment and the other as an Anaconda environment. RabbitMQ requires the Pika Library to function, to ensure that the scripts execute and create an environment in either VS Code or Anaconda.

## 5a. Creating VS Code Enviroment
To create a local Python virtual environment to isolate our project's third-party dependencies from other projects. Use the following commands to create an environment, when prompted in VS Code set the .venv to a workspace folder and select yes.

```
python - m venv .venv # Creates a new environment
.venv\Scripts\activate # Activates the new environment
```
Once the environment is created install the following:
```
python -m pip install -r requirements.txt
```

## 5b. Creating Anaconda Environment
If you have another enviroment that contains the required installs then activate it, I will be utilizing my preconstructed enviroment RabbitEnv.

To create an Anaconda environment open an Anaconda Prompt, the first thing that will pop up is the base. Then we are going to locate our folder, to do this type the following:
```
cd Dcuments\folder_where_repo_is\ 
cd Documents\ACoffinCSIS44671\-streaming-05-smart-smoker # This is where the file is located on my computer
```
To create an environment do the following:
```
conda create -n RabbitEnv # Creates the environment
conda activate RabbitEnv # Activates Environment
```
Once the environment is created execute the following:
```
python --version # Indicates Python Version Installed
conda config --add channels conda-forge # connects to conda forge
conda config --set channel_priority strict # sets priority
install pika # library installation
```
Each of these lines must be executed independetly, you have to use the forge to do this with Anaconda.

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


# 7. Developing Producer

# 8. Developing Consumers

# 9. Running Producer/Consumers

# 10. Final Output

# 11. Results

# 12. References


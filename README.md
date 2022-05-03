# SMT Project Experience

## Table of contents
1. [Introduction](#introduction)
2. [Technologies Required](#technologies_required)
    1. [Installation](#installation)
        1. [Python](#install_python)
        2. [Node.js](#install_nodejs)
        3. [MongoDB](#install_mongodb)
    2. [Version Check](#version_check)
        1. [Python](#version_check_python)
        2. [Nodejs](#version_check_nodejs)
        3. [MongoDB](#version_check_mongodb)
3. [Configuration & Setting Up](#setup)
    1. [Server](#server)
        1. [Cloning Repository](#cloning_repository)
        2. [Install Dependencies](#install_dependencies)
        3. [Database Setup](#database_setup) 
        4. [Chrome Browser and Chromedrive](#chrome_drive)
        5. [Reddit Account](#reddit_account)
        6. [Cronjob](#cronjob)
        7. [Environment File](#environment_file)
4. [Running the Application](#run_app)

---
## Introduction <a name="introduction"></a>
This is a project repository for SMU SMT Project Experience module. In this project, we are building a social listening tool system which consists of daily collection of social media data and building a web dashboard which displays various insightful charts and statistics, using the data collected. More information about our project can be found in the project report pdf file [link](https://github.com/CJianYu98/SMT_Project_Experience/blob/main/Final%20Report%20-%20The%20Listening%20Squad.pdf).

This repository contains instructions of setting up and running the application. The application was built on a **Linux Ubuntu** OS and the example codes below will be based on this OS. Since this application serves as a prototype, we deploy the application on localhost. 

Following sections provide instructions on how to setup and run our application on your local machine.

[Back To The Top](#SMT-Project-Experience)

---
## Technologies Required <a name="technologies_required"></a>
This project is created with the following technologies and versions. 
- [Python] : >= 3.8
- [Node] : >= 
- [MongoDB] : >= 5.0.6

If these technologies are installed in the server, follow the steps in the [Version Check](#version_check) segment to check the version installed in the server. If you have yet to install any, please refer to the [Installation](#installation) segment.

[Back To The Top](#SMT-Project-Experience)

---
## Installation <a name="installation"></a>
The following are command lines to install the required technologies.
<br>
Before we start installing the various technologies, let's update our Advanced Package Tool in our Ubuntu server. Run the following command to update apt package index:

```
sudo apt-get update && sudo apt-get upgrade -y
sudo apt update && sudo apt upgrade
```
<br>

### - Python <a name="install_python"></a>
Run the following command to change to the root directory:
```
cd /
```
<br>

Run the following command to install Python:
```
sudo apt-get install python3.8
```
<br>

### - Node.js <a name="install_nodejs"></a>
Run the follwoing command to install Node.js:
```
sudo apt install nodejs
```
<br>

Run the following command to install Node.js package manager:
```
sudo apt install npm
```

### - MongoDB <a name="install_mongodb"></a>
Follow the commands in this [link](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/) to install MongoDB 

[Back To The Top](#SMT-Project-Experience)

---
## Version Check <a name="version_check"></a>
The following are methods you can use to check the version of your current technologies.

### - Python <a name="version_check_python"></a>
Run the following command to check the version for Python:
```
python3 --version
```
If your current version of Python is older than **3.8**, [install](#install_python) the latest version.  
<br>

### - Node.js <a name="version_check_nodejs"></a>
Run the following command to check the version for Node.js:
```
node --verion
```
<br>

If your current version of Node.js is older than **--**, [install](#install_nodejs) the latest version.

### - MongoDB <a name="version_check_mongodb"></a>
Run the following command to check the version for MongoDB:
```
mongo --verion
```
<br>

If your current version of MongoDB is older than **5.0.6**, [install](#install_mongodb) the latest version.

[Back To The Top](#SMT-Project-Experience)

---
## Configuration & Setup <a name="setup"></a>
After you have installed the required technologies, you can proceed to setup the project. If you have yet to install/update the required technologies, please proceed the [Technologies Required](#technologies_required) segment to do so.
<br>

## Server <a name="server"></a>
The following instructions are for setting up and configuring the backend development of the project.
<br>

### - Cloning Repository <a name="cloning_repository"></a>
You may cd into your preferred directory to clone the project's repository. After cd into the directory, you may run the following command to clone project's repository:
```
sudo git clone https://github.com/CJianYu98/SMT_Project_Experience.git
```
You will be prompted to log in to a Github account. You may use any Github account which has access to clone the repository.
<br>

### - Install Dependencies <a name="install_dependencies"></a>
After cloning the repository, run the following command to cd into the project directory:
```
cd SMT_Project_Experience
```

We will have to install the necessary dependencies for the project. You may run the following command to install these dependencies:
```
pip3 install -r requirements.txt
```

**ML part to be completed**

### - Database Setup <a name="database_setup"></a>
Run the following command to enter mongo shell:
```
mongo
```
<br>

Next, you can set up a user for the project. Below is an example:
```
use smt483.createUser({
    user: 'user1',
    pwd: 'yourSecretPassword',
    roles: [{ role: 'readWrite', db:'smt483'}]
})
```
This sets up a user named **user1** with a password and is given read & write access to the **SMT483** database.
<br>

Next, we will enable auth and open MongoDB access to all IPs. First we will have to edit MongoDB config file, you may run the following command:
```
sudo nano /etc/mongod.conf
```
Look for the **net** line in the file and update the code lines as following:
```
# network interfaces
net:
    port: 27017
    bindIp: 0.0.0.0 
```
Scroll down to the **#security** section and add the following line. Make sure to uncomment the **security:** line.
```
security:
    authorization: 'enabled'
```
You may wanna make sure port 27017 is open on your server.
<br>

Lastly, we will restart our mongo daemon (mongod). You may run the following command:
```
sudo service mongod restart
```
<br>

To log in to your mongo shell remotely, you may run the following command:
```
mongo -u user1 -p yourSecretPassword <your_server_public_ip>/smt483
```

### - Chrome Browser and Chromedrive <a name="chrome_driver"></a>
We will need Chrome Browser and Chromdrive installed to run the daily collection of data from different social media platforms. To install them, you may refer to the instructions in this [link](https://skolo.online/documents/webscrapping/#pre-requisites).
<br>

### - Reddit Account <a name="reddit_account"></a>
Reddit account is required to perform data collection from Reddit. 
**To be completed**
<br>

### - Cronjob <a name="cronjob"></a>
ETL cronjobs were deployed on a dedicated Linux GPU server for our project. However, you may deployed all the following cronjobs on your Linux server. *Note that the time taken to run the machine learning models during ETL process may be long.

Run the following command to edit the crontab file:
```
crontab -e
```
<br>

Creating cronjobs for daily collection and ETL process:
```
# Reddit
0 0 */1 * * python3 /home/jianyu/SMT_Project_Experience/app/scraper/reddit/daily.py
0 */1 * * * cd /home/jianyu/SMT_Project_Experience && python3 -B -m app.database.reddit_daily_etl

# Twitter
0 0 */1 * * python3 /home/jianyu/SMT_Project_Experience/app/scraper/twitter/daily.py
0 */1 * * * cd /home/jianyu/SMT_Project_Experience && python3 -B -m app.database.twitter_daily_etl

# Youtube
0 0 */1 * * python3 /home/jianyu/SMT_Project_Experience/app/scraper/youtube/dailyYoutube.py
0 */1 * * * cd /home/jianyu/SMT_Project_Experience && python3 -B -m app.database.youtube_daily_etl
```

### - Environment File <a name="environment_file"></a>
In our project, we save our raw data files and log files in a Network-attached Storage (NAS). You may decide on the location/folder to store these files and edit the environment variables in the `.env` code example given below.

In the SMT_Project_Experience folder, you may create a `.env` file with the following fields:
```
############################ GENERAL ############################
TIMEZONE = "Asia/Singapore"

############################ SERVER ############################
TWITTER_DAILY_DATA_PATH = "<your_data_storage_folder>/twitter/daily"
REDDIT_DAILY_DATA_PATH = <your_data_storage_folder>/reddit/daily"
YOUTUBE_DAILY_DATA_PATH = <your_data_storage_folder>/youtube/daily"
FACEBOOK_HISTORICAL_DATA_PATH = <your_data_storage_folder>/facebook/historical"
REDDIT_HISTORICAL_DATA_PATH = <your_data_storage_folder>/reddit/historical"
REDDIT_DAILY_DATA_PATH = <your_data_storage_folder>/reddit/daily"

####################### LOGFILES #######################
TWITTER_DAILY_LOG_FILE = <your_data_storage_folder>/log/scraper/twitter/daily.log"
REDDIT_DAILY_LOG_FILE = <your_data_storage_folder>/log/scraper/reddit/daily.log"
YOUTUBE_DAILY_LOG_FILE = <your_data_storage_folder>/log/scraper/youtube/daily.log"
REDDIT_DAILY_ETL_LOG_FILE = <your_data_storage_folder>/log/database/reddit_etl.log"
TWITTER_DAILY_ETL_LOG_FILE = <your_data_storage_folder>/log/database/twitter_etl.log"
YOUTUBE_DAILY_ETL_LOG_FILE = <your_data_storage_folder>/log/database/youtube_etl.log"

####################### STATUS CHECK ########################
STATUS_CHECK_FILE = "<your_data_storage_folder>/daily_status.json"

############################ MONGODB ############################
DB_URL = ""
DB_TABLE_NAME = ""
DB_FACEBOOK_POSTS_COLLECTION = "facebook_posts"
DB_FACEBOOK_COMMENTS_COLLECTION = "facebook_comments"
DB_REDDIT_SUBMISSIONS_COLLECTION = "reddit_submissions"
DB_REDDIT_COMMENTS_COLLECTION = "reddit_comments"
DB_TWIITER_TWEETS_COLLECTION = "twitter_tweets"
DB_TWITTER_COMMENTS_COLLECTION = "twitter_comments"
DB_YOUTUBE_VIDEOS_COLLECTION = "youtube_videos"
DB_YOUTUBE_COMMENTS_COLLECTION = "youtube_comments"

############################ SCRAPING ############################
CUTOFF_DAYS = "14"  # Period in days
SCRAPE_FROM_DATE = "1640995200"

############################ REDDIT ############################
REDDIT_CLIENT_ID = ""
REDDIT_CLIENT_SECRET = ""
REDDIT_USER_AGENT = ""
REDDIT_USERNAME = ""
REDDIT_PASSWORD = ""

############################ YOUTUBE ############################
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

############################ ML ############################
MODEL_DATA_FOLDER_PATH = "./app/ml/models/model_data"
EMOTIONS_MODEL_PATH = "typeform/distilbert-base-uncased-mnli" #"facebook/bart-large-mnli"
INTENT_MODEL_PATH = "typeform/distilbert-base-uncased-mnli" #"facebook/bart-large-mnli"
TOPIC_MODEL_PATH = "typeform/distilbert-base-uncased-mnli" #"facebook/bart-large-mnli"
SENTIMENT_MODEL_PATH = "cardiffnlp/twitter-roberta-base-sentiment"
```
Make sure to fill up the values for `DB_URL`, `DB_TABLE_NAME` and all the fields under ```REDDIT``` section.

[Back To The Top](#SMT-Project-Experience)

---
## Running the Application <a name="run_app"></a>
Your setup is now configured and ready to run. 
<br>

To run the backend server application, you need to cd into SMT_Project_Exprience folder:
```
cd SMT_Project_Experience
```
Start the backend server using the following command:
```
uvicorn app.main:app --reload
```
<br>

To run the frontend application, you may run the following commands:
```
cd app\vue
```
```
npm install
```
```
npm run dev
```
<br>

Visit [localhost:3000](http://localhost:3000/) to view the application. 
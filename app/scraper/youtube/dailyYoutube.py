import json
import os
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import pandas as pd
import pytz
import telegram_send
from dotenv import load_dotenv
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Load environment variables
load_dotenv()

# # Change to file directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Read json file for channels to scrape
f = open("../accounts_to_scrape/youtube.json")
channels = json.load(f)

# Constants
YOUTUBE_DAILY_DATA_PATH = os.getenv("YOUTUBE_DAILY_DATA_PATH")
YOUTUBE_DAILY_LOG_FILE = os.getenv("YOUTUBE_DAILY_LOG_FILE")
STATUS_CHECK_FILE = os.getenv('STATUS_CHECK_FILE')

CHNL_TITLE = "Title"
CHNL_URL = "URL"
CHNL_THUMBNAIL = "Thumbnail"
channelVideos = pd.DataFrame(columns=[CHNL_TITLE, CHNL_URL, CHNL_THUMBNAIL])


VID_TITLE = "Title"
VID_VIEWS = "Views"
VID_DATE_UPLOADED = "Date Uploaded"
VID_LIKES = "Likes"
VID_DESCRIPTION = "Description"
VID_COMMENTS = "Comments"
VID_URL = "URL"
VID_THUMBNAIL = "Thumbnail"
videoDetails = pd.DataFrame(
    columns=[
        VID_TITLE,
        VID_VIEWS,
        VID_DATE_UPLOADED,
        VID_LIKES,
        VID_DESCRIPTION,
        VID_COMMENTS,
        VID_URL,
        VID_THUMBNAIL,
    ]
)

# Date Variables
today = datetime.now()
date = today.date()
STOPDATE = today - (timedelta(days=int(os.getenv("CUTOFF_DAYS"))))  # stop at 2 weeks ago
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))
sg_datetime = datetime.now(TIMEZONE)

# Add logger configurations
logger.add(
    YOUTUBE_DAILY_LOG_FILE,
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

############################### Methods ###############################

# scroll down the webpage
def scrollChannelPage():
    driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight)")
    time.sleep(0.75)


def scrollVideoPage():
    driver.execute_script("window.scrollBy(0,450)")  # scroll just enough to the top of comments
    time.sleep(3)


# retrieve title and url of videos in the channel
def getTitleAndURL(videos):
    global channelVideos

    for video in videos:
        anchorTag = video.find_element(By.XPATH, ".//a[@id='video-title']")
        title = anchorTag.get_attribute("title")
        href = anchorTag.get_attribute("href")

        if len(href) == 0 or href.isspace():
            continue
        
        dateValid = checkDate(href)

        if dateValid == 2: # faced error checking the date 
            continue
        elif dateValid == 0: # date is past STOPDATE
            break

        row = {CHNL_TITLE: title, CHNL_URL: href}
        channelVideos = channelVideos.append(row, ignore_index=True)
        getThumbnail(video)


# check video is within timeframe
def checkDate(video):
    result = 2 # default for error
    try:
        driver.switch_to.window(driver.window_handles[1])
        driver.get(video)
        wait = WebDriverWait(driver, 30)

        infoContainer = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='container' and @class='style-scope ytd-video-primary-info-renderer']",
                )
            )
        )
        uploadedTag = infoContainer.find_element(
            By.XPATH,
            "//div[@id='info-strings' and @class='style-scope ytd-video-primary-info-renderer']",
        )
        uploaded = uploadedTag.find_element(
            By.XPATH, ".//yt-formatted-string[@class='style-scope ytd-video-primary-info-renderer']"
        ).text
        logger.debug(uploaded)

        # if "Premiered" in uploaded:
        #     splitDate = uploaded.split(" ")
        #     newDate = f"{splitDate[1]} {splitDate[2][:-1]} {splitDate[3]}"
        #     date = datetime.strptime(newDate, "%b %d %Y")
        if "," in uploaded:
            splitDate = uploaded.split(" ")
            newDate = f"{splitDate[-3]} {splitDate[-2][:-1]} {splitDate[-1]}"
            date = datetime.strptime(newDate, "%b %d %Y")
            # logger.debug(newDate)
            # logger.debug(splitDate)
        elif "ago" in uploaded:
            date = datetime.now()
        else:
            newDate = uploaded
            date = datetime.strptime(newDate, "%d %b %Y")
        # logger.debug(date)

        # Note that earlier dates are considered smaller than later dates
        # i.e. 2022-01-14 < 2022-01-15
        result = 0 if STOPDATE > date else 1
        driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        logger.exception(e)
        driver.switch_to.window(driver.window_handles[0])
    finally:
        return result


# get thumbnail of each video
def getThumbnail(video):
    global channelVideos

    anchorTag = video.find_element(
        By.XPATH, ".//img[@id='img' and @class='style-scope yt-img-shadow']"
    )

    img = anchorTag.get_attribute("src")

    channelVideos.loc[len(channelVideos) - 1, CHNL_THUMBNAIL] = img


# retreive details of the video
def getInfo(container):
    global videoDetails

    # getting the title
    titleTag = container.find_element(
        By.XPATH, "//yt-formatted-string[@class='style-scope ytd-video-primary-info-renderer']"
    )
    title = titleTag.text

    # getting the number of views
    viewsTag = container.find_element(
        By.XPATH,
        "//ytd-video-view-count-renderer[@class='style-scope ytd-video-primary-info-renderer']",
    )
    views = viewsTag.find_element(
        By.XPATH, ".//span[@class='view-count style-scope ytd-video-view-count-renderer']"
    ).text

    # getting the date uploaded
    try:
        uploadedTag = container.find_element(
            By.XPATH,
            "//div[@id='info-strings' and @class='style-scope ytd-video-primary-info-renderer']",
        )
        uploaded = uploadedTag.find_element(
            By.XPATH, ".//yt-formatted-string[@class='style-scope ytd-video-primary-info-renderer']"
        ).text
        
        if "ago" in uploaded:
            today = datetime.now()
            if "hours" in uploaded:
                splitDate = uploaded.split(" ")
                hour= splitDate[2]
                newDate = (today - timedelta(hours=int(hour))).date()
                uploaded = newDate.strftime("%b %d, %Y")
            elif "minutes" in uploaded:
                splitDate = uploaded.split(" ")
                minute= splitDate[2]
                newDate = (today - timedelta(hours=int(minute))).date()
                uploaded = newDate.strftime("%b %d, %Y")
            else:
                uploaded = today.strftime("%b %d, %Y")
    except Exception as e:
            logger.exception(f"Error: Unable to get video uploaded date {e}")


    # getting the number of likes
    likesTag = container.find_element(
        By.XPATH,
        "//yt-formatted-string[@id='text' and @class='style-scope ytd-toggle-button-renderer style-text']",
    )
    likes = likesTag.text

    videoDetails.loc[len(videoDetails), VID_TITLE] = title
    videoDetails.loc[len(videoDetails) - 1, VID_VIEWS] = views
    videoDetails.loc[len(videoDetails) - 1, VID_DATE_UPLOADED] = uploaded
    videoDetails.loc[len(videoDetails) - 1, VID_LIKES] = likes


# retrieve description of the video
def getDescription(container):
    global videoDetails

    anchorTag = container.find_elements(
        By.XPATH, "//span[@class='style-scope yt-formatted-string']"
    )

    description = "".join(text.text for text in anchorTag)
    videoDetails.loc[len(videoDetails) - 1, VID_DESCRIPTION] = description


# retrieve comments of the video
def getComments(container):
    global videoDetails

    commentList = []

    comment = ''
    date = ''
    likes = '0'

    for thread in container:
        # retrieve comment
        commentsInView = thread.find_element(By.XPATH,".//div[@id='content' and @class='style-scope ytd-expander']")
        commentsTag = commentsInView.find_elements(By.XPATH,".//yt-formatted-string[@id='content-text'and @class='style-scope ytd-comment-renderer']")
        for c in commentsTag:
            comment = c.text

        # retrieve date posted for comment
        dateTag = thread.find_element(By.XPATH,".//yt-formatted-string[@class='published-time-text above-comment style-scope ytd-comment-renderer']/a")
        date = dateTag.text
        splitDate = date.split(" ")
        num= splitDate[0]
        newDate = datetime.now()

        if 'minutes' in date:
            newDate = (datetime.now() - timedelta(minutes=int(num))).date()
        elif 'hours' in date:
            newDate = (datetime.now() - timedelta(hours=int(num))).date()
        elif 'days' in date:
            newDate = (datetime.now() - timedelta(days=int(num))).date()
        elif 'months' in date:
            newDate = datetime.now() - relativedelta(months=int(num))
        
        date = newDate.strftime("%b %d, %Y")

        # retrieve num of likes for comment
        likesInView = thread.find_element(By.XPATH,".//div[@id='toolbar' and @class='style-scope ytd-comment-action-buttons-renderer']")
        likesTag = likesInView.find_element(By.XPATH,".//span[@id='vote-count-middle' and @class='style-scope ytd-comment-action-buttons-renderer']")
        likes = likesTag.text
        if likes == '':
            likes = '0'

        commentList.append({'Comment':comment,
                                'Date':date,
                                'Likes':likes})
    
    videoDetails.loc[len(videoDetails) - 1, VID_COMMENTS] = commentList

def clickMoreComments(container):
    for readMore in container:
        try:
            moreTag = readMore.find_element(
                By.XPATH, ".//ytd-expander[@id='expander' and @class='style-scope ytd-comment-renderer']"
            )
            moreText = moreTag.find_element(
                By.XPATH,".//tp-yt-paper-button[@id='more' and @class='style-scope ytd-expander']/span"
            )
            moreText.click()
        except Exception as e:
            continue
            # logger.debug(f"No click more element in comment {e}")

# scrape all the videos for each channel
def fullChannel(channelURL):
    # global videoCounter
    driver.get(channelURL)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[0])

    # Wait for initialize, in seconds
    wait = WebDriverWait(driver, 30)

    # Step 1: Get the main container housing all the videos
    mainContainer = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='items' and @class='style-scope ytd-grid-renderer']")
        )
    )

    # Step 2: List of all the videos
    videosInView = mainContainer.find_elements(
        By.XPATH, "//ytd-grid-video-renderer[@class='style-scope ytd-grid-renderer']"
    )

    # Get scroll height
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        # Scroll down to bottom
        scrollChannelPage()
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        videosInView = mainContainer.find_elements(
            By.XPATH, "//ytd-grid-video-renderer[@class='style-scope ytd-grid-renderer']"
        )

    getTitleAndURL(videosInView)


# scrape details for each video
def fullVideo(video):
    global videoDetails
    try:
        driver.get(video)
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[0])

        # Wait for initialize, in seconds
        wait = WebDriverWait(driver, 30)

        # Video Info
        infoContainer = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='container' and @class='style-scope ytd-video-primary-info-renderer']",
                )
            )
        )
        getInfo(infoContainer)

        # Video Description
        try:
            descContainer = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@id='content' and @class='style-scope ytd-expander']")
                )
            )
            description = descContainer.find_element(
                By.XPATH,
                "//div[@id='description' and @class='style-scope ytd-video-secondary-info-renderer']",
            )
            getDescription(description)
        except Exception as e:
            logger.exception(f"Error: Unable to get video description {e}")

        # Video Comments
        try:
            commentContainer = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='contents' and @class='style-scope ytd-item-section-renderer']",
                    )
                )
            )
            # wait.until(
            #     EC.presence_of_all_elements_located(
            #         (By.XPATH, "//div[@id='contents' and @class='style-scope ytd-item-section-renderer']")
            #     )
            # )
            commentsInView = commentContainer.find_elements(
                By.XPATH, "//div[@id='content' and @class='style-scope ytd-expander']"
            )
        except Exception as e:
            logger.exception(f"Error: Unable to locate comments container {e}")

        scrollVideoPage()
        # Get scroll height
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight)")
            time.sleep(2)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            commentsInView = commentContainer.find_elements(
                By.XPATH, "//div[@id='content' and @class='style-scope ytd-expander']"
            )
        #find long comments that require read more to expand
        readMoreInView = commentContainer.find_elements(
            By.XPATH,"//div[@id='main' and @class='style-scope ytd-comment-renderer']"
        )
        try:
            clickMoreComments(readMoreInView)

            # commentsInView = commentContainer.find_elements(
            #         By.XPATH, "//div[@id='content' and @class='style-scope ytd-expander']"
            # )
            readMoreInView = commentContainer.find_elements(
                By.XPATH,"//div[@id='main' and @class='style-scope ytd-comment-renderer']"
            )
        except Exception as e:
            logger.exception(f"Error: Unable to expand comments {e}")
        if len(readMoreInView) > 0:
            getComments(readMoreInView)
        else:
            videoDetails.loc[len(videoDetails) - 1, VID_COMMENTS] = []
    except Exception as e:
        logger.exception(f"Error: Unable to scrape video {e}")


# save file in json
def save_json(filename, new_dict):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(new_dict, f, ensure_ascii=False, indent=4, default=str)
    except:
        print(f"Error saving {filename}.")


############################### SCRAPING  ###############################
start = time.time()
telegram_send.send(messages=[f"YOUTUBE DAILY --> Daily data crawling started at {sg_datetime}"])
logger.info(f"Daily data crawling started at {sg_datetime}")

vdict = {}

for c in channels:
    # specify the path to chromedriver.exe
    s = Service(os.getenv("CHROMEDRIVER_PATH"))
    options = Options()
    options.headless = True
    options.add_argument(
        "chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')"
    )
    options.add_argument("--window-size=1920,1080")

    # open the webpage
    driver = webdriver.Chrome(service=s, options=options)

    logger.info(f"Scraping video URLs for channel {c}")

    # reset dataframes
    channelVideos = pd.DataFrame(columns=[CHNL_TITLE, CHNL_URL, CHNL_THUMBNAIL])
    videoDetails = pd.DataFrame(
        columns=[
            VID_TITLE,
            VID_VIEWS,
            VID_DATE_UPLOADED,
            VID_LIKES,
            VID_DESCRIPTION,
            VID_COMMENTS,
            VID_URL,
            VID_THUMBNAIL,
        ]
    )

    channelName = c
    channelURL = channels[c]

    try:
        # scrape the videos in the channel
        fullChannel(channelURL)
        logger.info(f"Videos URLs for channel {c} scraped successfully")
    except Exception as e:
        logger.exception(f"Error: Unable to scrape video URLs for channel {c} sucessfully {e}")

    # scrape details of each video
    for video in channelVideos.index:
        try:
            url = channelVideos["URL"][video]
            logger.info(f"Scraping video data for channel {c}: video url - {url}")
            fullVideo(url)

            videoDetails.loc[len(videoDetails) - 1, VID_URL] = url
            thumbnail = channelVideos["Thumbnail"][video]
            videoDetails.loc[len(videoDetails) - 1, VID_THUMBNAIL] = thumbnail

            logger.info(f"Video data for channel {c}: video url - {url} scraped successfully")
        except Exception as e:
            logger.exception(f"Error: Unable to scrape video data for channel {c}: video url - {url} successfully {e}")

    # add records to dict
    jvideos = videoDetails.to_json(orient="records")
    parsedV = json.loads(jvideos)
    vdict[channelName] = parsedV

    telegram_send.send(
        messages=[f"YOUTUBE DAILY --> Data scraping for channel {c} has successfully completed."]
    )
    logger.info(f"Data scraping for channel {c} has successfully completed.")

    driver.quit()
    for _ in range(5):
        os.system("pkill --oldest chrome")
    time.sleep(3)

# export file in json
save_json(f"{YOUTUBE_DAILY_DATA_PATH}/{today.date()}.json", vdict)

end = time.time()

file = open(STATUS_CHECK_FILE)
jobj = json.load(file)
jobj['youtube']['latest_collection_date'] = date.strftime("%Y-%m-%d")
with open(STATUS_CHECK_FILE, 'w') as f:
    json.dump(jobj, f, indent=4)

telegram_send.send(
    messages=[f"YOUTUBE DAILY --> Daily crawling completed.\nTOTAL TIME TAKEN: {end - start}"]
)
logger.info(f"Daily crawling completed.\nTOTAL TIME TAKEN: {end - start}")

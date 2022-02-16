import json
import os
import time
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Load environment variables
load_dotenv()

# # Change to file directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# read json file for channels to scrape
f = open("../accounts_to_scrape/youtube.json")
channels = json.load(f)

# CHANNEL VARIABLES
isChannelContinueTrue = True

CHNL_TITLE = "Title"
CHNL_URL = "URL"
CHNL_THUMBNAIL = "Thumbnail"
channelVideos = pd.DataFrame(columns=[CHNL_TITLE, CHNL_URL, CHNL_THUMBNAIL])

# VIDEO VARIABLES
isVideoContinueTrue = True

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

# DATE VARIABLES
today = datetime.now()
STOPDATE = today - (timedelta(days=int(os.getenv("CUTOFF_DAYS"))))  # stop at 2 weeks ago

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

        if checkDate(href) == 0:
            break

        row = {CHNL_TITLE: title, CHNL_URL: href}
        channelVideos = channelVideos.append(row, ignore_index=True)
        getThumbnail(video)


# check video is within timeframe
def checkDate(video):
    try:
        driver.switch_to.window(driver.window_handles[1])
        driver.get(video)
        wait = WebDriverWait(driver, 10)

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

        if "," in uploaded:
            splitDate = uploaded.split(", ")
            newDate = f"{splitDate[0]} {splitDate[1]}"
            date = datetime.strptime(newDate, "%b %d %Y")
        else:
            newDate = uploaded
            date = datetime.strptime(newDate, "%d %b %Y")

        # Note that earlier dates are considered smaller than later dates
        # i.e. 2022-01-14 < 2022-01-15
        result = 0 if STOPDATE > date else 1
        driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
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
    uploadedTag = container.find_element(
        By.XPATH,
        "//div[@id='info-strings' and @class='style-scope ytd-video-primary-info-renderer']",
    )
    uploaded = uploadedTag.find_element(
        By.XPATH, ".//yt-formatted-string[@class='style-scope ytd-video-primary-info-renderer']"
    ).text

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

    comments = []

    for thread in container:
        anchorTag = thread.find_elements(
            By.XPATH,
            ".//yt-formatted-string[@id='content-text'and @class='style-scope ytd-comment-renderer']",
        )
        comments.extend(comment.text for comment in anchorTag)
    videoDetails.loc[len(videoDetails) - 1, VID_COMMENTS] = comments


# scrape all the videos for each channel
def fullChannel(channelURL):
    # global videoCounter
    driver.get(channelURL)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[0])

    # Wait for initialize, in seconds
    wait = WebDriverWait(driver, 10)

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
    while isChannelContinueTrue:
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
    # global commentCounter
    driver.get(video)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[0])

    # Wait for initialize, in seconds
    wait = WebDriverWait(driver, 10)

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

    # Video Comments
    commentContainer = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='contents' and @class='style-scope ytd-item-section-renderer']")
        )
    )
    wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@id='contents' and @class='style-scope ytd-item-section-renderer']")
        )
    )
    commentsInView = commentContainer.find_elements(
        By.XPATH, "//div[@id='content' and @class='style-scope ytd-expander']"
    )

    scrollVideoPage()
    # Get scroll height
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while isVideoContinueTrue:
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

    getComments(commentsInView)


# save file in json
def save_json(filename, new_dict):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(new_dict, f, ensure_ascii=False, indent=4, default=str)
    except:
        print(f"Error saving {filename}.")


############################### SCRAPING  ###############################
# specify the path to chromedriver.exe
s = Service(os.getenv("CHROMEDRIVER_PATH"))


# open the webpage
driver = webdriver.Chrome(service=s)


start = time.time()
print("Beginning scraper now...")

vdict = {}

for c in channels:
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

    # scrape the videos in the channel
    fullChannel(channelURL)

    # scrape details of each video
    for video in channelVideos.index:
        url = channelVideos["URL"][video]
        fullVideo(url)

        videoDetails.loc[len(videoDetails) - 1, VID_URL] = url
        thumbnail = channelVideos["Thumbnail"][video]
        videoDetails.loc[len(videoDetails) - 1, VID_THUMBNAIL] = thumbnail

    # add records to dict
    jvideos = videoDetails.to_json(orient="records")
    parsedV = json.loads(jvideos)
    vdict[channelName] = parsedV

# export file in json
save_json("daily_youtube_data.json", vdict)

end = time.time()

print("Daily Youtube scraping completed.")
print("\n\n===========================================")
print("TOTAL TIME TAKEN: ", end - start)
print("===========================================\n\n")

driver.quit()

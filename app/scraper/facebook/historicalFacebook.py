import time
from datetime import datetime, timedelta
import pandas as pd
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

f = open('../accounts_to_scrape/facebook.json')
fbGroups = json.load(f)

#GROUP VARIABLES
isPostContinueTrue = True

POSTURL     = 'Source'
DATE        = 'Date Posted'
groupPosts = pd.DataFrame(columns=[POSTURL, DATE])

#POST VARIABLES
COLUMNONE   = 'Source'
COLUMNTWO = 'Date Posted'
COLUMNTHREE  = 'Description'
COLUMNFOUR  = 'Image' 
COLUMNFIVE   = 'Article Title'
COLUMNSIX = 'Reactions'
COLUMNSEVEN = 'Engagement'
COLUMNEIGHT = 'Comments'
postDetails = pd.DataFrame(columns=[COLUMNONE, COLUMNTWO, COLUMNTHREE, COLUMNFOUR, COLUMNFIVE, COLUMNSIX, COLUMNSEVEN, COLUMNEIGHT])

#DATE VARIABLES
enteredDate = "Jan 01 2018"
STOPDATE = datetime.strptime(enteredDate, '%b %d %Y')

############################### Methods ###############################
def scrollPage():
    # driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight)")
    driver.execute_script("window.scrollBy(0,300)")
    time.sleep(3)

#retrieve url for each post
def getURL(posts):
    global groupPosts
    
    for post in posts:
        if (checkDate(post) == 0):
            break
        
        anchorTag = post.find_element(By.XPATH,".//div[@class='buofh1pr']")
        #get date posted
        datePosted = anchorTag.find_element(By.XPATH,".//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']/span").text
        #get url of post
        urlTag = anchorTag.find_element(By.XPATH,".//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']")
        url = urlTag.get_attribute('href')
        
        row = {POSTURL : url, DATE : datePosted}
        groupPosts = groupPosts.append(row, ignore_index=True)

#scrape posts for each group
def fullGroup():
    global postCounter
    
    mainContainer = wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='rq0escxv l9j0dhe7 du4w35lb hpfvmrgz buofh1pr g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5 gile2uim qmfd67dx']")))
    
    scrollPage()
    postInView = mainContainer.find_elements(By.XPATH,"//div[@class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']")

    while isPostContinueTrue:
        bottomPost = postInView[len(postInView)-1]
        
        if (checkDate(bottomPost) == 1):
            # driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight)")
            driver.execute_script("window.scrollBy(0,700)")
            time.sleep(1) 
        # if (len(postInView) < postCounter):
        #     scrollPage()
        else:
            break
        postInView = mainContainer.find_elements(By.XPATH,"//div[@class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']")
        
    getURL(postInView)

#check post is within timeframe
def checkDate(post):
    result = 1
    
    try:
        anchorTag = post.find_element(By.XPATH,".//div[@class='buofh1pr']")
        datePosted = anchorTag.find_element(By.XPATH,".//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']/span").text
        # print(datePosted)
        today = datetime.now()
        ndate = datetime.now()
        
        #getting the type of date posted
        # i.e. ["Just now","9m","1h","2d","January 27 at 5:24 PM", "31 December 2021"]
        if (len(datePosted) == 2):
            if ('m' in datePosted):         #minutes ago
                ndate = today - (timedelta(minutes = int(datePosted[0])))
            elif ('h' in datePosted):       #hours ago
                ndate = today - (timedelta(hours = int(datePosted[0])))
            elif ('d' in datePosted):       #days ago  
                ndate = today - (timedelta(days = int(datePosted[0])))
        elif (len(datePosted) == 3):
            if ('m' in datePosted):         #minutes ago
                ndate = today - (timedelta(minutes = int(datePosted[:2])))
            elif ('h' in datePosted):       #hours ago
                ndate = today - (timedelta(hours = int(datePosted[:2])))
        elif ('Just' in datePosted or 'now' in datePosted):   #Just now
            ndate = today
        else:                               #More than a week ago
            splited = datePosted.split(' ')
            if (len(splited) == 3):           #not current year
                ndate = splited[1][:3] + " " + splited[0] + " " + splited[2]
                # print(ndate)
            else:                           #current year
                ndate = splited[0][:3] + " " + splited[1] + " " + str(datetime.today().year)
                # print(ndate)

        #checking if date posted falls within the timeframe
        # result = 1
        if STOPDATE > ndate:
            result = 0
        
        return result
    except:
        return result

#get description of post
def getDescrption(container):
    global postDetails

    description = container.find_element(By.XPATH,".//div[@class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q']/div").text

    postDetails.loc[len(postDetails)-1, COLUMNTHREE] = description

#get article image and title of post
def getArticleImageAndTitle(container):
    global postDetails

    imageContainer = container.find_element(By.XPATH,".//div[@class='pmk7jnqg kr520xx4']/img")
    image = imageContainer.get_attribute('src')
    postDetails.loc[len(postDetails)-1, COLUMNFOUR] = image

    title = container.find_element(By.XPATH,".//span[@class='a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ojkyduve']/span").text
    postDetails.loc[len(postDetails)-1, COLUMNFIVE] = title

#get number of reactions, shares and comments of post
def getEngagement(container):
    global postDetails

    try: 
        reaction = container.find_element(By.XPATH,".//span[@class='pcp91wgn']").text
        engagementContainer = container.find_elements(By.XPATH,".//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw m9osqain']")

        postDetails.loc[len(postDetails)-1, COLUMNSIX] = reaction

        engagement = ''
        for i in engagementContainer:
            engagement += i.text
            engagement += ' '
        postDetails.loc[len(postDetails)-1, COLUMNSEVEN] = engagement
    except: #no reactions in the post
        postDetails.loc[len(postDetails)-1, COLUMNSIX] = None
        postDetails.loc[len(postDetails)-1, COLUMNSEVEN] = None

#get comments of post
def getComments(container):
    global postDetails

    commentList = []
    try:
        commentsContainer = container.find_elements(By.XPATH,".//div[@class='cwj9ozl2 tvmbv18p']/ul/li")

        for comments in commentsContainer:  
            comment = comments.find_element(By.XPATH,".//div[@class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql']/div").text
            commentList.append(comment)
            
            # try: ##### comments under see more ##### ----> not working
            #     additionalComments = comments.find_elements(By.XPATH,".//div[@class='cxmm5t8 oygrvhab hcukyx3x c1et5uql o9v6fnle']/div")
            #     for addiComment in additionalComments:
            #         commentList.append(addiComment.text)
            # except:
            #     None
        postDetails.loc[len(postDetails)-1, COLUMNEIGHT] = commentList
    except:
        postDetails.loc[len(postDetails)-1, COLUMNEIGHT] = None

#get details of post
def fullPost(postURL):
    driver.get(postURL)
    time.sleep(2)

    try:
        mainContainer = wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='bp9cbjyn j83agx80 cbu4d94t d2edcug0']")))
        postContainer = mainContainer.find_element(By.XPATH,".//div[@class='j83agx80 l9j0dhe7 k4urcfbm']")

        getDescrption(postContainer)
        getArticleImageAndTitle(postContainer)
        getEngagement(postContainer)
        getComments(postContainer)

    except: ########### insert check for video ###########
        postDetails.loc[len(postDetails)-1, COLUMNTHREE] = None   
        postDetails.loc[len(postDetails)-1, COLUMNFIVE] = None
        postDetails.loc[len(postDetails)-1, COLUMNSIX] = None
        postDetails.loc[len(postDetails)-1, COLUMNSEVEN] = None 


############################### Scraping ###############################
#specify the path to chromedriver.exe
s = Service("C:\Program Files (x86)\chromedriver.exe")

#open the webpage
driver = webdriver.Chrome(service=s)
driver.get("http://www.facebook.com")
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[0])

#Wait for initialize, in seconds
wait = WebDriverWait(driver, 10)

#target username
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

#enter username and password
username.clear()
username.send_keys("thelisteningsquad483@gmail.com")
password.clear()
password.send_keys("smt483tls")

#find the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#wait to allow new page to load
time.sleep(1.25)

start = time.time()
print("Beginning scraper now...")

gdict = {}
pdict = {}

for group in fbGroups:
    #reset dataframes
    groupPosts = pd.DataFrame(columns=[POSTURL, DATE])
    postDetails = pd.DataFrame(columns=[COLUMNONE, COLUMNTWO, COLUMNTHREE, COLUMNFOUR, COLUMNFIVE, COLUMNSIX, COLUMNSEVEN, COLUMNEIGHT])

    groupName = group
    groupURL = fbGroups[group]

    driver.get("https://www.facebook.com/" + groupURL + "/")
    time.sleep(5)

    #scrape the posts in the group
    fullGroup()

    #add records to dict
    jgroup = groupPosts.to_json(orient="records")
    parsedG = json.loads(jgroup)
    gdict[groupName] = parsedG

    #scrape details of each post
    for post in groupPosts.index:
        url = groupPosts['Source'][post]
        postDetails.loc[len(postDetails), COLUMNONE] = url
        postDetails.loc[len(postDetails)-1, COLUMNTWO] = groupPosts['Date Posted'][post]
        fullPost(url)
    
    #add records to dict
    jposts = postDetails.to_json(orient="records")
    parsedP = json.loads(jposts)
    pdict[groupName] = parsedP

#save file in json
def save_json(filename, new_dict):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(new_dict, f, ensure_ascii=False, indent=4, default=str)
    except:
        print(f"Error saving {filename}.")

#export file in json
save_json("dailyFacebook1.json",gdict)
save_json("dailyFacebook2.json",pdict)

end = time.time()

print("Facebook scraping completed.")
print("\n\n===========================================")
print("TOTAL TIME TAKEN: ",end - start)
print("===========================================\n\n")

driver.quit()
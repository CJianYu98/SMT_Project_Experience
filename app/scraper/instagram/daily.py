# from bs4 import BeautifulSoup
from instascrape import Comment, Post, Profile, scrape_posts
from selenium.webdriver import Chrome

webdriver = Chrome("/Users/joshuawong/Documents/GitHub/SMT_Project_Experience/app/scraper/instagram/chromedriver")

SESSION_ID = "51262035845%3Ao9lFbVdjhAmJts%3A26" #"51262035845%3AwbHOYA6dOplLo2%3A1"

# listeningsquad
# SMT483tls!

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
    "cookie": f"sessionid={SESSION_ID};"
}

profile = Profile("a_tuanzebe38")
profile.scrape(headers=headers)

posts = profile.get_posts(webdriver=webdriver, login_first=True, login_pause=30)
scraped_posts, unscraped_posts = scrape_posts(posts, headers=headers, pause=10, silent=False)

scraped_posts.to_json("./app/scraper/twitter/test.json")
print("Profile scraped")



# profile = Profile("a_tuanzebe38")
# profile.scrape()
# recent_posts = profile.get_recent_posts()

# import pandas as pd

# posts_data = [post.to_dict() for post in recent_posts]
# posts_df = pd.DataFrame(posts_data)
# posts_df.to_json("./app/scraper/instagram/test.json")


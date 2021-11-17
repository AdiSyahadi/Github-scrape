## Github Scraper
![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
![Python](https://img.shields.io/badge/Python-14354C?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?&logo=streamlit&logoColor=white)
![Heroku](https://img.shields.io/badge/Heroku-430098?logo=heroku&logoColor=white)
![terminal](https://img.shields.io/badge/Windows%20Terminal-4D4D4D?&logo=Windows%20terminal&logoColor=white)
![vscode](https://img.shields.io/badge/Visual_Studio_Code-0078D4?&logo=visual%20studio%20code&logoColor=white)

- Github scraper app is used to scrape data for a specific user profile.
- Github scraper app gets a github profile name and check whether the given user name is exists or not.
- If the user name exists, app will scrape the data from that github profile.
- If the user name doesn't exists, app displays a info message.
- You can download the scraped data in `CSV`,`JSON` and `pandas profiling` HTML report formats.

### Installation :- 
To install all necessary requirement packages for the app 👇
```
pip install -r requirements.txt
```

### Packages Used :- 
```python
import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
```

### Function To Scrape the Data :- 
```python
def ScrapeData(user_name):
    url = "https://github.com/{}?tab=repositories".format(user_name)
    page = requests.get(url) 
    soup = BeautifulSoup(page.content, "html.parser")
    info = {"name": soup.find(class_="vcard-fullname").get_text()}
    info["image_url"] = soup.find(class_="avatar-user")["src"]
    info["followers"] = (
        soup.select_one("a[href*=followers]").get_text().strip().split("\n")[0]
    )
    info["following"] = (
        soup.select_one("a[href*=following]").get_text().strip().split("\n")[0]
    )

    try:
        info["location"] = soup.select_one("li[itemprop*=home]").get_text().strip()
    except:
        info["location"] = ""

    try:
        info["url"] = soup.select_one("li[itemprop*=url]").get_text().strip()
    except:
        info["url"] = ""

    repositories = soup.find_all(class_="source")
    repo_info = []
    for repo in repositories:
        try:
            name = repo.select_one("a[itemprop*=codeRepository]").get_text().strip()
            link = "https://github.com/{}/{}".format(user_name, name)
        except:
            name = ""
            link = ""
            
        try:
            updated = repo.find("relative-time").get_text()
        except:
            updated = ""

        try:
            language = repo.select_one("span[itemprop*=programmingLanguage]").get_text()
        except:
            language = ""

        try:
            description = repo.select_one("p[itemprop*=description]").get_text().strip()
        except:
            description = ""

        repo_info.append(
            {
                "name": name,
                "link": link,
                "updated ": updated,
                "language": language,
                "description": description,
            }
        )
    repo_info = pd.DataFrame(repo_info)
    return info, repo_info
```
### Demo GIF Image 👇:- 
![output_image](images/demo.gif)

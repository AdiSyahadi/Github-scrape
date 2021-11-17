import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(page_icon="⚡", page_title="Github Scraper")  # set page configuration


def ScrapeData(user_name):
    url = "https://github.com/{}?tab=repositories".format(
        user_name
    )  # accessing github profile
    page = requests.get(url)  # get request
    soup = BeautifulSoup(page.content, "html.parser")  # stores the html content
    info = {"name": soup.find(class_="vcard-fullname").get_text()}
    info["image_url"] = soup.find(class_="avatar-user")[
        "src"
    ]  # gets user profile image
    info["followers"] = (
        soup.select_one("a[href*=followers]").get_text().strip().split("\n")[0]
    )  # gets followers count
    info["following"] = (
        soup.select_one("a[href*=following]").get_text().strip().split("\n")[0]
    )  # gets following count

    # try to get location details if exists
    try:
        info["location"] = soup.select_one("li[itemprop*=home]").get_text().strip()
    except:
        info["location"] = ""

    # try to get url details if exists
    try:
        info["url"] = soup.select_one("li[itemprop*=url]").get_text().strip()
    except:
        info["url"] = ""

    # get all repositories as a pandas dataframe
    repositories = soup.find_all(class_="source")
    repo_info = []
    for repo in repositories:

        # repository name and link
        try:
            name = repo.select_one("a[itemprop*=codeRepository]").get_text().strip()
            link = "https://github.com/{}/{}".format(user_name, name)
        except:
            name = ""
            link = ""

        # repository last update time
        try:
            updated = repo.find("relative-time").get_text()
        except:
            updated = ""

        # repository programming language used
        try:
            language = repo.select_one("span[itemprop*=programmingLanguage]").get_text()
        except:
            language = ""

        # repository description
        try:
            description = repo.select_one("p[itemprop*=description]").get_text().strip()
        except:
            description = ""

        # append repository details as dict to the repo_info list
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


def main():
    st.title("Github Scraper")  # app title
    user_name = st.text_input("Enter Github Username")  # get github username from user

    # if the username is not empty
    if user_name:
        if user_name == "":
            st.info("Please, Enter a User Name...")
        else:
            try:
                info, repo_info = ScrapeData(
                    user_name
                )  # try to scrape the data for the specific user name
                pr = ProfileReport(repo_info, explorative=True)
                csv_expander = st.expander("CSV Preview")
                json_expander = st.expander("JSON Preview")
                report_expander = st.expander("Report Preview")
                for key, value in info.items():
                    if key != "image_url":
                        st.sidebar.subheader(
                            """
                            {} : {}
                            """.format(
                                key, value
                            )
                        )

                    else:
                        st.sidebar.image(value)
                        with csv_expander:
                            st.dataframe(repo_info)
                            st.download_button(
                                "Download",
                                data=repo_info.to_csv(),
                                file_name="githubdata.csv",
                            )

                        with json_expander:
                            st.json(repo_info.to_json())
                            st.download_button(
                                "Download",
                                data=repo_info.to_json(),
                                file_name="githubdata.json",
                            )

                        with report_expander:
                            st_profile_report(pr)
                            st.download_button(
                                "Download",
                                data=pr.to_html(),
                                file_name="githubreport.html",
                            )
            except:
                st.info(
                    "User doesn't exist"
                )  # displays if the username doesn't exists


if __name__ == "__main__":
    main()

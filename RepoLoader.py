import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests
from annotated_text import annotated_text
from PIL import Image
import base64

st.set_page_config(layout="wide", page_title="RepoLoader")

# Creating 3 columns
col1, col2, col3 = st.beta_columns([2, 8, 2])

# > COLUMN 1 - Empty
with col1:
    st.write("")

# > COLUMN 2
with col2:
    # RepoLoader  Logo
    image = Image.open("logo.png")
    st.image(image)

    # Username and Load Button
    USERNAME = st.text_input("Enter Github username", "")
    load_button = st.button("Load Repo 🔽")

    if load_button:

        # ! IF INPUT FIELD IS EMPTY SHOW ERROR
        if not USERNAME:
            st.markdown(
                "<h4 style='text-align: center; color:#FF4848;'>  Invalid username </h4>",
                unsafe_allow_html=True,
            )

        else:
            base_url = "https://github.com"
            url = f"https://github.com/{USERNAME}?tab=repositories"

            get_url = requests.get(url)

            # > IF success status 200 OK
            if get_url.status_code == 200:
                data = BeautifulSoup(get_url.text, "html.parser")

                # name of the Repo owner
                name_class = data.find_all(class_="p-name")
                for tag in name_class:
                    NAME = tag.text.strip()

                # total number of repo
                repo_class = data.find_all(class_="wb-break-all")
                TOTAL_REPO = len(repo_class)

                st.text("")

                annotated_text(
                    "Name of the owner : ",
                    (f"{NAME}", "", "#afa"),
                    (" ", " "),
                    "Total number of repos : ",
                    (f"{TOTAL_REPO}", "", "#afa"),
                )
                st.text("")

                date_list = []
                date = data.find_all("relative-time")
                for dates in date:
                    all_dates = dates.get_text()
                    date_list.append(all_dates)

                Repo = []
                url1 = []

                for _, i in enumerate(repo_class):
                    # To get link and add it with base url
                    for a in i.findAll("a"):
                        new_Url = base_url + a["href"]

                    project_name = i.text.strip("\nPublic")

                    Repo.append(project_name)
                    url1.append(new_Url)
                temp = list(zip(Repo, url1, date_list))

                # CREATING A DATAFRAME
                TABLE_REPO = pd.DataFrame(
                    temp, columns=["Project Name",
                                   "Project Link", "Last Updated"]
                )
                Final_data = st.dataframe(TABLE_REPO)

                # TO GET THE DATA AND MAKE IT AS A CSV FILE
                coded_data = base64.b64encode(
                    TABLE_REPO.to_csv(index=False).encode()
                ).decode()
                st.markdown(
                    f'<a href="data:file/csv;base64,{coded_data}" download="{USERNAME}.csv"> **Download {USERNAME} Data**</a> 📥 ',
                    unsafe_allow_html=True,
                )

            #! ELSE PRINT ERROR FOR STATUS CODE 404
            else:
                print(get_url.status_code)
                st.markdown(
                    "<h4 style='text-align: center; color:#FF4848;'>  Username Not exist  </h4>",
                    unsafe_allow_html=True,
                )
    # > This for ABOUT -> HOW TO USE SECTION.
    st.markdown(
        """
                   _________

                   # 📖 ABOUT
                   _________
                   
                   RepoLoader is for the developers who are constantly visiting Github which will make their work a little bit easy. It will save the developers 
                   time to visit GitHub and search the username of the particular repo and changing tabs and all this stuff so We have made the work simpler. 
                   Just search the username and you will get only what the user want.  Yeah, only Repos. 

                   ## 🔧 Features

                   - User can also download the repo dataset in CSV so that user can also use it for analysis, etc.
                   - NO need of opening GitHub and searching for the repos.
                   - Gives the name of the owner and the number of repositories is there in that.
                   - Shows only Repos name , with the last updated date and with the project links.
                   _________
                   # 💡 HOW TO USE
                   _________
                    
                   #### 1-> Enter the GitHub username and then click "Load Repo" button.
                    
                    ![](https://ik.imagekit.io/tfme5aczhhf/repoloader/tr:w-700/p1_TN37GSg7G.PNG?updatedAt=1633793484426)

                   #### 2-> This is what the user will get the output. 

                    ![](https://ik.imagekit.io/tfme5aczhhf/repoloader/tr:w-700/p2_Z4SMxmovL.PNG)

                    User can also download this data for further use.
                    ![](https://ik.imagekit.io/tfme5aczhhf/repoloader/tr:w-750/p3_ZgYGowiBx.PNG)

                    _________
                    ## Find me around the web 🌎:
                    
                    💻 [Portfolio](http://tancodes.atspace.cc/)
                    📌 [GitHub](https://github.com/TanCodes)
                    💼 [LinkedIN](https://www.linkedin.com/in/tanmay-barvi-2a0206126/)
                    🎬 [YouTube](https://www.youtube.com/channel/UC370GTtJnvWs8wDH9UXoBzQ?view_as=subscriber)
                    ❤️ [Instagram](https://instagram.com/_tancodes_)
                    🐦 [Twitter](https://twitter.com/_tancodes_)
                    _________
                
                    ###  HAPPY CODING WITH PYTHON 
                    ![](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen)
                    ![](https://forthebadge.com/images/badges/built-with-love.svg)
                    ![forthebadge](https://forthebadge.com/images/badges/open-source.svg)
                    ![](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
                    ![forthebadge](https://forthebadge.com/images/badges/check-it-out.svg)
                    _________
        """
    )

# > COLUMN 3 - Empty
with col3:
    st.write("")


# > Removing footer and main menu from default streamlit
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

import os
import time
import logging
import requests
import bs4
from selenium import webdriver
import logging
import json
import pprint

RootUrl = "https://steamcommunity.com/id/_hbs_/inventory/"
User_Agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                            " AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/91.0.4472.124 Safari/537.36"}
OutPutData = {}
Links = []
FinalData = {}
FFinal = []

def getHttpResponse(url, UserAgent=None):
    """Get base HTTP response"""
    if UserAgent != None:
        request = requests.get(url, headers=UserAgent)
        return request
    else:
        request = requests.get(url)
        return request
def getLinks(html_page):
    soup = bs4.BeautifulSoup(html_page, "html.parser")
    for x in soup.findAll("div", {"class": "games_list_tabs"}):
        for t in x.find_all("a", href=True):
            Links.append(t["href"])
        return Links
def getNames(URL, html_page):
    Titles = []
    Items = []
    Browser = webdriver.Chrome()
    Browser.get(URL)
    for t in Browser.find_elements_by_class_name("games_list_tab_name"):
        Titles.append(t.text)

    for h in Browser.find_elements_by_class_name("games_list_tab_number"):
        Items.append(h.text)

    for item in range(len(Titles)):
        OutPutData.update(
            {f"Game Title #{item}": Titles[item]}
        )
    for item in range(len(Items)):
        OutPutData.update(
            {f"Game Item #{item}": Items[item]}
        )

    return OutPutData
def getFileIntoJSON(data):
    with open("HBS_DATA.json", "w") as jsonFile:
        json.dump(data, jsonFile, indent=3)
        jsonFile.close()



def main(*args, **kwargs):
    BaseHttpResponse = getHttpResponse(RootUrl, User_Agent)
    if BaseHttpResponse.status_code == 200:
        Links = getLinks(BaseHttpResponse.text)
        OutPutData = getNames(RootUrl, BaseHttpResponse.text)
        if Links.__sizeof__() > 0 and OutPutData.__sizeof__() > 0:
            logging.info(f"{time.ctime()} SUCCESSFUL GETTING LINKS")
            for x in range(len(Links)):
                OutPutData.update({f"Game Link #{x}": Links[x]})

                FinalData = {
                    f"ID": str(x),
                    f"Game Link ": (str(RootUrl) + str(Links[x])),
                    f"Game Item ": OutPutData.get(f"Game Item #{x}"),
                    f"Game Title ": OutPutData.get(f"Game Title #{x}")
                }
                FFinal.append(FinalData)
            pprint.pprint(FFinal)
            getFileIntoJSON(FFinal)

            logging.info(f"{time.ctime()} SUCCESSFUL UPLOADING FILES")
        else:
            pass
    else:
        logging.error(f"{time.ctime()} ERROR CONNETION TO {RootUrl}")
if __name__ == '__main__':
    if os.path.isdir(os.getcwd() + "/Logs") == True:
        pass
    else:
        os.mkdir("Logs")
    logging.basicConfig(filename=f'Logs/steam_log_{time.time()}.log', filemode='w',
                        format='[%(name)s] - [%(levelname)s] - [%(message)s] <| ',
                        level=logging.INFO)
    StartProgram = time.time()
    main(RootUrl, User_Agent)
    EndProgram = time.time()
    TotalProgram = EndProgram - StartProgram
    logging.info(f"[{time.ctime()}] Total time of using program is : {TotalProgram}")
    quit()
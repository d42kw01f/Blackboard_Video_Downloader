from selenium import webdriver
import io
import time
import requests
import os
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

def gettingSourceCode():
    link = input('Enter the link here: ')

    # enter Chrome instead of Firefox here, if you are gonna use it.
    driver = webdriver.Firefox()

    driver.get(link)

    #this waits for the new page to load
    while(link == driver.current_url):
        time.sleep(15)

    # Writing the page source code into a file in the same directory.
    pageSource = driver.page_source
    with io.open('SP289021242.html', "w", encoding="utf-8") as f:
        f.write(pageSource)
    driver.quit()

def HTMLParsing():
    # getting the Video URL by parsing the created html file
    with open("SP289021242.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    FinalVidUrl = soup.find("video").get("src")

    print("\nVideo Dowloading URL :- \n{}".format(FinalVidUrl))
    return FinalVidUrl

def DownloadingVideos(url):
    # Downloading the video with chunk size of 256
    chunk_size = 256

    r=requests.get(url, stream=True)
    total_size_in_bytes= int(r.headers.get('content-length', 0))
    print('total',total_size_in_bytes)
    VidName = input('enter the name you want to use for the video: ')+".mp4"

    # Downloading the video
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    print("\n{} : downloading...".format(VidName))
    with open(VidName, 'wb') as f:
        for chunk in tqdm(r.iter_content(chunk_size=chunk_size)):
            progress_bar.update(len(chunk))
            f.write(chunk)
    progress_bar.close()

if __name__ == "__main__":
    gettingSourceCode()
    try:
        # TheUrl = HTMLParsing()
        TheUrl = 'https://ultra-au-prod-sms.collab.cloudflare.blackboardcdn.com/content/1015ec57-14d6-5c1f-9627-06223b1e3c1a/21/10/23/08/1015ec57-14d6-5c1f-9627-06223b1e3c1a_1_211023T082617868Z.mp4?X-Blackboard-Expiration=1636472155091&X-Blackboard-Signature=pW1khwYD%2BmHygAVpKD1ETgYC0JUpDw57Tua3VmXjcWc%3D&X-Blackboard-Client-Id=void&Expires=1636472155&Signature=TQwp7nQZfuMNCQEgfeoFm78~U3kK2gZOJYWtJ1O-D-gUrz5qDh4-GCZQEGTmbRNZGEdk~de1~xXKpl6Os0IwStyZXRp2kjbAh8nIH2Od4BKCc5NG5UidDZORAs8Y1iPSVEb2AS1Cn3C9ia118VchYxQFJ3yBKrhJNwmtM04vxVyjP5YbX83SMauFsqkYSTs3zNksLY9b1yZXUMm1K3n0jfmOOiS1uhTfWTko07xi4~FCoAdLGlu3cXhh0EY1gLWSAM7i9CVZqJJ1BJF1Vh1Pk98KUBuYPxK3daJtcQ02JC1mkUANt0YDRQysUGIGo3xQ8MdStPL8Ba2GbE5zK26iyQ__&Key-Pair-Id=APKAIOBDBIMXUOQOBYVA'
    except:
        print('SOMETHING WENT WRONG: I think you entered the url wrongly!!!')
        print('It should be like this: https://au.bbcollab.com/collab/ui/session/playback/load/...')
        print('Or the url has been expired.')
        exit()
    DownloadingVideos(TheUrl)
    os.remove("SP289021242.html")
    print("Download Finished!!!")

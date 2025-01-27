import requests as req
from bs4 import BeautifulSoup
import time 
import httpx
import asyncio

def FindUrls(url):
    print(f"processing : {url}")
    response = req.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    questions = soup.find_all(class_="bg-white rounded border border-solid border-gray-300 shadow-sm relative sm:rounded-none question__item")

    for question in questions:
        link_tag = question.find("a", class_="hover:text-blue-600 text-gray-900")
        if link_tag and link_tag.get("href"):
            url = link_tag["href"]
            full_url = f"https://www.bonyadvokala.com{url}" if url.startswith("/") else url
            with open ("urls.txt" , "a" , encoding="utf-8") as file :
                file.write(full_url+'\n')
#for first page 
FindUrls("https://www.bonyadvokala.com/%D9%85%D8%B4%D8%A7%D9%88%D8%B1%D9%87-%D8%AD%D9%82%D9%88%D9%82%DB%8C/international-law")

async def find_urls(client, url):
    print(f"Processing: {url}")
    try:
        response = await client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        questions = soup.find_all(class_="bg-white rounded border border-solid border-gray-300 shadow-sm relative sm:rounded-none question__item")

        urls = []
        for question in questions:
            link_tag = question.find("a", class_="hover:text-blue-600 text-gray-900")
            if link_tag and link_tag.get("href"):
                url = link_tag["href"]
                full_url = f"https://www.bonyadvokala.com{url}" if url.startswith("/") else url
                urls.append(full_url)

        return urls
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return []

#for other pages
async def main():
    base_url = "https://www.bonyadvokala.com/%D9%85%D8%B4%D8%A7%D9%88%D8%B1%D9%87-%D8%AD%D9%82%D9%88%D9%82%DB%8C/international-law?page="
    start_page =  2  #####################################################################
    end_page =  2  #####################################################################

    async with httpx.AsyncClient() as client:
        for n in range(start_page, end_page):
            new_url = f"{base_url}{n}"
            urls = await find_urls(client, new_url)
            with open("urls.txt", "a", encoding="utf-8") as file:
                file.writelines(url + '\n' for url in urls if urls)
            await asyncio.sleep(0.5)  

asyncio.run(main())

import aiohttp  
import asyncio  
from bs4 import BeautifulSoup  
import pandas as pd  
import math  

def calculate_legitimacy(score, votes, upvotes, weights):  
    W_S, W_V, W_U = weights  
    return (score * W_S) + (math.log10(votes + 1) * W_V) + (math.log10(upvotes + 1) * W_U)  

async def fetch_url(session, url):    
    try:  
        async with session.get(url, timeout=10) as response:   
            print(f"Fetching URL: {url}")   
            if response.status == 200:  
                return await response.text()  
            print(f"Failed to fetch URL {url}: HTTP {response.status}")  
            return None  
    except Exception as e:  
        print(f"Error fetching URL {url}: {e}")  
        return None  

def parse_html(html):    
    try:  
        soup = BeautifulSoup(html, "html.parser")  
        
        question_tag = soup.find(class_="body__summary p-0 m-0 mt-12 leading-loose text-gray-700 break-words")  
        question_summary = question_tag.text.strip() if question_tag else None  

        ai_response_tag = soup.find(class_="px-16 py-8 leading-loose bg-white rounded-lg shadow-sm")  
        if ai_response_tag:  
            return {  
                "question": question_summary,  
                "ai_response": ai_response_tag.text.strip(),  
                "responses": []  
            }  

        response_blocks = soup.find_all(class_="content__body p-0 m-0 leading-loose text-gray-700 break-words")  
        responses = []  
        for block in response_blocks:  
            try:  
                score_tag = block.find_next(class_="text-sm ltr inline-block font-bold text-gray-900")  
                score = float(score_tag.text.strip()) if score_tag else 0  

                votes_tag = block.find_next(class_="text-sm text-gray-6000")  
                votes = int(votes_tag.text.strip()) if votes_tag else 0  

                upvotes_tag = block.find_next(class_="inline-block text-gray-900 vote__count ltr")  
                upvotes = int(upvotes_tag.text.strip()) if upvotes_tag else 0  

                responses.append({  
                    "score": score,  
                    "votes": votes,  
                    "upvotes": upvotes,  
                    "response": block.text.strip()  
                })  
            except Exception as e:  
                print(f"Error parsing response block: {e}")  

        return {  
            "question": question_summary,  
            "ai_response": None,  
            "responses": responses  
        }  
    except Exception as e:  
        print(f"Error parsing HTML: {e}")  
        return None  

async def process_urls(urls, weights=(5, 2, 3), top_n=4):   
    results = []  
    semaphore = asyncio.Semaphore(100)   

    async with aiohttp.ClientSession() as session:  
        async def fetch_with_semaphore(url):  
            async with semaphore:  
                return await fetch_url(session, url)  

        tasks = [fetch_with_semaphore(url) for url in urls]  
        responses = await asyncio.gather(*tasks)  

        for url, html in zip(urls, responses):  
            if html:  
                data = parse_html(html)  
                if data:  
                    question = data["question"]  
                    ai_response = data["ai_response"]  
                    if ai_response:  
                        results.append({  
                            "URL": url,  
                            "Question": question,  
                            "AI Response": ai_response,  
                            "Rank": None,  
                            "Response": None,  
                            "Legitimacy Score": None  
                        })  
                    else:  
                        ranked = []  
                        for response in data["responses"]:  
                            legitimacy = calculate_legitimacy(response["score"], response["votes"], response["upvotes"], weights)  
                            ranked.append({  
                                "response": response["response"],  
                                "legitimacy": legitimacy  
                            })  
                        ranked = sorted(ranked, key=lambda x: x["legitimacy"], reverse=True)[:top_n]  
                        for idx, response in enumerate(ranked, 1):  
                            results.append({  
                                "URL": url,  
                                "Question": question,  
                                "AI Response": None,  
                                "Rank": idx,  
                                "Response": response["response"],  
                                "Legitimacy Score": response["legitimacy"]  
                            })  

    return results  

def main():  
    try:  
        df = pd.read_csv('urls1.txt', header=None, names=['URL'], dtype=str)  
        urls = df['URL'].tolist()  
        print(f"URLs to process: {urls}")   

        results = asyncio.run(process_urls(urls))  

        results_df = pd.DataFrame(results)  
        results_df.to_csv("lawyer_responses_ranked.csv", index=False, encoding="utf-8")  
        print("Processing complete. Results saved to 'lawyer_responses_ranked.csv'.")  
    except Exception as e:  
        print(f"An error occurred in main: {e}")  

if __name__ == "__main__":   
    main()
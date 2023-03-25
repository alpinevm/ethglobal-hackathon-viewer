import os
import aiohttp
import asyncio
import json
import re
import json

def extract_next_data(html, page: int):
    # Find the __NEXT_DATA__ script tag
    next_data_pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
    next_data_match = re.search(next_data_pattern, html, re.DOTALL)

    if next_data_match:
        next_data_json = next_data_match.group(1)
        next_data = json.loads(next_data_json)
        return next_data
    else:
        print("failed page", page)
        raise Exception("Could not find __NEXT_DATA__") 

# Example usage:
async def download_all_hackathons() -> list:
    """Downloads all hackathons from hackathon.com and saves them to a file"""
    start_page: int = 1
    end_page: int = 162
    base_url: str = "https://ethglobal.com/showcase/page/"
    async def fetch_page(page: int) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url + str(page)) as response:
                print(f"Fetching page {page}")
                return extract_next_data(await response.text(), page)["props"]["pageProps"]["projects"]
    # Gather and Flatten response
    return [item for sublist in await asyncio.gather(*[fetch_page(page) for page in range(start_page, end_page + 1)]) for item in sublist]
    
async def main():
    file_path = os.path.join(os.getcwd(), "hackathons.json")
    """
    hackathons: list = await download_all_hackathons()
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write(json.dumps(hackathons))
    """
    data = json.load(open(file_path))
    total = 2
    cur = 0
    for d in data:
        if total == cur:
            break
        if d['prizes'] != []:
            cur += 1
            print(json.dumps(d))

if __name__ == '__main__':
    asyncio.run(main())

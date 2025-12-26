import httpx
import os

#from dotenv import load_dotenv
#load_dotenv()

FANART_API_KEY = os.getenv('FANART_API_KEY')


async def get_fanart_movie(client: httpx.AsyncClient, id: str) -> dict:
    params = {
        "api_key": FANART_API_KEY
    }

    url = f"http://webservice.fanart.tv/v3/movies/{id}"
    response = await client.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
            return {"error": response.status_code}


async def get_fanart_series(client: httpx.AsyncClient, id: str) -> dict:
    params = {
        "api_key": FANART_API_KEY
    }

    url = f"http://webservice.fanart.tv/v3/tv/{id}"
    response = await client.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code}
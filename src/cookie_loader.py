import json
from apify import Actor


async def load_cookies(file_path='linkedin_cookies.json'):
    """
    Load cookies from a JSON file and return as a dictionary.
    """
    async with Actor:
        actor_input = await Actor.get_input() or {}

        # with open(file_path, 'r') as file:
        #     linkedin_cookies = json.load(file)

        cookies = actor_input.get('cookies')
        
        cookies = {cookie['name']: cookie['value'] for cookie in cookies}
        return cookies

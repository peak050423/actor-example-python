from apify import Actor
from datetime import datetime
import platform
import json
import csv
from .company_follower import getfollowers
from .post_likers import getLikersList

def get_current_timestamp():
    """
    Get current timestamp (cross-platform).
    """
    current_datetime = datetime.now()
    if platform.system() == "Windows":
        return current_datetime.strftime('%#m-%d-%Y_%#I-%M-%p')
    else:
        return current_datetime.strftime('%-m-%d-%Y_%-I-%M-%p')

async def main():
    async with Actor:
        # Get the value of the actor input
        actor_input = await Actor.get_input() or {}

        # Structure of input is defined in .actor/input_schema.json
        company_url = actor_input.get('company_url')
        follower_number = actor_input.get('follower_number')
        scraper_type = actor_input.get('scraper_type')

        if scraper_type:
            if scraper_type == 'Company Follower':
                if follower_number is None:
                    raise ValueError('followerNumber parameter is required')
                if company_url is None:
                    raise ValueError('companyUrl parameter is required')
            elif scraper_type == 'Post Like':
                if not actor_input.get('post_url'):
                    raise ValueError('postUrl parameter is required')                

        elif not scraper_type:
            raise ValueError('scraperType parameter is required')


        current_timestamp = get_current_timestamp()
        result = []
        filename = ""
        scraper_type = "1"

        if scraper_type == '1':  # Company Followers Scraper
    
            if not company_url or not follower_number:
                raise ValueError('Missing required parameters for company scraper')

            company_id = company_url.split('/')[4]
            followers_info = getfollowers(company_id, follower_number, current_timestamp)

            if not followers_info:
                raise ValueError('No data found')

            result = followers_info
            filename = f'followers_data_{current_timestamp}.csv'

        elif scraper_type == '2':  # Post Like Scraper
            post_url = input.get('postUrl')

            if not post_url:
                raise ValueError('Missing postUrl for post-like scraper')

            likers_info = getLikersList(post_url, current_timestamp)

            if not likers_info:
                raise ValueError('No data found')

            result = likers_info
            filename = f'likers_data_{current_timestamp}.csv'

        else:
            raise ValueError('Invalid scraper type')

            print(f'The result is: {result}')

        # Structure of output is defined in .actor/actor.json
        print(f'Pushing data to the dataset', result)
        print(f'Company_url: {company_url}')
        print(f'Follower number: {follower_number}')
        print(f'Scraper Type: {scraper_type}')

        if isinstance(result, str):
            result = json.loads(result)

        await Actor.push_data([
            {
                'company_url': company_url,
                'follower_number': follower_number,
                'result': json.loads(result),
            },
        ])

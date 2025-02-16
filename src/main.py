from apify import Actor


async def main():
    async with Actor:
        # Get the value of the actor input
        actor_input = await Actor.get_input() or {}

        # Structure of input is defined in .actor/input_schema.json
        company_url = actor_input.get('company_url')
        follower_number = actor_input.get('follower_number')

        print(f'First number: {company_url}')
        print(f'Second number: {follower_number}')

        result = f"{company_url} {follower_number}"

        print(f'The result is: {result}')

        # Structure of output is defined in .actor/actor.json
        await Actor.push_data([
            {
                'company_url': company_url,
                'second_number': follower_number,
                'sum': result,
            },
        ])

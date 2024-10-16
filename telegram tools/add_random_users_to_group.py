import json
import random
import string
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest

# Your API ID, API Hash, and Bot Token
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

# Initialize the Telegram client
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Function to generate random usernames
def generate_random_username(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Generate a list of 100 random usernames
usernames = [generate_random_username() for _ in range(100)]

# Save the usernames to a JSON file
with open('usernames.json', 'w') as file:
    json.dump(usernames, file)

# Function to add a user to a group
async def add_user_to_group(group_username, user_username):
    try:
        # Get the group and user entities
        group = await client.get_entity(group_username)
        user = await client.get_entity(user_username)
        
        # Add the user to the group
        await client(InviteToChannelRequest(group, [user]))
        print(f"Added {user_username} to {group_username}")
    except Exception as e:
        print(f"Failed to add {user_username} to {group_username}: {str(e)}")

# Main function
async def main():
    group_username = 'your_group_username'  # The group's username

    # Add random users to the group
    for _ in range(5):  # Change this number to add more users
        random_user = random.choice(usernames)
        await add_user_to_group(group_username, random_user)

if __name__ == '__main__':
    client.start()
    client.loop.run_until_complete(main())

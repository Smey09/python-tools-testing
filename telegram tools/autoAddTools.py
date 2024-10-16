from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
import random

# Your API ID, API Hash, and Bot Token
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

# Initialize the Telegram client
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# List of usernames to add to the group
usernames = ['username1', 'username2', 'username3', 'username4']  # Replace with actual usernames

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

    # Get a random user from the list
    random_user = random.choice(usernames)

    # Add the random user to the group
    await add_user_to_group(group_username, random_user)

if __name__ == '__main__':
    client.start()
    client.loop.run_until_complete(main())

# SporeBot - Mushroom Discord Bot

SporeBot is a Discord bot designed to fetch the wiki pages of a variety of different mushrooms, allowing the users to discover and learn about a variety of different species.

## Features

- **Random Mushroom Information**: Get information about random mushrooms
- **Specific Mushroom Lookup**: Search for information about particular mushrooms from $list
- **Visual Content**: Displays images from Wikipedia
- **Wiki Links**: Provides Wikipedia links for deeper reading
- **Comprehensive Database**: Covers 100+ mushroom species including:

## Commands

- `$mushroom` - Get a random mushroom fact
- `$mushroom [name]` - Look up a specific mushroom (e.g., `$mushroom shiitake`)
- `$list` or `$mushrooms` - See the first 20 available mushrooms

## Installation

### Prerequisites

- Python 3.7+
- Discord Bot Token

### Dependencies

Install the required Python packages:

```bash
pip install discord.py requests beautifulsoup4
```

### Setup

1. Clone this repository:
```bash
git clone https://github.com/Vvorx/SporeBot.git
cd SporeBot
```

2. Create a Discord application and bot:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to the "Bot" section and create a bot
   - Copy the bot token

3. Replace the bot token in `bot.py`:
```python
# Replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token
bot.run('YOUR_BOT_TOKEN_HERE')
```

4. Invite the bot to your server:
   - In the Discord Developer Portal, go to OAuth2 > URL Generator
   - Select "bot" scope and necessary permissions
   - Use the generated URL to invite the bot

## How It Works

### Web Scraping
SporeBot uses BeautifulSoup to scrape Wikipedia pages for mushroom information:
- Extracts text from article paragraphs
- Retrieves images and content
- Provides direct links to Wikipedia articles

### Database
The `mushrooms.py` file contains a mapping of common mushroom names to their corresponding Wikipedia pages.

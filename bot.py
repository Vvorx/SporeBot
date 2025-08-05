import discord
import requests
import random
import re
from bs4 import BeautifulSoup
from mushrooms import MUSHROOM_MAPPINGS

# Bot config
WIKI_URL = 'https://en.wikipedia.org/wiki/'
TIMEOUT = 10
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
EMBED_COLOR = 0x8B4513
# max text you want to display before cutting it off
MIN_TEXT = 50
MAX_TEXT = 1000

def get_image(soup):
    image_url = None
    
    # check infobox first
    infobox = soup.find('table', {'class': 'infobox'})
    if infobox:
        img = infobox.find('img')
        if img and img.get('src'):
            src = img['src']
            image_url = 'https:' + src if src.startswith('//') else src
    
    # fallback to content images
    if not image_url:
        content = soup.find('div', {'id': 'mw-content-text'})
        if content:
            images = content.find_all('img')
            skip = ['commons-logo', 'edit-icon', 'wikimedia']
            
            for img in images:
                if img.get('src'):
                    src = img['src']
                    if not any(s in src.lower() for s in skip):
                        image_url = 'https:' + src if src.startswith('//') else src
                        break
    
    return image_url

def get_text(soup):
    content = soup.find('div', {'id': 'mw-content-text'})
    if not content:
        return []
    
    paragraphs = content.find_all('p')
    good_text = []
    
    for p in paragraphs[:5]:
        text = p.get_text().strip()
        
        if MIN_TEXT < len(text) < MAX_TEXT:
            # clean it up
            text = re.sub(r'\[.*?\]', '', text)  # remove [1] references
            text = re.sub(r'\s+', ' ', text)     # fix spacing
            good_text.append(text.strip())
    
    return good_text

def find_page(name):
    name = name.strip().lower()
    
    for key, value in MUSHROOM_MAPPINGS.items():
        if key in name or name in key:
            return value
    
    # just try the name directly
    return name.replace(' ', '_').title()

def get_random():
    name = random.choice(list(MUSHROOM_MAPPINGS.keys()))
    fact, img, url = get_mushroom_info(name)
    return name, fact, img, url

def get_mushroom_info(name):
    try:
        page = find_page(name)
        url = WIKI_URL + page
        
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        
        if response.status_code == 404:
            return f"Couldn't find a page for '{name}'. Try something else!", None, None
        
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        img = get_image(soup)
        facts = get_text(soup)
        
        if facts:
            return facts[0], img, url
        else:
            return f"Found the page but no good info. Maybe try another mushroom?", img, url
            
    except Exception:
        return f"Something went wrong looking up {name}.", None, None

def make_embed(title, text, img=None, link=None):
    embed = discord.Embed(
        title=title,
        description=text,
        color=EMBED_COLOR
    )
    
    if img:
        embed.set_image(url=img)
    
    if link:
        embed.add_field(
            name="Read More",
            value=f"[Wikipedia]({link})",
            inline=False
        )
    
    return embed

def make_list():
    mushrooms = list(MUSHROOM_MAPPINGS.keys())[:20]
    text = (
        f"**{len(MUSHROOM_MAPPINGS)} mushrooms total!**\n\n" + 
        ", ".join([m.title() for m in mushrooms]) + 
        f"\n\n*Use `$mushroom [name]` to learn about any of these!*"
    )
    
    return make_embed("Available Mushrooms (First 20)", text)

class MushroomBot(discord.Client):
    
    async def on_ready(self):
        print(f'{self.user} is ready!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        await self.handle_command(message)
    
    async def handle_command(self, message):
        content = message.content.lower()
        
        if content.startswith(('$list')):
            await self.show_list(message)
        elif content.startswith(('$mushroom')):
            await self.show_mushroom(message)
    
    async def show_list(self, message):
        embed = make_list()
        await message.channel.send(embed=embed)
    
    async def show_mushroom(self, message):
        name = self.get_name(message.content)
        
        if name:
            await self.send_specific(message, name)
        else:
            await self.send_random(message)
    
    def get_name(self, content):
        if ' ' in content:
            parts = content.split(' ', 1)
            if len(parts) > 1:
                return parts[1].strip()
        return None
    
    async def send_specific(self, message, name):
        fact, img, url = get_mushroom_info(name)
        title = f"{name.title()}"
        embed = make_embed(title, fact, img, url)
        await message.channel.send(embed=embed)
    
    async def send_random(self, message):
        name, fact, img, url = get_random()
        title = f"{name.title()}"
        embed = make_embed(title, fact, img, url)
        
        await message.channel.send(embed=embed)
        await message.channel.send("💡 *Try `$mushroom shiitake` or `$list` to see more!*")

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = MushroomBot(intents=intents)
    bot.run('YOUR_BOT_TOKEN_HERE')

if __name__ == "__main__":
    main()
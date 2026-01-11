"""
Notice: This program uses the Telegram API and is part of the Telegram ecosystem.
Downloads all media files from a Telegram channel safely with PARALLEL DOWNLOADS.

# What this program Downloads:

- Videos
- Images
- Audio files
- Documents (PDFs, ZIPs, etc.)
- Any file attachments that Telegram considers "media"

# What it Does NOT Download:

- Plain text messages (message content is ignored)
- URLs/links in messages
- Stickers or GIFs (these might work, but aren't explicitly handled)
- Voice messages (should download as they're media files)

"""

import os
import re
import asyncio
from telethon import TelegramClient
from telethon.errors import RPCError
from telethon.tl.functions.messages import ImportChatInviteRequest

# =========================
# USER CONFIGURATION
# =========================
DOWNLOAD_FOLDER = r"C:\Telegram download"
CHANNEL = "https://telegram.me/channel-url" # <-- PUT TELEGRAM CHANNEL LINK
LIMIT = 5  # Number of files you want to download at once
API_ID = 0 # <-- PUT YOUR API/DATABASE/PAGE ID
API_HASH = ""  # <-- PUT YOUR API HASH HERE
SESSION_NAME = "mySession"

# PARALLEL DOWNLOAD SETTINGS
MAX_PARALLEL = 5  # Download 5 files at once (adjust based on your connection)

# =========================
# HELPERS
# =========================
def safe_filename(name: str, max_length: int = 200) -> str:
    """Make filename Windows-safe and length-safe."""
    name = re.sub(r'[\\/:*?"<>|]', '-', name)
    name = name.replace("\n", " ").strip()
    return name[:max_length]

# =========================
# ASYNC DOWNLOAD FUNCTION
# =========================
async def download_file(client, msg, filepath, filename, semaphore, stats):
    """Download a single file with semaphore control."""
    async with semaphore:  # Limit concurrent downloads
        try:
            print(f"⬇️  Downloading: {filename}")
            path = await client.download_media(msg, file=filepath)
            
            if path:
                stats['downloaded'] += 1
                print(f"✅ Saved: {filename}")
            else:
                stats['failed'].append(filename)
                print(f"⚠️  Download returned None for: {filename}")
                
        except RPCError as e:
            stats['failed'].append(filename)
            print(f"❌ Telegram error on {filename}: {e}")
        except Exception as e:
            stats['failed'].append(filename)
            print(f"❌ Error downloading {filename}: {e}")

# =========================
# MAIN PROGRAM
# =========================
async def main():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    
    print("✅ Client started")
    
    # Verify authentication
    try:
        me = await client.get_me()
        print(f"📱 Logged in as: {me.first_name}")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return
    
    # Try to access the channel
    try:
        # If it's an invite link, try to join
        if not CHANNEL.startswith('@'):
            try:
                hash_part = CHANNEL.split('+')[-1] if '+' in CHANNEL else CHANNEL
                await client(ImportChatInviteRequest(hash_part))
                print("✅ Joined channel via invite link")
            except Exception as join_error:
                print(f"ℹ️ Join attempt result: {join_error}")
        
        # Get channel entity
        entity = await client.get_entity(CHANNEL)
        print(f"📢 Accessing: {getattr(entity, 'title', 'Channel')}")
    except Exception as e:
        print(f"❌ Cannot access channel: {e}")
        print("\n💡 Tips:")
        print("  - For public channels: use '@channelname'")
        print("  - For private channels: use the invite hash")
        print("  - Make sure you have access to this channel")
        await client.disconnect()
        return
    
    print(f"📥 Scanning messages (downloading {MAX_PARALLEL} files at once)...\n")
    
    # Statistics
    stats = {
        'downloaded': 0,
        'failed': []
    }
    message_count = 0
    media_count = 0
    skipped = 0
    
    # Semaphore to limit concurrent downloads
    semaphore = asyncio.Semaphore(MAX_PARALLEL)
    
    # Collect download tasks
    download_tasks = []
    
    async for msg in client.iter_messages(CHANNEL, limit=LIMIT):
        message_count += 1
        
        if not msg.media:
            continue
        
        media_count += 1
        
        # Build filename
        date_prefix = msg.date.strftime("%Y-%m-%d")
        
        if msg.file and msg.file.name:
            filename = f"{date_prefix}_{msg.file.name}"
        else:
            ext = msg.file.ext if msg.file else ".bin"
            filename = f"{date_prefix}_media_{msg.id}{ext}"
        
        filename = safe_filename(filename)
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        
        # Skip if file already exists
        if os.path.exists(filepath):
            skipped += 1
            print(f"⏭️  Skipping: {filename}")
            continue
        
        # Add download task to list
        task = download_file(client, msg, filepath, filename, semaphore, stats)
        download_tasks.append(task)
    
    # Execute all downloads in parallel
    if download_tasks:
        print(f"\n🚀 Starting parallel download of {len(download_tasks)} files...\n")
        await asyncio.gather(*download_tasks)
    
    # Summary
    print("\n" + "="*40)
    print("SUMMARY")
    print("="*40)
    print(f"📊 Total messages scanned: {message_count}")
    print(f"🎬 Messages with media: {media_count}")
    print(f"✅ Downloaded: {stats['downloaded']}")
    print(f"⏭️  Skipped (already exist): {skipped}")
    print(f"❌ Failed: {len(stats['failed'])}")
    
    if stats['failed']:
        print("\n❌ Files that failed:")
        for f in stats['failed']:
            print(f"   - {f}")
    
    if media_count == 0:
        print("\n⚠️  No media found in the scanned messages.")
        print("💡 Try increasing LIMIT or check if the channel has media files.")
    
    print("\n🏁 Finished")
    
    await client.disconnect()

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    asyncio.run(main())
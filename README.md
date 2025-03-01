# OriChan Discord Bot

## Introduction

Welcome to OriChan, a fun and engaging Discord bot that brings AI-powered conversations to your server! OriChan lets you interact with a variety of unique "personas," each with their own distinct personality and role.  Engage in conversations, explore different personalities, and even collect and unlock new personas through our in-bot economy system!

## Features

* **AI-Powered Personas:** Converse with diverse AI personas, each offering a unique conversational experience.
* **Thread and Channel Conversations:** Start dedicated threads for longer conversations or chat directly in channels.
* **In-Bot Economy (OriCoins):** Earn OriCoins by being active in the server, claiming daily rewards, and participating in events.
* **Persona Collection and Gacha System:**
    * Open Persona Boxes to win rewards, including new personas.
    * Collect Persona Shards to unlock specific personas.
    * Explore different Persona Collections.
* **Daily Rewards:** Claim daily OriCoin rewards to keep your conversations flowing.
* **User Balance and Leaderboard:** Check your OriCoin balance and see who's at the top of the OriCoin leaderboard.
* **Character Limit Unlock:** Use Character Limit Unlock Cards for longer, more detailed messages in conversations.
* **Help Command:**  Get in-depth information on all of OriChan's commands and features.
* **Donation Support:** Help support the ongoing development of OriChan and unlock special perks!

## Getting Started

Using OriChan is easy! Here's how to get started:
- **Create Necessary Files First:** Create a Data folder in the same directory as OriChanRun.py with two files: APIKeys.txt (Your Google Gemini API Key) and BotToken.txt (Your Discord Bot Token)
- **You can change which AI model you want to use, but on default it's Google Gemini 2.0 Flash Exp**

1. **Invite OriChan to your server:** (Invite link would be placed here if this was a distributable bot)
2. **Start a conversation:**
    * **In a channel:** Mention OriChan in a message (e.g., `@OriChan Hello!`) or reply to OriChan's message to start a conversation.
    * **Start a thread:** Use the command `ori!startthread` (or `ori!st`) to create a new thread dedicated to a persona conversation. You can optionally specify a persona number after the command to choose a specific persona, or OriChan will use your currently selected persona.
3. **Interact with Personas:** Simply type your messages in the channel or thread, and OriChan will respond as the selected persona.
4. **Manage your Persona:**
    * Use `/changepersona` to change your active persona. You can browse through your unlocked personas or search for a specific one by name.
    * Use `ori!personaInventory` (or `ori!pi`, `ori!pinv`) to see a list of all personas you have unlocked.
5. **Economy Commands:**
    * Use `/balance` (or `ori!balance`) to check your OriCoin balance and other user information.
    * Use `ori!daily` (or `ori!d`) to claim your daily OriCoin reward.
    * Use `ori!baltop` (or `ori!leaderboard`, `ori!bt`) to view the top 10 OriCoin leaderboard.
6. **Gacha and Collection:**
    * Use `ori!showCollection` (or `ori!sc`, `ori!collection`, `ori!collections`, `ori!c`) to browse through available Persona Collections.
    * Use `ori!openBox` (or `ori!openbox`, `ori!pb`, `ori!personabox`, `ori!op`) to open Persona Boxes and win rewards.
    * Use `ori!unlockShards` (or `ori!shard`, `ori!Shard`) to use Persona Shards to unlock new personas.
    * Use `ori!toggleCL` (or `ori!clu`, `ori!unlockcl`, `ori!char`) to toggle Character Limit Unlock Cards for longer messages in conversations.
7. **Get Help:** Use `/help` (or `ori!help`) to display a detailed help menu with all commands and explanations.

## Commands

Here's a quick overview of OriChan's commands:

| Command                                  | Aliases                                | Description                                                                 |
|------------------------------------------|----------------------------------------|-----------------------------------------------------------------------------|
| `/help`                                 | `NONE`                             | Shows the help menu with command information.                               |
| `/balance`                               | `NONE`                          | Displays your OriCoin balance and user information.                          |
| `/baltop`                             | `NONE`           | Shows the top 10 users with the highest OriCoin balances.                   |
| `/daily`                              | `NONE`                                | Claims your daily OriCoin reward.                                          |
| `/donate`                             | `NONE`                                       | Provides information on how to donate and support OriChan.                  |
| `ori!give <@user> <amount>`               | `ori!transfer`, `ori!t`, `ori!g`     | Transfers OriCoins to another user.                                      |
| `/changepersona [Persona Name]`          |                                        | Changes your active persona. Persona name is optional for browsing.         |
| `ori!persona <persona name>`             | `ori!search`                           | Searches for a persona by name.                                            |
| `ori!personaInventory`                   | `ori!pi`, `ori!pinv`                   | Shows your unlocked persona inventory.                                      |
| `ori!startthread [persona number]`        | `ori!st`, `ori!St`                     | Starts a thread conversation with a persona. Number is optional.             |
| `ori!showCollection`                     | `ori!sc`, `ori!collection`, `ori!collections`, `ori!c` | Displays available Persona Collections.                                     |
| `ori!openBox`                            | `ori!openbox`, `ori!pb`, `ori!personabox`, `ori!op` | Opens a Persona Box to get rewards and personas.                           |
| `ori!unlockShards`                       | `ori!shard`, `ori!Shard`               | Uses Persona Shards to unlock random personas of a chosen rarity.           |
| `ori!toggleCL`                           | `ori!clu`, `ori!unlockcl`, `ori!char` | Toggles Character Limit Unlock Card usage for longer messages (if available). |

## Support and Donation

Need help or have questions? Feel free to ask in the server where OriChan is active!

If you enjoy using OriChan and want to support its development, you can donate! Use the `/donate` command or visit our Ko-fi page (https://ko-fi.com/orichan) for more information and perks for donating. Your support helps keep OriChan running and improving!

Thank you for using OriChan! We hope you enjoy your AI conversations!
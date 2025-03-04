# Slack PDF Assistant Bot

A Slack bot that answers questions about a user manual PDF document using Google's Gemini AI model.

## Overview

This Slack bot:
- Integrates with Slack using Socket Mode
- Uses Google Gemini to process and answer questions about a PDF document
- Caches PDF content to reduce token usage and improve response time
- Responds directly in Slack threads

## Prerequisites

- Python 3.8+
- Pipenv
- A Slack workspace where you can create bots
- Google Gemini API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/slack-pdf-assistant.git
cd slack-pdf-assistant
```

2. Create a virtual environment and install dependencies:
```bash
pipenv install
```

3. Create a `.env` file in the project root with your credentials:
```
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
GEMINI_API_KEY=your-gemini-api-key
```

4. Optional: Replace the user manual pdf

## Slack App Configuration

1. Create a new Slack app at [api.slack.com/apps](https://api.slack.com/apps)
2. Under "Socket Mode", enable Socket Mode
3. Under "OAuth & Permissions", add the following bot token scopes:
   - `app_mentions:read`
   - `chat:write`
   - `files:read`
   - `im:history`
   - `im:read`
   - `im:write`
   - `channels:history`
   - `channels:read`
4. Install the app to your workspace
5. Copy the Bot Token (`xoxb-...`) and App Token (`xapp-...`) to your `.env` file

## Running the Bot

Start the bot with:

```bash
python main.py
```

## Usage

1. Open an assistant thread to chat with the bot
2. Ask questions about the content in your PDF document
3. The bot will respond with information about the user manual

## Troubleshooting

- Ensure all tokens in the `.env` file are correct
- Verify the PDF file
- Check for error messages in the console
- Make sure your Gemini API key has sufficient quota


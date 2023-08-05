# EmoBot - Your Friendly AI Chatbot

![EmoBot Logo](link-to-your-logo.png)

EmoBot is a user-friendly AI chatbot built to assist you with various tasks and provide helpful information. Whether you need help with research questions, image requests, translations, or managing your Facebook page, EmoBot has got you covered!

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [How to Use EmoBot](#how-to-use-emobot)
  - [Chat Commands](#chat-commands)
  - [Facebook Messenger Integration](#facebook-messenger-integration)
- [System Capabilities](#system-capabilities)
- [Benefits](#benefits)
- [Contributing](#contributing)
- [License](#license)

## Introduction

EmoBot is an AI-powered chatbot developed using Python and integrated with OpenAI's GPT and DALL-E models. It is designed to be a friendly and helpful companion for individuals and businesses alike. With EmoBot, you can ask questions, request images, translate text, manage your Facebook page, and even schedule automated posts - all through a simple and intuitive interface.

Celery is a powerful asynchronous task queue system used in this system to handle background tasks, such as scheduling automated posts, analyzing user interactions, and triggering AI models for advanced responses. It ensures efficient processing of time-consuming tasks, enhances system performance, and enables EmoBot to deliver seamless and responsive user experiences on Facebook Messenger. In this system its used to schedule the automatic posting after every 5 hours.

## Features

- General research question handling
- Image handling with DALL-E text-to-image generation
- Language translation with GPT-based translation
- Image prompt generation for DALL-E image generation
- Automated post scheduling for your Facebook page
- Comment replies and reaction management on Facebook
- User interaction analysis to determine popular topics
- Responsive and colorful frontend

## Getting Started

### Prerequisites

Before using EmoBot, ensure you have the following:

1. Python 3.7 or higher installed
2. Facebook Messenger account (for Messenger integration)
3. OpenAI API key for GPT and DALL-E access
3. Celery schedular

### Installation

1. Clone the EmoBot repository:

```
git clone https://github.com/Levi-Chinecherem/emo-bot.git
cd emo-bot
```

2. Install the required Python packages:

```
pip install -r requirements.txt
```

### Configuration

1. Add your OpenAI API key to the configuration file: `config.py`
2. Configure your Facebook Messenger settings in `settings.py`

## How to Use EmoBot

### Chat Commands

To interact with EmoBot, simply send messages on your preferred platform (Facebook Messenger, etc.) using the following commands:

- `gp: your research question` - For general research questions
- `img: describe image request` - For image requests
- `translate to language: your text` - For language translation
- `img prompt: your description and purpose` - For image prompt generation

### Facebook Messenger Integration

EmoBot can be integrated with your Facebook Messenger page, allowing you to interact with the bot directly from your Messenger account. The bot can manage your page, automatically reply to comments, and schedule posts on your behalf.

## System Capabilities

EmoBot is capable of handling a wide range of tasks, including:

- Answering general research questions
- Generating images based on user descriptions
- Translating text to different languages
- Providing image prompts for DALL-E image generation
- Automating posts and managing comments on your Facebook page

## Benefits

EmoBot offers several benefits to individuals, companies, and startups:

- Save time by automating repetitive tasks on your Facebook page
- Improve engagement with automated post scheduling and comment replies
- Access intelligent AI capabilities for research and language translation
- Enhance creativity with DALL-E text-to-image generation

## Contributing

We welcome contributions from the community to make EmoBot even better. If you have ideas, bug fixes, or new features to propose, feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: EmoBot is an open-source project developed with love by the Levi Chinecherem C. If you have any questions or need assistance, feel free to reach out to us on GitHub or through the Facebook Messenger bot. We hope you enjoy using EmoBot and find it helpful in your daily tasks! 😄
Here’s an updated version of the README to reflect the functionality and use of GitHub Actions for scheduling:

---

# Twitter Bot

This repository contains a Python script that retrieves data from the [RAWG API](https://rawg.io/apidocs) and the [News API](https://newsapi.org/) to compose and post tweets. The script is designed to be run at scheduled intervals using **GitHub Actions**.

## Features

- Retrieves game-related data from the RAWG API.
- Fetches news articles from the News API.
- Composes and posts tweets with the fetched data.
- Scheduled execution using GitHub Actions.

## Prerequisites

Before using this bot, ensure you have the following:

- **API Keys**:
  - RAWG API Key.
  - News API Key.
  - Twitter Developer API keys (API key, API secret, Access token, and Access token secret).
- A **GitHub account** with access to create and manage repositories.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/dantealegria1/Twitter-Bot.git
cd Twitter-Bot
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory and add the following:

```env
RAWG_API_KEY=your_rawg_api_key
NEWS_API_KEY=your_news_api_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
```

### 3. Add `.env` to `.gitignore`

Ensure your `.env` file is ignored by Git to keep your credentials secure. The repository already includes `.env` in the `.gitignore`.

### 4. Install Dependencies

Use `pip` to install the required packages:

```bash
pip install -r requirements.txt
```

## How It Works

1. **Data Retrieval**:
   - The script fetches data from the RAWG API and News API.
   - It processes the data to create meaningful tweets about trending games or news.

2. **Tweet Posting**:
   - The script uses the Twitter API to post tweets composed from the fetched data.

3. **Scheduling with GitHub Actions**:
   - The bot is configured to run at regular intervals using a GitHub Actions workflow (`.github/workflows/twitter-bot.yml`).
   - The workflow triggers the Python script to execute on a predefined schedule.

## Usage

### Run Locally

You can run the script locally for testing:

```bash
python bot.py
```

### Automate with GitHub Actions

1. **Secrets Configuration**:
   - Add the required API keys as [GitHub Actions secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) in your repository:
     - `RAWG_API_KEY`
     - `NEWS_API_KEY`
     - `TWITTER_API_KEY`
     - `TWITTER_API_SECRET`
     - `TWITTER_ACCESS_TOKEN`
     - `TWITTER_ACCESS_TOKEN_SECRET`

2. **Workflow File**:
   - The `.github/workflows/twitter-bot.yml` file defines the schedule for running the script.

3. **Enable GitHub Actions**:
   - Ensure GitHub Actions is enabled for your repository.
   - The workflow will automatically execute based on the schedule defined in the YAML file.

## Contributing

Contributions are welcome! If you have ideas to enhance the bot, feel free to fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Let me know if you want me to help craft or refine specific sections, such as the GitHub Actions workflow file!

 

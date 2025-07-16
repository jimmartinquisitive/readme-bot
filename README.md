# readme-bot

[
![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
](https://www.python.org/downloads/)
[
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
](https://opensource.org/licenses/MIT)
[
![Build and Deploy](https://github.com/Azure/actions-workflow-samples/actions/workflows/main_readmebot.yml/badge.svg)
](https://github.com/Azure/actions-workflow-samples/actions/workflows/main_readmebot.yml)

An AI-powered tool that automatically generates comprehensive `README.md` files for your GitHub repositories by analyzing their source code.

## Description

**Readme-bot** is a Python application designed to streamline the documentation process for developers. It leverages the power of Google's Gemini Pro generative AI to read and understand the source code of a repository. Based on this analysis, it generates a well-structured and detailed `README.md` file, complete with a project description, features, setup instructions, and usage examples.

The primary goal is to eliminate the manual effort required to create and maintain documentation, ensuring that your projects are always presentable and easy for others to understand. The bot can be run in several modes: as a web service triggered by an API call, as an interactive CLI for specific repositories, or as a fully automated script that processes all your repositories.

## Features

-   **AI-Powered Content Generation:** Utilizes the Google Gemini API to analyze code and generate high-quality, context-aware documentation.
-   **Full GitHub Integration:** Authenticates with the GitHub API to fetch repository contents and seamlessly commit the generated `README.md` file.
-   **Smart Update Logic:** Automatically detects if a repository lacks a `README.md` or has recent code changes, and only generates/updates documentation when necessary.
-   **Intelligent Code Analysis:** Filters out irrelevant files (e.g., `.md`, `.gitignore`, images) and directories (e.g., `node_modules`, `__pycache__`) to provide the AI with only the most relevant source code.
-   **Multiple Execution Modes:**
    -   **Web Service:** Runs as a Flask application, exposing an API endpoint to trigger the documentation process.
    -   **Interactive CLI:** Provides a command-line interface to manually select a repository for README generation.
    -   **Automated Script:** A standalone script that iterates through and updates all of your repositories in one go.
-   **Deployment Ready:** Includes a pre-configured GitHub Actions workflow for continuous deployment to Azure Web Apps.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

-   Python 3.10+ (developed with 3.13)
-   `pip` for package management
-   A **Google Gemini API Key**. You can get one from [Google AI Studio](https://ai.google.dev/).
-   A **GitHub Personal Access Token (PAT)** with `repo` scope. You can create one [here](https://github.com/settings/tokens).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/readme-bot.git
    cd readme-bot
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a file named `.env` in the root of the project and add your API keys.

    ```dotenv
    # .env
    GEMINI_API_KEY="your_gemini_api_key_here"
    GITHUB_TOKEN="your_github_personal_access_token_here"
    ```

## Usage

Readme-bot can be run in three different modes depending on your needs.

### 1. Web Service (Primary Mode)

This mode runs a Flask web server, which is ideal for deployment and integration with webhooks. The documentation job is triggered by making a POST request to the `/trigger` endpoint.

```bash
# Start the Flask server
python main.py
```

The server will start on `http://0.0.0.0:5001`. To start the documentation job, send a POST request:

```bash
curl -X POST http://localhost:5001/trigger
```

This will start the process in a background thread, immediately returning a confirmation response.

### 2. Interactive CLI

This mode is perfect for generating a README for a single, specific repository. It will prompt you to choose from a list of your repositories and ask for confirmation before committing the file.

```bash
# Run the interactive script
python variations/manual_main.py
```

### 3. Fully Automated Script

This script runs the documentation process for all your repositories from top to bottom without any interaction. It's useful for batch updates or scheduled jobs.

```bash
# Run the automated script
python variations/automated_main.py
```

## File Structure

Here is a brief overview of the key files in the project:

```
.
├── .github/workflows/
│   └── main_readmebot.yml  # GitHub Actions workflow for CI/CD to Azure
├── variations/
│   ├── automated_main.py   # Script for fully automated batch processing
│   └── manual_main.py      # Script for the interactive CLI mode
├── ai_generator.py         # Handles interaction with the Google Gemini API
├── github_client.py        # Manages all GitHub API communication
├── main.py                 # The main Flask application entry point
├── requirements.txt        # Project dependencies
└── README.md               # This file
```
# Neutrino: AkashNet AI Deployment Suite

Welcome to Neutrino, an AI-powered deployment suite for the Akash Network. This application automates the process of deploying web applications on the Akash Network using Docker and SDL files generated by OpenAI's GPT-3.5-turbo model.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [License](#license)

## Introduction
Neutrino simplifies the deployment of web applications on the Akash Network by automating the generation of Dockerfiles and SDL files, building and pushing Docker images, and managing the deployment process.

## Features
### Clone GitHub Repositories
- **Description:** Allows users to clone repositories from GitHub.
- **Details:** Users need to provide the GitHub repository URL. The application will clone the repository to the local machine.

### Generate Dockerfiles using OpenAI
- **Description:** Automatically generates Dockerfiles using OpenAI's API.
- **Details:** Users need to provide configuration details for the Docker image. The application will use OpenAI to generate a Dockerfile based on the provided details.

### Build and Push Docker Images
- **Description:** Builds Docker images from the generated Dockerfiles and pushes them to Docker Hub.
- **Details:** Users need to provide their Docker Hub credentials. The application will build the Docker image and push it to the specified Docker Hub repository.

### Generate SDL Files for Akash Network
- **Description:** Generates SDL files required for deploying applications on the Akash Network.
- **Details:** Users need to provide configuration details for the SDL file. The application will generate an SDL file based on the provided details.

### Deploy Applications to Akash Network
- **Description:** Deploys applications to the Akash Network using the generated SDL files.
- **Details:** Users need to provide their Akash Network credentials and configuration details. The application will deploy the application to the Akash Network.

### Display Interesting Facts about Akash Network
- **Description:** Displays interesting facts and information about the Akash Network.
- **Details:** The application will fetch and display interesting facts about the Akash Network to keep users informed and engaged.

## Prerequisites
- Python 3.7+
- Docker
- Streamlit
- OpenAI API Key
- Akash Network account and credentials

## Installation
1. Clone the repository
2. Install the required Python packages: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file:
    - `OPENAI_API_KEY`: Your OpenAI API key.
    - `DOCKER_USERNAME`: Your Docker Hub username.
    - `DOCKER_PASSWORD`: Your Docker Hub password.
    - `AKASH_KEY_NAME`: Your Akash key name.
    - `AKASH_CHAIN_ID`: The chain ID for Akash.
    - `AKASH_NODE`: The Akash node URL.
    - `AKASH_FROM`: The Akash account name.
    - `AKASH_ACCOUNT_ADDRESS`: Your Akash account address.

## Usage
1. Run Docker in background
2. Run the Streamlit application: `streamlit run main.py`
3. Follow the steps in the web interface:
    - **Step 1:** Enter the GitHub repository URL.
    - **Step 2:** Enter Docker image configuration details.
    - **Step 3:** Enter SDL configuration details.
    - Click "Deploy" to start the deployment process (The AI will handle the dockerfile and SDL file generation)

Participating in [Akash Network Hackathon](https://dorahacks.io/hackathon/akashathon2/detail).
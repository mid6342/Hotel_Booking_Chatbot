# Hotel Booking Chatbot: Setup and Usage Guide

Welcome to the setup guide for the Hotel Booking Chatbot. Below you'll find detailed instructions to help you get started.

## Initial Installation
1. **Install Anaconda**: Download and install [Anaconda](https://www.anaconda.com/products/individual).
2. **Install Docker Desktop**: Get Docker Desktop from [Docker's official site](https://www.docker.com/products/docker-desktop).
3. **Ensure Python 3.7**: Verify that Python 3.7 is installed on your system.

## Setting Up Virtual Environment
1. **Create a New Virtual Environment in Anaconda**: 
   - Open Anaconda and set up a new virtual environment.
2. **Install Necessary Packages**: Within this environment, execute the following commands:
   - `pip install rasa` for RASA installation. [RASA Framework](https://rasa.com/docs/rasa/)
   - `pip install pandas` for Pandas installation. [Pandas Library](https://pandas.pydata.org/)

## Starting Docker for Entity Extraction
1. **Launch Docker Desktop**:
   - Open Docker Desktop on your machine.
2. **Run Docker Command**:
   - Open a standard terminal (e.g., Windows Command Prompt).
   - Execute `docker run -p 8000:8000 rasa/duckling` to start the Docker server for entity extraction.

## Running the Chatbot
1. **Prepare Your Environment**:
   - Open two terminal windows in Anaconda.
   - Ensure both terminals are active in the virtual environment.
2. **Navigate to Chatbot's Folder**:
   - Use `cd` command to navigate to your chatbot's directory.
3. **Start the Services**:
   - In the first terminal, initiate the actions server with `rasa run actions`.
   - In the second terminal, launch the chatbot interface using `rasa shell`.



---

This setup guide will assist you in installing and running your Hotel Booking Chatbot effectively. For more information on RASA and Pandas, please visit their official documentation.

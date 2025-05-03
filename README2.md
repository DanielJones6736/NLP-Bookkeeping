# NLP Bookkeeping Project
CS 6320 - Natural Language Processing   Spring 2025
Members: Luoqi Zhao, Daniel Jones, and Ryan Vera 

This project is a Natural Language Processing (NLP) application designed to interact with a simple database using natural language prompts. The project leverages the Gemini framework to process user inputs and execute database operations. 

## Project Overview

- **User Interface**: A graphical user interface (GUI) allows users to input prompts in natural language.
- **Backend**: The backend is implemented using Python's FastAPI framework, which processes the user input and interacts with the database.
- **Database**: A simple CSV file is used to simulate a database. This choice was made to keep the project focused on NLP and avoid the complexity of implementing a full-fledged database.

## Key Features

1. **Natural Language Interaction**: Users can interact with the system using natural language prompts.
2. **Function Calls via Gemini**: The Gemini framework is used to interpret user prompts and call appropriate functions to manipulate the database.
3. **CSV-based Database**: The database operations (e.g., read, write, update) are performed on a CSV file. Pandas library is used during runtimes

## How It Works

1. The user enters a prompt in the GUI.
2. The prompt is sent to the backend FastAPI server.
3. The backend uses Gemini to interpret the prompt and determine the required database operation.
4. The operation is performed on the CSV file, and the result is returned to the user.

## Limitations

- The project uses a CSV file as the database, which is not suitable for large-scale or complex applications.
- The focus is on NLP and function calling, so advanced database features (e.g., indexing, transactions) are not implemented.

## Prerequisites

- Python 3.8 or higher
- FastAPI
- Google Gemini framework
- A CSV file to act as the database

## Setup Instructions

1. Clone the repository.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
4. Open the GUI and start interacting with the system.

**Note**: The code and repository for the frontend GUI are hosted in a separate GitHub repository. You can find the website deployment [here](https://chat-wallet-next.operameiying.workers.dev).

## Future Work

- Replace the CSV file with a real database for better scalability.
- Enhance the NLP capabilities to handle more complex queries.
- Improve the GUI for a better user experience.

## Acknowledgments

This project was developed as part of the CS6320 - NLP course in Spring 2025.

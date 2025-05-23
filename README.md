# NLP Bookkeeping Project

CS 6320 - Natural Language Processing Spring 2025  
Members: Luoqi Zhao, Daniel Jones, and Ryan Vera

[YouTube Video Link](https://youtu.be/-VRr78dHZ_o)

This project is a Natural Language Processing (NLP) application designed to interact with a simple database using natural language prompts. The project leverages the Gemini framework to process user inputs and execute database operations.

## Project Overview

- **User Interface**: A graphical user interface (GUI) allows users to input prompts in natural language.
- **Backend**: The backend is implemented using Python's FastAPI framework, which processes the user input, interacts with the database, and calls the Google Gemini API.
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
3. Run the FastAPI server using the following configuration in `.vscode/launch.json` for debugging in the VSCode editor.
   ```
   {
       "name": "Python Debugger: FastAPI",
       "type": "debugpy",
       "request": "launch",
       "module": "uvicorn",
       "args": [
           "src.main:app",
           "--reload"
       ],
       "jinja": true
   }
   ```
4. Open the GUI using the `/docs` route and start interacting with the system. This route will open a SwaggerUI-like interface to conveniently interact with the API

<br/>
**Note**: The code and repository for the frontend GUI are hosted in a separate GitHub repository. 

You can find the website deployment [here](https://chat-wallet-next.operameiying.workers.dev).   
The link to the GitHub repository can be found [here](https://github.com/PigBehindTheCar/chat-wallet-next).

## API Documentation

The FastAPI backend provides the following routes for interacting with the system:

### Root Endpoint

- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns a simple welcome message to verify the server is running.
- **Response**:
  ```json
  {
  	"message": "Hello World..."
  }
  ```

### Health Check

- **URL**: `/health`
- **Method**: `GET`
- **Description**: Checks the health status of the server.
- **Response**:
  ```json
  {
  	"status": "ok"
  }
  ```

### Generate AI Response

- **URL**: `/genai/{prompt}`
- **Method**: `GET`
- **Description**: Processes a natural language prompt using the Google Gemini API and performs the appropriate database operation.
- **Parameters**:
  - `prompt` (string): The user input to be processed.
  - `max_output_tokens` (integer, optional): The maximum number of tokens for the AI response. Default is 512.
- **Response**:
  - On success:
    ```json
    {
      "status": "success",
      "result": { ... }
    }
    ```
  - On error:
    ```json
    {
    	"detail": "Invalid function call"
    }
    ```

### Get Transactions

- **URL**: `/transactions`
- **Method**: `GET`
- **Description**: Retrieves a list of transactions with optional filtering.
- **Parameters**:
  - `year` (integer, optional): Filter by year.
  - `month` (integer, optional): Filter by month (1-12).
  - `limit` (integer, optional): Maximum number of transactions to return.
  - `offset` (integer, optional): Number of transactions to skip.
- **Response**:
  ```json
  {
    "success": true,
    "data": [...],
    "message": "Transactions retrieved successfully",
    "timestamp": "2025-01-01T00:00:00"
  }
  ```

### Add Transaction

- **URL**: `/transactions`
- **Method**: `POST`
- **Description**: Adds a new transaction to the database.
- **Request Body**:
  ```json
  {
  	"date": "MM.DD.YYYY",
  	"day": "Mon",
  	"category": "Category",
  	"note": "Description",
  	"amount": 100.0
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": {...},
    "message": "Transaction added successfully",
    "timestamp": "2025-01-01T00:00:00"
  }
  ```

### Update Transaction

- **URL**: `/transactions/{id}`
- **Method**: `PUT`
- **Description**: Updates an existing transaction by ID.
- **Parameters**:
  - `id` (integer): Transaction ID.
- **Request Body**:
  ```json
  {
  	"date": "MM.DD.YYYY",
  	"day": "Mon",
  	"category": "Category",
  	"note": "Description",
  	"amount": 100.0
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": {...},
    "message": "Transaction updated successfully",
    "timestamp": "2025-01-01T00:00:00"
  }
  ```

### Delete Transaction

- **URL**: `/transactions/{id}`
- **Method**: `DELETE`
- **Description**: Deletes a transaction by ID.
- **Parameters**:
  - `id` (integer): Transaction ID.
- **Response**:
  ```json
  {
  	"success": true,
  	"message": "Transaction deleted successfully",
  	"timestamp": "2025-01-01T00:00:00"
  }
  ```

## Folder Structure

The project is organized as follows:

```
NLP-Bookkeeping/
│
├── src/
│   ├── main.py               # Entry point for the FastAPI backend
│   ├── database_tools.py     # Module for handling CSV-based database operations
│   └── config.py             # Configuration settings for Gemini API
│
├── data/
│   └── database.csv     # CSV file simulating the database
│
├── .vscode/
│   └── launch.json      # Debugging configuration for VSCode
│
├── requirements.txt     # List of required Python packages
├── .gitignore           # List of files that aren't included in the repository
├── LICENSE              # Contains licensing information
└── README.md            # Project documentation
```

## Future Work

- Replace the CSV file with a real database for better scalability.
- Enhance the NLP capabilities to handle more complex queries.
- Improve the GUI for a better user experience.

## Acknowledgments

This project was developed as part of the CS6320 - NLP course in Spring 2025 at the University of Texas as Dallas

# OpenAI Hotel Reviews Chatbot with Viber Integration

- This project serves as a Proof of Concept (PoC) demonstrating the integration of OpenAI's embedding API with hotel reviews data.
- The goal is to create a chatbot capable of responding to user queries based on the provided hotel reviews dataset.
- The embedding vectors generated from the reviews are stored in a local ChromaDB database for efficient querying.

## Features

- Utilizes OpenAI's embedding API to generate vectors for hotel reviews data.
- Implements a chatbot capable of responding to user queries based on the embedded data.
- Integrates with the Viber messaging app to provide a user-friendly interface for interacting with the chatbot.
- Implements a FastAPI backend server to set up a webhook with the Viber API, enabling seamless communication between the Viber app and the chatbot.
- Employs a separation of concerns structure with distinct files for configuration, chatbot logic, Viber bot setup, and the main application.

## Usage

1. Ensure the necessary environment variables are set up, including API keys for OpenAI and Viber.

2. Run the `main.py` file to start the FastAPI backend server.

3. Set up the Viber bot to communicate with the FastAPI server by configuring the webhook URL.

4. Interact with the chatbot via the Viber messaging app by sending text messages. The chatbot will respond based on the provided hotel reviews data.

## Project Structure

- **config.py**: Contains configuration settings, including API keys and file paths.
- **chatbot.py**: Implements the chatbot logic for initializing, handling messages, and generating responses.
- **viber_bot.py**: Sets up the Viber bot and handles incoming messages from the Viber app.
- **main.py**: Acts as the entry point to run the FastAPI backend server.

## Notes

- This project is a PoC and can be extended with additional features and enhancements for specific use cases.
- For advanced configurations or integrations, refer to the official documentation of the libraries used in this project.

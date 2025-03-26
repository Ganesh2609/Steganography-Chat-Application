# Chat Application with Image Steganography

This project is a real-time chat application built using Python's socket programming. It supports text and image-based messaging with an added feature of steganography, allowing users to hide messages within images. The application uses a client-server architecture and a MySQL database for storing messages.

---

## Features

- **Real-time Chat**: Users can send and receive text messages.
- **Image Steganography**: Messages can be hidden inside images before sending.
- **User Management**: Supports multiple clients with alias-based identification.
- **Message Storage**: Uses MySQL to store chat history.
- **GUI Interface**: Built with PyQt5 for an interactive user experience.
- **Client-Server Model**: Server handles multiple client connections.

---

## Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- MySQL Server
- Required Python libraries (see below)

### Install Dependencies

Using `pipenv`:

```sh
pip install pipenv
pipenv install
```

Or manually install dependencies:

```sh
pip install PyQt5 mysql-connector-python numpy opencv-python
```

---

## Database Setup

1. Open MySQL and create a user with necessary privileges.
2. The application will automatically create the required database (`chat`) and tables on first run.
3. To manually reset the database, run:

```sh
python Destroy.py
```

---

## Running the Application

### Start the Server

Run the server to handle client connections:

```sh
python server.py
```

### Start a Client

Run the client to connect to the server:

```sh
python main.py
```

Each client must enter their alias when prompted.

---

## File Descriptions

### `server.py`
- Initializes and manages client connections.
- Receives messages and forwards them to the appropriate recipient.
- Stores messages in the MySQL database.

### `main.py`
- Acts as the client-side GUI application using PyQt5.
- Handles sending and receiving messages.
- Uses `steno.py` for steganography.

### `clientfinal.py`
- Defines the PyQt5 UI structure for the chat application.

### `steno.py`
- Implements image steganography.
- Provides functions to encode and decode hidden messages within images.

### `Database.py`
- Handles MySQL database operations.
- Creates databases, tables, and stores/retrieves messages.

### `Destroy.py`
- Drops the database to reset all chat history.

### `Pipfile` & `Pipfile.lock`
- Contains dependency management details for `pipenv`.

---

## How It Works

1. **Client-Server Communication**
   - Clients connect to the server using sockets.
   - Messages are sent as serialized Python objects using `pickle`.

2. **Message Sending**
   - Regular text messages are sent normally.
   - If the user sends an image, the message is embedded inside using steganography.

3. **Message Receiving**
   - The server forwards messages to the intended recipient.
   - If an image with hidden text is received, it is decoded and displayed.

4. **Database Storage**
   - Messages are stored in a MySQL table under each user’s alias.

---

## Future Enhancements
- **Encryption**: Implement end-to-end encryption.
- **Voice Messages**: Add support for sending audio messages.
- **Mobile App**: Extend functionality to Android/iOS.


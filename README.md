# CS3305_team11

## Team Members
- Daniel Cagney
- Conor Shipsey
- Evelyn O'Donovan Cronin
- Yachitra Sivakumar
- Jack Moloney

## Project Description

The project report for CS3305 Group 11 details the development of "K.L.A.A.S - Knowledge Lookup and Archive Access Service," a comprehensive application aimed at enhancing file management, optimization, and sharing. Utilizing a modular architecture, the system integrates a desktop client built with PyQt5, a Flask-powered web server for file sharing, and a WebUI client for external access, focusing on user-friendly design and cross-platform compatibility. 

Key features include a dynamic search bar, efficient file management tools, file optimization techniques, and secure sharing capabilities through RESTful APIs. The rationale behind choosing PyQt5 and Flask is emphasized, highlighting cross-platform support, rich UI widgets, strong documentation, and flexibility. The project addresses technical challenges such as file synchronization, search optimization, and filesystem scanning efficiency, applying innovative solutions like a filesystem cache and normalized path handling. 

## Getting Started

These instructions will guide you through the installation and basic setup of our application. Please follow the steps carefully to ensure a successful setup.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.9 or later
- pip (Python package manager)

### Installation

1. Clone the repository to your local machine:
2. Navigate to the cloned repository's directory:
3. Install the required packages using pip:
   ```
   pip install -r requirements.txt
   ```
### Running the Application

Our application consists of two main components that need to be started: a server and the main program entry point.

#### Starting the Server

1. Navigate to the server folder:
   ```
   cd server
   ```
2. Run the server:
   ```
    python server.py
    ```
3. The server should now be running on `http://localhost:5000`.
4. Leave the server running and open a new terminal window to start the main program.
5. If you wish to stop the server, press `Ctrl + C`.
6. If you wish to restart the server, repeat steps 2-3.
7. Leave the server running and open a new terminal window or tab for the next steps.

#### Running the Main Program

1. From the root directory of the project, navigate to the python directory:
    ```
   cd python
   ```
2. Run the main program:
   ```
   python main.py
   ```
3. The main program should now be running and you should see the application's main menu.
4. To stop the main program, press `Ctrl + C`.
5. If you wish to restart the main program, repeat steps 2-3.

---

Thank you for using our application! We hope you find it useful. 

# Project Setup

## Prerequisites

* Node.js and npm : 
  *     [https://nodejs.org/]

## Steps

1. **Install dependencies:**

        cd server
        npm install

This will install the required dependencies for the Flask application automatically.

2. **Start the development server:**

        npm run dev
    
3. **Run the Flask Application**

Run `run.py` in the server directory to start the Flask application.

### To Build for Production
Generate production-ready CSS:

    npm run build

This will generate a `output.css` file in the `server/static/styles` directory.

Deploy your Flask application as usual.
 
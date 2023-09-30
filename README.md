# Website Monitor

Monitors websites for changes, and sends an email notification when one is detected.

## Installation

```bash
  git clone https://github.com/DevinParentice/website-watcher.git
  cd website-watcher
```

## Run Locally

### Backend

Create a `.env` file to the /backend folder and format it as such (replace with your own):

```bash
EMAIL_PASSWORD=example password
RECIPIENT_EMAIL=test@example.com
SENDER_EMAIL=test@example.com
```

To start the backend server, run the below commands:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

To run the watcher, open a new terminal and run:

```bash
python watcher.py
```

### Frontend

To start the frontend, run the below commands:

```bash
cd frontend
yarn install
yarn dev
```

Production build coming later.

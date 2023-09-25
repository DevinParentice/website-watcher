# Website Monitor

Monitors websites for changes, and sends an email notification when one is detected.

## Installation

```bash
  git clone https://github.com/DevinParentice/website-watcher.git
  pip install -r requirements.txt
```

## Run Locally

Edit `config.json` by adding the site(s) you want to monitor:

```bash
  {
    "websites": [
      {
        "name": "pinkyup_tea", // Name to give this monitor for tracking purposes.
        "url": "https://www.example.com", // URL to monitor.
        "delay": 10000, // Delay before checking again, in seconds.
        "elements": [ // The elements on the page you wish to monitor.
          { // For example, this monitors <span class="product__price">Example</span>
             "tag": "span",
             "class": "product__price"
          }
        ] // Can add multiple nodes for monitoring.
      } // Can add multiple sites for monitoring.
   ]
}
```

Create a `.env` file to the root directory of the project and format it as such (replace with your own):

```bash
EMAIL_PASSWORD=example password
RECIPIENT_EMAIL=test@example.com
SENDER_EMAIL=test@example.com
```

Run the script:

```bash
python watcher.py
```

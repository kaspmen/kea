from flask import Flask, request, logging, render_template, url_for
import logging
from datetime import datetime
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename='clicks.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(message)s', 
    datefmt='%d-%m-%Y %H:%M:%S',
    filemode='a'
)

# File to keep track of the number of clicks
COUNT_FILE = 'click_count.txt'

def get_click_count():
    """Read the current click count from the file."""
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, 'r') as f:
            count = f.read()
            return int(count) if count.isdigit() else 0
    return 0

def update_click_count(count):
    """Update the click count in the file."""
    with open(COUNT_FILE, 'w') as f:
        f.write(str(count))

def extract_browser(user_agent):
    """Extract browser information from the User-Agent string."""
    if 'Chrome' in user_agent and 'Safari' in user_agent and 'Edg' not in user_agent:
        return 'Chrome'
    elif 'Firefox' in user_agent:
        return 'Firefox'
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        return 'Safari'
    elif 'Edg' in user_agent:  # Microsoft Edge
        return 'Edge'
    elif 'OPR' in user_agent or 'Opera' in user_agent:
        return 'Opera'
    else:
        return 'Other'

@app.route('/<employee_id>')
def track(employee_id):
    # Extract information from the request
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    browser = extract_browser(user_agent)
    referer = request.headers.get('Referer', 'No Referrer')
    full_url = request.url  # This gives the full URL including Serveo URL
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check if the request is for favicon.ico and ignore it
    if employee_id == 'favicon.ico':
        return '', 204  # Return no content for favicon requests

    # Read and update the click count
    click_count = get_click_count() + 1
    update_click_count(click_count)

    # Log click information with additional details, including employee ID
    log_message = (f'Employee: {employee_id} - IP: {user_ip} - Browser: {browser} - Referer: {referer} - '
                   f'Full URL: {full_url} - Timestamp: {timestamp} - Total Clicks: {click_count}')
    
    # Write the log to the file
    logging.info(log_message)
    
    # Also print the log to the terminal (stdout)
    print(f'Click detected: {log_message}.')

    # Render the HTML template
    return render_template('index.html', employee_id=employee_id, click_count=click_count, browser=browser)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

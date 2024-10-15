### Overview
A service that transmits IP detection/block logs from multiple devices (nodes) running fail2ban to a central device (receiver), records the logs in a database on the central device, and sends notifications via a Telegram bot.
### Node
- Device where fail2ban is running
- Sends fail2ban detection logs to the receiver
#### `.env` File Configuration
```
NODE_NAME=
RECEIVER_IP=
RECEIVER_USERNAME=
RECEIVER_PW=
RECEIVER_PATH=
RECEIVER_PORT=
```
- `NODE_NAME`: Name of the node
- `RECEIVER_IP`: IP address of the receiver
- `RECEIVER_USERNAME`: Username used to send log files to the receiver via scp
- `RECEIVER_PW`: Password used to send log files to the receiver via scp
- `RECEIVER_PATH`: Full path of the log file on the receiver when sending log files via scp
- `RECEIVER_PORT`: Port number used to send log files to the receiver via scp
#### Execution
1. Navigate to the project directory
2. Create the `.env` file
3. Execute the script using `sudo nohup ./script &` or similar
### Receiver
- Device that receives detection logs sent by nodes
- Currently, only one device is set up to receive logs
#### Database Table Configuration
- `node`: Name of the node
- `rule`: fail2ban filtering rule
    - If `notify_found` is true, a Telegram notification is sent for IPs detected by fail2ban
    - If `notify_ban` is true, a Telegram notification is sent for IPs banned by fail2ban
- `log`: fail2ban logs
- `detected_ip`: List of detected IPs
#### `.env` File Configuration
```
NODE_NAME=
RECEIVER_IP=
RECEIVER_USERNAME=
RECEIVER_PW=
RECEIVER_PATH=
RECEIVER_PORT=
```
- `TELEGRAM_BOT_TOKEN`: Token of the Telegram bot that sends detection logs
- `TELEGRAM_USER_ID`: ID of the user who will receive logs from the Telegram bot
- `DB_NAME`: Name of the database where logs will be stored
- `DB_USER`: User for accessing the database
- `DB_PASSWD`: Password for the database access user
- `DB_HOST`: Database host address
- `DB_PORT`: Database port
#### Execution
1. Navigate to the project directory
2. Create the `.env` file
3. Create a virtual environment with `python3 -m venv venv`
4. Install dependencies with `pip3 install -r requirements.txt`
5. Activate the virtual environment using `source venv/bin/activate`
6. Execute the script using `sudo nohup ./script &` or similar

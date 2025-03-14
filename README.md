# Outlook Out-of-Office Scheduler

This project automatically enables or disables Out-of-Office (OOF) messages in Microsoft Exchange/Outlook based on the day of the week.

## Features

- Automatically enables OOF on specified days of the week
- Automatically disables OOF on other days
- Runs in a Docker container
- Checks OOF status every hour
- Configurable via environment variables

## Setup

1. Clone this repository
2. Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

3. Edit the `.env` file with your credentials and settings:

```
# Credentials
OUTLOOK_USERNAME=your_username@example.com
OUTLOOK_PASSWORD=your_password

# Server configuration
OUTLOOK_SERVER=mail.example.com
OUTLOOK_EMAIL=your_email@example.com

# Days to enable OOF (0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday)
# Comma-separated list of days
OOF_DAYS=5,6
```

## Running with Docker

### Using Docker Compose (recommended)

```bash
docker-compose up -d
```

This will build the Docker image and start the container in the background.

### Using Docker directly

Build the Docker image:

```bash
docker build -t outlook-oof .
```

Run the container:

```bash
docker run -d --name outlook-oof --restart always --env-file .env outlook-oof
```

## Logs

You can check the logs to see if the OOF status is being updated correctly:

```bash
docker-compose logs -f
```

Or if using Docker directly:

```bash
docker logs -f outlook-oof
```

## Troubleshooting

- If you're having connection issues, make sure your Exchange server URL is correct
- Check that your username and password are correct
- Ensure that the email address is the primary SMTP address for the account
- Some Exchange servers may require additional configuration or have specific security policies 
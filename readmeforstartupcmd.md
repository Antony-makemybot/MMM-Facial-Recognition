# Raspberry Pi Startup Script Guide

This guide provides detailed instructions on creating a script that automatically runs a list of commands every time your Raspberry Pi starts up.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Method 1: Using `cron`](#method-1-using-cron)
  - [Step 1: Create a Shell Script](#step-1-create-a-shell-script)
  - [Step 2: Make the Script Executable](#step-2-make-the-script-executable)
  - [Step 3: Edit the Crontab](#step-3-edit-the-crontab)
- [Method 2: Using Systemd](#method-2-using-systemd)
  - [Step 1: Create a Shell Script](#step-1-create-a-shell-script-1)
  - [Step 2: Make the Script Executable](#step-2-make-the-script-executable-1)
  - [Step 3: Create a Systemd Service File](#step-3-create-a-systemd-service-file)
  - [Step 4: Enable the Service](#step-4-enable-the-service)
- [Testing Your Setup](#testing-your-setup)
- [Troubleshooting](#troubleshooting)
- [Conclusion](#conclusion)

## Prerequisites

- A Raspberry Pi running Raspbian or another compatible Linux distribution.
- Basic knowledge of using the terminal.

## Method 1: Using `cron`

### Step 1: Create a Shell Script

1. Open a terminal on your Raspberry Pi.
2. Create a new script:
   ```bash
   nano ~/startup_commands.sh
### Step 2 : chmod +x ~/startup_commands.sh
### Step 3: Edit the Crontab
Open the crontab file:

```bash
  Copy code
  crontab -e

### Add the following line at the end of the file:

```bash
@reboot /home/pi/startup_commands.sh

Save and exit the crontab editor (usually Ctrl + X, then Y, and then Enter).

### Method 2: Using Systemd
### Step 1: Create a Shell Script
(Refer to Method 1, Step 1)

### Step 2: Make the Script Executable
(Refer to Method 1, Step 2)

### Step 3: Create a Systemd Service File
Create a new service file:
```bash
sudo nano /etc/systemd/system/startup_commands.service

### Add the following content to the file:
```ini
[Unit]
Description=Run startup commands

[Service]
ExecStart=/home/pi/startup_commands.sh
Type=oneshot
RemainAfterExit=true

[Install]
WantedBy=multi-user.target

Save and exit the editor (usually Ctrl + X, then Y, and then Enter).

### Step 4: Enable the Service
Run the following command to enable your service:

```bash
sudo systemctl enable startup_commands.service

Testing Your Setup
Reboot your Raspberry Pi to test if the commands run as expected:

```bash
sudo reboot

After rebooting, check if the commands were executed successfully:

If using cron, you may need to check logs or outputs defined in your script.
If using systemd, check the service status:

```bash
sudo systemctl status startup_commands.service

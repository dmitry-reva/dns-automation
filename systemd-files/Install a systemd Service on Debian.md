# Install a systemd Service on Debian

This README shows how to install and manage a custom systemd service on Debian-based systems.

## 1. Create a service file

Create a unit file in `/etc/systemd/system/`.

```bash
sudo nano /etc/systemd/system/dns-automation.service
```

Example content:

```ini
[Unit]
Description=DNS Automation Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/dns-automation/app.py
WorkingDirectory=/opt/dns-automation
Restart=always
User=www-data
Group=www-data
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

[Install]
WantedBy=multi-user.target
```

## 2. Reload systemd

```bash
sudo systemctl daemon-reload
```

## 3. Enable the service

```bash
suda systemctl enable dns-automation.service
```

## 4. Start the service

```bash
suda systemctl start dns-automation.service
```

## 5. Check the status

```bash
suda systemctl status dns-automation.service
```

## 6. View logs

```bash
sudo journalctl -u dns-automation.service -f
```

## 7. Stop or restart the service

```bash
# Перечитать конфигурацию systemd
sudo systemctl daemon-reload

# Включить и запустить таймер (сервис включать не нужно — его запускает таймер)
sudo systemctl enable --now dns-automation.timer

# Проверить статус таймера
systemctl status dns-automation.timer

# Посмотреть расписание, когда следующий запуск
systemctl list-timers | grep dns-automation
```

## 8. Disable the service

```bash
suda systemctl disable dns-automation.service
suda systemctl stop dns-automation.service
```

## 9. Remove the service

```bash
sudo rm /etc/systemd/system/dns-automation.service
sudo systemctl daemon-reload
```

## Notes

-- Replace `dns-automation.service` with your service name.
- Make sure the executable path in `ExecStart` exists and is correct.
- If the service should run as root, remove the `User` and `Group` lines.

## Install and update dns-automation.timer

Create the timer unit at `/etc/systemd/system/dns-automation.timer`:

```init
[Unit]
Description=Run DNS Automation periodically

[Timer]
# Example: daily at 02:00
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Install and enable the timer:

```bash
sudo nano /etc/systemd/system/dns-automation.timer
sudo systemctl daemon-reload
sudo systemctl enable --now dns-automation.timer
sudo systemctl status dns-automation.timer
```

Update the timer (after editing the unit file):

```bash
# After editing /etc/systemd/system/dns-automation.timer
sudo systemctl daemon-reload
# Restart the timer so changes take effect
sudo systemctl restart dns-automation.timer
# Verify schedule and next run
systemctl list-timers | grep dns-automation
sudo systemctl status dns-automation.timer
```

Notes:
- Ensure `/etc/systemd/system/dns-automation.service` exists and the timer's service name matches it (dns-automation.service).
- Use `sudo journalctl -u dns-automation.service -f` to view service logs when the timer triggers the service.
- To disable the timer: `sudo systemctl disable --now dns-automation.timer`.

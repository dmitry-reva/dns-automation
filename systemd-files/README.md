# Установка и запуск сервиса DNS‑Automation 

(используйте файлы из текущей папки репозитория)

> Исправьте пользователя и пусть в файле ~/dns-automation/systemd-files/dns-automation.service

> Проверьте, что все пути корректны; если нужен запуск от root — удалите строки `User`

1. Скопируйте файлы в `/etc/systemd/system/`:
   ```bash
   cd ~/dns-automation/systemd-files
   sudo cp dns-automation.service dns-automation.timer /etc/systemd/system/
   ```
2. Перезагрузите systemd:
   ```bash
   sudo systemctl daemon-reload
   ```
3. Включите и запустите сервис:
   ```bash
   sudo systemctl enable --now dns-automation.service
   ```
4. Включите таймер (он будет запускать сервис по расписанию):
   ```bash
   sudo systemctl enable --now dns-automation.timer
   ```

Проверка и управление:
- Статус сервиса: `sudo systemctl status dns-automation.service`
- Статус таймера: `systemctl status dns-automation.timer`
- Расписание таймера: `systemctl list-timers | grep dns-automation`
- Логи сервиса: `sudo journalctl -u dns-automation.service -f`

При необходимости:
- Перезапуск сервиса: `sudo systemctl restart dns-automation.service`
- Остановка сервиса: `sudo systemctl stop dns-automation.service`
- Отключение таймера: `sudo systemctl disable --now dns-automation.timer`
- Удаление файлов: `sudo rm /etc/systemd/system/dns-automation.{service,timer}` + `sudo systemctl daemon-reload`


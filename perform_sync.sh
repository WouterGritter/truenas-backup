echo "Starting sync in 60 seconds."
/usr/bin/sleep 50
echo "Starting sync in 10 seconds."
/usr/bin/sleep 10

cd ~/truenas-backup/
/usr/bin/python3 discord_helper.py start-phase

LOG_FILE=logs/rsync-$(/usr/bin/date +%Y-%m-%d--%H-%M-%S).log
echo "Logging to file: $LOG_FILE"

/usr/bin/rsync -traP --delete --backup --backup-dir=/mnt/merged/truenas-sync-backup/ --exclude=plex/ root@10.43.70.121:/mnt/pool/ /mnt/merged/truenas-sync/ >> $LOG_FILE 2>&1

echo >> $LOG_FILE
df -h | grep 'Filesystem\|/mnt/merged' >> $LOG_FILE

/usr/bin/python3 discord_helper.py end-phase $LOG_FILE

echo "Shutting down in 60 seconds."
/usr/bin/sleep 50
echo "Shutting down in 10 seconds."
/usr/bin/sleep 10

/usr/sbin/shutdown now

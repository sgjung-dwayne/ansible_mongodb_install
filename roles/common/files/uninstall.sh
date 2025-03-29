
rm -rf /data/mongo* /log/mongo* /log/backup
rm -rf /tmp/mongo*.sock
rm -rf /etc/logrotate.d/mongo*
sed -i '/backup/d' /var/spool/cron/root
userdel -r mongo
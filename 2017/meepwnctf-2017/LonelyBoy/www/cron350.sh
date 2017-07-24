#!/bin/bash
while :
do
    sleep 1
    chattr +i /var/www/html/upload/*/index.php || echo 1
    php cron.php || break
done
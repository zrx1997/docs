#!/bin/bash
proc_num=`pgrep php-fpm | wc -l`
php_fpm_config_file=`grep 'pm.max_children' /usr/local/webserver/php/etc/php-fpm.conf | cut -d'=' -f2 | sed 's/ //g'`
if [ $proc_num -le $php_fpm_config_file ];
then
    echo 0
else
    echo 1
fi

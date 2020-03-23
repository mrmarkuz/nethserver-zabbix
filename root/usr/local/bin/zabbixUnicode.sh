#!/bin/bash
systemctl stop zabbix-server
sudo -i -u postgres pg_dump zabbix > /tmp/pre-encoding-fix-backup.sql
sudo -i -u postgres psql -c "alter database zabbix rename to zabbix_pre_encoding_fix_backup"
sudo -i -u postgres psql -c "create database zabbix with encoding 'UNICODE' template=template0"
sudo -i -u postgres PGCLIENTENCODING=SQL_ASCII psql zabbix -f /tmp/pre-encoding-fix-backup.sql
systemctl start zabbix-server

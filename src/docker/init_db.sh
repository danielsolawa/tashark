#!/bin/bash


docker exec -i tashark_db sh -c 'exec mysql -u tashark_user -p"XK_3-rRxeUZ5" tashark' < init.sql
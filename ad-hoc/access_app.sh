#! /bin/bash

path_log=/home/divirta-se/ad-hoc/app_access/app-requests-divirta-se-dev-uai-com-br.log
path_sql=/home/divirta-se/ad-hoc/app_access/app-requests-da.sql

gawk -v re='/(access)/([a-z_0-9]+)/([0-9]+)/([0-9]+)/eq.gif' '{match($0, re, gres); print gres[1],gres[2],gres[3],gres[4]}' $path_log |  \
sort -n |  \
uniq -c |  \
awk '{ if ($2 == "access") print "UPDATE envportal.conteudo SET acesso=acesso+"$1" WHERE \
schema=\x27" $3 "\x27 AND id_conteudo="$4 " AND id_site="$5 ";"}' > $path_sql

echo -n '' > $path_log

/usr/bin/python2.6 /home/divirta-se/ad-hoc/app_access/access_app.py

exit

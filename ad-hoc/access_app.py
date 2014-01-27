# encoding: utf-8
# Open the pre-processed file app-requests.sql to insert the access
#
#
import sys
sys.path.append("/home/divirta-se/Publica/publica")
sys.path.append("/home/divirta-se/Publica")
import settings
from publica.db.modules.pygresql import pgdb

fsql = open("/home/divirta-se/ad-hoc/app_access/app-requests-da.sql", "r")
sql = fsql.read().strip()
fsql.close()
if sql:
    dsn = "%s:publica_portal_divirtase:%s" % (settings.DATABASE_HOST_WRITE, settings.DATABASE_PORT_WRITE)
    conn = pgdb.connect(dsn,
                        settings.DATABASE_USER_WRITE,
                        settings.DATABASE_PASSWORD_WRITE,
                        host="%s:%s" % (settings.DATABASE_HOST_WRITE,
                                        settings.DATABASE_PORT_WRITE))
    cursor = conn.cursor()
    cursor.execute(sql)
    print "ok"
    cursor.close()
    conn.close()


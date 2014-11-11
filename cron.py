import fb
import psycopg2

loop = 1
while True:
    loop += 1
    con = psycopg2.connect(database='flobbitdb', user='edward', password='yolomol0')
    con.autocommit = True
    cur = con.cursor()
    cur.execute("select fb_id, name from \"Groups\"")
    for item in cur.fetchall():
        if loop % 5:
            if item[1] != "Hackathon Hackers": continue
        try:
            print "Saving first page of : " + item[1]
            fb.save_recent(item[0])
        except Exception, e: print str(e) + " in cron.py"
    
    con.close()

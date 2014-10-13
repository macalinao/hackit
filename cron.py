import fb
import psycopg2

while True:
    con = psycopg2.connect(database='flobbitdb', user='edward', password='yolomol0')
    con.autocommit = True
    cur = con.cursor()
    cur.execute("select fb_id, name from \"Groups\"")
    for item in cur.fetchall():
        try:
            print "Saving first page of : " + item[1]
            fb.save_recent(item[0])
        except: 
            pass

    con.close()

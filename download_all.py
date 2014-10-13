import fb
import psycopg2

con = psycopg2.connect(database='flobbitdb', user='edward', password='yolomol0')
con.autocommit = True
cur = con.cursor()

cur.execute("select fb_id from \"Groups\"")
for item in cur.fetchall():
    try:
        print "Saving: " + item[0]
        fb.save_all(item[0])
    except: 
        pass


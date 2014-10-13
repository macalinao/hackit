from flask import Flask, render_template
import psycopg2
from psycopg2.extras import DictCursor
from urlparse import urlparse 

app = Flask(__name__)
def get_top_day():
    con = psycopg2.connect(database="flobbitdb", user="edward", password="yolomol0")
    cur = con.cursor(cursor_factory=DictCursor)
    cur.execute("""select count(*) from "Posts";
    SELECT *
    FROM   "Posts"
    WHERE  time >  now() - interval '24 hours'
    ORDER BY active DESC
    LIMIT 10;""")
    li = cur.fetchall()
    con.close()
    return li

@app.route("/")
def hello():
    li = get_top_day()
    print type(li)
    for i in li: 
        if i['link'] == "":
            i['link'] = 'self'
        else:
            i['link'] = urlparse(i['link']).netloc
    return render_template("index.html", li=li)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

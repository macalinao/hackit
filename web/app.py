import markdown
from flask import Flask, render_template, Markup
import psycopg2
from psycopg2.extras import RealDictCursor
from urlparse import urlparse 
import arrow
import re

app = Flask(__name__)

_link = re.compile(r'(?:(http://)|(www\.))(\S+\b/?)([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]*)(\s|$)', re.I)
def convertLinks(text): 
    def replace(match):
        groups = match.groups()
        protocol = groups[0] or ''  # may be None
        www_lead = groups[1] or ''  # may be None
        return '<a href="http://{1}{2}" rel="nofollow">{0}{1}{2}</a>{3}{4}'.format(
            protocol, www_lead, *groups[2:])
    return _link.sub(replace, text)

def get_posts(sql, var=None):
  con = psycopg2.connect(database="flobbitdb", user="edward", password="yolomol0")
  cur = con.cursor(cursor_factory=RealDictCursor)
  if var == None:
    cur.execute(sql)
  else: 
    cur.execute(sql, var)
  li = cur.fetchall()
  con.close()
  li = process_posts(li)
  return li
def process_posts(li):
  for i in li: 
    for key, value in i.iteritems():
        try:
          i[key] = value.decode("utf-8")
        except: pass
    if i['link'] == "":
        i['link'] = '/p/' + str(i['id'])
        i.update({'nice_link':'self'})
    else:
        i.update({'nice_link':urlparse(i['link']).netloc})
    i['full_post'] = Markup(convertLinks(markdown.markdown(i['full_post'])))
    i['time'] = arrow.get(i['time']).humanize()
    # i['fb_user_name'] = i['fb_user_name'].decode('utf-8', errors='ignore')
  return li
def get_top_seconds(seconds):
  sql = """
            SELECT *
            FROM   "Posts", "Groups"
            WHERE (extract(epoch from now()) - time < %s)
            AND "Posts".group_id = "Groups".fb_id
            ORDER BY active DESC
            LIMIT 20;"""
  var = (seconds,)
  return get_posts(sql, var)
def get_new():
  sql = """
            SELECT *
            FROM   "Posts", "Groups"
            WHERE "Posts".group_id = "Groups".fb_id
            ORDER BY time DESC
            LIMIT 20;"""
  return get_posts(sql)
def get_post(id):
    sql = """
            SELECT *
            FROM "Posts", "Groups"
            WHERE "Posts".group_id = "Groups".fb_id
            AND id = %s"""
    return get_posts(sql, (id,))
def get_top_day():
  return get_top_seconds(86400)
def get_top_month():
  return get_top_seconds(2628000)
def get_top_year():
  return get_top_seconds(31536000)
def get_comments(id):
  con = psycopg2.connect(database="flobbitdb", user="edward", password="yolomol0")
  cur = con.cursor(cursor_factory=RealDictCursor)
  sql = """SELECT * FROM "Comments"
           WHERE post_id = %s
        """
  cur.execute(sql, (id,))
  li = cur.fetchall()
  con.close()
  print "--------------------"
  print(len(li))
  li = process_comments(li)
  return li
def process_comments(li):
  for i in li: 
        for key, value in i.iteritems():
            try:
              i[key] = value.decode("utf-8")
            except: pass
        try:
            i['time'] = arrow.get(i['time']).humanize()
            i['comment'] = convertLinks(i['comment'])
        except: pass

  return li
@app.route("/")
def index():
  li = get_top_day()
  return render_template("index.html", li=li)
@app.route("/month")
def top_month():
  li = get_top_month()
  return render_template("index.html", li=li)
@app.route("/year")
def top_year():
  li = get_top_year()
  return render_template("index.html", li=li)
@app.route("/new")
def new():
  li = get_new()
  return render_template("index.html", li=li)

@app.route("/p/<int:id>")
def comments(id):
  post = None
  try:
      post = get_post(id)[0]
      print(type(post))
      print("title" + post['title'])
  except Exception as e: print(e) 
  comments = get_comments(id)
  return render_template("post.html", comments=comments, post=post)
if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)

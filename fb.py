from time import sleep
import facebook
import sys
import psycopg2
import re
import lib
import requests
import traceback

APP_ID = '281793872016719'
APP_SECRET = 'e91a9a2e78f1e25e3142a16a6da5252e'

# connect to db
    
con = psycopg2.connect(database="flobbitdb", user='edward', password='yolomol0')
con.autocommit = True
cur = con.cursor()

token = facebook.get_app_access_token(APP_ID, APP_SECRET)
graph = facebook.GraphAPI(token)

loop = 0
def get_post_id(fb_id):
  cur.execute("SELECT id from \"Posts\" where fb_id = %s", (fb_id,))
  inserted_id = cur.fetchone()
  if inserted_id:
     return inserted_id[0]
  else: return None
def get_comment_id(fb_id):
  cur.execute("SELECT id FROM \"Comments\" WHERE fb_id = %s", (fb_id,))
  inserted_id = cur.fetchone()
  if inserted_id:
     return inserted_id[0]
  else: return None
def get_title_from_post(full_post):
  title = lib.title_generator(lib.remove_url(full_post))
  title = lib.strip_newline(title)
  return title
def get_link_from_post(full_post):
  urls = lib.find_urls(full_post)
  if len(urls) > 0: return urls[0]
  else: return ""
def get_summary_from_id(fb_id):
  return graph.get_object(fb_id + "?fields=likes.summary(1),comments.summary(1)")
def get_likes_from_summary(summary):
  likes = 0
  try: 
    likes = summary['likes']['summary']['total_count']
    likes = int(likes)
  except: pass
  return likes
def get_comment_count_from_summary(summary):
  comment_count = 0
  try:
    comment_count = summary['comments']['summary']['total_count']
  except: pass
  return comment_count
def save_comment_info(datum, inserted_id):
  try:
    comment_obj = graph.get_object(use_epoch(datum['id']))['comments']
    comments = comment_obj['data']
    while True:
      # comments = datum['comments']['data']
      for c in comments:
          votes = c['like_count']
          comment = c['message']
          fb_id = c['id']
          time = c['created_time']
          post_id = inserted_id
          fb_user_id = c['from']['id']
          fb_user_name = c['from']['name']
          comment_id = get_comment_id(fb_id)
          if comment_id:
            query = """
            UPDATE "Comments"
            SET votes = %s,
                comment = %s,
                fb_id = %s,
                time = %s,
                post_id = %s,
                fb_user_id = %s,
                fb_user_name = %s
                WHERE id = %s
            """
            cur.execute(query, (votes, comment, fb_id, time, post_id, fb_user_id, fb_user_name, comment_id))
          else: 
            query = """INSERT INTO "Comments"
            (votes, comment, fb_id, time, post_id, fb_user_id, fb_user_name) VALUES 
            (%s, %s, %s, %s,  %s, %s, %s)"""
            cur.execute(query, (votes, comment, fb_id, time, post_id, fb_user_id, fb_user_name))
            comment_id = get_comment_id(fb_id)
          print "saved comment"
      if 'next' in comment_obj['paging']:
        print "next page of comments.. sleeping"
        sleep(0.9)
        comments = requests.get(comment_obj['paging']['next']).json()
      else: break
  except Exception as e: print "comment exception: " + str(e)  
def save_post_info(datum):
  try: 
    fb_id = datum['id']
    full_post = datum['message']
    title = get_title_from_post(full_post)
    original_url = datum['actions'][0]['link']
    link = get_link_from_post(full_post)
    time = datum['created_time']
    summary = get_summary_from_id(fb_id)
    likes = get_likes_from_summary(summary)
    comment_count = get_comment_count_from_summary(summary)
    active = likes + comment_count
    group_id = datum['to']['data'][0]['id']
    fb_user_name = datum['from']['name']
    fb_user_id = datum['from']['id']
    print(group_id)
    inserted_id = get_post_id(fb_id)
    if inserted_id:
      query = """
      UPDATE "Posts"
      SET fb_id = %s,
          title = %s,
          full_post = %s,
          link = %s,
          likes = %s,
          comments = %s,
          active = %s,
          time = %s,
          group_id = %s,
          original_url = %s,
          fb_user_id = %s,
          fb_user_name = %s
      WHERE id = %s"""
      cur.execute(query, (fb_id, title, full_post, link, likes, comment_count, likes+comment_count, time, group_id, original_url, fb_user_id, fb_user_name, inserted_id))
      print "updated post: %s" %(inserted_id,)
    else:
      query = """INSERT INTO \"Posts\" 
      (fb_id, title, full_post, link, likes, comments, active, time, group_id, original_url, fb_user_id, fb_user_name) 
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
      cur.execute(query, 
        (fb_id, title, full_post, link, likes, comment_count, 
          likes+comment_count, time, group_id, original_url, fb_user_id, fb_user_name))
      inserted_id = get_post_id(fb_id)
    return inserted_id
  except Exception as e: 
    print("Post error: " + str(e))
    print( traceback.print_exc() )
def use_epoch(obj):
  return obj + "?date_format=U"
def get_feed(group_id):
  feed = graph.get_object(use_epoch(str(group_id) + "/feed"))
  return feed
def save_post_and_comments(datum):
  inserted_id = save_post_info(datum)
  save_comment_info(datum, inserted_id)
def save_all(group_id):
  con = psycopg2.connect(database="flobbitdb", user='edward', password='yolomol0')
  con.autocommit = True
  cur = con.cursor()
  feed = get_feed(group_id)
  data = feed['data']
  loop = 0
  while True:
    for datum in data:
      sleep(1) # fb rate limiting
      loop += 1
      print str(loop) + "posts"
      save_post_and_comments(datum)
    if "next" in feed['paging']:
         print "getting next page..."
         feed = requests.get(feed['paging']['next']).json()
         data = feed['data']
    else:
         print "no more new pages, DONE!"
         break
  con.close()
def save_recent(group_id):
  loop = 0
  con = psycopg2.connect(database="flobbitdb", user='edward', password='yolomol0')
  con.autocommit = True
  cur = con.cursor()
  feed = get_feed(group_id)
  data = feed['data']
  print str(len(data)) + "in page"
  for datum in data:
    loop += 1
    print(str(loop) + "posts in group saved")
    sleep(1) # fb rate limiting
    save_post_and_comments(datum)
  con.close()

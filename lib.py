from nltk import tokenize
import re


def find_urls(s):
    return re.findall(r'(https?://\S+)', s)
def remove_url(s):
    return re.sub(r'(https?://\S+)', '', s, flags=re.MULTILINE)
def get_post_id(fb_id):
    cur.execute("select id from \"Posts\" where fb_id = %s", (fb_id,))
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

 
def title_generator(s):
    def chomp(s): 
        # if not s: return ""
        #print "chomping.."
        return s[:297] + "..."
    if len(s) < 300: 
        #print "under 300"
        return s
    else: return chomp(s)
    # if len(s.split("\n\n")) > 1: 
    #     print ("found double new line")
    #     return chomp(s.split("\n\n")[0])
#    else: 
#        print "attempting to tokenize..."
#        title = ""
#        next_title = ""
#        sentences = tokenize.sent_tokenize(s)
#        for i in range(0, len(sentences)):
#            if len(title) < 300:
#                title = next_title
#                next_title = title + sentences[i]
#            else:
#                return chomp(title)
#    return chomp(title)
def strip_newline(s):
    #print "stripping newline"
    #print s
    return " ".join(s.split("\n"))

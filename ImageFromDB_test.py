import sqlite3
import base64
import urllib.request, io
import contextlib

#Connect to SQLite DB
print("Connecting to SQLite database...")
conn = sqlite3.connect('mtgDB.db')
c = conn.cursor()

#get the image BLOB
c.execute('SELECT name, image, image_url from cards where set_Code = \'' + setcode +  '\' limit 1')
#print(c.fetchone()[0])
imageFile = c.fetchall()

data = None
for x in range(len(imageFile)):
    print(imageFile[x][0])
    fh = open(str(imageFile[x][0]) + ".png", "wb")
    fh.write(base64.b64decode(imageFile[x][1]))
    fh.close()
    
    #below is a test to compare a direct download incase quality is below expectations
    
    # with contextlib.closing(urllib.request.urlopen(imageFile[x][2], data)) as fp:
        # image = fp.read()
    # fh = open(str(imageFile[x][0]) + "_direct.png", "wb")
    # fh.write(base64.b64decode(imageFile[x][1]))
    # fh.close()
    
    # print(imageFile[x])

c.close()


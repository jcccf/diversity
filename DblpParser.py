import sqlite3
import re

DBLP_FILE = "/Volumes/My Passport/Work/dblp-data.xml"
SQLITE_DB = "/Volumes/My Passport/Work/dblp.sqlite"

conn = sqlite3.connect(SQLITE_DB)
c = conn.cursor()

obj_regex = re.compile("\s*<OBJECT\s+ID=\"([0-9]+)\"\s*/>\s*")
link_regex = re.compile("\s*<LINK ID=\"[0-9]+\" O1-ID=\"([0-9]+)\" O2-ID=\"([0-9]+)\"/>")
attribute_regex = re.compile("\s*<ATTRIBUTE NAME=\"([\w\-]+)\".+>\s*")
attr_regex = re.compile("\s*<ATTR-VALUE ITEM-ID=\"([0-9]+)\">\s*")
colvalue_regex = re.compile("\s*<COL-VALUE>\s*([\w\-]+)\s*</COL-VALUE>\s*")

# Read in objects
mode = "objects_tag_start"
with open(DBLP_FILE, 'r') as f:
  for l in f:
    if mode == "objects_tag_start":
      if "<OBJECTS>" in l:
        mode = "objects"
    elif mode == "objects":
      if "</OBJECTS>" in l:
        mode = "links_tag_start"
      else:
        print "OBJS", obj_regex.match(l).groups()
    elif mode == "links_tag_start":
      if "<LINKS>" in l:
        mode = "links"
    elif mode == "links":
      # Process links
      if "</LINKS>" in l:
        mode = "attributes_start"
      else:
        print "LINKS", link_regex.match(l).groups()
    elif mode == "attributes_start":
      if "<ATTRIBUTES>" in l:
        mode = "attributes"
    elif mode == "attributes":
      amatch = attribute_regex.match(l)
      if amatch is not None:
        print "Attribute", amatch.groups()
        mode = "attr_start"
    elif mode == "attr_start":
      if "</ATTRIBUTE>" in l:
        mode = "attr_start"
      else:
        amatch = attr_regex.match(l)
        if amatch is not None:
          print "Attr", amatch.groups()
          mode = "colvalue_start"
    elif mode == "colvalue_start":
      amatch = colvalue_regex.match(l)
      if amatch is not None:
        print "Colvalue", amatch.groups()
        mode = "attr_start"
    else:
      print "Whaaat...?", l


# c.execute("INSERT INTO objects (type) VALUES('hello')")
conn.commit()
c.close()

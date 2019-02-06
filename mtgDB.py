#Functions for MTG Database Project
#Written by: https://github.com/TastyBanelingz
#Last updated 2/5/2019

class mtgDB:

    def init__(self, arg1=None):
            self.text = arg1

    def InitializeDB():
        #Run this function first to create the database schema
        from mtgsdk import Card
        from mtgsdk import Set
        import sqlite3
        import base64
        import urllib.request, io
        import contextlib
        conn = sqlite3.connect('mtgDB.db')
        c = conn.cursor()

        #Connect to SQLite DB
        print("Connecting to SQLite database...")
        conn = sqlite3.connect('mtgDB.db')
        c = conn.cursor()

        #Drop tables
        c.executescript('''
        DROP TABLE IF EXISTS sets;
        DROP TABLE IF EXISTS cards;
        DROP TABLE IF EXISTS mtgsets;
        ;''')

        print("Tables Dropped")

        # Create tables
        c.execute('''CREATE TABLE if not exists sets (
                id   INTEGER       UNIQUE
                               PRIMARY KEY
                               NOT NULL,
            code VARCHAR (255),
            name VARCHAR (255),
            gatherer_code VARCHAR (255),
            old_code VARCHAR (255),
            magic_cards_info_code VARCHAR (255),
            release_date VARCHAR (255),
            border VARCHAR (255),
            stype VARCHAR (255),
            block VARCHAR (255),
            online_only VARCHAR (255),
            booster VARCHAR (255),
            mkm_id VARCHAR (255),
            mkm_name VARCHAR (255)
            );''')
            
        c.execute('''CREATE TABLE if not exists cards (
                id   INTEGER       UNIQUE
                               PRIMARY KEY
                               NOT NULL,
            name VARCHAR (255),
            multiverse_id VARCHAR (255),
            layout VARCHAR (255),
            names VARCHAR (255),
            mana_cost VARCHAR (255),
            cmc int (18),
            colors VARCHAR (255),
            color_identity VARCHAR (255),
            type_line VARCHAR (255),
            supertypes VARCHAR (255),
            types VARCHAR (255),
            subtypes VARCHAR (255),
            rarity VARCHAR (255),
            text VARCHAR (750),
            flavor VARCHAR (750),
            artist VARCHAR (255),
            number VARCHAR (255),
            power VARCHAR (18),
            toughness VARCHAR (18),
            loyalty int (18),
            border VARCHAR (255),
            image_url VARCHAR (255),
            set_code VARCHAR (255),
            set_name VARCHAR (255),
            image VARCHAR(255)
            );''')

        print("Tables created")

        conn.commit()

        conn.close()

    def UpdateDB():
    #This is the master update script
    #Will first refresh the SETS table and then check to see if any sets are not present on CARDS table
    #Will then attempt to grab all cards in all sets that are currently not present
    
    #WARNING: 
    #Will take a long time on first load.  
    #Reccommend using UpdateSet() if you only care about specific sets.
        from mtgsdk import Card
        from mtgsdk import Set
        import sqlite3
        import base64
        import urllib.request, io
        import contextlib
        conn = sqlite3.connect('mtgDB.db')
        c = conn.cursor()

        #Drop tables
        c.executescript('''
        DROP TABLE IF EXISTS sets;
        DROP TABLE IF EXISTS mtgsets;
        ;''')
        print('Sets Table Dropped')

        c.execute('''CREATE TABLE if not exists sets (
            id   INTEGER       UNIQUE
            PRIMARY KEY
            NOT NULL,
            code VARCHAR (255),
            name VARCHAR (255),
            gatherer_code VARCHAR (255),
            old_code VARCHAR (255),
            magic_cards_info_code VARCHAR (255),
            release_date VARCHAR (255),
            border VARCHAR (255),
            stype VARCHAR (255),
            block VARCHAR (255),
            online_only VARCHAR (255),
            booster VARCHAR (255),
            mkm_id VARCHAR (255),
            mkm_name VARCHAR (255)
            );''')
        print("Sets Table created")

        #insert values
        sets = Set.all()
        for x in range (0, len(sets)):
            code =str(sets[x].code)
            name =str(sets[x].name)
            gatherer_code =str(sets[x].gatherer_code)
            old_code  =str(sets[x].old_code)
            magic_cards_info_code  =str(sets[x].magic_cards_info_code)
            release_date  =str(sets[x].release_date)
            border  =str(sets[x].border)
            stype  =str(sets[x].type)
            block  =str(sets[x].block)
            online_only  =str(sets[x].online_only)
            booster  =str(sets[x].booster)
            mkm_id  =str(sets[x].mkm_id)
            mkm_name  =str(sets[x].mkm_name)
            
            #to prevent single quote insert errors
            name = name.replace("'", "''")
            c.execute("INSERT INTO sets VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(None,code,name,gatherer_code,old_code,magic_cards_info_code,release_date,border,stype,block,online_only,booster,mkm_id,mkm_name ))
            #print("Set #" + str(x) + " of " + str(len(sets)))

        print('Sets Table Populated')

        #Clear 'NONE' values from SETS
        c.execute('''UPDATE sets SET id = null where id='None' ''')
        c.execute('''UPDATE sets SET code = null where code='None' ''')
        c.execute('''UPDATE sets SET name = null where name='None' ''')
        c.execute('''UPDATE sets SET gatherer_code = null where gatherer_code='None' ''')
        c.execute('''UPDATE sets SET old_code = null where old_code='None' ''')
        c.execute('''UPDATE sets SET magic_cards_info_code = null where magic_cards_info_code='None' ''')
        c.execute('''UPDATE sets SET release_date = null where release_date='None' ''')
        c.execute('''UPDATE sets SET border = null where border='None' ''')
        c.execute('''UPDATE sets SET stype = null where stype='None' ''')
        c.execute('''UPDATE sets SET block = null where block='None' ''')
        c.execute('''UPDATE sets SET online_only = null where online_only='None' ''')
        c.execute('''UPDATE sets SET booster = null where booster='None' ''')
        c.execute('''UPDATE sets SET mkm_id = null where mkm_id='None' ''')
        c.execute('''UPDATE sets SET mkm_name = null where mkm_name='None' ''')
        print('Sets Table Cleaned')

        c.execute("SELECT DISTINCT code from sets where code not in (select distinct set_code from cards)")
        codes = c.fetchall()
        z = 0

        print("Adding cards from the following Sets:")
        print(codes)
        for z in range(0, len(codes)-1):
            codes[z] = str(codes[z]).replace('(','')
            codes[z] = codes[z].replace(')','')
            codes[z] = codes[z].replace(',','')
            codes[z] = codes[z].replace('\'','')
            print("Now getting cards from: " + codes[z])

            for y in range (1, 10000):
                cards = Card.where(set=codes[z]).where(page=y).where(pageSize=100).where(orderBy='set').all()
                #cards = Card.where(orderBy='name').all()
                for x in range (0, len(cards)):
                    name    =str(cards[x].name)
                    multiverse_id    =str(cards[x].multiverse_id)
                    layout    =str(cards[x].layout)
                    names    =str(cards[x].names)
                    mana_cost    =str(cards[x].mana_cost)
                    cmc    =str(cards[x].cmc)
                    colors =str(cards[x].colors)
                    color_identity    =str(cards[x].color_identity)
                    type_line    =str(cards[x].type)
                    types    =str(cards[x].types)
                    supertypes    =str(cards[x].supertypes)
                    subtypes    =str(cards[x].subtypes)
                    rarity    =str(cards[x].rarity)
                    text    =str(cards[x].text)
                    flavor    =str(cards[x].flavor)
                    artist    =str(cards[x].artist)
                    number    =str(cards[x].number)
                    power    =str(cards[x].power)
                    toughness    =str(cards[x].toughness)
                    loyalty    =str(cards[x].loyalty)
                    set_code    =str(cards[x].set)
                    set_name    =str(cards[x].set_name)
                    image_url    =str(cards[x].image_url)
                    border   =str(cards[x].border)
                    
                    # and len(str(cards[x].names)) == 0
                    if cards[x].names is not None and len(cards[x].names) != 0:
                        #print(cards[x].names)
                        if cards[x].names.index(name) == 0:
                            names = cards[x].names[1]
                        else:
                            names = cards[x].names[0]
                
                    #Image BLOB
                    data = None
                    if cards[x].image_url is not None:
                        #method to download card images from the 
                        with contextlib.closing(urllib.request.urlopen(image_url, data)) as fp:
                            image = base64.b64encode(fp.read())
                    else:
                        image = "No Image Available"
                    
                    #to prevent single quote import issues
                    text = text.replace("'", "''")
                    flavor = flavor.replace("'", "''")
                    name = name.replace("'", "''")
                    names = names.replace("'", "''")
                    names = names.replace('[', '')
                    names = names.replace(']', '')
                    names = names.replace('"', '')
                    set_name = set_name.replace("'", "''")
                    artist = artist.replace("'", "''")
                    mana_cost = mana_cost.replace('{', '')
                    mana_cost = mana_cost.replace('}', '')
                    color_identity = color_identity.replace('[', '')
                    color_identity = color_identity.replace(']', '')
                    color_identity = color_identity.replace(',', '')
                    color_identity = color_identity.replace(' ', '')
                    color_identity = color_identity.replace("'", '')
                    types = types.replace('[', '')
                    types = types.replace(']', '')
                    types = types.replace(',', '')
                    types = types.replace("'", '')
                    supertypes = supertypes.replace('[', '')
                    supertypes = supertypes.replace(']', '')
                    supertypes = supertypes.replace(',', '')
                    supertypes = supertypes.replace("'", '')
                    subtypes = subtypes.replace('[', '')
                    subtypes = subtypes.replace(']', '')
                    subtypes = subtypes.replace(',', '')
                    subtypes = subtypes.replace("'", '')
                    colors = colors.replace('White', 'W')
                    colors = colors.replace('Blue', 'U')
                    colors = colors.replace('Black', 'B')
                    colors = colors.replace('Red', 'R')
                    colors = colors.replace('Green', 'G')
                    colors = colors.replace(']', '')
                    colors = colors.replace('[', '')
                    colors = colors.replace(',', '')
                    colors = colors.replace(' ', '')
                    colors = colors.replace("'", "")
                    
                    c.execute("INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(None,name,multiverse_id,layout,names,mana_cost,cmc,colors,color_identity,type_line,supertypes,types,subtypes,rarity,text,flavor,artist,number,power,toughness,loyalty,border,image_url,set_code,set_name, image))
                    print(name + ' ' + set_code)
                    
                if(len(cards) == 0):
                    conn.commit()
                    break
                    
            #cards
            c.execute('''UPDATE cards SET id = null where id='None' ''')
            c.execute('''UPDATE cards SET name = null where name='None' ''')
            c.execute('''UPDATE cards SET multiverse_id = null where multiverse_id='None' ''')
            c.execute('''UPDATE cards SET layout = null where layout='None' ''')
            c.execute('''UPDATE cards SET names = null where names='None' ''')
            c.execute('''UPDATE cards SET mana_cost = null where mana_cost='None' ''')
            c.execute('''UPDATE cards SET cmc = null where cmc='None' ''')
            c.execute('''UPDATE cards SET colors = null where colors='None' ''')
            c.execute('''UPDATE cards SET color_identity = null where color_identity='None' ''')
            c.execute('''UPDATE cards SET type_line = null where type_line='None' ''')
            c.execute('''UPDATE cards SET supertypes = null where supertypes='None' ''')
            c.execute('''UPDATE cards SET types = null where types='None' ''')
            c.execute('''UPDATE cards SET subtypes = null where subtypes='None' ''')
            c.execute('''UPDATE cards SET rarity = null where rarity='None' ''')
            c.execute('''UPDATE cards SET text = null where text='None' ''')
            c.execute('''UPDATE cards SET flavor = null where flavor='None' ''')
            c.execute('''UPDATE cards SET artist = null where artist='None' ''')
            c.execute('''UPDATE cards SET number = null where number='None' ''')
            c.execute('''UPDATE cards SET power = null where power='None' ''')
            c.execute('''UPDATE cards SET toughness = null where toughness='None' ''')
            c.execute('''UPDATE cards SET loyalty = null where loyalty='None' ''')
            c.execute('''UPDATE cards SET border = null where border='None' ''')
            c.execute('''UPDATE cards SET image_url = null where image_url='None' ''')
            c.execute('''UPDATE cards SET set_code = null where set_code='None' ''')
            c.execute('''UPDATE cards SET set_name = null where set_name='None' ''')

            # Save (commit) the changes
            conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

        print("done")

    def UpdateSet(setcode):
        #Does the same as UpdateDB() but for only 1 set at a time.
        #This is best for if you only want a specific set of cards or are concerned about timeouts on API calls.
        from mtgsdk import Card
        from mtgsdk import Set
        import sqlite3
        import base64
        import urllib.request, io
        import contextlib

        conn = sqlite3.connect('mtgDB.db')
        c = conn.cursor()

        #Remove Entries from the card table for that set
        c.execute('''DELETE FROM CARDS where set_code in (\'''' + setcode + '''\')''')

        for y in range (1, 10000):
            cards = Card.where(set=setcode).where(page=y).where(pageSize=100).where(orderBy='set').all()
            #cards = Card.where(orderBy='name').all()
            for x in range (0, len(cards)):
                name    =str(cards[x].name)
                multiverse_id    =str(cards[x].multiverse_id)
                layout    =str(cards[x].layout)
                names    =str(cards[x].names)
                mana_cost    =str(cards[x].mana_cost)
                cmc    =str(cards[x].cmc)
                colors =str(cards[x].colors)
                color_identity    =str(cards[x].color_identity)
                type_line    =str(cards[x].type)
                types    =str(cards[x].types)
                supertypes    =str(cards[x].supertypes)
                subtypes    =str(cards[x].subtypes)
                rarity    =str(cards[x].rarity)
                text    =str(cards[x].text)
                flavor    =str(cards[x].flavor)
                artist    =str(cards[x].artist)
                number    =str(cards[x].number)
                power    =str(cards[x].power)
                toughness    =str(cards[x].toughness)
                loyalty    =str(cards[x].loyalty)
                set_code    =str(cards[x].set)
                set_name    =str(cards[x].set_name)
                image_url    =str(cards[x].image_url)
                border   =str(cards[x].border)
                
                # and len(str(cards[x].names)) == 0
                if cards[x].names is not None and len(cards[x].names) != 0:
                    #print(cards[x].names)
                    if cards[x].names.index(name) == 0:
                        names = cards[x].names[1]
                    else:
                        names = cards[x].names[0]
            
                #Image BLOB
                data = None
                if cards[x].image_url is not None:
                    #method to download card images from the 
                    with contextlib.closing(urllib.request.urlopen(image_url, data)) as fp:
                        image = base64.b64encode(fp.read())
                else:
                    image = "No Image Available"
                
                #to prevent single quote import issues
                text = text.replace("'", "''")
                flavor = flavor.replace("'", "''")
                name = name.replace("'", "''")
                names = names.replace("'", "''")
                names = names.replace('[', '')
                names = names.replace(']', '')
                names = names.replace('"', '')
                set_name = set_name.replace("'", "''")
                artist = artist.replace("'", "''")
                mana_cost = mana_cost.replace('{', '')
                mana_cost = mana_cost.replace('}', '')
                color_identity = color_identity.replace('[', '')
                color_identity = color_identity.replace(']', '')
                color_identity = color_identity.replace(',', '')
                color_identity = color_identity.replace(' ', '')
                color_identity = color_identity.replace("'", '')
                types = types.replace('[', '')
                types = types.replace(']', '')
                types = types.replace(',', '')
                types = types.replace("'", '')
                supertypes = supertypes.replace('[', '')
                supertypes = supertypes.replace(']', '')
                supertypes = supertypes.replace(',', '')
                supertypes = supertypes.replace("'", '')
                subtypes = subtypes.replace('[', '')
                subtypes = subtypes.replace(']', '')
                subtypes = subtypes.replace(',', '')
                subtypes = subtypes.replace("'", '')
                colors = colors.replace('White', 'W')
                colors = colors.replace('Blue', 'U')
                colors = colors.replace('Black', 'B')
                colors = colors.replace('Red', 'R')
                colors = colors.replace('Green', 'G')
                colors = colors.replace(']', '')
                colors = colors.replace('[', '')
                colors = colors.replace(',', '')
                colors = colors.replace(' ', '')
                colors = colors.replace("'", "")
                
                c.execute("INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(None,name,multiverse_id,layout,names,mana_cost,cmc,colors,color_identity,type_line,supertypes,types,subtypes,rarity,text,flavor,artist,number,power,toughness,loyalty,border,image_url,set_code,set_name, image))
                print(name + ' ' + set_code)
                
            if(len(cards) == 0):
                conn.commit()
                break
                
        #cards
        c.execute('''UPDATE cards SET id = null where id='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET name = null where name='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET multiverse_id = null where multiverse_id='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET layout = null where layout='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET names = null where names='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET mana_cost = null where mana_cost='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET cmc = null where cmc='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET colors = null where colors='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET color_identity = null where color_identity='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET type_line = null where type_line='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET supertypes = null where supertypes='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET types = null where types='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET subtypes = null where subtypes='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET rarity = null where rarity='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET text = null where text='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET flavor = null where flavor='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET artist = null where artist='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET number = null where number='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET power = null where power='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET toughness = null where toughness='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET loyalty = null where loyalty='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET border = null where border='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET image_url = null where image_url='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET set_code = null where set_code='None' and set_code = \'''' + setcode + '''\'''' )
        c.execute('''UPDATE cards SET set_name = null where set_name='None' and set_code = \'''' + setcode + '''\'''' )

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

        print("done")

    def GetSetImages(setcode):
        import sqlite3
        import base64
        import urllib.request, io
        import contextlib

        #Connect to SQLite DB
        print("Connecting to SQLite database...")
        conn = sqlite3.connect('mtgDB.db')
        c = conn.cursor()

        #get the image BLOB
        c.execute('SELECT name, image, image_url from cards where set_Code = \'' + setcode +  '\' limit 10')
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


        
    def select_all_mtgsets():
    #NOT USED AT THIS TIME
        import sqlite3
        import urllib.request, io
        conn = sqlite3.connect('mtgDB.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT code FROM sets")
        codes = c.fetchall()
        filter_codes = ''
        
        for code in codes:
            filter_codes += str(code)
            filter_codes += '|'
            
        filter_codes = filter_codes[:-1]
        filter_codes = filter_codes.replace('(','')
        filter_codes = filter_codes.replace(')','')
        filter_codes = filter_codes.replace(',','')
        filter_codes = filter_codes.replace('\'','')
        filter_codes = filter_codes + '\''
        filter_codes =   '\'' + filter_codes
        conn.commit()
        conn.close()
        return(codes)

    def select_max_releaseDate():
    #NOT USED AT THIS TIME
        import sqlite3
        import urllib.request, io
        conn = sqlite3.connect('mtgDB.db')
        c = conn.cursor()
        c.execute("select  release_date from mtgsets order by 1 desc limit 1")
        date = c.fetchall()
        return(date)

    #Function to return the Python Install Path
    def GetPythonPath():
        import os
        import sys
        return(os.path.dirname(sys.executable))

    #Function to return the valid import Python path locations
    def GetSysPath():
        import sys
        return(sys.path)


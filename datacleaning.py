import sqlite3
import pandas as pd 

#Pembuatan DATABASE
db = sqlite3.connect('database.db',check_same_thread=False)
db.row_factory = sqlite3.Row
c = db.cursor()
c.execute("create table if not exists databases (id INTEGER PRIMARY KEY AUTOINCREMENT, original TEXT, cleansed TEXT);")
db.commit()


# Data Cleaning
# Mengganti seluruh karakter menjadi lowercase 
def lowerchar(text): 
    return text.lower()

# Menghilangkan seluruh karakter non-alphanumerik 
def rmv_nonalphanumeric(text):
    text = re.sub('[^0-9A-Za-z]+',' ',text)
    return text

# Menghilangkan karakter yang tidak diperlukan 
def rmv_unnchar(text): 
    text = re.sub('\n',' ',text) #menghilangkan enter pada teks 
    text = re.sub('rt',' ',text) #menghilangkan simbol retweet pada twitter
    text = re.sub('user',' ',text) #menghilangkan karakter username 
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text)
    text = re.sub('  +',' ',text) #menghilangkan kelebihan spasi
    return text

# import dictionary alay untuk mapping kata2 tidak baku  
alay_dict = pd.read_csv('data mentah/new_kamusalay.csv', encoding='latin-1', header=None)
# rename kolom pada dictionary 
alay_dict = alay_dict.rename(columns={0:'original',
                                    1:'replacement'})

# Mengubah kata-kata yang tidak baku pada teks 
alay_dict_map = dict(zip(alay_dict['original'], alay_dict['replacement']))
def baku(text):
    return ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])

# Gabungan fungsi 
def textprep(text):
    text = lowerchar(text)
    text = baku(text)
    text = rmv_nonalphanumeric(text)
    text = rmv_unnchar(text)
    return text

    

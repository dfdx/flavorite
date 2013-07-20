
import csv

rating_map = {
    1 : -2,
    2 : -1,
    3 : 0,
    4 : 1,
    5 : 2,
    10 : 5,  # favorited
    20 : 1,  # saved for later
    30 : 0,  # don't know
    69 : 0,  # not interested
    100 : 0, # consumed
}


def read_tsv(path):
    with open(path) as tsv:
        for values in csv.reader(tsv, dialect="excel-tab"):
            yield values

            
def transform_rating(rating):
    return rating_map.get(int(rating), 0)
    
            
def load_data(interests_filename, ratings_filename):
    """Loads all data and creates required mappings"""
    id2name = {}
    id2url = {}
    name2url = {}
    interests = read_tsv(interests_filename)
    interests.next()   # skip headline
    for interest in interests:
        id2name[interest[0]] = interest[1]
        id2url[interest[0]] = interest[2]
        name2url[interest[1]] = interest[2]
    show_records = read_tsv(ratings_filename)
    show_records.next()   # skip headline
    item_data = ((user, id2url.get(inter_id, '<no>'), transform_rating(rating))
                 for user, inter_id, rating, tstamp
                 in show_records)
    item_data.next()  # skip tsv headline
    return {
        'item_data' : item_data,
        'id2name' : id2name,
        'id2url' : id2url,
        'name2url' : name2url,
    }    


def shorten_dataset(filename_in, filename_out, nlines=100000):
    """Reads first nlines lines of Combosaurus data from filename_in
       and writes shortened data to filename_out
    """
    with open(filename_in) as fin, open(filename_out, 'w') as fout:
        for line in fin.readlines():
            fout.write(line)
            nlines -= 1
            if nlines == 0:
                return
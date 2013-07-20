#!/usr/bin/env python

import sys
import os
from flavorite import Recommender
from combosaurus import load_data
from datetime import datetime

def find_closest_demo():
    data = load_data('../data/dump_interests.tsv',
                     '../data/dump_ratings_small.tsv')
    item_data = data['item_data']
    recom = Recommender()
    recom.build(item_data)
    return recom.find_closest('doctor-who', 10)

    
def save_load_demo():
    data = load_data('../data/dump_interests.tsv',
                     '../data/dump_ratings_small.tsv')
    item_data = data['item_data']
    recom = Recommender()
    recom.build(item_data)
    print 'Saving to `recom.pkl`...'
    recom.save('recom.pkl')
    recom2 = Recommender()
    print 'Loading back...'
    recom2.load('recom.pkl')
    os.remove('recom.pkl')
    print 'Done.'

    
def load_sim_demo():
    recom = Recommender()
    recom.load('recom.pkl')
    print recom.similarity('doctor-who', 'torchwood')
    

def build_and_save(filename):
    print '[', datetime.now(), '] loading data...'
    data = load_data('../data/dump_interests.tsv',
                     '../data/dump_ratings.tsv')
    print '[', datetime.now(), '] forcing item data to be loaded...'
    item_data = list(data['item_data'])
    print '[', datetime.now(), '] building recommender...'
    recom = Recommender()    
    recom.build(item_data)
    recom.save(filename)
    print 'Done.'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'build_and_save':
            build_and_save(sys.argv[2])
        elif cmd == 'find_closest':
            find_closest_demo()
        elif cmd == 'save_load':
            save_load_demo()
        elif cmd == 'load_sim':
            load_sim_demo()
        else:
            print 'No such command'
    else:
        print 'Usage: python demo.py cmd [args]'

        
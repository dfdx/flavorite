#!/usr/bin/env python

import os
import sys
import pickle
import heapq as hq
import scipy.sparse as sp
from datetime import datetime
from scipy import *


def mult_scalar(mat1, mat2):
    return mat1.dot(mat2.T)[0, 0]

def vlength(mat):
    return sqrt(mult_scalar(mat, mat))
    

def cosine_similarity(item_1_mat, item_2_mat):
    """Compute cosine similarity between matrices of 2 items
    """
    length = vlength(item_1_mat) * vlength(item_2_mat)
    if length != 0:
        return mult_scalar(item_1_mat, item_2_mat) / length
    else:
        return 0

    
class Recommender(object):
    """Recommender engine based on cosine similarity

       item_data  - dictionary of item_id->item_matrix, where item_matrix is
       1xN matrix
    """

    def __init__(self):
        pass
    
    def build(self, item_data, nusers=None, reporter=sys.stdout):
        """item_data - sequence of triples (user_id, item_id, rating)
           nusers    - number of users. If None, recommender will compute it,
                       but it will force item_data to be evaluated.
           reporter  - output stream to report progress, defaults to sys.stdout
                       
        """        
        if not nusers:
            # calculate nusers
            item_data = list(item_data)
            user_ids = set([])
            for item_id, user_id, rating in item_data:
                user_ids.add(user_id)
            nusers = len(user_ids)
        # create items
        items = {}
        user_id_to_pos = {}
        next_user_pos = 0
        rec_count = 0
        for user_id, item_id, rating in item_data:
            rec_count += 1
            if rec_count % 10000 == 0:
                reporter.write('[ %s ] %s records processed\n' %
                               (datetime.now(), rec_count))
            if user_id in user_id_to_pos.keys():
                user_pos = user_id_to_pos[user_id]
            else:
                user_pos = next_user_pos
                next_user_pos += 1
                user_id_to_pos[user_id] = user_pos                
            if item_id in items.keys():                
                items[item_id][0, user_pos] = rating
            else:                                    
                items[item_id] = sp.lil_matrix((1, nusers))                
                items[item_id][0, user_pos] = rating
        for item_id, mat in items.iteritems():
            items[item_id] = sp.csr_matrix(items[item_id])
        self.items = items
                
            

    def find_closest(self, item_id, n):
        """Find n item ids closest to specified one or None if there's no
           such item_id
        """
        print 'trying to find item closest to %s' % item_id
        this_mat = self.items.get(item_id, None)        
        if this_mat == None:
            return None
        def sim_with_item(cur_item):
            return cosine_similarity(this_mat, cur_item[1])
        item_gen = self.items.iteritems()
        closest_pairs =  hq.nlargest(n, item_gen, key=sim_with_item)
        return [item_id for item_id, mat in closest_pairs]
    
        
def demo():
    import parser
    data = parser.load_data('dump_ratings_small.tsv')
    item_data = data['item_data']
    recom = Recommender()
    recom.build(item_data)
    return recom.find_closest('doctor-who', 10)


def build_and_save(filename):
    import parser
    print '[', datetime.now(), '] loading data...'
    data = parser.load_data('../data/dump_ratings.tsv')
    print '[', datetime.now(), '] forcing item data to be loaded...'
    item_data = list(data['item_data'])
    print '[', datetime.now(), '] building recommender...'
    recommender = Recommender()    
    recommender.build(item_data)
    with open(filename, 'w') as f:
        pickle.dump(recommender, f)
    print 'Done.'


# if __name__ == '__main__':
#    build_and_save('recommender.pkl')
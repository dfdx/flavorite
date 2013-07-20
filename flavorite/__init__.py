#!/usr/bin/env python

import os
import sys
import pickle
import heapq as hq
import scipy.sparse as sp
from datetime import datetime
from scipy import *


## cosine similarity

def mult_scalar(v1, v2):
    """Computes scalar multiplication of 2 vectors.
       Vectors should be represented as 1xN matrices (row vectors).
    """
    return v1.dot(v2.T)[0, 0]

def vlength(v):
    return sqrt(mult_scalar(v, v))
    
def cosine(v1, v2):
    """Compute cosine between 2 vectors.
       Vectors should be represented as 1xN matrices (row vectors). 
    """
    length = vlength(v1) * vlength(v2)
    if length != 0:
        return mult_scalar(v1, v2) / length
    else:
        return 0


# recommender
        
class Recommender(object):
    """Recommender engine based on cosine similarity

       items  - dictionary of item_id->item_vector, where item_vector is
                1xN sparse matrix.

       Though this class may be used as is, it can also work as a base class
       for other recommenders. To do so, it is enough to override sim() method
       to compute similarity between vectors of 2 items. 
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
        
    def sim(self, v1, v2):
        """Low-level method for computing similarity between vectors
           of 2 items. Override *this* method if you want to intoduce
           new recommendation algorithm. 
        """
        return cosine(v1, v2)
        
    def similarity(self, item1_id, item2_id):
        """High-level method to find out similarity of 2 items.
           It is intended to be used from outside the class,
           to override recommendation algorithm check out sim() method.
        """
        v1, v2 = (self.items.get(item1_id), self.items.get(item2_id))
        if v1 != None and v2 != None:
            return self.sim(v1, v2)
        else:
            return None
            
    def find_closest(self, item_id, n):
        """Find n item ids closest to specified one or None if there's no
           such item_id
        """
        this_mat = self.items.get(item_id)
        if this_mat == None:
            return None
        def sim_with_item(cur_item):
            return cosine(this_mat, cur_item[1])
        item_gen = self.items.iteritems()
        closest_pairs =  hq.nlargest(n + 1, item_gen, key=sim_with_item)
        return [item_id for item_id, mat in closest_pairs][1:]
    
    def save(self, filename):
        with open(filename, 'w') as f:
            pickle.dump(self.items, f)

    def load(self, filename):
        with open(filename) as f:
            self.items = pickle.load(f)

            

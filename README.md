Flavorite
=========

Favorite is simple (but still powerfull!) recommendation engine based on cosine similarity between items. It requies only sequence of tuples like `(user_id, item_id, rating)` and allows to find top N items closest to the given one (people-who-liked-that-also-liked-this kind of algorithm). This repository is packed with parser for [Combosaurus](http://combosaurus.com/) data and can be directly used to find most similar shows (see below). 


Installation
------------

Install binary using pip:

    pip install flavorite

or build it from source: 

    git clone https://github.com/faithlessfriend/flavorite
    python setup.py install

Usage
-----

Assuming that `data` is iterator of tuples like `(user_id, item_id, rating)` and `item_id` is some id of the item (normally string or number):

    import flavorite as flv
	recom = flv.Recommender()
	recom.build(data)
	# or just load existing model:
	# recom.load(model_file)
	recom.find_closest(item_id, 10)



Example Using Combosaurus Data
------------------------------

TODO: Upload recommender model somewhere
TODO: Merge Usage and Example sections

The easiest way to try out recommender with Combosaurus data is to download [precomputed recommender model](http://todo) and just load it into `Recommender` instanse: 

    import flv
    recom = flv.Recommender()
	recom.load(model_file)

[Combosaurus data](http://combosaurus.com/about/data)

...to be continued...


Flavorite
=========

Favorite is simple (but still powerfull!) recommendation engine based on cosine similarity between items. It requies only sequence of tuples like `(user_id, item_id, rating)` and allows to find top N items closest to the given one (people-who-liked-that-also-liked-this kind of algorithm). This repository is packed with parser for [Combosaurus](http://combosaurus.com/) data and can be directly used to find most similar shows (see below). 


Installation
------------

After you have cloned/downloaded sources, cd to project directory and run: 

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

First of all, download [Combosaurus data](http://combosaurus.com/about/data). 

...to be continued...


import numpy as np
from scipy.sparse import csr_matrix

# maps movie_ids to movie names
movies = {}

with open( "../Webscope_R4/ydata-ymovies-mapping-to-eachmovie-v1_0.txt" , "r" ) as f:
    the_file = f.readlines()
    for line in the_file:
        movie_id, movie_name, _ = line.split("\t")
        movies[ movie_id ] = movie_name

user_vectors = {}

with open( "../Webscope_R4/ydata-ymovies-user-movie-ratings-train-v1_0.txt" , "r") as f:
    the_file = f.readlines()
    for line in the_file:
        user_id, movie_id, _, rating = line.split("\t")

        rating = rating.rstrip('\n')

        if user_id in user_vectors:
            user_vectors[ user_id ].append( (movie_id, rating) )
        else:
            user_vectors[ user_id ] = [ (movie_id, rating) ]

#print user_vectors

print "* Movies:\t",len(movies)
print "* Users:\t",len(user_vectors)

A = csr_matrix([[1, 2, 0], [0, 0, 3], [4, 0, 5]])

print A

"""
with open( "../Webscope_R4/ydata-ymovies-user-movie-ratings-test-v1_0.txt" , "r" ) as f:
    the_file = f.readlines()
    for line in the_file:
        user_id, movie_id, _, rating = line.split("\t")
        #print user_id, movie_id, rating
"""


### Item-based similiarty measures http://www.cs.carleton.edu/cs_comps/0607/recommend/recommender/itembased.html
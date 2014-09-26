import numpy as np
from math import sqrt
from scipy.sparse import csr_matrix
from random import choice

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
            user_vectors[ user_id ][ movie_id ] = float( rating )
        else:
            user_vectors[ user_id ] = {}
            user_vectors[ user_id ][ movie_id ] = float( rating )

def euclidean_distance( user_ratings, user_a, user_b ):
    if user_a == user_b:
        print "*** ERROR! User A and User B are identical"
        return -1

    len_of_intersection_set = 0

    rating_score = []
    for item in user_ratings[ user_a ]:
        if item in user_ratings[ user_b ]:
            rating_score.append( pow( user_ratings[ user_a ][ item ] - user_ratings[ user_b ][ item ],2 ) )
            len_of_intersection_set += 1
    if len_of_intersection_set > 0:
        return 1 / ( 1 + sum( rating_score ) )
    else:
        return 0

def pearson_correlation_score():
    pass

print "* Movies:\t",len(movies)
print "* Users:\t",len(user_vectors)

user_id_match = {}

"""
for elem in user_vectors.items():
    print elem
    print
"""
users = user_vectors.keys()
user_a = choice( users )
user_b = choice( users )

print euclidean_distance( user_vectors, user_a, user_b )

#UserMatrix = csr_matrix([[1, 2, 0], [0, 0, 3], [4, 0, 5]])

"""
with open( "../Webscope_R4/ydata-ymovies-user-movie-ratings-test-v1_0.txt" , "r" ) as f:
    the_file = f.readlines()
    for line in the_file:
        user_id, movie_id, _, rating = line.split("\t")
        #print user_id, movie_id, rating
"""

### Item-based similiarty measures http://www.cs.carleton.edu/cs_comps/0607/recommend/recommender/itembased.html
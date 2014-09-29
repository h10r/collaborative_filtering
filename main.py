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

def pearson_correlation_score( user_ratings, user_a, user_b ):
    if user_a == user_b:
        print "*** ERROR! User A and User B are identical"
        return -1

    intersection_set = []

    for item in user_ratings[ user_a ]:
        if item in user_ratings[ user_b ]:
            intersection_set.append( item )

    if len( intersection_set ) == 0:
        return 0.0

    sum_user1 = 0.0
    sum_user2 = 0.0

    squared_sum_user1 = 0.0
    squared_sum_user2 = 0.0
    squared_sum_product = 0.0

    for item in intersection_set:
        sum_user1 += user_ratings[ user_a ][ item ]
        sum_user2 += user_ratings[ user_b ][ item ]

        squared_sum_user1 += pow( user_ratings[ user_a ][ item ], 2 )
        squared_sum_user2 += pow( user_ratings[ user_b ][ item ], 2 )
    
        squared_sum_product += user_ratings[ user_a ][ item ] * user_ratings[ user_b ][ item ]

    upper = squared_sum_product - ( ( sum_user1 * sum_user2 ) / len( intersection_set ) )
    lower1 = ( squared_sum_user1 - pow( sum_user1, 2 ) / len( intersection_set ) )
    lower2 = ( squared_sum_user2 - pow( sum_user2, 2 ) / len( intersection_set ) )
    lower = sqrt( lower1 * lower2 )

    if lower > 0:
        r = upper / lower
        return r
    else:
        return 0

def simliarity_score( user_ratings, user_a, user_b ):
    return pearson_correlation_score( user_ratings, user_a, user_b )

def get_similiar_users_for( user_ratings, this_user, output_matches=10 ):
    user_similiarities = []

    for other_user in user_ratings.keys():
        if this_user == other_user:
            continue
        user_similiarities.append( ( simliarity_score( user_ratings, this_user, other_user ), other_user ) )

    user_similiarities.sort()
    # get top five
    best_matches = user_similiarities[len(user_similiarities)-1-output_matches:len(user_similiarities)-1]

    return best_matches

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

#print "euclidian",euclidean_distance( user_vectors, user_a, user_b )
#print "pearson", pearson_correlation_score( user_vectors, user_a, user_b )
print "score", simliarity_score( user_vectors, user_a, user_b )

print get_similiar_users_for( user_vectors, user_a )

#UserMatrix = csr_matrix([[1, 2, 0], [0, 0, 3], [4, 0, 5]])

"""
with open( "../Webscope_R4/ydata-ymovies-user-movie-ratings-test-v1_0.txt" , "r" ) as f:
    the_file = f.readlines()
    for line in the_file:
        user_id, movie_id, _, rating = line.split("\t")
        #print user_id, movie_id, rating
"""

### Item-based similiarty measures http://www.cs.carleton.edu/cs_comps/0607/recommend/recommender/itembased.html
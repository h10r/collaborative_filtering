import numpy as np
from math import sqrt
from scipy.sparse import csr_matrix
from random import choice

##################################################################################################
#
# Collaborative Filtering implementation in Python
#
# Based on Chapter 2, Making Recommendations.
# In: Toby Segaran. 2007. Programming Collective Intelligence. O'Reilly. 
#
##################################################################################################
# Load files
##################################################################################################

# maps movie_ids to movie names
movies = {}

# init movie names
with open( "../Webscope_R4/ydata-ymovies-mapping-to-eachmovie-v1_0.txt" , "r" ) as f:
    the_file = f.readlines()
    for line in the_file:
        movie_id, movie_name, _ = line.split("\t")
        movies[ movie_id ] = movie_name

user_ratings = {}

# init user ratings
with open( "../Webscope_R4/ydata-ymovies-user-movie-ratings-train-v1_0.txt" , "r") as f:
    the_file = f.readlines()
    for line in the_file:
        user_id, movie_id, _, rating = line.split("\t")

        rating = rating.rstrip('\n')

        if user_id in user_ratings:
            user_ratings[ user_id ][ movie_id ] = float( rating )
        else:
            user_ratings[ user_id ] = {}
            user_ratings[ user_id ][ movie_id ] = float( rating )

##################################################################################################
# Similiarity function
##################################################################################################

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

##################################################################################################
# CF implementation
##################################################################################################

def similarity_score( user_ratings, user_a, user_b ):
    return pearson_correlation_score( user_ratings, user_a, user_b )

def get_similiar_users_for( user_ratings, this_user, output_matches=10 ):
    user_similiarities = []

    for other_user in user_ratings.keys():
        if this_user == other_user:
            continue
        user_similiarities.append( ( similarity_score( user_ratings, this_user, other_user ), other_user ) )

    user_similiarities.sort()
    # get top five
    best_matches = user_similiarities[len(user_similiarities)-1-output_matches:len(user_similiarities)-1]

    return best_matches

def get_recommendations_by_weighted_average( user_ratings, this_user, N = 10 ):
    similarity_times_ranking = {}
    similarity = {}

    for other_user in user_ratings.keys():
        if this_user == other_user:
            continue
        sim_score = similarity_score( user_ratings, this_user, other_user )

        if sim_score > 0.0:
            for item in user_ratings[ other_user ]:

                # ignore movies the user already saw / rated
                if not item in user_ratings[ this_user ]:
                    # make sure you can just add to the value
                    similarity.setdefault(item,0)
                    similarity_times_ranking.setdefault(item,0)

                    similarity[ item ] += sim_score
                    similarity_times_ranking[ item ] += user_ratings[ other_user ][ item ] * sim_score

    rankings = []
    for item in similarity_times_ranking.keys():
        rankings.append( ( similarity_times_ranking[ item ] / similarity[ item ], item ) )

    rankings.sort()

    for r in rankings[ len(rankings)-N:len(rankings) ]:
        score, movie_id = r

        if movie_id in movies:
            print movies[ movie_id ]
        else:
            print "UNKNOWN MOVIE ID", movie_id

def get_movie_ratings_from_user_ratings( user_ratings ):
    movie_ratings = {}

    for user in user_ratings:
        for movie in user_ratings[user]:
            movie_ratings.setdefault(movie,{})
            movie_ratings[ movie ][ user ] = user_ratings[ user ][ movie ]
    
    return movie_ratings

print "*" * 100
print "*** Movies:\t",len(movies)
print "*** Users:\t",len(user_ratings)
print "*" * 100

def test_recommendations():
    """
    for elem in user_ratings.items():
        print elem
        print
    """
    users = user_ratings.keys()
    user_a = choice( users )
    user_b = choice( users )

    #print "euclidian",euclidean_distance( user_ratings, user_a, user_b )
    #print "pearson", pearson_correlation_score( user_ratings, user_a, user_b )
    print "score", similarity_score( user_ratings, user_a, user_b )

    print "Recommendation for:",user_a,"{",user_ratings[ user_a ],"}"

    #print get_similiar_users_for( user_ratings, user_a )
    print get_recommendations_by_weighted_average( user_ratings, user_a )

test_recommendations()

### Item-based similiarty measures http://www.cs.carleton.edu/cs_comps/0607/recommend/recommender/itembased.html
import requests
import pandas as pd

BASE_URL = 'https://api.themoviedb.org/3'
API_TOKEN = 'e99ba1f86c34f02729fc252f84f1a169'

titles = []

for i in range(1,101):
    r = requests.get(BASE_URL+f'/tv/popular?api_key=e99ba1f86c34f02729fc252f84f1a169&language=en-US&page={i}').json()
    titles += r['results']

users_count = {}
reviewed_titles = []
total_reviews = 0
reviews = {
    'user': [],
    'tv_show': [],
    'rating': [],
    'id': []
}
tv_shows = {
    'tv_show': [],
    'genres': [],
    'id': []
}


for title in titles:
    title_reviews = []
    title_reviews += requests.get(BASE_URL+f"/tv/{title['id']}/reviews?api_key=e99ba1f86c34f02729fc252f84f1a169&language=en-US").json()['results']

    if len(title_reviews):
        title_reviews += requests.get(BASE_URL+f"/tv/{title['id']}/reviews?api_key=e99ba1f86c34f02729fc252f84f1a169&language=en-US&page=2").json()['results']

        total_reviews += len(title_reviews)
        reviewed_titles.append(title)
        title_name = title['name']
        
        tv_shows['tv_show'].append(title_name)
        tv_shows['genres'].append(title['genre_ids'])
        tv_shows['id'].append(title['id'])

        for review in title_reviews:
            reviewer_username = review['author_details']['username']
            rating = review['author_details']['rating']

            reviews['rating'].append(rating)
            reviews['tv_show'].append(title_name)
            reviews['user'].append(reviewer_username)
            reviews['id'].append(review['id'])

            if reviewer_username in users_count:
                users_count[reviewer_username] += 1
            else:
                users_count[reviewer_username] = 1

reviews_df = pd.DataFrame.from_dict(reviews)
reviews_df.to_csv('reviews.csv')

tv_shows_df = pd.DataFrame.from_dict(tv_shows)
tv_shows_df.to_csv('tv_shows.csv')

print(f'Total titles: {len(reviewed_titles)}')
print(f'Total reviews: {total_reviews} - {len(reviews["rating"])}')
print(f'Total users: {len(users_count)}')
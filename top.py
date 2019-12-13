from bs4 import BeautifulSoup
import csv
import json
import requests
from movieDAO import movieDAO

class IMDB_top_movies:

    api = 'c460f163'
    csv_file_name = 'ImdbTopMovies.csv'
    imdb_url = 'http://www.imdb.com/chart/top?ref=ft_250'

    def __init__(self, api, csv_file_name, imdb_url):
        self.api = api
        self.csv_file_name = csv_file_name
        self.imdb_url = imdb_url

    # Get top 100 movie ids from http://www.imdb.com/chart/top?ref=ft_250 
    # Check each movie link and scrape movie's ID that is a part or URL
    # id looks like tt0111161
    def imdb_id_crawler(self):
        r_imdb = requests.get(self.imdb_url)
        imdb_content = r_imdb.text
        soup = BeautifulSoup(imdb_content, 'lxml')

        top_100_ids_list = []

        # getting id's of top 100 movies
        movies_ids = soup.find_all('td', {'class': 'titleColumn'})[:100]

        for movie_id in movies_ids:
            links = movie_id.find_all('a')
            for link in links:
                href = link.get('href')
                movie_id = href.split('/')[2]  # takes only id
            top_100_ids_list.append(movie_id)

        return top_100_ids_list


# Using movie IDs get details from omdb api
    def omdb_api_details(self):

        api = 'c460f163'
        print(api)
        movies_details = dict()
        top_100_ids_list = self.imdb_id_crawler()

        for movie_id in top_100_ids_list:
            omdb_url = 'http://www.omdbapi.com/' + '?i=' + movie_id + '&apikey=' + api
            r_omdb = requests.get(omdb_url)
            details = r_omdb.json()
            print('Detils: ', details)
            movies_details[details['Title']] = details['Year']

        sorted_movies = sorted(movies_details.items(), key=lambda x: x[1])
        return sorted_movies

# Write results into CSV file
    def generate_csv(self):
        sorted_movies = self.omdb_api_details()
        csv_file_name = self.csv_file_name
        with open(csv_file_name, 'w', newline='') as f:
            columns = ['Title', 'Year']
            writer = csv.writer(f, dialect='excel')
            writer.writerow(columns)
            for data in sorted_movies:
                writer.writerow(data)


if __name__ == "__main__":
    Top100 = IMDB_top_movies(
        'c460f163', 'ImdbTopMovies.csv', 'http://www.imdb.com/chart/top?ref=ft_250')
    Top100.imdb_id_crawler()
    print("List of top 100 id's: {}.\nThere are {} movies on the list.".format(
        Top100.imdb_id_crawler(), len(Top100.imdb_id_crawler())))
    Top100.omdb_api_details()
    print("Sorted movies: {}".format(Top100.omdb_api_details()))
    Top100.generate_csv()
    print("Done")
    movieDAO.clear_table()
    movieDAO.top_movies()
    print("Updated")

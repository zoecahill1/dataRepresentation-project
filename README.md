<p align="center">
  <img src="/img/banner2.png" alt="banner"/>
</p>

<br>

# Data Representation - Project
This repository contains my solution for the assessment of Data Representation in GMIT

## Instructions
<p align="center">
  <img src="/img/project.jpg" alt="banner"/>
</p>

## Directory of Files
1. database.sql contains the SQL to create the required databases
2. top.py will scrape IMDB for the top 100 movie IDs and then use OMDB API to match those IDs to the correct infomation it then writes them to ImdbTopMovies.csv and updates the topmovies datbase using this CSV. This is how you populate the topmovies table for the first time and also how you would update it
3. home.html should be considered the start page of the project - all pages are linked through the nav bars
4. movieViewer.html is the admin page - it has restriced access as it contains the functions that can alter the database. Only those with the username and password may access it
5. topMovieViewer.html shows the top 100 movies from IMDB retrieved using the top.py file.
6. leader.html get the leaderboard ranks the movies by votes recieved from highest to lowest.
7. moviesearch.html is an interface where you can search for details about various movies from IMDB using the OMDB API. 
8. simpleerver.py is the flask app of this project
9. movieDAO.py contains the interface to the database project

## How to Run the Project
1. Navigate to the project folder in cmd
2. Create your virtual environment using the command **python -m venv venv**
3. Install the requirements into that venv using the command **pip install -r requirements.txt**
4. Create the databases using the database.sql file. This file has dummy data included for the movies table.
5. To populate the topmovies run the top.py file using the command **python top.py**
6. Now set the flask server running the command **set FLASK_APP=simpleserver**
7. Run using **flask run**
8. The project should now be running. Navigate to localhost/home.html if running locally on your machine to see the first page

## How to Download the Repository
1. On GitHub, navigate to the main page of the repository.
2. Under the repository name, click Clone or download.
3. In the Clone with HTTPs section, click to copy the clone URL for the repository.
4. Open Git Bash.
5. Change the current working directory to the location where you want the cloned directory to be made.
6. Type git clone, and then paste the URL you copied in Step 2. 7/ Press Enter. Your local clone will be created.


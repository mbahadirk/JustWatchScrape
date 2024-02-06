import pandas as pd
from bs4 import BeautifulSoup
import requests

def scrape_movie_info(url):
    # Send a request to the provided URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract genres information from the HTML
    genres = ""
    h3 = soup.find_all('h3', {'class': 'detail-infos__subheading'})
    for i in h3:
        if i.text == "Genres":
            genres = i.next_sibling.text

    # Extract other movie information from the HTML
    title = soup.find('h1').text
    release_year = soup.find('span', {'class': 'text-muted'}).text
    release_year = release_year.strip('( )')
    streaming_services = [i.find('img')['alt'] for i in soup.find_all('div', {'class': 'buybox-row__offers'})]

    # Extract the rating information from the HTML
    div = soup.find('div', {'class': 'jw-scoring-listing__rating'})
    if div and div.find_next_sibling():
        rating = div.find_next_sibling().find('span').text.split('  ')[0]
    else:
        rating = "no rating info"

    # Create a dictionary to store the movie data
    movie_data = {
        'Title': title,
        'Year': release_year,
        'Rating': rating,
        'Genres': genres,
        'Streaming_Services': streaming_services,
        'URL': url
    }
    print(movie_data)
    return movie_data


def scrape_justwatch(url):
    movies_data = []
    # Send a request to the provided URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract movie links from the HTML
    div = soup.find('div', {'class': 'title-list-grid'})
    div_items = div.find_all('a', {'class': 'title-list-grid__item--link'})

    # Scrape movie information for each link
    for item in div_items:
        movie_url = f"https://www.justwatch.com{item['href']}"
        movie_data = scrape_movie_info(movie_url)
        movies_data.append(movie_data)

    return movies_data


# Scrape movie data from JustWatch for movies released after 2000
movies_data = scrape_justwatch('https://www.justwatch.com/in/movies?release_year_from=2000')

# Scrape TV show data from JustWatch for shows released after 2000
tv_shows_data = scrape_justwatch('https://www.justwatch.com/in/tv-shows?release_year_from=2000')

# Combine data for movies and TV shows
all_data = movies_data + tv_shows_data

# Create a DataFrame
df = pd.DataFrame(all_data)

# Write the DataFrame to a CSV file
df.to_csv('justwatch_data.csv', index=False)

# Read the CSV file and load it into a DataFrame (for verification)
read_df = pd.read_csv('justwatch_data.csv')

# Display the DataFrame
print(read_df)

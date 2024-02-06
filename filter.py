import pandas as pd
from datetime import datetime

def filterTime():
    # Load the dataset from the CSV file
    df = pd.read_csv('justwatch_data.csv')

    # Convert the 'Year' column to integers
    df['Year'] = df['Year'].astype(int)

    # Filter movies and TV shows released in the last two years
    current_year = datetime.now().year
    filtered_df = df[df['Year'] >= current_year - 2]

    # Display the filtered dataset
    print(filtered_df)

    # Save the filtered dataset to a new CSV file
    filtered_df.to_csv('justwatch_data_filtered_time.csv', index=False)

# Include only movies and TV shows with an IMDb rating of 7 or higher.
def filterIMDB(selectedRating):
    # Load the dataset from the CSV file
    df = pd.read_csv('justwatch_data.csv')

    # Convert the 'Year' column to integers
    df['Year'] = df['Year'].astype(int)

    # Get the current year
    current_year = datetime.now().year

    # Filter movies and TV shows released in the last two years
    df = df[df['Year'] >= current_year - 2]

    # Check the values in the 'Rating' column
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(0.0)
    df = df[df['Rating'] >= selectedRating]

    # Display the filtered dataset
    print(df)

    # Save the filtered dataset to a new CSV file
    df.to_csv('justwatch_data_filtered_IMDB.csv', index=False)

def averageRating():
    # Load the dataset from the CSV file
    df = pd.read_csv('justwatch_data.csv')

    # Convert the 'Rating' column to numeric and handle 'no rating info' as NaN
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # Drop rows with NaN values in the 'Rating' column
    df = df.dropna(subset=['Rating'])

    # Calculate the average rating
    average_rating = df['Rating'].mean()

    # Display the result
    print(f"The average rating is: {average_rating}")

def topGenres():
    # Load the dataset from the CSV file
    df = pd.read_csv('justwatch_data.csv')

    # Split the values in the 'Genres' column and create a list for each genre
    genres_list = []
    for genres in df['Genres']:
        genres_list.extend(genres.split(', '))

    # Count how many times each genre appears
    genres_count = pd.Series(genres_list).value_counts()

    # Take the top 5 genres
    top_5_genres = genres_count.head(5)

    # Display the result
    print("The top 5 genres with the most movies and TV shows are:")
    print(top_5_genres)

def topService():
    # Load the dataset from the CSV file
    df = pd.read_csv('justwatch_data.csv')

    # Split the values in the 'Streaming Services' column and create a list for each service
    services_list = []
    for services in df['Streaming_Services']:
        services_list.extend(eval(services))

    # Count how many times each service appears
    services_count = pd.Series(services_list).value_counts()
    services_count = services_count.head(5)

    # Identify the most common service
    most_common_service = services_count.idxmax()

    # Display the result
    print(f"The streaming service with the most movies and TV shows is: {most_common_service}")
    print(services_count)

topService()

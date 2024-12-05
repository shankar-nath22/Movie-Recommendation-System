import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    # api_key = "eyJhbGciOiJIUzI1NiJ9..UXCeOFowOMUNxymCEwkRuqSzpK-SBy86h8OSHH0FdSM"
    # url = "https://api.themoviedb.org/3/movie/{}?api_key=eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYmY1MjZhNWQ3ZWIyNmZkZTVlZmY0OTJhODIzMjM0NyIsIm5iZiI6MTczMzQwNTQ1My41MTUsInN1YiI6IjY3NTFhYjBkOGFmNmQzZmViM2FmZWFiNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UXCeOFowOMUNxymCEwkRuqSzpK-SBy86h8OSHH0FdSM&language=en-US".format(movie_id)
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYmY1MjZhNWQ3ZWIyNmZkZTVlZmY0OTJhODIzMjM0NyIsIm5iZiI6MTczMzQwNTQ1My41MTUsInN1YiI6IjY3NTFhYjBkOGFmNmQzZmViM2FmZWFiNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UXCeOFowOMUNxymCEwkRuqSzpK-SBy86h8OSHH0FdSM",
        "accept": "application/json"
    }

    try:
        data = requests.get(url, headers=headers, timeout=10)
        data = requests.get(url, headers=headers)
        data.raise_for_status()  # Raise an error if the request was unsuccessful
        data = data.json()
        
        if 'poster_path' not in data:
            print(f"Poster path not found for movie_id {movie_id}")
            return None
        
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return None

st.header("Movies Recommendation System using Machine Learning")
movies = pickle.load(open('artificats/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artificats/similarity.pkl', 'rb'))
print(type(similarity))


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    index = int(index)
    try:
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    except Exception as e:
        raise ValueError(f"Error accessing similarity matrix with index {index}: {e}")
    
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:13]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        movie_name = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_id)
        if poster_url:
            print(f"Poster URL for {movie_name}: {poster_url}")
            recommended_movie_posters.append(poster_url)
        else:
            print(f"No poster found for {movie_name}")
            recommended_movie_posters.append("https://via.placeholder.com/500x750?text=No+Poster+Available")
        
        recommended_movie_names.append(movies.iloc[i[0]].title)
        
    return recommended_movie_names,recommended_movie_posters


movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get recommendation',
    movie_list
)


def display_posters(recommended_movie_names, recommended_movie_posters):
    # Number of movies
    num_movies = len(recommended_movie_names)

    # Loop through movies in batches of 4
    for i in range(0, num_movies, 4):
        cols = st.columns(4)  # Create 4 columns for the row
        for j in range(4):  # Iterate through the 4 movies in the current batch
            if i + j < num_movies:  # Check if the index is valid
                with cols[j]:
                    st.text(recommended_movie_names[i + j])
                    st.image(recommended_movie_posters[i + j])


if st.button('Show Recommendation'):
    # Get recommended movies
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Display the movies in rows of 4
    display_posters(recommended_movie_names, recommended_movie_posters)

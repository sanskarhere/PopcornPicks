import pickle
import streamlit as st
import requests

# ✅ TMDb V3 API Key
API_KEY = "eeeac149744c594e234a7535ca59a404"

# Function to fetch poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        data = requests.get(url, timeout=10).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        print(f"⚠️ Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"

# Function to recommend movies
def recommender(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:  # Top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Pick your favorite movie and find similar ones from a dataset of 5,000 movies!</h4>", unsafe_allow_html=True)

# Load movies & similarity data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection
movies_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie you like:", movies_list)

# Show recommendations
if st.button("Show Recommendation"):
    recommended_movies_name, recommended_movies_posters = recommender(selected_movie)
    
    st.write("🎯 Recommended movies based on your interests:")
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            if idx < len(recommended_movies_name):
                st.text(recommended_movies_name[idx])
                st.image(recommended_movies_posters[idx], use_container_width=True)
            else:
                st.text("N/A")
                st.image("https://via.placeholder.com/500x750?text=No+Image", use_container_width=True)

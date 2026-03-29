import pandas as pd
import streamlit as st
import plotly.express as px
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(layout="wide")

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv(os.path.join("data", "spotify.csv"))
df.fillna(0, inplace=True)

# 🔥 OPTIONAL: Reduce size for speed (recommended)
df = df.sample(20000, random_state=42)

# -------------------------------
# SPOTIFY DARK UI 🎧
# -------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #121212;
    color: white;
}
.spotify-title {
    font-size: 60px;
    font-weight: bold;
    color: #1DB954;
    text-align: center;
}
.card {
    background-color: #181818;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
# -------------------------------
# ADVANCED HEADER 🎧
# -------------------------------
# -------------------------------
# HEADER 🎧
# -------------------------------
st.markdown("""
<div style='text-align:center; padding:20px;'>
    <h1 style='color:#22c55e; font-size:48px; margin-bottom:5px;'>
        🎧 SPOTIFY ANALYTICS
    </h1>
    <p style='color:#94a3b8; font-size:18px;'>
        Interactive Music Insights & Recommendation Dashboard
    </p>
    <p style='color:#22c55e; font-size:14px; margin-top:5px;'>
        🚀 Built by Deepak
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #333;'>", unsafe_allow_html=True)

# -------------------------------


# -------------------------------
# FILTERS
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    artist = st.selectbox("Select Artist", df['artists'].unique())

with col2:
    popularity = st.slider("Popularity", 0, 100, 50)

filtered_df = df[(df['artists'] == artist) & (df['popularity'] >= popularity)]

# -------------------------------
# FEATURED SONG 🎵
# -------------------------------
st.subheader("🎧 Featured Song")

if not filtered_df.empty:
    song = filtered_df.sample(1).iloc[0]

    st.markdown(f"""
    <div class="card">
        <h2>{song['track_name']}</h2>
        <p><b>Artist:</b> {song['artists']}</p>
        <p><b>Popularity:</b> {song['popularity']}</p>
        <p><b>Genre:</b> {song['track_genre']}</p>
        <p><b>Energy:</b> {song['energy']}</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# CHARTS 🎯
# -------------------------------
col3, col4, col5 = st.columns(3)

# 🎵 Popularity
with col3:
    fig1 = px.histogram(df, x="popularity", nbins=30,
                        title="Popularity Distribution",
                        color_discrete_sequence=["#1DB954"])
    st.plotly_chart(fig1, use_container_width=True)

# ⚡ Energy vs Danceability
with col4:
    fig2 = px.scatter(df, x="danceability", y="energy",
                      color="popularity",
                      title="Energy vs Danceability",
                      color_continuous_scale="greens")
    st.plotly_chart(fig2, use_container_width=True)

# 🎤 Top Artists
with col5:
    top_artists = df['artists'].value_counts().head(10)
    fig3 = px.bar(x=top_artists.index, y=top_artists.values,
                  title="Top Artists",
                  color=top_artists.values,
                  color_continuous_scale="greens")
    st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# SECOND ROW
# -------------------------------
col6, col7 = st.columns(2)

# 🎶 Tempo
with col6:
    fig4 = px.histogram(df, x="tempo", nbins=30,
                        title="Tempo Distribution",
                        color_discrete_sequence=["#1DB954"])
    st.plotly_chart(fig4, use_container_width=True)

# 🎼 Genres
with col7:
    genre_count = df['track_genre'].value_counts().head(10)
    fig5 = px.bar(y=genre_count.index,
                  x=genre_count.values,
                  orientation='h',
                  title="Top Genres",
                  color=genre_count.values,
                  color_continuous_scale="greens")
    st.plotly_chart(fig5, use_container_width=True)

# -------------------------------
# RECOMMENDATION SYSTEM 🤖 (FIXED)
# -------------------------------
st.subheader("🤖 Song Recommendation")

features = ['danceability', 'energy', 'tempo', 'loudness']

scaler = StandardScaler()
scaled = scaler.fit_transform(df[features])

song_name = st.selectbox("Select Song", df['track_name'])

def recommend(song_name):
    idx = df[df['track_name'] == song_name].index[0]

    # 🔥 MEMORY SAFE (only 1 vs all)
    sim_scores = cosine_similarity([scaled[idx]], scaled)[0]

    scores = list(enumerate(sim_scores))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]

    recs = []
    for i in scores:
        recs.append(df.iloc[i[0]]['track_name'])
    return recs

if st.button("Recommend"):
    results = recommend(song_name)
    for r in results:
        st.write("🎵", r)
st.markdown("""
<hr style="border:1px solid #444;">
<p style='text-align:center; color:#22c55e; font-size:16px;'>
    🚀 Developed by Deepak | Spotify Analytics Dashboard
</p>
""", unsafe_allow_html=True)
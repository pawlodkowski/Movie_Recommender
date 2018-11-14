# Movie_Recommender
**Contributors**:  Matthias Heerens, Helena Schock, Paul Wlodkowski
## Machine learning model for recommending movies.
- In a web interface (powered by Django and currently optimized for Firefox), the user rates 5 movies (on a scale from 1 to 5) that are randomly generated.
- This user input is then fed into 2 unsupervised machine-learning models:
  - Collaborative Filtering (based on cosine similarity); and
  - Non-negative Matrix Factorization (NMF).
- Both of these models are trained on a database of movies (including user ratings) from MovieLens.org.
- The models generate a list of recommended movies based on the user's input, and these recommendations are fed back to the Django interface and presented to the user.

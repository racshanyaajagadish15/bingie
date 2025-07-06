import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz

class OTTRecommender:
    def __init__(self, data_path='app/data/cleaned_combined_movies.csv'):
        self.df = pd.read_csv(data_path)
        self._prepare_data()
        self.vectorizer, self.tfidf_matrix = self._build_tfidf_matrix()
    
    def _prepare_data(self):
        """Prepare the data for recommendations"""
        columns_to_fill = ['title', 'cast', 'listed_in', 'description']
        for col in columns_to_fill:
            self.df[col] = self.df[col].fillna('').astype(str)
        
        self.df['combined_features'] = (self.df['title'] + ' ' +
                                      self.df['cast'] + ' ' +
                                      self.df['listed_in'] + ' ' +
                                      self.df['description'])
    
    def _build_tfidf_matrix(self):
        """Build TF-IDF matrix"""
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(self.df["combined_features"])
        return vectorizer, tfidf_matrix
    
    def recommend(self, title, platform_filter=None, year_range=None, duration_range=None, top_n=10):
        """Main recommendation function"""
        title = title.lower()
        scores = self.df["title"].apply(lambda x: fuzz.ratio(x.lower(), title))
        best_idx = scores.idxmax()

        if scores[best_idx] < 50:
            return []

        cosine_similarities = cosine_similarity(self.tfidf_matrix[best_idx], self.tfidf_matrix).flatten()
        similar_indices = cosine_similarities.argsort()[::-1][1:top_n+20]

        results = []
        for idx in similar_indices:
            row = self.df.iloc[idx]
            if platform_filter and row["Platform"] not in platform_filter:
                continue
            if year_range:
                if row["release_year"] < year_range[0] or row["release_year"] > year_range[1]:
                    continue
            if duration_range:
                try:
                    if (row["duration_time"] < duration_range[0] or
                        row["duration_time"] > duration_range[1]):
                        continue
                except:
                    continue

            results.append({
                "title": row["title"],
                "description": row["description"],
                "platform": row["Platform"],
                "release_year": int(row["release_year"]),
                "similarity": round(float(cosine_similarities[idx]), 3)
            })
            if len(results) >= top_n:
                break
        return results
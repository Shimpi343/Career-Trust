import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationEngine:
    """NLP-based recommendation engine for job opportunities"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.opportunity_vectors = None
        self.opportunities = None
    
    def fit(self, opportunities):
        """Train the recommendation engine"""
        self.opportunities = opportunities
        descriptions = [opp.get('description', '') for opp in opportunities]
        self.opportunity_vectors = self.vectorizer.fit_transform(descriptions)
    
    def recommend(self, user_skills, user_interests, num_recommendations=5):
        """Get recommendations based on user profile"""
        user_profile = ' '.join(user_skills + user_interests)
        user_vector = self.vectorizer.transform([user_profile])
        
        similarities = cosine_similarity(user_vector, self.opportunity_vectors)[0]
        top_indices = np.argsort(similarities)[::-1][:num_recommendations]
        
        return [self.opportunities[i] for i in top_indices]
    
    def save(self, filepath):
        """Save model to disk"""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load(filepath):
        """Load model from disk"""
        with open(filepath, 'rb') as f:
            return pickle.load(f)

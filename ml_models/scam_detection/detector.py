import pickle
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class ScamDetector:
    """ML-based fraud detection for job postings and emails"""
    
    # Suspicious keywords and patterns
    SUSPICIOUS_KEYWORDS = [
        'upfront', 'payment', 'fee', 'bank details', 'wire transfer',
        'urgent', 'guaranteed', 'work from home easy', 'make money fast',
        'no experience required', 'guaranteed income', 'limited time',
        'act now', 'click here', 'verify account', 'confirm identity'
    ]
    
    EMAIL_PATTERNS = {
        'suspicious_domain': r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',
        'multiple_exclamation': r'!{2,}',
        'multiple_question': r'\?{2,}',
        'unusual_sender': r'^[a-z0-9._%+-]+@(?!gmail|yahoo|outlook|company)?',
    }
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        self.is_trained = False
    
    def extract_features(self, text):
        """Extract features from text"""
        features = {}
        text_lower = text.lower()
        
        # Count suspicious keywords
        suspicious_count = 0
        for keyword in self.SUSPICIOUS_KEYWORDS:
            suspicious_count += text_lower.count(keyword)
        features['suspicious_keyword_count'] = suspicious_count
        
        # Check for unusual patterns
        features['has_url'] = 1 if 'http' in text else 0
        features['has_email'] = 1 if '@' in text else 0
        features['text_length'] = len(text)
        features['uppercase_ratio'] = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        
        return features
    
    def fit(self, texts, labels):
        """Train the detector with labeled data"""
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)
        self.is_trained = True
    
    def predict(self, text):
        """Predict if text is scam (returns probability 0-100)"""
        if not self.is_trained:
            return None
        
        X = self.vectorizer.transform([text])
        probability = self.model.predict_proba(X)[0][1] * 100
        
        return probability
    
    def analyze(self, text):
        """Comprehensive analysis of text"""
        result = {
            'scam_score': 0,
            'is_suspicious': False,
            'indicators': [],
            'confidence': 0
        }
        
        # Count suspicious keywords
        suspicious_keywords = []
        text_lower = text.lower()
        for keyword in self.SUSPICIOUS_KEYWORDS:
            if keyword in text_lower:
                suspicious_keywords.append(keyword)
        
        result['indicators'].extend(suspicious_keywords)
        result['scam_score'] = len(suspicious_keywords) * 15
        result['scam_score'] = min(result['scam_score'], 100)
        result['is_suspicious'] = result['scam_score'] > 50
        
        return result
    
    def save(self, filepath):
        """Save model to disk"""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load(filepath):
        """Load model from disk"""
        with open(filepath, 'rb') as f:
            return pickle.load(f)

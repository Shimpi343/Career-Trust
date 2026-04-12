import pytest
import sys
sys.path.insert(0, '../')

from ml_models.scam_detection.detector import ScamDetector

class TestScamDetector:
    
    def test_suspicious_keywords(self):
        detector = ScamDetector()
        text = "Earn money fast! Send upfront payment now."
        analysis = detector.analyze(text)
        
        assert len(analysis['indicators']) > 0
        assert analysis['scam_score'] > 0
    
    def test_legitimate_job(self):
        detector = ScamDetector()
        text = """
        Software Engineer Position
        We are looking for a talented software engineer with 2+ years of experience.
        Responsibilities include developing and maintaining web applications.
        Please submit your resume to hr@company.com
        """
        analysis = detector.analyze(text)
        
        assert analysis['is_suspicious'] == False
        assert analysis['scam_score'] < 30

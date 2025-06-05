import spacy 
from sklearn.linear_model import LogisticRegression
import numpy as np

class EmotionTracker:
    def __init__(self):
        self,nlp = spacy.load("en_core_web_sm")
        self.emotion_classsifier = LogisticRegression() # Placeholder for trained model
        self.emotion_history = []

    def analyze_text(self, text):
        """Analyze text for emotional content."""
        doc = self.nlp(text)
        # Placeholder : Use a pre-trained classifier to detect emotions
        emotion_vector = np.random.rand(5) # [joy, anger, sadness, fear, suprise]
        return emotion_vector
    
    def track_emotional_arr(self, story_events):
        """Track the emotional arc of the story"""
        for event in story_events:
            emotion = self.analyze_text(event["description"])
            self. emotion_history.append(emotion)
        return self.emotion_history
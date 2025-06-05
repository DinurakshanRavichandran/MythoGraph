import spacy 
from sklearn.linear_model import LogisticRegression
import numpy as np

class EmotionTracker:
    def __init__(self):
        self,nlp = spacy.load("en_core_web_sm")
        self.emotion_classsifier = LogisticRegression()
        self.emotion_history = []

    
import spacy 
from sklearn.linear_model import LogisticRegression
import numpy as np
import matplotlib as plt

class EmotionTracker:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.emotion_labels = ["joy", "anger", "sadness", "fear", "surprise"]
        self.emotion_keywords = {
            "joy": ["happy", "laugh", "smile", "joy", "love", "cheerful"],
            "anger": ["angry", "furious", "rage", "yell", "hate", "resent"],
            "sadness": ["sad", "cry", "tears", "grief", "lonely", "sorrow"],
            "fear": ["afraid", "scared", "fear", "terror", "panic", "horror"],
            "surprise": ["surprise", "shock", "astonish", "amazed", "unexpected"]
        }
        self.emotion_history = []

    def analyze_text(self, text):
        """
        Analyze text for emotional content using a keyword heuristic.
        Returns a normalized emotion vector [joy, anger, sadness, fear, surprise].
        """
        doc = self.nlp(text.lower())
        emotion_vector = np.zeros(len(self.emotion_labels))

        for token in doc:
            for idx, emotion in enumerate(self.emotion_labels):
                if token.lemma_ in self.emotion_keywords[emotion]:
                    emotion_vector[idx] += 1

        # Normalize to make it a probability distribution (if any emotion found)
        if emotion_vector.sum() > 0:
            emotion_vector = emotion_vector / emotion_vector.sum()

        return emotion_vector
    
    def track_emotional_arr(self, story_events):
        """
        Track the emotional arc over a sequence of story events.
        Each event is expected to be a dict with at least a 'description' key.
        """
        for event in story_events:
            description = event.get("description", "")
            if not description:
                continue
            emotion = self.analyze_text(description)
            self.emotion_history.append(emotion)
        return self.emotion_history
    
    def plot_arc(self):
        """
        Plot the emotional arc of the story using Matplotlib.
        """
        if not self.emotion_history:
            print("No emotion data to plot.")
            return

        emotions = np.array(self.emotion_history)
        for i, label in enumerate(self.emotion_labels):
            plt.plot(emotions[:, i], label=label.capitalize())
        plt.title("Emotional Arc of the Story")
        plt.xlabel("Event Index")
        plt.ylabel("Emotion Intensity")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
    def reset(self):
        """Clear the emotion history to restart tracking."""
        self.emotion_history = []
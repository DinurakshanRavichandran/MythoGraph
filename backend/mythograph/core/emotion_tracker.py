import torch
import numpy as np
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import expit as sigmoid  # for multi-label probs

class GoEmotionTracker:
    def __init__(self, map_to="mytho5"):
        self.model_name = "monologg/bert-base-cased-goemotions"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.model.eval()

        self.goemotions_labels = [
            "admiration", "amusement", "anger", "annoyance", "approval", "caring",
            "confusion", "curiosity", "desire", "disappointment", "disapproval",
            "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
            "joy", "love", "nervousness", "optimism", "pride", "realization", "relief",
            "remorse", "sadness", "surprise"
        ]

        # Define mappings
        self.target_model = map_to
        self.target_labels, self.label_map = self._build_label_mapping(map_to)
        self.emotion_history = []

    def _build_label_mapping(self, target):
        """
        Maps GoEmotions 27 → desired categories.
        Supported targets: "mytho5", "plutchik8", "go27"
        """
        if target == "mytho5":
            labels = ["joy", "anger", "sadness", "fear", "surprise"]
            mapping = {
                "joy": ["joy", "love", "amusement", "excitement", "gratitude", "optimism", "relief"],
                "anger": ["anger", "annoyance", "disapproval", "remorse"],
                "sadness": ["sadness", "grief", "disappointment"],
                "fear": ["fear", "nervousness"],
                "surprise": ["surprise", "realization"]
            }
        elif target == "plutchik8":
            labels = ["joy", "trust", "fear", "surprise", "sadness", "disgust", "anger", "anticipation"]
            mapping = {
                "joy": ["joy", "love", "excitement", "amusement", "gratitude", "relief"],
                "trust": ["approval", "caring", "gratitude"],
                "fear": ["fear", "nervousness"],
                "surprise": ["surprise", "realization"],
                "sadness": ["sadness", "grief", "disappointment"],
                "disgust": ["disgust", "remorse"],
                "anger": ["anger", "annoyance", "disapproval"],
                "anticipation": ["desire", "curiosity"]
            }
        else:  # raw goemotions
            labels = self.goemotions_labels
            mapping = {label: [label] for label in labels}

        # Build reverse index: goemotion_label → target_label_index
        label_map = {g: idx for idx, (t, gs) in enumerate(mapping.items()) for g in gs}
        return labels, label_map

    def analyze_text(self, text):
        """Classify text and return mapped emotion vector."""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        probs = sigmoid(logits[0].numpy())  # shape: [27]
        
        mapped = np.zeros(len(self.target_labels))
        for i, p in enumerate(probs):
            label = self.goemotions_labels[i]
            if label in self.label_map:
                mapped[self.label_map[label]] += p

        return mapped / (mapped.sum() + 1e-6)  # normalize

    def track_emotional_arc(self, story_events):
        for event in story_events:
            description = event.get("description", "")
            if not description:
                continue
            emotion = self.analyze_text(description)
            self.emotion_history.append(emotion)
        return self.emotion_history

    def plot_arc(self):
        if not self.emotion_history:
            print("No emotion data to plot.")
            return

        emotions = np.array(self.emotion_history)
        for i, label in enumerate(self.target_labels):
            plt.plot(emotions[:, i], label=label.capitalize())
        plt.title(f"Emotional Arc ({self.target_model.upper()})")
        plt.xlabel("Event Index")
        plt.ylabel("Emotion Intensity")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def reset(self):
        self.emotion_history = []

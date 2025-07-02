import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Training data: emotions and sample texts
data = {
    'text': [
        # Happy
        "I am so happy today!", "What a beautiful day", "I'm feeling great", "happy",

        # Sad
        "I am really sad", "This is depressing", "I feel terrible", "sad",

        # Angry
        "I'm very angry", "This makes me furious", "I hate this", "angry",

        # Funny
        "I'm on a seafood diet. I see food, I eat it.",
        "My dog thinks I'm hilarious. That’s enough.",
        "If I had a dollar for every smart thing I say, I'd be broke.",
        "Life’s too short to be serious all the time — so if you can't laugh, call me.",
        "My mirror and I had a staring contest. I lost.",
        "Why be moody when you can shake your booty?",
        "Sometimes I talk to myself. We both laugh.",
        "I'm not lazy, I'm just on power-saving mode.",
        "My humor is 80% sarcasm, 20% bad timing.",
        "I laugh at my own jokes so you don't have to. is not it funny.",


        # Bold
        "I know my worth, I don’t need validation.",
        "I’m not afraid to stand out.",
        "I speak my mind, always.",
        "I don't follow the crowd, I lead it.",
        "Confidence is my middle name.",
        "I don't back down from challenges.",
        "I stand tall, even when I stand alone.",
        "I'm unapologetically me.",
        "Being bold isn't a choice, it's who I am.",
        "I'm fearless when it matters.",


        # Neutral
        "I don't know what to feel", "Meh", "Okay, I guess",

        # Dumb (added more!)
        "totally dumb",
        "That was so dumb I forgot how to breathe",
        "Why did I even say that... dumb dumb dumb",
        "My brain just stopped working 💀",
        "This is peak stupidity 😂",
        "That joke broke my last brain cell",
        "I lost 10 IQ points reading this",
        "Certified dumb moment",
        "This is the dumbest thing I've ever seen",
        "Dumber than a brick wearing sunglasses",
        "No thoughts, just dumb"
    ],
    'emotion': [
        # Happy
        "happy", "happy", "happy", "happy",

        # Sad
        "sad", "sad", "sad", "sad",

        # Angry
        "angry", "angry", "angry", "angry",

        # Funny (10)
        "funny", "funny", "funny", "funny", "funny",
        "funny", "funny", "funny", "funny", "funny",

        # Bold (10)
        "bold", "bold", "bold", "bold", "bold",
        "bold", "bold", "bold", "bold", "bold",

        # Neutral
        "neutral", "neutral", "neutral",

        # Dumb (new samples)
        "dumb",
        "dumb",
        "dumb",
        "dumb",
        "dumb",
        "dumb",
        "dumb",
        "dumb",
        "dumb",
        "dumb",
        "dumb"
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Feature extraction
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])

# Model training
model = MultinomialNB()
model.fit(X, df['emotion'])

# Save both model and vectorizer
joblib.dump((model, vectorizer), 'emotion_model.pkl')


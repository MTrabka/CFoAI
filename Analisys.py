import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.util import ngrams
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


unwanted_phrases = [
    " participant",
    "suggests",
    " ai ",
    "responses ",
    "model",
    "rich",
    "strongly",
    "human",
    "language",
    "AI",
    "demonstrate",
    "exhibits"
]

# Load your data (assuming you have a 'reasoning' column in your DataFrame)
df = pd.read_csv("TT_Answers.csv", sep=";")
AI_judge=df[df["Judge ID"]=="AI"]
Human_judge=df[df["Judge ID"]!="AI"]
# Function to clean and tokenize text
def clean_text(text):
    text = text.lower()
    for word in unwanted_phrases:
        text = text.replace(word, "")
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text)  # Tokenize the text and convert to lowercase
    stemmer = nltk.PorterStemmer()  # Użyj stemmera, aby znormalizować słowa
    return [stemmer.stem(word) for word in words if word.isalpha() and word not in stop_words]

def generate_frequencies(text_data, n=1):
    tokens = clean_text(text_data)
    if n > 1:
        tokens = list(ngrams(tokens, n))
    return Counter(tokens)


# Funkcja do tworzenia wykresów słupkowych
def plot_bar_chart(counter, title, top_n=10):
    most_common = counter.most_common(top_n)
    labels, values = zip(*most_common)
    labels = [' '.join(label) if isinstance(label, tuple) else label for label in labels]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title(title)
    plt.xlabel("Words/Phrases")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


# Połącz tekst z kolumny 'Reasoning' dla każdej grupy
AI_text = " ".join(AI_judge['Reasoning'].dropna())
Human_text = " ".join(Human_judge['Reasoning'].dropna())

# Licz najczęstsze słowa i frazy (unigramy i bigramy)
AI_unigrams = generate_frequencies(AI_text, n=1)
Human_unigrams = generate_frequencies(Human_text, n=1)
AI_bigrams = generate_frequencies(AI_text, n=2)
Human_bigrams = generate_frequencies(Human_text, n=2)

# Wykresy dla unigramów
plot_bar_chart(AI_unigrams, "Top 10 Most Common Words in AI Judge", top_n=10)
plot_bar_chart(Human_unigrams, "Top 10 Most Common Words in Human Judge", top_n=10)

# Wykresy dla bigramów
plot_bar_chart(AI_bigrams, "Top 10 Most Common Phrases (Bigrams) in AI Judge", top_n=10)
plot_bar_chart(Human_bigrams, "Top 10 Most Common Phrases (Bigrams) in Human Judge", top_n=10)


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

# Function to clean and tokenize text
def clean_text(text):
    text = text.lower()
    for word in unwanted_phrases:
        text = text.replace(word, "")
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text)  # Tokenize the text and convert to lowercase
    return [word for word in words if word.isalpha() and word not in stop_words]  # Keep only alphabets and remove stop words

# Combine all text from the 'reasoning' column
df_human = df[df['Answer'] == 'human']
text_data = " ".join(df_human['Reasoning'].dropna().apply(clean_text).apply(lambda x: ' '.join(x)))

# Tokenize the text and extract n-grams (bigrams, trigrams, etc.)
n = 1  # For bigrams (use 3 for trigrams, etc.)
n_grams = ngrams(text_data.split(), n)
print(n_grams)
# Count the frequency of n-grams
n_gram_freq = Counter(n_grams)


# Prepare data for the word cloud: create a dictionary of n-gram frequency
phrase_freq = { ' '.join(ngram): count for ngram, count in n_gram_freq.items() }

# Create the word cloud from the n-grams
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(phrase_freq)

# Plot the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # No axes for the word cloud
plt.show()

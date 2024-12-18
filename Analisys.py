import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("TT_Answers.csv", sep=";")

categories_keywords = {
    "Tangential Thinking and Digression": [
        "digression", "tangential", "off-topic", "rambling", "jumping between threads", "wandering",
        "diverging", "straying", "unrelated", "sidetrack", "non-sequitur", "out of context", "jumping ahead"
    ],
    "Emotional Nuances and Self-deprecating Humor": [
        "emotional", "self-deprecating", "humor", "vulnerable", "self-awareness", "sarcasm",
        "irony", "mocking myself", "apologetic", "embarrassment", "guilt", "self-critical", "playful",
        "laughing at myself", "awkwardness", "self-doubt", "self-ironical","emotions"
    ],
    "Inconsistent Recall and Uncertainty": [
        "inconsistent", "uncertain", "forgotten", "memory", "uncertainty", "don't remember", "not sure",
        "maybe", "perhaps", "guessing", "could be", "it seems", "I think", "unsure", "vague", "mistaken",
        "confused", "imperfect memory", "unclear", "uncertain", "misremember", "I can't recall"
    ],
    "Rich Sensory Descriptions": [
        "sensory", "smell", "taste", "touch", "visual", "sound", "vivid", "description", "feeling", "texture",
        "scent", "flavor", "hearing", "color", "sharp", "warm", "cold", "bright", "soft", "rough", "tactile",
        "crisp", "soundscape", "aroma", "tasteful", "clear image", "scents", "touchable", "loud", "quiet",
        "piercing", "smooth", "softness", "moist", "juicy", "melodic"
    ],
    "Lack of Precision in Factual Details": [
        "lack of precision", "factual errors", "inaccurate", "wrong", "misleading", "incorrect", "ambiguous",
        "misleading", "vague", "false", "unverified", "error", "unreliable", "unproven", "approximate",
        "questionable", "confusing", "imprecise", "overgeneralized", "misinterpreted"
    ],
    "Emotional Complexity and Nuance": [
        "emotional complexity", "depth", "nuance", "emotion", "feelings", "complex emotions", "intense feelings",
        "mixed emotions", "contradictory emotions", "conflicted", "emotional depth", "turbulent emotions",
        "sensitive", "layers of feeling", "nuanced", "multi-layered", "complicated feelings", "emotionally rich"
    ],
    "Overly Consistent Narrative Structure": [
        "overly consistent", "structured", "predictable", "formulaic", "rigid", "repetitive", "monotonous",
        "unvaried", "pre-determined", "conventional", "mechanical", "stereotypical", "static", "unchanging",
        "standardized", "uniform", "robotic", "lacking variation", "structured storytelling"
    ],
    "Realistic Reasoning and Decision-Making": [
        "realistic reasoning", "decision-making", "logical", "practical", "rational", "realistic", "real-life",
        "sensible", "reasonable", "pragmatic", "thoughtful", "deliberate", "considered", "problem-solving",
        "weighing options", "rational decision", "real-world solution", "practical reasoning", "common sense"
    ],
    "Absurdity in Responses": [
        "absurd", "ridiculous", "impossible", "unbelievable", "far-fetched", "laughable", "nonsensical",
        "irrational", "outlandish", "out of this world", "implausible", "incredible", "silly", "preposterous",
        "bizarre", "unthinkable", "absurdity", "unrealistic", "impractical", "grotesque", "unbelievable"
    ],
    "Evasive and Inconsistent Responses": [
        "evasive", "vague", "inconsistent", "avoiding", "unclear", "non-committal", "dodging", "shifting",
        "elusive", "ambiguous", "indirect", "hesitant", "deceptive", "contradictory", "non-specific", "uncertain",
        "circumlocution", "deflecting", "disjointed", "obscure", "non-answering"
    ],
    "Exaggerated Detail and Long-Winded Responses": [
        "exaggerated", "long-winded", "overly detailed", "excessive details", "rambling", "over-elaborate",
        "overdescribing", "too much detail", "verbose", "talking too much", "extra details", "over-explained",
        "overblown", "overstated", "unnecessary information", "lengthy response", "extended explanation",
        "unnecessary elaboration"
    ],
    "Awkward Language Use": [
        "awkward", "unnatural", "stilted", "odd phrasing", "strange wording", "clumsy", "uncomfortable",
        "forced", "jarring", "unnatural phrasing", "wrong tone", "offbeat", "unfamiliar phrasing",
        "awkward phrasing", "disjointed language", "ungraceful", "stiff", "robotic tone", "clunky"
    ],
    "Grammatical Inconsistencies": [
        "grammar errors", "spelling mistakes", "incorrect punctuation", "sentence fragments", "run-on sentences",
        "misused words", "subject-verb agreement errors", "punctuation mistakes", "spelling errors",
        "inconsistent tenses", "misplaced commas", "incorrect use of articles", "wrong prepositions",
        "syntax errors", "poor sentence structure"
    ],
    "Personal Experience and Real-Life Examples": [
        "real experience", "personal experience", "real-life example", "memories", "personal story",
        "my experience", "from my life", "real-world example", "anecdote", "firsthand experience",
        "lived experience", "life lesson", "real story", "in my case", "I remember", "personally",
        "from my perspective"
    ],
    "Casual Language and Informal Speech": [
        "informal", "casual", "colloquial", "spoken language", "slang", "chatty", "relaxed", "informal tone",
        "everyday language", "conversational", "chat", "talking casually", "laid-back", "jargon",
        "informal speech", "casual phrasing", "street language", "casual words", "informal register", "slang terms"
    ]
}

def match_category(reasoning):
    matched_categories = []
    for category, keywords in categories_keywords.items():
        if any(keyword.lower() in reasoning.lower() for keyword in keywords):
            matched_categories.append(category)
    return ', '.join(matched_categories) if matched_categories else "No match"

df["Criteria"] = df["Reasoning"].apply(match_category)

for category in categories_keywords:
    df[category] = df["Reasoning"].apply(lambda reasoning: 1 if any(keyword.lower() in reasoning.lower() for keyword in categories_keywords[category]) else 0)

human_df=df[df["Judge ID"]!="AI"]
ai_df=df[df["Judge ID"]=="AI"]

human_category_counts = human_df.iloc[:, len(human_df.columns) - len(categories_keywords):].sum()
ai_category_counts = ai_df.iloc[:, len(ai_df.columns) - len(categories_keywords):].sum()
human_total = len(human_df)
ai_total = len(ai_df)

human_category_counts_normalized = human_category_counts / human_total * 100
ai_category_counts_normalized = ai_category_counts / ai_total * 100
category_comparison_normalized = pd.DataFrame({
    'Human (%)': human_category_counts_normalized,
    'AI (%)': ai_category_counts_normalized
})
print(category_comparison_normalized)
ax = category_comparison_normalized.plot(kind='bar', figsize=(14, 8), color=['skyblue', 'lightcoral'])

plt.xlabel("Criteria")
plt.ylabel("Proportion (%)")


plt.xticks(rotation=45, ha='right')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)


for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}%',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                fontsize=10, color='black',
                xytext=(0, 10), textcoords='offset points')


plt.tight_layout()
plt.show()

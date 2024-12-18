import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("TT_Answers.csv", sep=";")
df["Participant"] = df["Participant"].str.replace(r'human\d+', 'human', regex=True)
df["Judge ID"] = df["Judge ID"].str.replace(r'Judge\d+', 'Judge', regex=True)

df["Correct"] = df["Participant"] == df["Answer"]

correct_answer = df.groupby('Conversation ID')["Correct"].sum()


total_answers = df.groupby('Conversation ID')["Correct"].count()


percent_correct = (correct_answer / total_answers) * 100

plt.figure(figsize=(10, 6))
ax = percent_correct.plot(kind='bar', color='skyblue')
plt.title("Percentage of Correct Answers per Conversation ID")
plt.xlabel("Conversation ID")
plt.ylabel("Percentage of Correct Answers (%)")
plt.xticks(rotation=90)

for i, v in enumerate(percent_correct):
    ax.text(i, v + 2, f"{v:.2f}%", ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()

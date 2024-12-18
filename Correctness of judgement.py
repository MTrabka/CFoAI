import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("TT_Answers.csv", sep=";")


df['Participant'] = df['Participant'].str.replace(r'^human\d*$', 'human', regex=True)


AI_judge = df[df["Judge ID"] == "AI"]
Human_judge = df[df["Judge ID"] != "AI"]


AI_judge['correct'] = AI_judge['Answer'] == AI_judge['Participant']
counts = AI_judge['correct'].value_counts()


labels = ['Correct', 'Incorrect']
sizes = [counts.get(True, 0), counts.get(False, 0)]
colors = ['#34A853', '#EA4335']
explode = [0.1, 0]

plt.figure(figsize=(8, 8))
plt.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    explode=explode,
    labeldistance=1.1,
    textprops={'fontsize': 14},
    wedgeprops={'edgecolor': 'white', 'linewidth': 4}
)
plt.title('AI Judge: Proportion of Correctness', fontsize=16, fontweight='bold')
plt.show()


Human_judge['correct'] = Human_judge['Answer'] == Human_judge['Participant']
Hcounts = Human_judge['correct'].value_counts()


Hsizes = [Hcounts.get(True, 0), Hcounts.get(False, 0)]

plt.figure(figsize=(8, 8))
plt.pie(
    Hsizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    explode=explode,
    labeldistance=1.1,
    textprops={'fontsize': 14},
    wedgeprops={'edgecolor': 'white', 'linewidth': 4}
)
plt.title('Human Judges: Proportion of Correctness', fontsize=16, fontweight='bold')
plt.show()

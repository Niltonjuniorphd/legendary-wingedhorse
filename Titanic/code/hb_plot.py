import matplotlib.pyplot as plt
import seaborn as sns


def hb_plot(df, feature):
    fig, ax = plt.subplots(2, 1)

    sns.histplot(df[feature].value_counts(dropna=False), ax=ax[0])
    sns.boxplot(df[feature], ax=ax[1], orient='h',)
    plt.tight_layout()

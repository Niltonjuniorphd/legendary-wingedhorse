import matplotlib.pyplot as plt
import seaborn as sns

def hb_plot(df, feature):
    '''
    plot the histogram and boxplot

    input: 
    df -> pandas dataframe
    feature -> string - name of the feature(column) to plot

    output:
    matplotlib and seaborn graphs
    '''
    fig, ax = plt.subplots(2, 1)

    sns.histplot(df[feature].value_counts(dropna=False), ax=ax[0])
    ax[0].set_ylabel(feature)
    ax[0].set_xlabel('')
    sns.boxplot(df[feature], ax=ax[1], orient='h',)
    ax[0].set_ylabel('')
    ax[0].set_xlabel('')

    plt.tight_layout()


def deep_hb_plot(df):
    """
    Generates detailed graphical visualizations for each numerical column in a DataFrame.

    This function creates a histograms and  a boxplot for every numerical column in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the numerical columns to visualize.

    Returns:
    None

    """
     
    for i in df.select_dtypes('number').columns:
        print(i)
        fig, ax = plt.subplots(1, 2, figsize=(10, 3))
        sns.boxplot(data=df, x=i, ax=ax[0], orient='horizontal')
        sns.histplot(df[i], ax=ax[1], kde=True)
        ax[1].axvline(df[i].mean(), color='r',
                      label='Mean', linestyle='dotted')
        ax[1].axvline(df[i].median(), color='g', label='Median', linewidth=2)

        for j in range(0, len(df[i].mode())):
            ax[1].axvline(df[i].mode()[j], color='y', label='Mode')
        ax[1].legend()
        plt.show()


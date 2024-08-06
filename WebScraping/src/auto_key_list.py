# %%
import pandas as pd
from fpdf import FPDF
from nyt_app import nyt_summary
from gem_app import generate_gemini_response
from functions import (format_date_column,
                       full_text,
                       remover_artigos_preposicoes,
                       df_words_key, save_plot,
                       add_figure_to_pdf, add_list_to_pdf,
                       write_text_to_pdf,
                       get_news,
                       create_result_table,
                       save_table
                       )

# %%
hard_key = input('type the hard_key: ')  # get the word keys

# get the news from https://search.folha.uol.com.br using the hard_key
noticias_t = get_news(hard_key)
df = create_result_table(noticias_t)  # transform the news in a dataframe
save_table(df, hard_key)  # save the dataframe as a csv file

# %%
# clean some datetime language context portuguese->english and create datetime columns
df = format_date_column(df)
# join the text from the news as unique variable
content_text = full_text(df['content_text'])
# remove articles and prepositions from the text
full_text_cleaned = remover_artigos_preposicoes(content_text)
# create a dataframe with the words counts
df_c = df_words_key(full_text_cleaned, df)

dfw = pd.concat([df, df_c.drop(0, axis=1).astype('int')],
                axis=1)  # concat the dataframes

# %%
result = df_c.select_dtypes('float').sum()[0:50].sort_values(ascending=False)
# create a list of dictionaries with the words counts
result_list = [{index: value} for index, value in result.items()]
print(result_list)

# %%
# save figures to show the time frequence of the news
data1 = df['year'].value_counts()
data2 = df['month'].value_counts()

save_plot(data1, 'plot1.png', 'Year', 'Count', 'Year Distribution')
save_plot(data2, 'plot2.png', 'Month', 'Count', 'Month Distribution')

# %%
# summary texts using google gemini API
summary1 = generate_gemini_response(f'generate a text report containing general factual informations. The report should focus on the key words: {result.index[0:50]} that emerge as focal points in the text {content_text}. The report should be concise, informative, and engaging, providing a comprehensive overview of the text.')
summary1 = summary1.encode("utf-8", "replace").decode("utf-8")

print(f'reult summary1: {summary1}\n')

# %%
full_text_nyt = nyt_summary(hard_key)

summary2 = generate_gemini_response(f'generate a summary using the text: {full_text_nyt}')
summary2 = summary2.encode("utf-8", "replace").decode("utf-8")

print(f'reult summary2: {summary2}\n')
# %%
# Create a PDF document
pdf = FPDF()
pdf.add_page()

add_figure_to_pdf(pdf, 'plot1.png', 'Figure 1: Year Distribution')

add_figure_to_pdf(pdf, 'plot2.png', 'Figure 2: Month Distribution')

add_list_to_pdf(pdf, result_list, 'Page 3: Summary of Integer Columns')

write_text_to_pdf(pdf, summary1)
write_text_to_pdf(pdf, summary2)

pdf.output(f'multiple_plots_document_{hard_key}.pdf')

# %%
with open('unique_string_vector.txt', 'w', encoding='utf-8') as file:
    file.write(content_text)

# %%

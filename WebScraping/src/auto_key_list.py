#%%
import pandas as pd
import seaborn as sns
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
from fpdf import XPos, YPos
import re

from gem_nil import generate_gemini_response

#df = pd.read_csv('data_2024-08-01_maduro.csv')
#df = pd.read_csv('data_2024-08-05_ações_da_petrobras.csv')
#df = pd.read_csv('data_2024-08-05_ações_da_petrobras.csv')
df = pd.read_csv('data_2024-08-05_munições_não_letais.csv')


for i, j in enumerate(df['date']):
    df.loc[i, 'date_b'] = pd.to_datetime(j.replace('às', '')
                                         .replace('à', '')
                                         .replace('mai', 'may')
                                         .replace('out', 'oct')
                                         .replace('set', 'sep')
                                         .replace('dez', 'dec')
                                         .replace('º','')
                                         .replace('ago', 'aug')
                                         .replace('abr', 'apr')
                                         .replace('fev', 'feb')
                                         .replace('sem date', ''), dayfirst=True).date()

df['date_b'] = pd.to_datetime(df['date_b'])
df['day'] = df['date_b'].dt.day
df['month'] = df['date_b'].dt.month
df['year'] = df['date_b'].dt.year


df = df.sort_values(by=['date_b'], ascending=False)
df = df.reset_index()

content_text = df['content_text']


full_text = ' '.join(content_text.unique())\
    .replace('...', '')\
    .replace('\r\n', ' ')\
    .replace('\n', ' ')\
    .replace('.', ' ')\
    .replace('  ', ' ')\
    .replace('   ', ' ')\
    .replace('(', '')\
    .replace(')', '')\
    .replace(',', '')\
    .replace('"', '')\
    .strip()


def remover_artigos_preposicoes(texto):
    palavras_para_remover = r'\b(?:que|...|:|mas|ver|foi|tem|dia|dispensar|diz|ou|pelo|pelos|anos|agora|ser|quando|mais|gente|ano|deste|como|seu|é|não|se|ter|sido|são|duas|ele|ela|ficou|e|a|o|as|os|um|uns|uma|umas|de|do|da|dos|das|em|no|na|nos|nas|por|pelos|pela|pelas|ao|aos|à|às|com|para|perante|contra|entre|sob|era|sua|está|dizer|já|eu|você|sobre|trás)\b'
    
    # Usando regex para substituir as palavras por uma string vazia
    texto_limpo = re.sub(palavras_para_remover, '', texto, flags=re.IGNORECASE)
    
    # Remover espaços múltiplos resultantes da substituição
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    
    return texto_limpo

# Exemplo de uso
texto = full_text
full_text_cleaned = remover_artigos_preposicoes(texto)
print(full_text_cleaned)


with open('unique_string_vector.txt', 'w', encoding='utf-8') as file:
    file.write(full_text)


keys = pd.Series(full_text_cleaned.lower().strip().split(' '))


df_c=pd.Series()
for i, j in enumerate(df['content_text']):
    col = pd.DataFrame()
    for p in keys.value_counts().head(100).index:
        if ((len(p) > 2) and (p in j.lower())):
            col.loc[i, p] = 1
            
        else:
            col.loc[i, p] = 0
    df_c = pd.concat([df_c, col], axis=0)

dfw = pd.concat([df, df_c.drop(0, axis=1).astype('int')], axis=1)


# Assuming dfw is already defined
result = df_c.select_dtypes('float').sum()[0:50].sort_values(ascending=False)

# Transform the result into a list of dictionaries
result_list = [{index: value} for index, value in result.items()]

# Print the result
print(result_list)


# Function to create and save a plot
def save_plot(data, filename, xlabel, ylabel, title):
    sns.barplot(x=data.index, y=data.values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(filename)
    plt.close()

# Function to add a figure with a header to the PDF
def add_figure_to_pdf(pdf, image_file, header_text, x=10, y=20, w=190):
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, header_text, align='C')
    pdf.image(image_file, x=x, y=y, w=w)
    pdf.ln(85)  # Adjust the space between images

def add_list_to_pdf(pdf, result_list, header_text):
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, header_text, align='C')
    pdf.ln(1)
    pdf.set_font('helvetica', '', 10)
    
    for i, item in enumerate(result_list):
        for key, value in item.items():
            pdf.cell(0, 5, f'{i} - {key}: {value}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

def write_text_to_pdf(pdf, text):
  # Set font for the PDF
    pdf.set_font("helvetica", size=10)
    
    # Add a cell (a text block) to the PDF
    pdf.multi_cell(0, 10, text)
    

# Sample data for different figures
data1 = df['year'].value_counts()  # Replace 'another_column' with your actual column
data2 = df['month'].value_counts()

# Save the first figure
save_plot(data1, 'plot1.png', 'Year', 'Count', 'Year Distribution')

# Save the second figure
save_plot(data2, 'plot2.png', 'Month', 'Count', 'Month Distribution')

# Create a PDF document
pdf = FPDF()
pdf.add_page()

# Insert the first figure with a header
add_figure_to_pdf(pdf, 'plot1.png', 'Figure 1: Year Distribution')

pdf.add_page()
# Insert the second figure with a header
add_figure_to_pdf(pdf, 'plot2.png', 'Figure 2: Month Distribution')

pdf.add_page()
# Insert the result_list into the PDF with a header
add_list_to_pdf(pdf, result_list, 'Page 3: Summary of Integer Columns')


summary1 = generate_gemini_response(f'generate a brief summary of the text: {full_text}, using the key words {result.index[0:50]} as a guide. The summary should be concise, informative, and engaging, providing a comprehensive overview of the key points and their significance in the text.')
summary1 = summary1.encode("utf-8", "replace").decode("utf-8")

summary2 = generate_gemini_response(f'generate a text report containing general factual informations incorporating global data from news articles. The report should focus on the key {result.index[0:50]} words that emerge as focal points in the text. The report should be concise, informative, and engaging, providing a comprehensive overview of the key points and their significance in the text.')
summary2 = summary2.encode("utf-8", "replace").decode("utf-8")



print(summary1)
print(summary2)




pdf.add_page()
write_text_to_pdf(pdf, summary1)

pdf.add_page()
write_text_to_pdf(pdf, summary2)

#%%
# Save the PDF
pdf.output('multiple_plots_document.pdf')



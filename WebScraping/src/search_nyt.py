import pandas as pd
from fpdf import FPDF
from nyt_app import nyt_summary
from gem_app import generate_gemini_response
from functions import write_text_to_pdf
import os

hard_key = input('type the (one word) hard_key to searching for: ')  # get the word key

print('Searching for news in the New York Times API...\n')

try:
    full_text_nyt = nyt_summary(hard_key)
except:
    full_text_nyt = 'No results found'
    print('No results found')
    

print('Creating summary using GEMINI LLM...')
summary = generate_gemini_response(f'A summary should be generated using the news aggregated in the following text: {full_text_nyt}.\
                                    It should be written in an informative manner, using a clear and engaging tone,\
                                    and should provide a comprehensive overview of the core of the text.') # propt to GEMINI LLM

summary = summary.encode("utf-8", "replace").decode("utf-8")

print('Creating the PDF...')

pdf = FPDF()
write_text_to_pdf(pdf, summary)
pdf.output(f'sumary_nyt_{hard_key}.pdf')

print(r'Saving summary PDF on {path}\sumary_nyt_{hard_key}.pdf'.format(path=os.getcwd(), hard_key=hard_key))
print('All done!')
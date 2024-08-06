import pandas as pd
from fpdf import FPDF
from nyt_app import nyt_summary
from gem_app import generate_gemini_response
from functions import write_text_to_pdf

hard_key = input('type the hard_key: ')  # get the word keys

try:
    full_text_nyt = nyt_summary(hard_key)
except:
    full_text_nyt = 'No results found'
    print('No results found')

summary = generate_gemini_response(f'Generate a summary using the text: {full_text_nyt}. Write the summary in a informative way, using a clear and engaging tone, providing a comprehensive overview of the text.')
summary = summary.encode("utf-8", "replace").decode("utf-8")

pdf = FPDF()

write_text_to_pdf(pdf, summary)
pdf.output(f'sumary_nyt_{hard_key}.pdf')


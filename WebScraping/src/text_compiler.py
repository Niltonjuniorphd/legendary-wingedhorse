# %%
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# %%
df = pd.read_csv('data_2024-07-19_bala_de_borracha.csv')
df.drop_duplicates()
# %%

# %%
content_text = df['content_text']

# %%
full_text = ' '.join(content_text.unique())\
    .replace('...', '')\
    .replace('\r\n', ' ')\
    .replace('\n', ' ')\
    .replace('  ', ' ')\
    .strip()

# %%
print(full_text)


# %%
with open('unique_string_vector.txt', 'w', encoding='utf-8') as file:
    file.write(full_text)

# %%

def summarize_text(prompt: str, text: str) -> str:
    try:
        # Load the pre-trained model and tokenizer
        model_name = "facebook/bart-large"  # You can choose other models like t5-base
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Create a summarization pipeline
        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

        # Combine prompt and text
        combined_text = prompt + "\n" + text

        # Ensure the combined text does not exceed the model's maximum token limit
        inputs = tokenizer.encode(combined_text, return_tensors='pt', max_length=1024, truncation=True)

        # Generate summary
        summary_ids = model.generate(inputs, max_length=2000, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary

    except IndexError as e:
        return "An error occurred while generating the summary: " + str(e)
    except Exception as e:
        return "An unexpected error occurred: " + str(e)

# %%
# Example usage
prompt = "You will receive a text comprising a summary of the latest news items, constructed using the redlines from several news sources. Your task is to produce a summary of this text, focusing on the core information:"
text = full_text
summary = summarize_text(prompt, text)


# %%
print(summary)
# %%
with open('summary.txt', 'w', encoding='utf-8') as file:
    file.write(summary)
# %%

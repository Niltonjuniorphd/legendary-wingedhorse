from requests_code_word_folha import get_news, create_result_table, save_table

noticias_t, hard_key = get_news()
df = create_result_table(noticias_t)
save_table(df, hard_key)
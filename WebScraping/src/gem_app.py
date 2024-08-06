import google.generativeai as genai
import os


def generate_gemini_response(prompt):
    # Configure a API key
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Parâmetros de geração
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1024,
        "response_mime_type": "text/plain",
    }

    # Parâmetros de moderação da geração
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

    # Inicialize o modelo
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    # Defina o prompt
    # prompt = "Qual é a capital do Brasil e por que ela foi escolhida?"

    # Gere a resposta
    chat_session = model.start_chat()
    response = chat_session.send_message(prompt)

    # Imprima a resposta
    return response.text

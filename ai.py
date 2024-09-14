from groq import Groq
import google.generativeai as genai

# Initialize Groq and Gemini
groq_client = Groq(api_key="ENTER YOUR GROQ API")
genai.configure(api_key='ENTER YOUR GEN-AI API')

def groq_prompt(prompt, img_context):
    convo = [{'role': 'user', 'content': prompt}]
    chat_completion = groq_client.chat.completions.create(messages=convo, model='llama3-70b-8192')
    response = chat_completion.choices[0].message
    return response.content

def function_call(prompt):
    sys_msg = (
        'You are an AI function calling model... (Complete message here)'
    )
    function_convo = [{'role': 'system', 'content': sys_msg},
                      {'role': 'user', 'content': prompt}]
    chat_completion = groq_client.chat.completions.create(messages=function_convo, model='llama3-70b-8192')
    return chat_completion.choices[0].message

def handle_coding_task(task):
    # Task handling logic here
    pass

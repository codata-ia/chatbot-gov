import constants
import os
import json

from openai import OpenAI
from fileReader import saveConversation


# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY

client = OpenAI()

model = "gpt-3.5-turbo-1106"

def processMessage(user_message, messages_history):
    messages_history += [{"role": "user", "content": user_message}]

    chatbot_response = getBotResponse(messages_history)
    
    messages_history += [{"role": "assistant", "content": chatbot_response}]
    
    saveConversation(user_message, chatbot_response)
    
    return chatbot_response, messages_history

def getBotResponse(messages_history):
    response = client.chat.completions.create(
        model = model,
        messages = messages_history,
        temperature = 0.1
    )
    return response.choices[0].message.content
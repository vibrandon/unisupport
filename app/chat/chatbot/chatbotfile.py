from flask import Flask
import os

class ChatbotMessager:
    def __init__(self):
        pass


    def response(self, message):
        message = message.lower()
        if not message or message.strip() == "":
            return "I'm sorry, you haven't typed anything; is there anything I can you with today? Try asking about the matching system, feeling stressed or wellbeing profiles!"
        message = message.lower()

        if any(word in message for word in ["hey", "hello", "hi", "good morning", "good afternoon", "good evening"]):
            return "Hi! my name is Kami, and I am the UniSupport assistant! Is there any way that I can help you today?"

        if any(word in message for word in ["panic", "anxious", "stressed", "nervous", "scared"]):
            return "Hey, please remember to take it easy on yourself, and implement some self-care, would you like me to suggest some calming activities?"

        if any(word in message for word in ["calming"]):
            return"Some suggestions to help calm you, would include taking a relaxing bath, going for a walk or some physical activity, as well as spending time with loved ones, I hope you feel better soon!"

        if any(word in message for word in ["deadline", "exam", "stress", "assignment"]):
            return "Academic life can be very hard to manage at times, may I suggest you request for an adjustment or extension? I can redirect you to those?"

        if any(word in message for word in ["adjustment", "extension", "submission"]):
            return "The details for these services are found on the home page, links provided!"

        if any(word in message for word in ["matching", "professionals"]):
            return "You can match with qualified professionals based on your needs and preferences, manually or automatically! The link is on the home page."

        if any(word in message for word in ["wellbeing", "profile", "survey"]):
            return "Your wellbeing survey reports are found under student wellbeing on the home page!"

        if any(word in message for word in ["thank you", "appreciate", "thanks", "thx", "thankful"]):
            return "Hey, You're welcome! Do you require any other assistance? I'm always here to help!"

        return "Hi, are you feeling stressed regarding an upcoming deadline, or need assistance in matching on the system?"
#this is a simple word matching system, the word that is detected in the users message is returned with a response to matched to their query
    def get_response(self, message, chat_history=None):
        message = "" if message is None else message
        chatbot_response= self.response(message)
        if chat_history is None:
            chat_history = []

        chat_history.append({"role":"user", "message": message})
        chat_history.append({"role": "chatbot", "message": chatbot_response})

        return chatbot_response, chat_history

#this functions initialises an empty list and returns this list by adding the chatbots response and the users message.

#example sentences to be used in the recording:
#I am feeling anxious about upcoming exams
#please suggest some calming activities
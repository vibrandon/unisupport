import pytest
from app.chat.chatbot.chatbotfile import ChatbotMessager

@pytest.fixture
def chatbot():
    return ChatbotMessager()

def test_for_blank_message(chatbot):
    response, chat_history = chatbot.get_response("")

    assert response is not None, "Sorry, the message cannot be None."
    assert isinstance(response, str), "Sorry, the message needs to be a string."
    assert len(response) > 0, "Sorry, the message was empty."

    assert "I'm sorry, you haven't typed anything; is there anything I can you with today? Try asking about the matching system, feeling stressed or wellbeing profiles!" in response

    assert isinstance(chat_history, list)
    assert len(chat_history) == 2
    assert chat_history[0]["role"] == "user"
    assert chat_history[0]["message"] == ""
    assert chat_history[1]["role"] == "chatbot"
    assert chat_history[1]["message"] == response
#the chat history should contain both the user and the chatbots input to the chat
    response2, chat_history2 = chatbot.get_response(None)

    assert response2 is not None
    assert isinstance(response2, str)
    assert len(response2) > 0

    assert isinstance(chat_history2, list)
    assert len(chat_history2) == 2

# this negative test case checks to ensure a message sent by the user is not none, is a string and that the message sent is not empty it also makes sure the message is not empty.
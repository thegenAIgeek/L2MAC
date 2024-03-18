import pytest
from chat import Chat

def test_chat_creation():
	chat = Chat('Test Chat')
	assert chat.name == 'Test Chat'
	assert isinstance(chat.id, str)
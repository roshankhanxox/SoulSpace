# chatbot/views.py
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
from .models import Conversation
from .serializers import ConversationSerializer
from django.conf import settings

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the chatbot model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start the chat session with the predefined history
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                'You are a friendly and helpful chatbot named "soulBot." Your primary role is to assist users by answering their questions and providing support on various topics, including mental health, general inquiries, and safety concerns.'
            ],
        },
        {
            "role": "model",
            "parts": ["Hello! I'm soulBot. How can I assist you today?"],
        },
    ]
)


class ChatbotAPIView(APIView):
    def post(self, request):
        user_message = request.data.get("message")

        # Send the user's message to the chat session
        response = chat_session.send_message(user_message)

        # Save the conversation to the database
        conversation = Conversation.objects.create(
            user_message=user_message, bot_response=response.text
        )

        # Serialize the conversation for the response
        serializer = ConversationSerializer(conversation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        # Retrieve all conversation history for display
        conversations = Conversation.objects.all().order_by("-created_at")
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

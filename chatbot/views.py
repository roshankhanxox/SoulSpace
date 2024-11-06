# chatbot/views.py
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
from .models import Conversation
from .serializers import ConversationSerializer
from django.conf import settings
from django.core.mail import send_mail
from profiles.models import Friend
from django.contrib.auth.models import User  # Import your Friend model
from rest_framework.exceptions import PermissionDenied

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
                'You are a friendly and helpful chatbot named "soulBot." Your primary role is to assist users by answering their questions and providing support on various topics, including mental health, general inquiries, and safety concerns.YOU also must flag dangerous emotions such as emotions of selfharm by adding the keyword [FLAGS] TO THE END OF YOUR RESPONSE'
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
        print(response)

        # Save the conversation to the database
        conversation = Conversation.objects.create(
            user_message=user_message, bot_response=response.text
        )

        response_text = response._result.candidates[0].content.parts[0].text

        # Check if the response text contains the flag keyword
        if response_text.endswith("[FLAGS] \n"):
            print("flagged")
            # Ensure the user is authenticated
            if not request.user.is_authenticated:
                raise PermissionDenied("You must be logged in to perform this action.")

            user = request.user  # Get the current authenticated user
            user = request.user  # Get the current user
            friends = Friend.objects.filter(user=user)  # Get user's friends
            friend_usernames = [
                friend.friend_user.username for friend in friends
            ]  # Get usernames of friends

            friend_emails = []
            for username in friend_usernames:
                try:
                    # Get the email address for each friend using their username
                    friend_user = User.objects.get(username=username)
                    friend_emails.append(friend_user.email)
                except User.DoesNotExist:
                    # Handle the case where the user does not exist
                    continue  # Assuming Friend model has a friend_user field that links to User
            print(friend_emails)
            user_name = (
                request.user.username
            )  # Get the user's name (you can use 'first_name' or 'full_name' if you prefer)

            # Create a personalized message for the email subject and body
            subject = f"URGENT Your friend {user_name} has is feeling down!!!!!!"
            message_body = f"THIS IS URGENT \n, your friend {user_name} is showcasing selwf harm tendencies. \nPlease help him he needs some human support!!!!!!!!!!!!"

            # Send email notifications to friends
            send_mail(
                subject,
                message_body,
                "ran398321@gmail.com",  # Use your email address
                friend_emails,  # Recipient's email address (friends' emails)
                fail_silently=False,
            )

        # Serialize the conversation for the response
        serializer = ConversationSerializer(conversation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        # Retrieve all conversation history for display
        conversations = Conversation.objects.all().order_by("-created_at")
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Comment, LogEntry
from EmoBotApp.models import UserInteraction, Comment
from EmoBotApp.tasks import generate_content_task, reply_to_comment_task, react_to_comment_task
from django.shortcuts import render
import openai

from .tasks import (
    reply_to_comment_task,
    react_to_comment_task,
    generate_content_task
)

# ...

# Initialize OpenAI DALL-E API key
openai.api_key = 'YOUR_DALLE_API_KEY'



# The custom home view that provides details about the system
def home(request):
    system_info = {
        'system_name': 'EmoBot - The AI Chatbot',
        'system_description': 'EmoBot is an AI-powered chatbot designed to assist users with various tasks and requests.',
        'capabilities': {
            'commands': {
                'gp': {
                    'description': 'Handles all-time research questions.',
                    'example': 'Example: gp: What is the capital of France?',
                },
                'img': {
                    'description': 'Handles image requests.',
                    'example': 'Example: img: Show me pictures of cats.',
                },
                'translate to <language>': {
                    'description': 'Handles translation requests to the specified language.',
                    'example': 'Example: translate to Spanish: Hello, how are you?',
                },
                'img prompt': {
                    'description': 'Handles image prompt generation requests.',
                    'example': 'Example: img prompt: Generate a picture of a beach scene.',
                },
                # Add more commands and their descriptions here...
            },
            'page_management': {
                'post_every_5_hours': {
                    'description': 'Automatically make a post every 5 hours based on the most popular topic.',
                },
                'automatic_comment_replies': {
                    'description': 'Automatically reply to comments on the Facebook page.',
                },
                'automatic_reactions': {
                    'description': 'Automatically react to comments on the Facebook page.',
                },
                # Add more page management abilities and their descriptions here...
            },
        },
        'benefits': {
            'individuals': [
                'Quickly get answers to all-time research questions.',
                'Receive images and translations based on your requests.',
                'Generate image prompts to get customized images.',
                'Enjoy a seamless experience with an AI-powered chatbot.',
            ],
            'companies_startups': [
                'Automate customer support with automatic comment replies.',
                'Engage with users through automatic reactions to comments.',
                'Generate informative posts every 5 hours to keep your audience engaged.',
                'Enhance user interaction and satisfaction with AI capabilities.',
            ],
        },
    }

    return render(request, 'home.html', {'system_info': system_info})



@csrf_exempt
def facebook_webhook(request):
    if request.method == 'GET':
        verify_token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if verify_token == 'YOUR_FACEBOOK_VERIFY_TOKEN':
            return JsonResponse({'hub.challenge': challenge})
        else:
            return HttpResponseBadRequest('Invalid verify token')

    elif request.method == 'POST':
        data = request.body.decode('utf-8')
        try:
            messaging_events = json.loads(data)['entry'][0]['messaging']
            for event in messaging_events:
                if 'message' in event and 'text' in event['message']:
                    message_text = event['message']['text']
                    process_user_message(message_text)
        except KeyError:
            pass

        return JsonResponse({'status': 'success'})
    else:
        return HttpResponseBadRequest('Invalid request method')

# The info function view that returns useful commands and examples
def info(request):
    commands_info = {
        'gp': {
            'description': 'Handles all-time research questions.',
            'example': 'Example: gp: What is the capital of France?',
        },
        'img': {
            'description': 'Handles image requests.',
            'example': 'Example: img: Show me pictures of cats.',
        },
        'translate to <language>': {
            'description': 'Handles translation requests to the specified language.',
            'example': 'Example: translate to Spanish: Hello, how are you?',
        },
        'img prompt': {
            'description': 'Handles image prompt generation requests.',
            'example': 'Example: img prompt: Generate a picture of a beach scene.',
        },
        # Add more commands and their descriptions here...
    }

    return JsonResponse(commands_info)


def process_user_message(message_text):
    # Split the message by ':'
    parts = message_text.split(':', 1)
    if len(parts) == 2:
        command = parts[0].strip()
        actual_text = parts[1].strip()
    else:
        # If there's no ':', assume the entire message is the command
        command = message_text.strip()
        actual_text = ''

    if command == 'gp':
        # Handle 'gp' command (all-time research questions)
        response = handle_gp_command(actual_text)
    elif command == 'img':
        # Handle 'img' command (image handling)
        response = handle_img_command(actual_text)
    elif command == 'img prompt':
        # Handle 'img prompt' command (image prompt generation)
        response = handle_img_prompt_command(actual_text)
    else:
        # Check for 'translate to <language>' command
        parts = command.split(' ')
        if len(parts) >= 3 and parts[0] == 'translate' and parts[1] == 'to':
            target_language = ' '.join(parts[2:]).strip()
            response = handle_translation_command(actual_text, target_language)
        else:
            # Handle unknown commands
            response = "Unknown command. Here are the useful commands:\n\n"
            for command, info in commands_info.items():
                response += f"\n- {command}: {info['description']}\n   {info['example']}"

    # Send the response back to the user via Facebook Messenger API
    send_response_to_messenger(sender_id, response)  # Replace 'sender_id' with the actual sender ID


@csrf_exempt
def analyze_user_interactions(request):
    # Implement logic to analyze user interactions to identify popular topics.
    # Trigger the Celery task to generate content based on popular topics.
    generate_content_task.delay(topic)
    return JsonResponse({'status': 'success'})

@csrf_exempt
def reply_to_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return HttpResponseBadRequest("Comment not found.")

    reply_to_comment_task.delay(comment_id)
    return JsonResponse({'status': 'success', 'message': 'Reply generation initiated.'})

@csrf_exempt
def react_to_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return HttpResponseBadRequest("Comment not found.")

    react_to_comment_task.delay(comment_id)
    return JsonResponse({'status': 'success', 'message': 'Reaction initiated.'})


def handle_gp_command(message_text):
    # Use ChatGPT to generate a response to the user's general research request
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",  # You can choose a different GPT-3 engine based on your subscription.
            prompt=message_text,
            max_tokens=150,  # Adjust the response length based on your preference.
            temperature=0.7,  # Adjust temperature for randomness of responses.
        )
        generated_text = response['choices'][0]['text']
        return generated_text
    except Exception as e:
        return str(e)

def handle_img_command(message_text):
    # Use OpenAI DALL-E API to generate images based on the user's prompt
    try:
        # Request 2 images from DALL-E API using the user's prompt (message_text)
        response = openai.Image.create(model="image-alpha-001", prompt=message_text, n=2)

        # Extract the URLs of the generated images from the API response
        image_urls = [img['url'] for img in response['data']]

        # Return the image URLs as a response to the user
        return image_urls
    except Exception as e:
        return str(e)

def handle_translation_command(message_text, target_language):
    # Use ChatGPT to translate the user's request (message_text) to the specified target_language
    try:
        # Construct the translation prompt
        prompt = f"translate to {target_language}: {message_text}"

        # Request translation from ChatGPT using the prompt
        response = openai.Completion.create(
            engine="text-davinci-002",  # Choose an appropriate engine for translation
            prompt=prompt,
            max_tokens=150,  # Adjust the response length based on your preference.
            temperature=0.7,  # Adjust temperature for randomness of responses.
        )
        
        # Extract the translated text from the API response
        translated_text = response['choices'][0]['text']
        return translated_text
    except Exception as e:
        return str(e)

def handle_img_prompt_command(message_text):
    # Use ChatGPT to generate a useful command prompt for DALL-E image generation
    try:
        # Request the prompt from ChatGPT using the user's message_text
        response = openai.Completion.create(
            engine="text-davinci-002",  # Choose an appropriate engine
            prompt=message_text,
            max_tokens=150,  # Adjust the response length based on your preference.
            temperature=0.7,  # Adjust temperature for randomness of responses.
        )

        # Extract the generated command prompt from the API response
        command_prompt = response['choices'][0]['text']
        return command_prompt
    except Exception as e:
        return str(e)

def send_response_to_messenger(recipient_id, response):
    # ... (same as the previous implementation)
    pass
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from celery import shared_task
import openai
import requests
from datetime import datetime, timedelta
from .models import LogEntry, Comment
import random

# Initialize OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Download NLTK resources
nltk.download('vader_lexicon')

def preprocess_comment(comment_text):
    # Perform preprocessing such as removing stopwords, special characters, and tokenization.
    # For this example, we will do simple tokenization by splitting the comment into words.
    words = comment_text.split()
    return ' '.join(words)

def perform_sentiment_analysis(processed_text):
    # Use sentiment analysis model (e.g., VADER Sentiment) to get sentiment score.
    sentiment_analyzer = SentimentIntensityAnalyzer()
    sentiment_score = sentiment_analyzer.polarity_scores(processed_text)['compound']
    return sentiment_score

def map_reaction(sentiment_score):
    # Determine the appropriate reaction based on the sentiment score.
    if sentiment_score >= 0.5:
        reaction_type = 'love'
    elif sentiment_score >= 0.1:
        reaction_type = 'like'
    elif sentiment_score <= -0.1:
        reaction_type = 'angry'
    else:
        reaction_type = 'wow'
    return reaction_type



AI_TOPICS = [
    "Machine learning",
    "Deep learning",
    "Natural language processing",
    "Computer vision",
    "Artificial intelligence in healthcare",
]

WEB_DEV_TOPICS = [
    "Django web development",
    "Flask web development",
    "Frontend development with React",
    "Backend development with Node.js",
    "Web scraping with Python",
]

def choose_random_topic():
    # Randomly choose between AI topics and web development topics
    topics = random.choice([AI_TOPICS, WEB_DEV_TOPICS])
    return random.choice(topics)

@shared_task
def post_about_topic(topics):
    # Use GPT to generate content based on the selected topic
    content = generate_content_task(topic)
    return


@shared_task
def generate_content_task(topic):
    prompt = f"Given the popularity of {topic}, please provide some insights or content."
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        n=1
    )

    if prompt > 0:
        generated_content = response['choices'][0]['text']
        schedule_post_on_facebook(generated_content)

    log_message = f"Generate Content task initiated for topic: {topic}"
    log_entry = LogEntry(command='post_content', message=log_message)
    log_entry.save()

@shared_task
def schedule_post_on_facebook(content):
    access_token = 'YOUR_FACEBOOK_PAGE_ACCESS_TOKEN'
    post_url = f'https://graph.facebook.com/v12.0/YOUR_FACEBOOK_PAGE_ID/feed'
    post_data = {
        'access_token': access_token,
        'message': content,
        'published': 'false',
        'scheduled_publish_time': (datetime.now() + timedelta(hours=4)).isoformat()
    }

    try:
        response = requests.post(post_url, data=post_data)
        response_json = response.json()

        log_message = f"Post scheduled at {post_data['scheduled_publish_time']}. "
        if 'id' in response_json:
            post_id = response_json['id']
            log_message += f"Post ID: {post_id}"
        else:
            log_message += "Failed to schedule the post."
            log_message += f"Response: {response_json}"

        log_entry = LogEntry(command='schedule_post', message=log_message)
        log_entry.save()

    except requests.RequestException as e:
        log_message = f"Error while scheduling the post: {e}"
        log_entry = LogEntry(command='schedule_post', message=log_message)
        log_entry.save()

@shared_task
def reply_to_comment_task(comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return

    user_comment = comment.text

    prompt = f"User comment: {user_comment}. Please provide a relevant reply."
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1
    )

    if 'choices' in response and len(response['choices']) > 0:
        generated_reply = response['choices'][0]['text']
        post_comment_on_facebook(comment.post_id, generated_reply)

    log_message = f"Reply to Comment task initiated for comment_id: {comment_id}"
    log_entry = LogEntry(command='post_comment', message=log_message)
    log_entry.save()

@shared_task
def react_to_comment_task(comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return

    # Implement logic to analyze user_comment and determine the sentiment or context.
    # For example, assume reaction_type is determined based on some analysis.
    reaction_type = 'like'

    react_to_comment_on_facebook(comment_id, reaction_type)

    log_message = f"React to Comment task initiated for comment_id: {comment_id}"
    log_entry = LogEntry(command='react_to_comment', message=log_message)
    log_entry.save()



def post_comment_on_facebook(post_id, reply):
    access_token = 'YOUR_FACEBOOK_PAGE_ACCESS_TOKEN'
    comment_url = f'https://graph.facebook.com/v12.0/{post_id}/comments'
    comment_data = {
        'access_token': access_token,
        'message': reply
    }

    try:
        response = requests.post(comment_url, data=comment_data)
        response_json = response.json()

        if response.status_code == 200:
            log_message = f"Comment '{reply}' added to post {post_id} successfully."
        else:
            log_message = "Failed to add comment to the post."
            log_message += f"Response: {response_json}"

        log_entry = LogEntry(command='post_comment', message=log_message)
        log_entry.save()

    except requests.RequestException as e:
        log_message = f"Error while posting the comment: {e}"
        log_entry = LogEntry(command='post_comment', message=log_message)
        log_entry.save()


def react_to_comment_on_facebook(comment_id, reaction_type):
    access_token = 'YOUR_FACEBOOK_PAGE_ACCESS_TOKEN'
    reaction_url = f'https://graph.facebook.com/v12.0/{comment_id}/reactions'
    reaction_data = {
        'access_token': access_token,
        'type': reaction_type
    }

    try:
        response = requests.post(reaction_url, data=reaction_data)
        response_json = response.json()

        if response.status_code == 200:
            log_message = f"Reaction '{reaction_type}' added to comment {comment_id} successfully."
        else:
            log_message = "Failed to add reaction to the comment."
            log_message += f"Response: {response_json}"

        log_entry = LogEntry(command='react_to_comment', message=log_message)
        log_entry.save()

    except requests.RequestException as e:
        log_message = f"Error while adding the reaction: {e}"
        log_entry = LogEntry(command='react_to_comment', message=log_message)
        log_entry.save()

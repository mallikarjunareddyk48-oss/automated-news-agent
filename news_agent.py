import os
import smtplib
from email.mime.text import MIMEText
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo

# 1. Configure the AI Agent
agent = Agent(
    model=OpenAIChat(
        id="google/diffusiongemma-26b-a4b-it", 
        api_key=os.environ.get("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"),
        base_url="https://integrate.api.nvidia.com/v1"
    ),
    tools=[DuckDuckGo()],
    show_tool_calls=False # Keeps the output clean
)

# 2. Tell the AI what to search for
prompt = """
Search the web for the most important news from the past hour in these 3 categories:
1. Breaking Global/India News
2. Technology News
3. AI (Artificial Intelligence) News
Summarize the top stories in clean, easy-to-read bullet points.
"""

print("Fetching news...")
response = agent.run(prompt)
news_summary = response.content

# 3. Configure the Email Sender using secure environment variables
sender_email = os.environ.get("GMAIL_ADDRESS")
sender_password = os.environ.get("GMAIL_APP_PASSWORD")
receiver_email = sender_email # Sending the news to yourself

# 4. Format the Email
msg = MIMEText(news_summary)
msg['Subject'] = 'Hourly Update: Breaking, Tech & AI News'
msg['From'] = sender_email
msg['To'] = receiver_email

# 5. Send the Email
print("Sending email...")
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(sender_email, sender_password)
    server.send_message(msg)

print("Success! News sent to your inbox.")

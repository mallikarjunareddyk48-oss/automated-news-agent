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
    show_tool_calls=False
)

# 2. Tell the AI EXACTLY what to do (Now asking for Links!)
prompt = """
Search the web for the most important news from the past hour in these 3 categories:
1. Breaking Global/India News
2. Technology News
3. AI (Artificial Intelligence) News

For EVERY news item you find, you MUST provide:
- A clear Headline
- A short 2-3 line detailed summary of what happened
- The ORIGINAL URL LINK (Source link) to read the full article.

Format the output cleanly so it is easy to read in an email.
"""

print("Fetching news with links...")
response = agent.run(prompt)
news_summary = response.content

# 3. Configure the Email Sender
sender_email = os.environ.get("GMAIL_ADDRESS")
sender_password = os.environ.get("GMAIL_APP_PASSWORD")
receiver_email = sender_email

# 4. Format the Email
msg = MIMEText(news_summary)
msg['Subject'] = 'Hourly Update: Detailed News with Links 🔗'
msg['From'] = sender_email
msg['To'] = receiver_email

# 5. Send the Email
print("Sending email...")
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(sender_email, sender_password)
    server.send_message(msg)

print("Success! News with links sent to your inbox.")

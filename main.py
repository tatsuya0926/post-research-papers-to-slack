import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging
from database.database import Database
from config import SLACK_API_TOKEN, SLACK_CHANNEL, DATABASE_NAME
from utils.utilts import get_papers, fetch_interesting_points, fetch_summary

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

db = Database(DATABASE_NAME)
db.init_database()

client = WebClient(token=SLACK_API_TOKEN)


def post_to_slack(main_text, reply_text):
    try:
        main_response = client.chat_postMessage(channel=SLACK_CHANNEL, text=main_text)
        thread_ts = main_response["ts"]
        reply_response = client.chat_postMessage(channel=SLACK_CHANNEL, text=reply_text, thread_ts=thread_ts)
    except SlackApiError as e:
        logger.error(f"Error posting to Slack: {e}")

def main():
    try:
        paper = get_papers(db)
        summary = fetch_summary(paper)
        interesting_points = fetch_interesting_points(paper)
        main_text = f"""
        *タイトル:* {paper.title}
        *著者名:* {paper.authors}
        *リンク:* {paper.url}
        """

        reply_text = f"""
        *概要:*\n{summary}
        *提出日:* {paper.submitted}
        *面白いポイント:*\n{interesting_points}
        ChatPDFで読む: https://www.chatpdf.com/
        """
        post_to_slack(main_text, reply_text)
        logger.info(f"Posted a paper: {paper.title}")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()

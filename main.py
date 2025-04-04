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


def post_to_slack(text):
    try:
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=text)
    except SlackApiError as e:
        logger.error(f"Error posting to Slack: {e}")

def main():
    try:
        paper = get_papers(db)
        summary = fetch_summary(paper)
        interesting_points = fetch_interesting_points(paper)
        text = f"""
            *タイトル: {paper.title}*\n\n
            *概要*\n{summary}\n\n
            *リンク*\n{paper.url}\n\n
            *提出日*\n{paper.submitted}\n\n
            *以下、面白いポイント*\n{interesting_points}\n\n
            ChatPDFで読む: https://www.chatpdf.com/ \n\n
            論文を読む: {paper.url}.pdf
        """
        post_to_slack(text)
        logger.info(f"Posted a paper: {paper.title}")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()

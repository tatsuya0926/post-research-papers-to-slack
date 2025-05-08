import arxiv
import ollama
import pytz
import time
import logging
from pydantic import BaseModel
from typing import List
from config import SEARCH_KEYWORDS, SEARCH_AUTHORS

logger = logging.getLogger(__name__)


def retry_on_error(func, retries=3, delay=5):
    def wrapper(*args, **kwargs):
        for _ in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Error: {e}, Retrying...")
                time.sleep(delay)
        logger.error("Exceeded maximum retries.")
        return None

    return wrapper


class ArxivResponse(BaseModel):
    entry_id: str
    title: str
    authors: str
    summary: str
    url: str
    submitted: str


def fetch_interesting_points(result):
    response = ollama.chat(
        model="schroneko/gemma-2-2b-jpn-it", 
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"""
                以下の論文がどういう点で面白いかについて理系専門家向けに解説し、論文の本文を読みたくなるように魅力づけをして促して下さい。\n論文タイトル: {result.title}\n概要: {result.summary}"""
            },
        ],
    )
    content = response["message"]["content"].strip()
    return content


def fetch_summary(result):
    response = ollama.chat(
        model="schroneko/gemma-2-2b-jpn-it",
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"""論文タイトル: {result.title}\n概要: {result.summary}\n\n日本語の箇条書き（・で表記）で要約してください。""",
            },
        ],
    )
    summary = response["message"]["content"].strip()
    return summary


def get_papers(
    db,
    keyword: List[str] = SEARCH_KEYWORDS,
    authors: List[str] = SEARCH_AUTHORS,
    max_results: int = 20,
    max_pages: int = 5,
):
    title_query = " OR ".join(f'ti:"{k}"' for k in keyword)
    if authors:
        author_query = " OR ".join(f'au:"{a}"' for a in authors)
        query = f"({title_query}) OR ({author_query})"
    else:
        query = title_query

    exclude_ids = set(db.get_excluded_papers())
    tz = pytz.timezone("Asia/Tokyo")

    for page in range(max_pages):
        total_to_fetch = max_results * (page + 1)
        search = arxiv.Search(
            query=query,
            max_results=total_to_fetch,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        all_results = list(search.results())

        start_idx = page * max_results
        end_idx = start_idx + max_results
        page_results = all_results[start_idx:end_idx]

        for result in page_results:
            if result.entry_id in exclude_ids:
                continue

            submitted_jst = result.published.astimezone(tz)
            submitted_fmt = submitted_jst.strftime("%Y年%m月%d日 %H時%M分%S秒")
            authors_str = ", ".join(a.name for a in result.authors)

            resp = ArxivResponse(
                entry_id=result.entry_id,
                title=result.title,
                authors=authors_str,
                summary=result.summary,
                url=result.pdf_url,
                submitted=submitted_fmt,
            )
            db.add_paper(result.entry_id)
            logger.info(f"INSERT : {result.entry_id} / {result.title}")
            return resp

        if len(page_results) < max_results:
            break

    raise LookupError(f"No new papers found for query: {query!r}")
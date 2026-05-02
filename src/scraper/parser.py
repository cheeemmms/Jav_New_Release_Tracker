import arrow

from src.scraper.engine import random_delay


def parse_star_page(soup, star_name, cutoff_date_str):
    cutoff = arrow.get(cutoff_date_str, "YYYY-MM-DD")
    results = []

    movie_items = soup.select("a.movie-box")

    for item in movie_items:
        title_elem = item.select_one(".photo-frame img")
        title = title_elem.get("title", "") if title_elem else ""

        url = item.get("href", "")
        if url and not url.startswith("http"):
            url = f"https://www.javbus.com{url}"

        date_elem = item.select_one("date")
        raw_date = date_elem.text.strip() if date_elem else ""
        if len(raw_date) > 10:
            raw_date = raw_date[-10:]

        movie_date = None
        try:
            movie_date = arrow.get(raw_date, "YYYY-MM-DD")
        except Exception:
            try:
                movie_date = arrow.get(raw_date)
            except Exception:
                continue

        if movie_date < cutoff:
            break

        is_vr = "VR" in title or "【VR】" in title
        if is_vr:
            continue

        results.append({
            "title": title,
            "url": url,
            "date": raw_date,
            "star": star_name,
        })

        random_delay(0.1, 0.3)

    return results

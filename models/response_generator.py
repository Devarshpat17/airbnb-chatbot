import json
from transformers import pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def extract_fields(doc):
    data = doc.get('data', {})
    return {
        "Host Name": data.get('host', {}).get('name', 'N/A'),
        "Property Name": data.get('name', 'N/A'),
        "Summary": data.get('summary', 'N/A'),
        "Price": data.get('price', 'N/A'),
        "Address": data.get('address', {}).get('street', 'N/A')
    }


def filter_reviews(raw_data):
    """Return a copy of raw_data without the 'reviews' field."""
    if isinstance(raw_data, dict):
        filtered = dict(raw_data)
        filtered.pop('reviews', None)
        return filtered
    return raw_data

def extract_reviews(raw_data):
    """Extract reviews from raw_data, if present."""
    if isinstance(raw_data, dict):
        return raw_data.get('reviews', [])
    return []

def generate_response(docs, query):
    # Deduplicate and only use the top 3 docs
    seen = set()
    unique_docs = []
    for d in docs:
        snippet = str(d['data'])[:512]
        if snippet not in seen:
            seen.add(snippet)
            unique_docs.append(d)
        if len(unique_docs) == 3:
            break

    results = []
    for doc in unique_docs:
        fields = extract_fields(doc)
        results.append((fields, doc['data']))  # Save both fields and raw data

    # Check if the query is about reviews
    query_lower = query.lower()
    wants_reviews = "review" in query_lower or "rating" in query_lower or "feedback" in query_lower

    response_lines = []
    for idx, (fields, raw_data) in enumerate(results, 1):
        if wants_reviews:
            # Only show reviews, summarize everything else
            reviews = extract_reviews(raw_data)
            other_info = dict(raw_data)
            other_info.pop('reviews', None)
            # Summarize other info (excluding description/summary)
            other_info.pop('summary', None)
            summary_text = json.dumps(other_info, indent=2, ensure_ascii=False)
            # Optionally, summarize the summary_text if too long (commented for accuracy)
            # if len(summary_text) > 300:
            #     summary = summarizer(
            #         summary_text,
            #         max_length=60,
            #         min_length=20,
            #         do_sample=False,
            #         clean_up_tokenization_spaces=True,
            #         no_repeat_ngram_size=3
            #     )
            #     summary_text = summary[0]['summary_text']
            response_lines.append(
                f"--- Property {idx} Reviews ---\n"
                f"Other Info:\n{summary_text}\n"
                f"Reviews:\n{json.dumps(reviews, indent=2, ensure_ascii=False) if reviews else 'No reviews found.'}\n"
            )
        else:
            # Default: show all fields, but filter out reviews from source JSON
            filtered_data = filter_reviews(raw_data)
            response_lines.append(
                f"--- Property {idx} ---\n"
                f"Host Name: {fields['Host Name']}\n"
                f"Property Name: {fields['Property Name']}\n"
                f"Summary: {fields['Summary']}\n"
                f"Price: {fields['Price']}\n"
                f"Address: {fields['Address']}\n"
                f"Source JSON:\n{json.dumps(filtered_data, indent=2, ensure_ascii=False)}\n"
            )
    return "\n".join(response_lines)

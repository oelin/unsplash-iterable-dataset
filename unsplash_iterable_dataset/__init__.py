from io import BytesIO
import json
from typing import Dict, Iterable, List, Optional
import random

import datasets
import PIL
from PIL import Image
import requests


UNSPLASH_RESULTS_URL = 'https://unsplash.com/napi/topics/{}/photos?page={}&per_page=16'


def download_image(url: str) -> Optional[PIL.Image.Image]:
    """Download an image."""

    try:
        response = requests.get(url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))

        return image
    except:
        return


def download_unsplash_results(topic: str, cursor: int) -> Optional[List]:
    """Download Unplash results."""

    try:
        response = requests.get(UNSPLASH_RESULTS_URL.format(topic, cursor))
        response = json.loads(response.text)

        results = response or None

        return results
    except:
        return


def process_unsplash_results(topic: str, results: List) -> Iterable[Dict]:
    """Process unsplash results."""

    for result in results:

        # Required fields.

        if result.get('plus'): continue
        if not (text := result.get('alt_description')): continue
        if not (urls := result.get('urls')): continue
        if not (image_url := urls.get('full')): continue
        if not (image := download_image(image_url)): continue

        # Optional fields.

        id = result.get('id')

        result = {
            'id': id,
            'image': image,
            'text': text,
            'topic': topic,
        }

        yield result


def search_unsplash(topics: List[str], limit: int) -> Iterable[Dict]:
    """Search Unsplash and yield results."""

    cursors = {topic: 0 for topic in topics}  # Cursors for each topic.
    counter = 0
    ids = {}

    while counter < limit:
        topic = random.choice(topics)
        cursor = cursors[topic]
        cursors[topic] += 1
        results = download_unsplash_results(topic, cursor)

        if not results:
            cursor[topic] = 0  # We've reached the end of this topic.
            continue
        
        for result in process_unsplash_results(topic, results):

            # Omit duplicates.

            if (id := result.get('id')):
                if ids.get(id):
                    continue
                else:
                    ids[id] = True
                
            yield result

            counter += 1


def UnsplashIterableDataset(
    topic: str,
    limit: int,
) -> datasets.IterableDataset:
    """Unsplash iterable dataset."""

    generator = lambda: search_unsplash([topic], limit)
    dataset = datasets.IterableDataset.from_generator(generator)

    return dataset

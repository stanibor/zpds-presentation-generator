import openai
from typing import List

openai.api_key = "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"
TEXT_MODEL = "text-davinci-003"


def key_words_list2str(key_words: List[str]):
    """
    This method is used to convert list of key words to string
    :param key_words: list of key words
    :return: string of key words
    """
    key_words_str = ''
    for word in key_words:
        key_words_str += word
        key_words_str += ', '
    return key_words_str[:-2]


def generate_title_slide(key_words: list):
    """
    This method is used to generate title slide for presentation
    :param key_words: list of keywords
    :return: title of presentation
    """
    prompt = f'Generate short title of presentation based on key words: {key_words_list2str(key_words)} without quotation marks'
    title = openai.Completion.create(engine=TEXT_MODEL, prompt=prompt, max_tokens=100).choices[0].text
    return title.replace('\n', '')


def generate_introduction_speech(presenatation_title: str):
    """
    This method is used to generate introduction speech for presentation
    :param presenatation_title: title of presentation
    :return: introduction speech string for presentation
    """
    prompt = f'Assume you are presenter. Generate introduction for presentation about: {presenatation_title}. Max 50 words in string format.'
    intro = openai.Completion.create(engine=TEXT_MODEL, prompt=prompt, max_tokens=500).choices[0].text
    return intro.replace('\n', '')


def generate_slide_titles(key_words: List[str], number_of_slides: int):
    """
    This method is used to generate slide titles for presentation
    :param key_words: list of keywords
    :param number_of_slides: number of slides in presentation
    :return: list of slide titles
    """
    prompt = f'Generate {number_of_slides} slide titles for whole presentation based on keywords: {key_words_list2str(key_words)} separated by comas without quotation marks and without numeration. Max 7 words.'
    titles = openai.Completion.create(engine=TEXT_MODEL, prompt=prompt, max_tokens=500).choices[0].text
    return titles.strip().split(', ')


def generate_slide_caption(slide_title: str):
    """
    This method is used to generate slide caption for slide
    :param slide_title: title of slide
    :return: slide caption string
    """
    prompt = f'Generate slide text as string based on title: {slide_title}. Maximum 15 words.'
    slide_text = openai.Completion.create(engine=TEXT_MODEL, prompt=prompt, max_tokens=500).choices[0].text
    return slide_text.replace('\n', '')


def generate_slide_speech_description(slide_title: str):
    """
    This method is used to generate slide description speech for slide
    :param slide_title: title of slide
    :return: slide description speech string
    """
    prompt = f'Generate slide description speech as string based on title: {slide_title}. Maximum 100 words in string format'
    slide_text = openai.Completion.create(engine=TEXT_MODEL, prompt=prompt, max_tokens=4000).choices[0].text
    return slide_text.replace('\n', '')


def generate_summary_speech(presentation_title: str):
    """
    This method is used to generate summary speech for presentation
    :param presentation_title: title of presentation
    :return: summary speech string
    """
    prompt = f'Assume you are presenter. Generate summary for presentation about: {presentation_title}. Max 50 words in string format.'
    summary = openai.Completion.create(engine=TEXT_MODEL, prompt=prompt, max_tokens=500).choices[0].text
    return summary.replace('\n', '')


# based on https://medium.com/geekculture/scrape-google-inline-images-with-python-85837af2fe17
import requests, lxml, re, urllib.parse, base64
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def get_image_for_slide(slide_title: str, slide_number: int):
    """
    This method is used to get image for slide. It is based on google search.
    It tries to download first image from google search and save it to images folder.
    :param slide_title: title of slide
    :param slide_number: number of slide
    :return: tuple with boolean if image was downloaded or not and path to image
    """
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    print(slide_title)
    params = {
        "q": slide_title,
        "sourceid": "chrome"
    }
    with requests.session() as session:
        html = session.get("https://www.google.com/search", cookies={'CONSENT': 'YES+'}, params=params, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    for result in soup.select('div[jsname=dTDiAc]'):
        link = f"https://www.google.com{result.a['href']}"
        being_used_on = result['data-lpage']
        print(f'Link: {link}\nBeing used on: {being_used_on}\n')

    # finding all script (<script>) tags
    script_img_tags = soup.find_all('script')

    # https://regex101.com/r/L3IZXe/4
    img_matches = list(enumerate(re.findall(r"s='data:image/jpeg;base64,(.*?)';", str(script_img_tags))))
    if len(img_matches):
        try:
            final_image = Image.open(BytesIO(base64.b64decode(str(img_matches[0][1]))))
            final_image.save(f'slide_image_{slide_number}.jpg', 'JPEG')
            print("Image ok")
            return True, f'slide_image_{slide_number}.jpg'
        except:
            print("Image couldn't be saved")
            return False, ''
    else:
        print("Image scrapper failed to scrap images")
        return False, ''


def get_presentation_data(key_words: List[str], n_of_slides: int):
    """
    This method is used to generate presentation data.
    :param key_words: list of keywords
    :param n_of_slides: number of slides in presentation
    :return: dictionary with presentation data
    """
    example_generated_data = {}
    title = generate_title_slide(key_words)
    example_generated_data["title"] = title
    example_generated_data["introduction_speech"] = generate_introduction_speech(title)
    example_generated_data["intro_image"] = get_image_for_slide(title, 0)
    example_generated_data['slides'] = []
    slide_titles = generate_slide_titles(key_words, n_of_slides)
    texts = [generate_slide_caption(slide_title) for slide_title in slide_titles]
    speeches = [generate_slide_speech_description(slide_title) for slide_title in slide_titles]
    i = 1
    for slide_title, text, speech in zip(slide_titles, texts, speeches):
        slide = {
            'title': slide_title,
            'text': text,
            'img': get_image_for_slide(slide_title, i),
            'speech': speech
        }
        i += 1
        example_generated_data['slides'].append(slide)
    example_generated_data['summary'] = generate_summary_speech(title)

    return example_generated_data

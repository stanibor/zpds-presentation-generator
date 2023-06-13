# ZPDS Presentation Generator

## Overall view

**ZPDF Presentation Generator** is an application for automated creation of .pptx presentations about any topic based on given keywords. Presentation slides, slides descriptions and voiceover are created.

## Technology used
Python is used as programming language for this project.
Main libraries, frameworks and models used are:
* Streamlit - framework used to create App
* Chat GPT3 - (openai library) - language model for creation of presentation content
* pptx - library for managing .pptx presentations
* torch and speechbrain - libraries used for text-to-speech conversion
* ngrok - app for exposing our application to the internet

## ChatGPT

The operation of the module responsible for generating presentations can be divided into 2 stages:

1. Generation of slide titles based on keywords.
2. On slied title basis, the content of the note to be spoken is then generated, as well as the search for a photo, which is then downloaded and inserted into the presentation.
The solution utilise "text-davinci-003 "language model provided by openAI. At this point, there is one predefined template written using the python-pttx library containing generative placement of elements on the initial (title), middle (title description and photo) and final (thank you) slides.

## Structure

The overall UI application is defined in app.py file.

Additional functions are defined in audio_functions.py and defined_functions.py. The former file consists functions related to text-to-speech model, while the other file consists functions creating and managing the pptx presentation.

## Installing dependencies

In order to install all required libraries generate a virtual environment:
```
python3 -m venv PATH/TO/VENV
```
and activate it:
```
source PATH/TO/VENV/bin/activate
```
Make sure you have poetry installed:
```
pip install poetry
```
Then install all required libraries using poetry:
```
poetry install
```



## Use

In order to run ZPDS Presentation Generator locally use command:
```
streamlit run app.py
```

In order to expose the application to the internet **ngrok** is used. Use command:
```
ngrok http 8501
```
to obtain _web link_ which you can use to access the app.

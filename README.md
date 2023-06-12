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

## Structure

The overall UI application is defined in app.py file.

Additional functions are defined in audio_functions.py and defined_functions.py. The former file consists functions related to text-to-speech model, while the other file consists functions creating and managing the pptx presentation.

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

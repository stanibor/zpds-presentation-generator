import streamlit as st
from pptx import Presentation
from pptx.util import Inches
from defined_functions import key_words_list2str, generate_title_slide, generate_introduction_speech, generate_slide_titles, generate_slide_caption, generate_slide_speech_description, generate_summary_speech, get_image_for_slide, get_presenation_data


def main():
    st.markdown("<h1 style='text-align: center; color: White;background-color:#e84343'>Presentation Creator</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: Black;'>Drop in The required Inputs and we will do  the rest.</h3>", unsafe_allow_html=True)
    st.sidebar.header("What is this Project about?")
    st.sidebar.text("It a Web app that would help the user create presentations and present them.")
    st.sidebar.header("What tools where used to make this?")
    st.sidebar.text("Chat GPT3 and more.")

    n_of_slides = st.number_input("Input number of core slides",1,20)
    words = st.text_input("Input context words, semicolon separated")
    list_of_words = words.split(";")

    if 'dwn_avail' not in st.session_state:
        st.session_state.dwn_avail = 0
    if 'dwn_avi_avail' not in st.session_state:
        st.session_state.dwn_avi_avail = 0

    if st.button("Generate slides"):
        with st.spinner('Wait for it...'):
            st.session_state.dwn_avail = 1
            data = get_presenation_data(list_of_words, n_of_slides)
            with open('slide_notes.txt', 'w', encoding="utf8") as f:
                f.write(data['introduction_speech'])
                for slide_data in data['slides']:
                    f.write(slide_data['speech'])
                    f.write('\n')
                f.write(data['summary'])

            pres = Presentation()

            #Slide Intro

            slide = pres.slides.add_slide(pres.slide_layouts[2])
            title_shape = slide.shapes.title
            title_shape.text = data['title']
            left = top = Inches(2)
            width = height = Inches(3)

            #Slides

            for slide_data in data['slides']:
                slide_layout = pres.slide_layouts[1]  # Use layout with title and content
                slide = pres.slides.add_slide(slide_layout)
                # Set the slide title
                title = slide.shapes.title
                title.text = slide_data['title']
                # Add a text field
                content = slide.placeholders[1]  # Use the second placeholder for content
                content.text = slide_data['text']
                # Add a picture
                picture_path = slide_data['img'][1]  # Replace with the actual path to your picture
                left = Inches(4)  # Adjust the position of the picture
                top = Inches(4)
                width = Inches(4)  # Adjust the size of the picture
                height = Inches(3)
                if len(slide_data['img'][1]):
                    slide.shapes.add_picture(picture_path, left, top, width, height)

            slide = pres.slides.add_slide(pres.slide_layouts[2])
            title_shape = slide.shapes.title
            title_shape.text = 'Thank you'
            left = top = Inches(2)
            width = height = Inches(3)

            pres.save('presentation.pptx')
        st.success('Done!')
    
    if st.session_state.dwn_avail == 1:
        with open('presentation.pptx', "rb") as file:  # , encoding="ISO-8859-1"
            btn = st.download_button(
                    label="Download presentation .pptx",
                    data=file,
                    file_name='presentation.pptx',
                    disabled=(st.session_state.dwn_avail == 0)
                )
            presentation = file
        with open('slide_notes.txt', "r", encoding="utf8") as file:
            btn = st.download_button(
                    label="Download slide notes .txt",
                    data=file,
                    file_name='slide_notes.txt',
                    disabled=(st.session_state.dwn_avail == 0)
                )
            slide_notes = file

    presentation_dl = st.file_uploader("Upload presentation .pptx")
    slide_notes_dl = st.file_uploader("Upload slide notes .txt")
    voice_sample = st.file_uploader("Upload voice sample .wav")

    if st.button("Generate a spoken presentation"):
        if presentation is None or slide_notes is None or voice_sample is None:
            st.write("Files are not provided!")
        else:
            st.session_state.dwn_avi_avail = 1

    st.download_button("Download spoken presentation .avi", "123", disabled=(st.session_state.dwn_avi_avail == 0))


if __name__ == '__main__':
    main()

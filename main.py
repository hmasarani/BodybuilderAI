import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
from streamlit_option_menu import option_menu
import time


template = """
    Below are user inputs for a workout split based on TNF (A bodybuilder)
    Your goal is to:
    - Properly generate a workout (sets AND Reps)
    - Convert the input to a specified work out split

    Here is an example of workout split by TNF:
    (Always use similar variations) + (Always 5 sets per body part per workout with exception to legs)
        1- Chest:
            a) Machine Chest Press: 2 Sets (6-8 repetitions) to failure
            b) Incline Smith Machine Press: 2 set (6-8 repetitions) to failure
            c) Machine Chest Flies: 1 set (6-8 repetitions) to failure
        2- Back And Triceps
            a) Single-Hand Cable Pull downs: 2 Sets (6-8 repetitions) to failure
            b) Incline Smith Machine Rows (Upper Back) with incline seat: 2 set (6-8 repetitions) to failure
            c) Close grip rows: 1 set (6-8 repetitions) to failure
            d) JM Press: 2 set (6-8 repetitions) to failure
            e) Tricep cable pushdowns: 2 set (6-8 repetitions) to failure 
        3- Shoulders & Biceps
            a) Smith Machine Barbell Shoulder Press: 2 Sets (6-8 repetitions) to failure
            b) Cable Lateral Raises: 2 set (6-8 repetitions) to failure
            c) Reverse Machine Flies: 1 set (6-8 repetitions) to failure
            d) Preacher Machine curls: 2 sets (6-8 repetitions) to failure
            e) Hammer Curls: 2 sets (6-8 repetitions) to failure 
        4- Legs
            a) Hack Squats: 2 Sets (6-8 repetitions) to failure
            b) Sissy Squats: 2 set (6-8 repetitions) to failure
            c) Seated Hamstring Curls: 1 set (6-8 repetitions) to failure
            d) Calve raises: 1 sets (6-8 repetitions) to failure


    Please start with 'This workout is brought you by TNF' 

    Use Bullet points only.

    Your response is ALWAYS variations of the workout examples provided. 
    
    IMPORTANT!:  Don't provide the same list from the above given. However, Keep the number of sets the same.

    IMPORTANT: Write a short explanation of how to perform each exercise after listing the exercise. 
    
    Below is the bodybuilder and body part:
    BODYBUILDER: {bodybuilder}
    BODY PART: {bodypart}
    
    YOUR RESPONSE:
"""
#from langchain
prompt = PromptTemplate(
    input_variables=["bodybuilder", "bodypart"],
    template=template,
)

#from openAI
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.2, openai_api_key=openai_api_key)
    return llm


st.set_page_config(layout="wide")

selected = option_menu(None, ["Home", 'Contact'], 
    icons=['house', 'inbox'], 
    menu_icon="cast", default_index=0, orientation="horizontal")


if selected == "Home": 
    col1, col2 = st.columns(2)

    with col1: 
        st.markdown("## Fitness influencers have different perspectives on what's considered an :blue[\"Optimal\"] workout style for hypertrophy. \n\n### This A.I tool \
                    will help you customize your workouts based on your favourite Fitness influencer! your inputs will be converted into a workout based on information collected from influencers such as :blue[TNF, JPG Coaching], and many more [coming soon...]. \n\n This tool \
                    is powered by [LangChain](https://langchain.com/) and [OpenAI](https://openai.com) and made by \
                    [@HMasarani](https://linkedin.com/in/hmasarani). \n\n View Source Code on [Github](https://github.com/hmasarani/BodybuilderAI/blob/main/main.py)")

    with col2:
        st.image(image='TNF.jpg', width=500, caption='TNF')


    st.markdown("## Try Now, For Free! ")
    st.header("Create Your Workout :blue[_in seconds_], optimally and easily")
    def get_api_key():
        user_input = st.text_area(label= "Enter OPENAI API Key", placeholder="Enter your OpenAI API Key", key="openai_api_key_input")
        return user_input
    
    openai_api_key = get_api_key()
    col1, col2 = st.columns(2)
    with col1:
        option_bodybuilder = st.selectbox(
            'Which style would you like to try?',
            ('TNF', 'TNF'))
        
    with col2:
        if option_bodybuilder == 'TNF':
            option_bodyPart = st.selectbox(
            'Which Body Part would like to train?',
            ('Chest', 'Back & Triceps', 'Shoulders & Biceps', 'Legs'))

    st.button(label="go")

    if option_bodyPart and option_bodybuilder and st.button:
        if not openai_api_key:
            st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
            st.stop()        
        
        llm = load_LLM(openai_api_key = openai_api_key)
        prompt_with_info =  prompt.format(bodybuilder = option_bodybuilder, bodypart = option_bodyPart)


        workout = llm(prompt_with_info)

        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.2)
            my_bar.progress(percent_complete + 10, text=progress_text)
        
        st.write("Results: ")
        st.write(workout)


if selected == "Contact":
    st.header(":mailbox: Get In Touch With Me!")


    contact_form = """
    <form action="https://formsubmit.co/masaranihassan@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="Name">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Submit</button>
    </form>
    """

    

    st.markdown(contact_form, unsafe_allow_html=True)

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("style.css")

    








import streamlit as st
import asyncio
from datetime import datetime, timedelta
from clients.d_id import DIdClient
from clients.heygen import create_heygen_video
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch API key from environment variables
d_id_api_key = os.getenv('D_ID_API_KEY')

# Initialize DIdClient with the API key from environment variable
d_id_client = DIdClient(api_key=d_id_api_key)

async def check_video_status_async(d_id_client, talk_id, timeout=600):
    start_time = datetime.now()
    with st.spinner("Video is being processed..."):
        while not d_id_client.is_video_ready(talk_id):
            # Check if the timeout has been reached
            if (datetime.now() - start_time).seconds > timeout:
                st.error("Video processing timed out.")
                return None
            await asyncio.sleep(30)  # Increase the interval to reduce requests
    return d_id_client.get_video_url(talk_id)

def generate_video(edited_script):
    # Initialization
    if 'video_engine' not in st.session_state:
        st.session_state['video_engine'] = 'D-ID'
    video_engine_choice = st.session_state['video_engine']

    # Log the video generation engine
    st.write(f"Generating Video with {video_engine_choice}...")

    # Decide which video engine to use
    if video_engine_choice == "Heygen":
        video_url = create_heygen_video(edited_script)
        if video_url:
            st.write(f"Video created successfully! [Watch here]({video_url})")
        else:
            st.error("Failed to create video.")
    else:
        st.write("Video Generation with D-ID")

        # File uploader for source video
        uploaded_file = st.file_uploader("Upload a source video file", type=["mp4", "mov", "avi"])
        if uploaded_file is None:
            st.warning("Please upload a source video file to proceed.")
            return None

        # Save the uploaded file to a temporary location
        temp_video_path = f"temp_{uploaded_file.name}"
        with open(temp_video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Create a talk for D-ID video generation
        talk = d_id_client.create_talk(temp_video_path, edited_script)
        talk_id = talk.get("id")
        print(f"Talk ID: {talk_id}")

        # Check if the video is ready with timeout
        video_url = asyncio.run(check_video_status_async(d_id_client, talk_id, timeout=600))
        if video_url:
            st.write(f"Video URL: {video_url}")
            # Preview the video
            st.video(video_url)
        else:
            st.error("Failed to create video.")

    return video_url

# Example usage
if __name__ == "__main__":
    st.title("Video Generation Tool")
    edited_script = st.text_area("Enter the script for the video:")
    if st.button("Generate Video"):
        if edited_script.strip():
            generate_video(edited_script)
        else:
            st.warning("Please enter a script to proceed.")

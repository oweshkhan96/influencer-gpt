import streamlit as st
from app.create_video_script import create_video_script
from app.generate_video import generate_video
from app.get_trends import get_trends
from app.upload_video import upload_video

# Application Title
st.title("Influencer GPT")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    ["Home", "Get Trends", "Create Video Script", "Generate Video", "Upload Video"]
)

# Page: Home
if page == "Home":
    st.header("Welcome to Influencer GPT")
    st.write("Use this app to generate viral videos, explore trends, and automate your influencer workflow.")

# Page: Get Trends
elif page == "Get Trends":
    st.header("Discover Trends")
    query = st.text_input("Enter a topic to search trends:")
    source = st.radio("Select trend source:", options=["Twitter", "GPT"], index=1)

    if st.button("Find Trends"):
        if query.strip():
            trends = get_trends(query, st.session_state)
            st.write("Here are the top trends:")
            for trend in trends:
                st.write(f"- {trend}")
        else:
            st.warning("Please enter a topic to search trends.")

# Page: Create Video Script
elif page == "Create Video Script":
    st.header("Create a Viral Video Script")
    topic = st.text_input("Enter a topic for the video:")
    if st.button("Generate Script"):
        if topic.strip():
            script = create_video_script(topic)
            st.text_area("Generated Script", script, height=200)
        else:
            st.warning("Please enter a topic to generate a script.")

# Page: Generate Video
elif page == "Generate Video":
    st.header("Generate Video")
    edited_script = st.text_area("Enter or edit your video script:")
    source_url = st.text_input("Enter a source video URL:")
    if st.button("Generate Video"):
        if edited_script.strip() and source_url.strip():
            video_url = generate_video(edited_script, source_url)
            if video_url:
                st.success("Video generated successfully!")
                st.video(video_url)
            else:
                st.error("Failed to generate the video.")
        else:
            st.warning("Please provide a script and a source URL to generate a video.")

# Page: Upload Video
elif page == "Upload Video":
    st.header("Upload Video to YouTube")
    video_url = st.text_input("Enter the video URL to upload:")
    if video_url.strip():
        upload_video(video_url)
    else:
        st.warning("Please enter a video URL to proceed.")

# Footer
st.sidebar.write("Developed with ❤️ using Streamlit")

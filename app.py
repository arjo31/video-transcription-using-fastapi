import requests
import streamlit as st

st.title("Upload videos")

def upload_videos(video, tags):
    url = "http://127.0.0.1:8000/upload-video"
    file = {'file': (video.name, video)}
    data = {'id': video.file_id, 'tags': tags, 'name': video.name}
    response = requests.post(url=url, files=file, data=data)
    return response

if 'tags' not in st.session_state:
    st.session_state.tags = ""
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

video = st.file_uploader(label="Upload your videos", type=['mp4', 'mkv', 'avi', 'mov'])
if video and video != st.session_state.uploaded_file:
    st.session_state.uploaded_file = video
    st.session_state.tags = ""
    st.success("Files uploaded successfully...")

tag = st.text_input(label="Tags", placeholder="Enter your tags (separate by comma)", value=st.session_state.tags)

button = st.button("Upload", type="primary")

if tag:
    st.session_state.tags = tag
    if button:
        with st.spinner(text="Transcribing text..."):
            res = upload_videos(st.session_state.uploaded_file, st.session_state.tags)
            st.write(res.json()["result"])
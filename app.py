import os
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini
model = genai.GenerativeModel("gemini-1.5-pro-latest")

def get_transcript(video_url):
    try:
        video_id = video_url.split("v=")[1].split("&")[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

def summarize_with_gemini(text):
    response = model.generate_content(
        f"Summarize this YouTube video transcript in bullet points. Focus on key ideas, facts, and conclusions:\n\n{text}"
    )
    return response.text

# Streamlit UI
st.title("YouTube Summarizer with Gemini")
video_url = st.text_input("Enter YouTube Video URL")

if video_url:
    with st.spinner("Fetching transcript..."):
        transcript = get_transcript(video_url)
        if transcript:
            with st.spinner("Generating summary..."):
                summary = summarize_with_gemini(transcript)
                st.subheader("Summary")
                st.write(summary)

            # Q&A Section
            question = st.text_input("Ask a question about the video")
            if question:
                answer = model.generate_content(
                    f"Answer this question based on the transcript:\n\nTranscript:\n{transcript}\n\nQuestion: {question}"
                )
                st.subheader("Answer")
                st.write(answer.text)
import os
import tempfile
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_mistralai import ChatMistralAI as Mistral
import streamlit as st
import streamlit.components.v1 as components
import requests
import time
import yt_dlp

# Load environment variables (for local dev only)
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# LLM and prompt setup
llm = Mistral(model_name="mistral-large-latest", temperature=0.7)

# ==============================
# Step 1: AssemblyAI Audio Transcription Function
# ==============================
def transcribe_audio(audio_file_path):
    """
    Transcribe audio using AssemblyAI API.
    Args:
        audio_file_path (str): Path to audio file
    Returns:
        str: Transcript text or None if error
    """
    ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
    if not ASSEMBLYAI_API_KEY:
        st.error("❌ AssemblyAI API key not found. Set ASSEMBLYAI_API_KEY in environment.")
        return None
    try:
        st.write("🎧 Uploading audio to AssemblyAI...")
        headers = {'authorization': ASSEMBLYAI_API_KEY}
        # Upload audio file
        with open(audio_file_path, 'rb') as f:
            upload_response = requests.post(
                'https://api.assemblyai.com/v2/upload',
                headers=headers,
                data=f
            )
        if upload_response.status_code != 200:
            st.error(f"❌ Error uploading audio: {upload_response.text}")
            return None
        audio_url = upload_response.json()['upload_url']
        st.write("📤 Audio uploaded. Submitting for transcription...")
        # Submit for transcription
        transcript_response = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            json={"audio_url": audio_url},
            headers=headers
        )
        if transcript_response.status_code != 200:
            st.error(f"❌ Error submitting transcription: {transcript_response.text}")
            return None
        transcript_id = transcript_response.json()['id']
        # Poll for completion
        polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        while True:
            status_response = requests.get(polling_endpoint, headers=headers)
            status_json = status_response.json()
            status = status_json['status']
            if status == 'completed':
                st.write("✅ Transcription complete!")
                return status_json['text']
            elif status == 'failed':
                st.error("❌ Transcription failed.")
                return None
            else:
                st.write(f"⏳ Transcription status: {status} ...")
                time.sleep(4)
    except Exception as e:
        st.error(f"❌ Error in transcribing audio: {str(e)}")
        return None

# ==============================
# Step 2: Mistral Summarization
# ==============================
summary_prompt_template = """
You are a professional content summarizer. Your task is to create a clear, concise summary of a video transcript.

Input: {transcript_text}

Task: Summarize this transcript in bullet points with clear, concise sentences. 
Ensure the summary is easy to read and captures the main points.

Requirements:
- Use bullet points (•) for each main idea
- Keep each point concise (1-2 sentences max)
- Focus on key information and main takeaways
- Maintain a logical flow
- Use simple, clear language

Output: A well-structured summary with bullet points
"""

summary_prompt = PromptTemplate(
    input_variables=["transcript_text"], 
    template=summary_prompt_template
)

summary_chain = summary_prompt | llm

def generate_summary(transcript_text):
    try:
        if not transcript_text or not transcript_text.strip():
            st.error("❌ No transcript text provided for summarization")
            return None
        
        st.write("🤖 Asking Mistral AI to summarize transcript...")
        response = summary_chain.invoke({"transcript_text": transcript_text})
        ai_summary = response.content
        
        st.write("✅ Summary generated successfully!")
        return ai_summary
        
    except Exception as e:
        st.error(f"❌ Error generating summary: {str(e)}")
        return None

# ==============================
# Step 3: Streamlit UI
# ==============================
st.title("YouSum 🎥")
st.markdown("### YouTube Video Summarizer with Mistral")
st.markdown("""
This app will transcribe uploaded audio (simulated) and then summarize the transcript using Mistral AI.

**Steps:**
1. Upload audio file (or YouTube audio extracted separately)
2. Wait for transcription to complete
3. Mistral AI generates bullet point summary
""")

def download_youtube_audio(youtube_url):
    """
    Download YouTube video as mp4 and extract audio as mp3 using yt_dlp.
    Returns: path to downloaded mp3 file
    """
    try:
        # Use the working yt_dlp configuration
        filename_mp4 = "youtube_video.mp4"
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': filename_mp4,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            # final mp3 file
            audio_file = os.path.splitext(filename_mp4)[0] + ".mp3"

        if os.path.exists(audio_file) and os.path.getsize(audio_file) > 0:
            return audio_file
        else:
            st.error("❌ Downloaded audio file is empty or missing.")
            return None

    except Exception as e:
        st.error(f"❌ Error downloading YouTube audio: {str(e)}")
        return None

# YouTube link section
st.markdown("---")
st.markdown("## 📺 Enter YouTube Link for Transcription")
youtube_url = st.text_input("Paste a YouTube video link here (audio will be extracted automatically):")

# Audio upload section
st.markdown("---")
st.markdown("## 🎤 Upload Audio for Transcription")
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

# Determine which audio source to use
audio_path = None
if youtube_url:
    with st.spinner("🔗 Downloading audio from YouTube..."):
        audio_path = download_youtube_audio(youtube_url)
elif uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(uploaded_file.read())
        audio_path = tmp_file.name

if audio_path:
    st.write("🔍 Debug: Checking downloaded audio file...")
    if os.path.exists(audio_path):
        st.write(f"✅ File exists: {audio_path}")
        size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        st.write(f"📦 File size: {size_mb:.2f} MB")
        with open(audio_path, "rb") as f:
            sample_bytes = f.read(10)
            st.write(f"🔹 First 10 bytes of file: {sample_bytes}")
    else:
        st.error("❌ Audio file does not exist. Download failed.")

    with st.spinner("🎧 Transcribing audio..."):
        transcript = transcribe_audio(audio_path)
    
    if transcript:
        st.success("✅ Transcript generated!")
        with st.expander("🔍 View Transcript"):
            st.write(transcript)
        
        # Generate summary using Mistral
        with st.spinner("🤖 Generating summary with Mistral AI..."):
            summary = generate_summary(transcript)
        
        if summary:
            st.success("📋 Summary Generated!")
            st.markdown("---")
            st.markdown("## 📝 Summary")
            st.write(summary)
    else:
        st.error("❌ Failed to generate transcript.")
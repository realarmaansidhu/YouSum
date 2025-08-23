# YouSum 🎥 - A YouTube Video Summarizer by Armaan Sidhu

Transform long YouTube videos into concise, easy-to-read summaries! YouSum uses AssemblyAI for accurate transcription and MistralAI for intelligent summarization, all wrapped in a beautiful Streamlit interface.

## ✨ Features

- **YouTube Integration**: Simply paste a YouTube URL and get instant summaries
- **AI Transcription**: High-accuracy speech-to-text conversion using AssemblyAI
- **Smart Summarization**: Intelligent content summarization powered by MistralAI
- **Beautiful UI**: Clean, intuitive Streamlit interface with progress indicators
- **Cloud-Based**: No local models required - everything runs via APIs
- **Multiple Formats**: Get summaries in bullet points, paragraphs, or structured formats
- **Download Options**: Save summaries as text files for offline reading
- **Progress Tracking**: Real-time updates during transcription and summarization

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

You'll need two API keys:

#### MistralAI API Key
1. Go to [MistralAI Console](https://console.mistral.ai/)
2. Sign up/Login and get your API key
3. Set as environment variable: `MISTRAL_API_KEY`

#### AssemblyAI API Key
1. Go to [AssemblyAI Console](https://www.assemblyai.com/)
2. Sign up/Login and get your API key (free tier available)
3. Set as environment variable: `ASSEMBLYAI_API_KEY`

### 3. Run the App

```bash
streamlit run yousum.py
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in your project directory:

```bash
MISTRAL_API_KEY=your_mistral_api_key_here
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
```

### Streamlit Cloud Deployment
If deploying to Streamlit Cloud, add these as secrets in your app settings:
- `MISTRAL_API_KEY`
- `ASSEMBLYAI_API_KEY`

## 📖 How It Works

1. **Input**: Paste a YouTube video URL into the app
2. **Audio Extraction**: Download and extract audio from the YouTube video
3. **Transcription**: Upload audio to AssemblyAI for accurate speech-to-text conversion
4. **Summarization**: Send transcript to MistralAI for intelligent content summarization
5. **Output**: Display a clean, structured summary with key points and insights
6. **Download**: Option to save the summary as a text file

## 🎯 Perfect For

- **Students**: Quickly understand lecture content and key concepts
- **Researchers**: Extract main points from long research presentations
- **Professionals**: Get executive summaries of industry talks and webinars
- **Content Creators**: Analyze competitor content and identify key themes
- **Anyone**: Save time by getting the essence of long videos in minutes

## 🛠 Technical Details

- **Frontend**: Streamlit with modern, responsive design
- **Transcription**: AssemblyAI for high-accuracy speech recognition
- **Summarization**: MistralAI (via LangChain) for intelligent content analysis
- **YouTube Processing**: yt-dlp for reliable video and audio extraction
- **Audio Handling**: Temporary file management for cloud processing
- **Progress Tracking**: Real-time updates with Streamlit progress bars
- **Error Handling**: Comprehensive error handling and user feedback

## 📁 Project Structure

```
YouSum/
├── yousum.py          # Main application
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🔒 Security Notes

- Never commit your `.env` file to version control
- API keys are loaded from environment variables or Streamlit secrets
- All API calls are made securely over HTTPS
- Temporary audio files are automatically cleaned up

## 🚀 Deployment

### Local Development
```bash
streamlit run yousum.py
```

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Add your API keys as secrets:
   - `MISTRAL_API_KEY`
   - `ASSEMBLYAI_API_KEY`
4. Deploy!

## 💡 Usage Tips

- **Best Results**: Use videos with clear speech and minimal background noise
- **Video Length**: Works best with videos under 2 hours (AssemblyAI limits)
- **Language Support**: Currently optimized for English content
- **File Formats**: Supports all major YouTube video formats
- **Processing Time**: Depends on video length (typically 1-3 minutes for 10-minute videos)

## 🌟 What Makes YouSum Special

- **Accuracy**: AssemblyAI provides industry-leading transcription accuracy
- **Intelligence**: MistralAI creates contextually relevant summaries
- **Speed**: Cloud-based processing means no waiting for local models
- **Reliability**: Robust error handling and progress tracking
- **User Experience**: Clean interface with clear progress indicators
- **Accessibility**: Works on any device with a web browser

## 🔮 Future Features

- **Timestamp Highlights**: Show key moments with video timestamps
- **Multiple Summary Styles**: Executive summary, detailed analysis, bullet points
- **Language Support**: Multi-language transcription and summarization
- **Batch Processing**: Handle multiple videos at once
- **Custom Prompts**: User-defined summarization preferences
- **Export Formats**: PDF, Word, and other document formats

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve YouSum!

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Summarizing with YouSum! 📝**

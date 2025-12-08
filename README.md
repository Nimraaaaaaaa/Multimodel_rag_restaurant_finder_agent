# 🍽️ Restaurant Finder Agent

An AI-powered restaurant recommendation system for Pakistan that uses **Groq LLM (Llama 4)**, **SerpAPI**, and **TripAdvisor** to find the best dining options based on user preferences.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

- 🤖 **AI-Powered Recommendations** - Uses Groq's Llama 4 Scout 17B model for intelligent restaurant suggestions
- 🔍 **Real-time Web Scraping** - Fetches live restaurant data from TripAdvisor using SerpAPI's Google Search
- 🌆 **Multi-City Support** - Search restaurants in Lahore, Karachi, Islamabad, Faisalabad, and Murree
- 📸 **Image Upload Support** - Upload food images for context-aware recommendations (optional)
- 💬 **Conversational Memory** - Remembers last 5 queries for better context understanding
- 🎨 **Beautiful UI** - Clean and modern Streamlit interface with custom styling
- ⚡ **Fast API Backend** - RESTful API built with FastAPI for high performance
- 📊 **Detailed Results** - Shows restaurant names, locations, ratings, descriptions, and TripAdvisor links

## 🏗️ System Architecture

```
┌─────────────────────────┐
│   Streamlit Frontend    │  ← User Interface (app.py)
│   (localhost:8501)      │
└───────────┬─────────────┘
            │ HTTP POST
            ▼
┌─────────────────────────┐
│   FastAPI Backend       │  ← API Server (main.py)
│   (localhost:8000)      │
└───────────┬─────────────┘
            │
            ├─────────────────────┬────────────────────┐
            ▼                     ▼                    ▼
┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐
│  Agentic Agent   │  │   Web Scraper    │  │  Image Handler  │
│  (Groq LLM)      │  │   (SerpAPI)      │  │  (Optional)     │
│  Llama 4 Scout   │  │   TripAdvisor    │  │                 │
└──────────────────┘  └──────────────────┘  └─────────────────┘
            │                     │
            └──────────┬──────────┘
                       ▼
            ┌──────────────────┐
            │  Combined JSON   │
            │  Response        │
            └──────────────────┘
```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5df7b55d-9843-4417-b37d-396dab38810f" />

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed on your system
- **Groq API Key** - Get free access at [console.groq.com](https://console.groq.com)
- **SerpAPI Key** - Get free tier at [serpapi.com](https://serpapi.com)
- **Internet Connection** - For API calls and web scraping

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/restaurant-finder-agent.git
cd restaurant-finder-agent
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

**Option A: Direct in Files (Quick Setup)**

Edit `agentic_agent.py` (line 7):
```python
api_key = "gsk_your_groq_api_key_here"
```

Edit `scraper.py` (line 4):
```python
SERP_API_KEY = "your_serpapi_key_here"
```

**Option B: Environment Variables (Recommended)**

**Windows:**
```bash
set GROQ_API_KEY=gsk_your_groq_api_key_here
set SERP_API_KEY=your_serpapi_key_here
```

**Mac/Linux:**
```bash
export GROQ_API_KEY="gsk_your_groq_api_key_here"
export SERP_API_KEY="your_serpapi_key_here"
```

Then update the files to read from environment:
```python
# In agentic_agent.py
api_key = os.getenv("GROQ_API_KEY", "fallback_key")

# In scraper.py
SERP_API_KEY = os.getenv("SERP_API_KEY", "fallback_key")
```

### 5. Run the Application

**Terminal 1 - Start Backend:**
```bash
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Terminal 2 - Start Frontend:**
```bash
streamlit run app.py
```

Browser will open automatically at `http://localhost:8501`

### 6. Test the Application

1. Select **Islamabad** from city dropdown
2. Enter **"loaded fries"** in search box
3. Click **"🔍 Find Restaurants"**
4. View AI recommendations and restaurant results!

## 🎮 How to Use

### Basic Search

1. **Select City** - Choose your preferred city from dropdown (Lahore, Karachi, Islamabad, Faisalabad, Murree)
2. **Enter Query** - Type what you're looking for in the search box
3. **Click Search** - Press "🔍 Find Restaurants" button
4. **View Results** - See AI recommendations and scraped restaurant data

### Advanced Search with Image

1. **Upload Image** - Click "Upload dish image" and select a food photo
2. **Describe Preference** - Enter additional text like "restaurants like this"
3. **Search** - The AI will consider the image context in recommendations

### Example Queries

**Simple Queries:**
- `biryani`
- `pizza`
- `chinese food`
- `italian restaurants`

**Specific Queries:**
- `loaded fries near DHA`
- `best biryani in Johar Town`
- `rooftop dining in F7`
- `haleem in old city`

**Location-Based:**
- `restaurants in Gulberg`
- `cafes near Centaurus Mall`
- `desi food in Saddar`

## 📁 Project Structure

```
restaurant-finder-agent/
│
├── app.py                 # Streamlit frontend UI
├── main.py                # FastAPI backend server
├── agentic_agent.py       # AI agent with Groq LLM integration
├── scraper.py             # TripAdvisor scraper using SerpAPI
├── requirements.txt       # Python package dependencies
├── README.md              # This documentation file
├── .gitignore             # Git ignore file (add API keys here)
└── temp_*.jpg             # Temporary uploaded images (auto-deleted)
```

### File Descriptions

**`app.py`** - Streamlit Frontend
- User interface with city selector and search input
- Displays AI recommendations and restaurant cards
- Handles image uploads
- Shows backend connection status

**`main.py`** - FastAPI Backend
- REST API endpoint `/recommend`
- Handles form data and file uploads
- Coordinates between AI agent and scraper
- Returns JSON responses

**`agentic_agent.py`** - AI Agent
- Integrates Groq's Llama 4 Scout 17B model
- Maintains conversation memory (last 5 queries)
- Generates contextual recommendations
- Coordinates with scraper

**`scraper.py`** - Web Scraper
- Uses SerpAPI to search Google for TripAdvisor results
- Parses restaurant data (name, location, rating, description)
- Supports multi-city searches
- Returns structured JSON data

## 🛠️ Tech Stack

### Backend Technologies
- **FastAPI** (0.104+) - Modern, fast web framework for building APIs
- **Uvicorn** - Lightning-fast ASGI server
- **Groq SDK** (0.4+) - Ultra-fast LLM inference with Llama 4
- **SerpAPI** - Google Search API for reliable web scraping
- **BeautifulSoup4** - HTML parsing and data extraction
- **Python Multipart** - Form data handling

### Frontend Technologies
- **Streamlit** (1.28+) - Interactive web application framework
- **Requests** - HTTP library for API communication
- **Custom CSS** - Enhanced UI styling

### AI/ML Stack
- **Groq Cloud API** - High-performance LLM infrastructure
- **Meta Llama 4 Scout 17B** - Advanced language model for recommendations
- **Conversational Memory** - Context retention across queries

## 🔑 API Documentation

### Endpoint: `POST /recommend`

Get restaurant recommendations based on user preferences.

### Endpoint: `GET /`

Health check endpoint.

**Response:**
```json
```

## ⚙️ Configuration

### Groq LLM Configuration

**Model Selection** (`agentic_agent.py`, line 23):
```python
llm = GroqModelWrapper(llm_client, "meta-llama/llama-4-scout-17b-16e-instruct")
```

**Available Models:**
- `llama-4-scout-17b-16e-instruct` (Default - Best for recommendations)
- `llama-3-70b-8192` (Alternative)
- `mixtral-8x7b-32768` (More creative)

### City Configuration

**Supported Cities** (`scraper.py`, line 10):
```python
locations = ["Lahore", "Islamabad", "Murree", "Faisalabad", "Karachi"]
```

To add more cities, append to the list:
```python
locations = ["Lahore", "Islamabad", "Murree", "Faisalabad", "Karachi", "Peshawar", "Multan"]
```

### Memory Configuration

**Conversation History** (`agentic_agent.py`, line 32):
```python
# Keeps last 5 conversations
if len(chat_memory) > 5:
    chat_memory.pop(0)
```

Change `5` to adjust memory size (higher = more context but slower).

### Search Results Configuration

**Results per City** (`scraper.py`, line 17):

### Debug Mode

Enable detailed logging by checking the terminal outputs:

**FastAPI Terminal:**
```
📥 Request: best biryani | City: lahore
✅ Image saved: temp_food.jpg
🤖 Asking LLM for recommendations...
✅ LLM Response: For best biryani...
🔍 Scraping TripAdvisor for: best biryani in lahore
  ✅ Found 10 results for lahore
```

## 📦 Dependencies

**Core Dependencies:**
```
fastapi==0.104.1          # Web framework
uvicorn==0.24.0           # ASGI server
streamlit==1.28.0         # Frontend framework
groq==0.4.2               # Groq LLM SDK
requests==2.31.0          # HTTP client
beautifulsoup4==4.12.2    # HTML parser
python-multipart==0.0.6   # Form data handler
lxml==4.9.3               # XML/HTML parser
```

Install all at once:
```bash
pip install -r requirements.txt
```
### Contribution Ideas

- [ ] Add more cities (Peshawar, Multan, etc.)
- [ ] Integrate Google Maps API for directions
- [ ] Add restaurant booking functionality
- [ ] Implement user reviews and ratings
- [ ] Add cuisine type filters
- [ ] Create mobile app version
- [ ] Add price range filtering
- [ ] Implement user authentication
- [ ] Add favorite restaurants feature
- [ ] Multi-language support (Urdu, English)

..
```

## 📧 Contact & Support

**Developer:** Nimra
**Email:** nimraaishere@gmail.com  



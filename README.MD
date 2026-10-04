# Plant Doctor AI

Plant Doctor AI is an AI-powered vision chatbot that helps users identify plant diseases from images. Users can upload a photo of a plant, receive an AI-generated diagnosis, and email the generated plant health report directly to themselves.

The application uses Google's Gemini Vision model for image analysis and Streamlit for the web interface.

---

## Features

- Plant identification from images
- Plant disease detection
- Severity assessment
- Treatment recommendations
- Preventive measures
- Interactive AI chatbot
- Email plant health report

---

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- Gmail SMTP
- HTML Email

---

## Project Structure

```
PlantDoctorAI/
│
├── app.py
├── prompts.py
├── requirements.txt
├── .streamlit/
│   └── secrets.toml
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Create a virtual environment

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure API Keys

Copy the example secrets file:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

(or create `secrets.toml` manually on Windows)

Then replace the placeholder values with your own credentials.

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

GMAIL_ADDRESS = "your_email@gmail.com"
GMAIL_APP_PASSWORD = "your_gmail_app_password"
```

---

### 5. Run the application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## How It Works

1. Enter your name and email address.
2. Upload an image of a plant.
3. Gemini analyzes the image and generates a diagnosis.
4. The chatbot displays:
   - Plant identification
   - Disease (if any)
   - Severity
   - Treatment
   - Preventive measures
5. Click **Send Report** to receive the diagnosis via email.

---

## Notes

- Supported image formats: JPG, JPEG, PNG
- Requires an active internet connection.
- Gmail App Password is required for email functionality.
- AI-generated diagnoses are for informational purposes only and should not replace expert agricultural advice.

---

## Future Improvements

- Telegram integration
- Multi-language support
- PDF report generation
- Disease history tracking
- Weather-aware disease recommendations

---

## License

This project is developed for educational purposes.
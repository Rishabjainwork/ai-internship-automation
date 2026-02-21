# 🤖 IITGN SRIP Internship Automation Bot

An automated Python script that scrapes research projects from the IIT Gandhinagar SRIP portal, generates a custom, highly-tailored Statement of Purpose (SOP) for each project using Google's Gemini AI, and automatically fills and submits the application forms.

## ✨ Features
* **Web Scraping:** Automatically extracts all available internship projects, faculty names, and project codes from the SRIP portal.
* **AI-Powered SOPs:** Uses the Gemini model to read the specific project description and write a custom, highly relevant 200-word SOP.
* **Auto-Fill & Submit:** Uses Playwright to navigate the application portal, select the correct faculty/project dropdowns, fill in personal details, and submit the form.
* **Record Keeping:** Automatically saves a generated text file of every SOP (`/sops`) and takes a screenshot of every filled form before submission (`/screenshots`).

## ⚠️ Disclaimer
**For Educational Purposes Only.** This script was created to demonstrate web automation and API integration. Please use responsibly. Do not use this script to spam the university servers or submit applications for projects you are not genuinely interested in. Be mindful of API rate limits and server load.

## 🛠️ Prerequisites
* Python 3.8+
* A free Google Gemini API Key

## 🚀 Installation & Setup

**1. Clone the repository**
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

**2. Install required Python packages**
pip install python-dotenv playwright google-generativeai

**3. Install Playwright browsers**
playwright install chromium

**4. Add your API Key**
Create a file named exactly `.env` in the root folder of the project and add your Gemini API key:
GEMINI_API_KEY=AIzaSyYourActualApiKeyGoesHere

## ⚙️ Configuration
Before running the script, you **must** open your Python file and update your personal details in the `# 3. Personal Details` section of the code (Name, Phone, Email, University, etc.). 

You can also adjust which projects you want to apply to by modifying the array slice in Step 2:
# Currently set to apply to projects from row 28 to 99
for idx, internship in enumerate(internships[28:100], start=28):

## 💻 Usage
Simply run the Python script. A visible Chromium browser will open so you can watch the bot work in real-time.

python your_script_name.py

## 📂 Folder Structure
Once run, the script will automatically generate the following folders:
* `/sops` - Contains `.txt` files of every Gemini-generated SOP.
* `/screenshots` - Contains `.png` screenshots of every filled application form just before submission.

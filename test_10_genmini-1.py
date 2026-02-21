import time
import random
import os 
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import google.generativeai as genai

# ... (Setup and Gemini config remains the same) ...

# Create screenshots directory if it doesn't exist
os.makedirs("screenshots", exist_ok=True)
# Create sops directory if it doesn't exist
os.makedirs("sops", exist_ok=True)

#loading environment variables from .env file
load_dotenv()

#gemini api key configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-flash-preview")

PROJECTS_URL = "https://srip.iitgn.ac.in/portal/projects-newpage/"
APPLY_URL = "https://srip.iitgn.ac.in/portal/apply-now/"


#this is a fake SOP generator function that return a dummy SOP for testing purposes. replace it with actual function that call gemini api to generate SOP based on project description.
def generate_fake_sop(description):

    return "This is a fake SOP generated for testing purposes. The project description is: " + description


def generate_sop(description):
    prompt = f"""
    You are writing a genuine Statement of Purpose for an undergraduate student applying to a research internship.

    Internship Description:
    {description}

    The student:
    - Has strong knowledge of Data Structures and Algorithms
    - Is comfortable with C++ and Python
    - Has built a Python automation project
    - Is highly motivated to learn and contribute

    Instructions:
    - Write in layman terms, as if explaining to a human reader.
    - Write in first person.
    - Keep the tone natural, thoughtful, and specific.
    - Avoid generic phrases like "I am passionate about".
    - Explain why this particular internship matches the student's interests.
    - Mention relevant skills only where they logically connect to the project.
    - Keep it under 400 words.
    - Do not include phone number, email, or personal identifiers.
    - Make the writing flow naturally with varied sentence lengths.

    Write the SOP.
    """
    response = model.generate_content(prompt)
    return response.text


def run_automation():
    with sync_playwright() as p:
        # Launch once
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # --- STEP 1: Extract All Projects ---
        print("Scraping projects...")
        page.goto(PROJECTS_URL)
        page.wait_for_selector("table#DataTables_Table_0")
        page.select_option('select[name="DataTables_Table_0_length"]', value='-1')
        
        # Give it a moment to render all rows
        page.wait_for_timeout(2000) 
        rows = page.locator("table#DataTables_Table_0 tbody tr")
        
        internships = []
        for i in range(rows.count()):
            row = rows.nth(i)
            internships.append({
                "description": row.locator('td[data-column-index="2"] div').inner_text(),
                "faculty": row.locator('td[data-column-index="3"]').inner_text().strip(),
                "project_code": row.locator('td[data-column-index="0"]').inner_text().strip()
            })

        # --- STEP 2: Apply to a Slice (e.g., x:y-1) ---
        for idx, internship in enumerate(internships[28:100], start=28):
            print(f"\n--- Processing Row {idx}: {internship['project_code']} ---")
            
            # 1. Generate SOP (Only if tokens are available)
            try:
                sop = generate_sop(internship["description"])
                
                # Save SOP to file
                with open(f"sops/sop_{idx}.txt", "w", encoding="utf-8") as f:
                    f.write(sop)
            except Exception as e:
                print(f"Gemini Error (Likely out of tokens): {e}")
                continue # Skip this one if AI fails

            # 2. Fill the form
            page.goto(APPLY_URL)
            page.wait_for_selector('#input_36_24_1', timeout=10000) # Increased timeout
            
            # Faculty -> Wait for Project -> Project Code -> Wait for Title
            page.select_option('#input_36_24_1', label=internship["faculty"])
            page.wait_for_function("() => document.querySelector('#input_36_24_2')?.options.length > 1")
            
            page.select_option('#input_36_24_2', label=internship["project_code"])
            page.wait_for_function("() => document.querySelector('#input_36_24_3')?.options.length > 1")
            
            page.select_option('#input_36_24_3', index=1)

            # 3. Personal Details
            page.fill('#input_36_4', 'Rishab Jain')
            page.fill('#input_36_5', 'YOUR PHONE NUMBER')
            page.fill('#input_36_45', 'NATIONALITY-INDIAN')
            page.fill('#input_36_11', 'YOUR PHONE NUMBER')
            page.fill('#input_36_8', 'YOUR EMAIL ID')
            page.fill('#input_36_3', 'YOUR PERMANENT CITY')
            page.fill('#input_36_12', 'YOUR COURSE')
            page.fill('#input_36_13', 'YOUR BRANCH EG - computer science')
            page.fill('#input_36_14', 'COLLEGE NAME')
            page.fill('#input_36_21', 'YEAR OF JOINING COLLEGE')
            page.check('#choice_36_17_1')
            page.fill('#input_36_20', 'YOUR CURRENT CGPA')
            page.fill('#input_36_15_3', 'LOCATION OF COLAGE')
            page.fill('#input_36_15_4', 'STATE OF YOUR COLLEGE')
            page.fill('#input_36_7', 'PROFESSIONAL EMAIL ID')
            page.fill('#input_36_7_2', 'CONFIRM PROFESSIONAL EMAIL ID')
            page.select_option('#input_36_15_6', value='India')
    

            page.fill('#input_36_10', 'DD-MM-YYYY') 
            
            page.fill('#input_36_23', sop)
            
            # 4. Save progress & Submit
            page.screenshot(path=f"screenshots/form_{idx}.png")
            print(f"Form filled for {internship['project_code']}. Submitting...")
            
            # UNCOMMENT THIS WHEN READY
            # page.click('#gform_submit_button_36')
            # page.wait_for_selector('.gform_confirmation_message', timeout=15000)
            print(f"Submitting form for {internship['project_code']}...")
            
            page.locator('body').click()
            page.wait_for_timeout(500)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(4000) # Wait for any lazy-loaded elements
            
            page.locator('body').click()
            page.wait_for_timeout(500)
            submit_button = page.locator('#gform_submit_button_36')
            submit_button.click()
            page.wait_for_timeout(25000)

            time.sleep(random.randint(2, 5)) # Be nice to the server

        browser.close()

if __name__ == "__main__":
    run_automation()
    

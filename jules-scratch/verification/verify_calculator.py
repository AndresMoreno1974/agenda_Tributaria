import os
from playwright.sync_api import sync_playwright, Page, expect
import subprocess
import time

def verify_calculator(page: Page):
    # Start the HTTP server
    server_process = subprocess.Popen(['python', '-m', 'http.server', '8000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2) # Give the server a moment to start

    try:
        # Go to the local HTML file served by the HTTP server
        page.goto('http://localhost:8000/index.html')

        # Wait for the page to load and check its title
        expect(page).to_have_title("Comparative Calculator")

        # Take a screenshot of the page
        page.screenshot(path="jules-scratch/verification/calculator_verification.png")

    finally:
        # Stop the HTTP server
        server_process.terminate()

# Boilerplate to run the verification
if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        verify_calculator(page)
        browser.close()

import os
from playwright.sync_api import sync_playwright, Page, expect
import subprocess
import time

def verify_pdf_generation(page: Page):
    # Listen for console messages
    page.on("console", lambda msg: print(f"BROWSER_CONSOLE: {msg.text}"))

    # Start the HTTP server
    server_process = subprocess.Popen(['python', '-m', 'http.server', '8000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2) # Give the server a moment to start

    try:
        # Go to the local HTML file served by the HTTP server
        page.goto('http://localhost:8000/index.html')

        # Show the form 260
        page.get_by_role("button", name="Preparar Declaración Anual (Form. 260)").click()

        # Wait for the form to be visible
        form_260 = page.locator("#form-260")
        expect(form_260).to_be_visible()

        # Open the details section for "Ingresos Anuales Consolidados"
        page.get_by_text("Ingresos Anuales Consolidados").click()

        # Fill in some income data
        page.locator("#ingresos-g1-260").fill("100000000")
        page.locator("#ingresos-g2-260").fill("50000000")

        # Listen for the download event
        with page.expect_download() as download_info:
            # Click the "Planeación Fiscal" button
            page.get_by_role("button", name="Planeación Fiscal").click()

        download = download_info.value
        expect(download.suggested_filename).to_be("comparativa_fiscal.pdf")

        # Take a screenshot
        page.screenshot(path="jules-scratch/verification/pdf_generation_verification.png")

    finally:
        # Stop the HTTP server
        server_process.terminate()

# Boilerplate to run the verification
if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        verify_pdf_generation(page)
        browser.close()

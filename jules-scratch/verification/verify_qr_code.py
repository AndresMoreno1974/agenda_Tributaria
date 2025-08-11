import os
from playwright.sync_api import sync_playwright, Page, expect

def verify_qr_code(page: Page):
    # Get the absolute path to the HTML file
    # This is necessary because the test is run from a different directory
    file_path = os.path.abspath('index.html')

    # Go to the local HTML file
    page.goto(f'file://{file_path}')

    # Find the "Bancolombia" button and click it
    bancolombia_button = page.get_by_role("button", name="Bancolombia")
    bancolombia_button.click()

    # Wait for the modal to be visible
    modal = page.locator("#qrModal")
    expect(modal).to_be_visible()

    # Take a screenshot of the modal
    modal.screenshot(path="jules-scratch/verification/verification.png")

# Boilerplate to run the verification
if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        verify_qr_code(page)
        browser.close()

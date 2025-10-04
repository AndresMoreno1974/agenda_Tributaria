import asyncio
import re
from playwright.async_api import async_playwright, expect
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Get the absolute path to the index.html file
        file_path = os.path.abspath('index.html')
        await page.goto(f'file://{file_path}')

        # 1. Paste CV text
        cv_text = """
Curriculum Vitae

Juan Pérez

Email: juan.perez@example.com
Teléfono: +123456789
"""
        await page.locator("#cvPaste").fill(cv_text)

        # 2. Select category and subcategory
        await page.locator("#categoria").select_option("📌 Según la naturaleza de la postulación")
        await page.locator("#subcategoria").select_option("Carta tradicional o estándar")

        # 3. Select a template
        await page.locator(".template-tile").first.click()

        # 4. Generate the letter
        await page.locator("#generateBtn").click()

        # 5. Verify the name was extracted correctly using a regex for whitespace
        # This makes the test robust against changes in newlines or spaces.
        closing_regex = re.compile(r"Atentamente,\s*Juan Pérez")
        await expect(page.locator("#previewArea")).to_contain_text(closing_regex)

        # 6. Verify the CV is appended for reference, also using a regex
        cv_reference_regex = re.compile(r"COPIA DE TU CV PARA REFERENCIA:")
        cv_content_regex = re.compile(r"Curriculum Vitae\s*Juan Pérez")
        await expect(page.locator("#previewArea")).to_contain_text(cv_reference_regex)
        await expect(page.locator("#previewArea")).to_contain_text(cv_content_regex)

        print("Name extraction and letter generation verified successfully.")

        # 7. Take a screenshot for visual confirmation
        screenshot_path = "jules-scratch/verification/verification.png"
        await page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        # 8. Verify the download functionality
        print("Testing .docx download...")
        async with page.expect_download() as download_info:
            await page.locator("#downloadDocx").click()

        download = await download_info.value
        # Check if the download is initiated with the correct filename
        if download.suggested_filename == "carta-de-presentacion.docx":
            print("Download initiated successfully with correct filename.")
        else:
            print(f"Error: Download initiated with incorrect filename: {download.suggested_filename}")

        # Clean up the downloaded file
        await download.delete()
        print("Download test complete and artifact deleted.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
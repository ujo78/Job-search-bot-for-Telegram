from playwright.async_api import async_playwright, Page, Browser
from typing import Optional, Dict, List
import asyncio
import os

class FormFiller:
    def __init__(self, resume_text: str, user_info: Dict):
        self.resume_text = resume_text
        self.user_info = user_info
        self.browser = None

    async def init_browser(self):
        """Initialize Playwright browser."""
        p = await async_playwright().start()
        self.browser = await p.chromium.launch(headless=True)

    async def close_browser(self):
        """Close browser."""
        if self.browser:
            await self.browser.close()

    async def fill_greenhouse(self, page: Page, form_data: Dict) -> bool:
        """Fill Greenhouse job application form."""
        try:
            # Common fields
            await self._fill_text_field(page, 'input[name*="first"]', self.user_info.get('first_name', ''))
            await self._fill_text_field(page, 'input[name*="last"]', self.user_info.get('last_name', ''))
            await self._fill_text_field(page, 'input[type="email"]', self.user_info.get('email', ''))
            await self._fill_text_field(page, 'input[name*="phone"]', self.user_info.get('phone', ''))

            # Resume upload
            await self._upload_resume(page)

            return True
        except Exception as e:
            print(f"Greenhouse fill error: {e}")
            return False

    async def fill_lever(self, page: Page, form_data: Dict) -> bool:
        """Fill Lever job application form."""
        try:
            await self._fill_text_field(page, 'input[name*="name"]', self.user_info.get('full_name', ''))
            await self._fill_text_field(page, 'input[type="email"]', self.user_info.get('email', ''))
            await self._fill_text_field(page, 'input[type="tel"]', self.user_info.get('phone', ''))
            await self._upload_resume(page)
            return True
        except Exception as e:
            print(f"Lever fill error: {e}")
            return False

    async def fill_ashby(self, page: Page, form_data: Dict) -> bool:
        """Fill Ashby job application form."""
        try:
            await self._fill_text_field(page, 'input[placeholder*="name"], input[placeholder*="Name"]', self.user_info.get('full_name', ''))
            await self._fill_text_field(page, 'input[type="email"]', self.user_info.get('email', ''))
            await self._upload_resume(page)
            return True
        except Exception as e:
            print(f"Ashby fill error: {e}")
            return False

    async def _fill_text_field(self, page: Page, selector: str, value: str):
        """Fill a text field with value."""
        if not value:
            return

        try:
            await page.fill(selector, value)
        except Exception:
            pass

    async def _upload_resume(self, page: Page):
        """Upload resume file."""
        try:
            resume_path = self.user_info.get('resume_path', '')
            if resume_path and os.path.exists(resume_path):
                file_input = await page.query_selector('input[type="file"]')
                if file_input:
                    await file_input.set_input_files(resume_path)
        except Exception as e:
            print(f"Resume upload error: {e}")

    async def screenshot_form(self, page: Page) -> Optional[bytes]:
        """Take screenshot of filled form."""
        try:
            return await page.screenshot()
        except Exception as e:
            print(f"Screenshot error: {e}")
            return None

    async def submit_form(self, page: Page) -> bool:
        """Submit the form."""
        try:
            # Look for submit button variations
            submit_button = await page.query_selector('button:has-text("Submit"), button[type="submit"], button:has-text("Apply"), button:has-text("Send")')
            if submit_button:
                await submit_button.click()
                await asyncio.sleep(2)  # Wait for submission
                return True
        except Exception as e:
            print(f"Submit error: {e}")
        return False

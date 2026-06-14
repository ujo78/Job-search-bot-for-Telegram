from typing import Optional, Dict
from applier.ats_detector import detect_ats
from applier.form_filler import FormFiller
import os

class ApplySession:
    def __init__(self, job: Dict, resume_text: str, user_info: Dict, db, screenshots_dir: str):
        self.job = job
        self.resume_text = resume_text
        self.user_info = user_info
        self.db = db
        self.screenshots_dir = screenshots_dir
        self.ats_type = detect_ats(job.get('url', ''))
        self.form_filler = FormFiller(resume_text, user_info)
        self.screenshot_path = None

    async def prepare_form_preview(self) -> Optional[str]:
        """Navigate to job URL, fill form, take screenshot, return screenshot path."""
        try:
            await self.form_filler.init_browser()

            # Get the browser and navigate
            browser = self.form_filler.browser
            page = await browser.new_page()

            job_url = self.job.get('url', '')
            await page.goto(job_url, timeout=10000)

            # Fill based on ATS type
            if self.ats_type == 'greenhouse':
                await self.form_filler.fill_greenhouse(page, {})
            elif self.ats_type == 'lever':
                await self.form_filler.fill_lever(page, {})
            elif self.ats_type == 'ashby':
                await self.form_filler.fill_ashby(page, {})

            # Screenshot
            screenshot_bytes = await self.form_filler.screenshot_form(page)
            if screenshot_bytes:
                filename = f"apply_{self.job.get('url_hash', 'unknown')}.png"
                self.screenshot_path = os.path.join(self.screenshots_dir, filename)
                with open(self.screenshot_path, 'wb') as f:
                    f.write(screenshot_bytes)

            await page.close()
            return self.screenshot_path
        except Exception as e:
            print(f"Preview preparation error: {e}")
            return None
        finally:
            await self.form_filler.close_browser()

    async def submit_application(self) -> bool:
        """Submit the filled form."""
        try:
            await self.form_filler.init_browser()
            browser = self.form_filler.browser
            page = await browser.new_page()

            job_url = self.job.get('url', '')
            await page.goto(job_url, timeout=10000)

            # Fill and submit
            if self.ats_type == 'greenhouse':
                await self.form_filler.fill_greenhouse(page, {})
            elif self.ats_type == 'lever':
                await self.form_filler.fill_lever(page, {})
            elif self.ats_type == 'ashby':
                await self.form_filler.fill_ashby(page, {})

            success = await self.form_filler.submit_form(page)
            await page.close()
            return success
        except Exception as e:
            print(f"Submit application error: {e}")
            return False
        finally:
            await self.form_filler.close_browser()

    async def get_summary(self) -> str:
        """Get a text summary of the form fields."""
        return f"""
Job: {self.job.get('title', '')}
Company: {self.job.get('company', '')}
ATS Type: {self.ats_type}

Filled fields:
- Name: {self.user_info.get('full_name', 'N/A')}
- Email: {self.user_info.get('email', 'N/A')}
- Phone: {self.user_info.get('phone', 'N/A')}
- Resume: Attached

Ready to submit.
        """

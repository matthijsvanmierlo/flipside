
from playwright.sync_api import sync_playwright, expect
import time

def verify_ungraded_mode(page):
    # 1. Arrange: Go to the app
    page.goto("http://localhost:8000/index.html")

    # 2. Wait for loading (or skip welcome modal if present)
    # The app might show a welcome modal first time.
    # We can try to click "GET STARTED" if it appears.
    try:
        page.get_by_role("button", name="GET STARTED").click(timeout=2000)
    except:
        pass # Modal might not be there if localStorage persisted or logic differs

    # 3. Create a Deck if needed, or use the default "Getting Started" deck if present.
    # The default deck "Getting Started 🚀" should be there if localStorage is empty.
    # Let's try to find "Study" button for the first deck.
    # We can just click the first "Study" button we find.
    page.get_by_role("button", name="Study").first.click()

    # 4. Now we should be in StudySetup.
    # Select "Type Def" mode (Ungraded only appears for typing modes)
    page.get_by_text("Type Def").click()

    # 5. Verify Grading section appears
    expect(page.get_by_text("Grading Mode")).to_be_visible()

    # 6. Click "UNGRADED (PRACTICE)"
    page.get_by_text("UNGRADED (PRACTICE)").click()

    # 7. Start Session
    page.get_by_role("button", name="START SESSION").click()

    # 8. We are in session. Type anything.
    # Input has placeholder "Type your answer..."
    page.get_by_placeholder("Type your answer...").fill("random wrong answer")

    # 9. Click Check Answer
    page.get_by_role("button", name="CHECK ANSWER").click()

    # 10. Verify "REVIEW ANSWER" is shown instead of "NOT QUITE"
    expect(page.get_by_text("REVIEW ANSWER")).to_be_visible()
    expect(page.get_by_text("NOT QUITE")).not_to_be_visible()

    # 11. Screenshot
    page.screenshot(path="verification/ungraded_mode.png")
    print("Screenshot taken: verification/ungraded_mode.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_ungraded_mode(page)
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")
        finally:
            browser.close()

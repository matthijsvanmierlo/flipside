from playwright.sync_api import sync_playwright, expect
import time

def verify_definition_first(page):
    # 1. Arrange: Go to the app
    page.goto("http://localhost:8000/index.html")

    # 2. Skip welcome if needed
    try:
        page.get_by_role("button", name="GET STARTED").click(timeout=2000)
    except:
        pass

    # 3. Go to study the first deck
    page.get_by_role("button", name="Study").first.click()

    # 4. We should be in StudySetup. Verify "Display Side" is visible (default mode is flashcards)
    expect(page.get_by_text("Display Side")).to_be_visible()

    # 5. Select "DEFINITION FIRST"
    page.get_by_text("DEFINITION FIRST").click()

    # 6. Start Session
    page.get_by_role("button", name="START SESSION").click()

    # 7. Verify the card front shows "DEFINITION" label
    expect(page.locator(".card-front").get_by_text("DEFINITION")).to_be_visible()

    # 8. Screenshot
    page.screenshot(path="verification/definition_first.png")
    print("Screenshot taken: verification/definition_first.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_definition_first(page)
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")
            raise e
        finally:
            browser.close()

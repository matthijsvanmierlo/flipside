from playwright.sync_api import sync_playwright, expect
import time

def verify_flipside(page):
    page.goto("http://localhost:8000/index.html")

    # 1. Handle Welcome Modal
    print("Checking for Welcome Modal...")
    # It might take a moment for the modal to appear (animation)
    page.wait_for_selector("text=Welcome to Flipside!")
    page.screenshot(path="verification/1_welcome.png")

    # Click Get Started
    page.get_by_role("button", name="GET STARTED").click()

    # 2. Verify Title and Absence of Rename Button
    print("Verifying Title and Absence of Rename Button...")
    # Verify Header title is "Flipside"
    expect(page.locator("h1")).to_have_text("Flipside")

    # Verify Rename Project button is NOT present
    expect(page.get_by_title("Rename Project")).not_to_be_visible()

    print("Title verified and Rename Button absent.")
    page.screenshot(path="verification/2_header_verified.png")

    # 3. Create New Deck (Test Transition)
    print("Creating new deck...")
    page.get_by_role("button", name="Create New").click()

    # Should be in Edit View
    # Check for "Edit Collection" text
    page.wait_for_selector("text=Edit Collection")

    # Verify Symbol Toolbar exists (part of editor)
    page.wait_for_selector("text=Accents")

    print("Navigated to Deck Editor.")
    page.screenshot(path="verification/4_editor.png")

    # 4. Test Alert (Custom Dialog)
    # Click insert without active field
    print("Testing Custom Alert...")
    # Click 'pi' symbol (in Math tab, or just Accents 'á')
    # Accents is active by default. Click first button 'á'
    page.get_by_role("button", name="á").click()

    # Alert should appear
    page.wait_for_selector("text=Click inside a text box first to insert a symbol.")
    page.screenshot(path="verification/5_alert.png")

    # Close alert
    page.get_by_role("button", name="OK").click()

    print("Verification Complete.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_flipside(page)
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")
        finally:
            browser.close()

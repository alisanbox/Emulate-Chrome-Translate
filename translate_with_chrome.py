import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

# ==================================================
# 🎯 ALL SETTINGS — TWEAK THESE FREELY
# ==================================================
INPUT_FOLDER = "to_translate"
OUTPUT_FOLDER = "translated"

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 900

PAGEDOWN_WAIT = 0.1
RIGHTCLICK_WAIT = 1.2
WAIT_AFTER_T = 5.0
WAIT_AFTER_SCROLL = 8.0       # ✅ Wait 10 seconds AFTER scroll BEFORE saving

BOTTOM_CONFIRM_COUNT = 6
MIN_SCROLLS = 10
# ==================================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(INPUT_FOLDER, exist_ok=True)

def setup_chrome():
    chrome_options = Options()
    
    prefs = {
        "translate.enabled": True,
        "translate.target_language": "en",
        "profile.default_content_setting_values.translation": 1,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    chrome_options.add_argument("--lang=en")
    chrome_options.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
    chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.set_page_load_timeout(120)
    return driver

def rightclick_then_press_T(driver):
    """Right-click → Python sends T key directly to Chrome menu"""
    body = driver.find_element(By.TAG_NAME, "body")
    
    print("🖱️  Right-clicking... menu should OPEN...")
    ActionChains(driver).context_click(body).perform()
    
    print(f"⏱️  Waiting {RIGHTCLICK_WAIT}s for menu to appear...")
    time.sleep(RIGHTCLICK_WAIT)
    
    print("⌨️  Sending 'T' key DIRECTLY to Chrome menu...")
    pyautogui.press("t")
    
    print(f"⏳ Waiting {WAIT_AFTER_T}s for translation to finish...")
    time.sleep(WAIT_AFTER_T)

def scroll_to_bottom_proper(driver):
    """Scroll until actual bottom — tracks position, not height"""
    print(f"🔽 Scrolling (wait={PAGEDOWN_WAIT}s)...")
    
    last_position = -1
    same_count = 0
    scroll_count = 0
    
    while same_count < BOTTOM_CONFIRM_COUNT or scroll_count < MIN_SCROLLS:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(PAGEDOWN_WAIT)
        
        current_position = driver.execute_script("return window.pageYOffset;")
        scroll_count += 1
        
        if current_position == last_position and scroll_count >= MIN_SCROLLS:
            same_count += 1
            print(f"   Scroll {scroll_count}: pos = {current_position}px → confirm {same_count}/{BOTTOM_CONFIRM_COUNT}")
        else:
            same_count = 0
            last_position = current_position
            print(f"   Scroll {scroll_count}: pos = {current_position}px → moving...")
    
    print(f"✅ BOTTOM REACHED! Total PageDown: {scroll_count}")
    
    # ✅ WAIT 10 SECONDS AFTER SCROLL BEFORE SAVING
    print(f"⏳ Waiting {WAIT_AFTER_SCROLL}s before saving...")
    time.sleep(WAIT_AFTER_SCROLL)

def get_output_filename(original_name):
    """✅ Replace CH/JP → EN in filename"""
    base, ext = os.path.splitext(original_name)
    
    # Replace CH → EN (case-insensitive)
    if "CH" in base.upper():
        new_base = base.upper().replace("CH", "EN")
        print(f"📋 Renamed: CH → EN → {new_base}{ext}")
    # Replace JP → EN (case-insensitive)
    elif "JP" in base.upper():
        new_base = base.upper().replace("JP", "EN")
        # Restore original case except for JP→EN
        pattern_jp = "JP" in base
        pattern_jp_lower = "jp" in base
        if pattern_jp:
            new_base = base.replace("JP", "EN")
        elif pattern_jp_lower:
            new_base = base.replace("jp", "en")
        print(f"📋 Renamed: JP → EN → {new_base}{ext}")
    else:
        new_base = base + "_en"
        print(f"📋 No CH/JP found → appended _en → {new_base}{ext}")
    
    return f"{new_base}{ext}"

def translate_file(driver, filepath):
    filename = os.path.basename(filepath)
    print(f"\n📖 Opening: {filename}")
    
    file_url = "file:///" + os.path.abspath(filepath).replace("\\", "/")
    driver.get(file_url)
    
    # Ensure Translate appears in menu
    driver.execute_script("document.documentElement.lang = 'zh-CN';")
    time.sleep(2)
    
    # Right-click + T → translate
    rightclick_then_press_T(driver)
    
    # Scroll + wait 10s before saving
    scroll_to_bottom_proper(driver)
    
    # Extract FULL translated text
    translated_text = driver.execute_script("return document.body.innerText;")
    if not translated_text or len(translated_text) < 50:
        translated_text = driver.find_element(By.TAG_NAME, "body").text
    
    # ✅ Save with CH/JP → EN renamed
    out_name = get_output_filename(filename)
    out_path = os.path.join(OUTPUT_FOLDER, out_name)
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(translated_text)
    
    preview = translated_text[:200].replace("\n", " | ")
    print(f"✅ Saved → {out_name} ({len(translated_text)} characters)")
    print(f"   Preview: {preview}...")

def main():
    driver = setup_chrome()
    print("🌐 Ready — Right-Click+T | Scroll → Wait 10s | CH/JP→EN Rename")
    print("=" * 65)
    print("🖱️  ⌨️  Workflow: Open → Right-click+T → Scroll → Wait 10s → Save")
    print("📋 Filename rule: CH_xxx.txt → EN_xxx.txt | JP_xxx.txt → EN_xxx.txt")
    print("=" * 65)
    
    try:
        files = [f for f in os.listdir(INPUT_FOLDER) 
                 if f.lower().endswith((".txt", ".html", ".htm"))]
        
        if not files:
            print(f"\n📁 Put your files in '{INPUT_FOLDER}' folder!")
            return
        
        print(f"\n📋 Found {len(files)} file(s)")
        for fname in files:
            translate_file(driver, os.path.join(INPUT_FOLDER, fname))
        
        print("\n🎉 ALL DONE! Check 'translated' folder.")
        input("Press Enter to close Chrome...")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
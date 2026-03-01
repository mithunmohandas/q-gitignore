import asyncio
from playwright.async_api import async_playwright

async def scrape_and_sum():
    seeds = range(71, 81)
    total_sum = 0
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for seed in seeds:
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            print(f"Scraping: {url}")
            await page.goto(url)
            
            # Wait for the table to be rendered by JS
            await page.wait_for_selector("table")
            
            # Extract all numeric text from table cells (td)
            cells = await page.query_selector_all("td")
            for cell in cells:
                text = await cell.inner_text()
                try:
                    # Clean the text and convert to float/int
                    val = float(text.strip())
                    total_sum += val
                except ValueError:
                    continue # Skip non-numeric headers or labels
                    
        await browser.close()
    
    print(f"FINAL_TOTAL_SUM: {total_sum}")

if __name__ == "__main__":
    asyncio.run(scrape_and_sum())

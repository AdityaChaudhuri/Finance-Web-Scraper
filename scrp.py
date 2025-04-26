from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime

# Setup options
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")

# Setup driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Go to Yahoo Finance Gainers
driver.get('https://finance.yahoo.com/markets/stocks/gainers/')

# Find all stock rows
rows = driver.find_elements(By.TAG_NAME, 'tr')

# Lists to store data
symbols, names, prices, changes, changes_percent, pe_ratios = [], [], [], [], [], []

# Extract data
for row in rows:
    try:
        symbols.append(row.find_element(By.XPATH, './td[1]').text)
        names.append(row.find_element(By.XPATH, './td[2]').text)
        prices.append(row.find_element(By.XPATH, './td[4]').text)
        changes.append(row.find_element(By.XPATH, './td[5]').text)
        changes_percent.append(row.find_element(By.XPATH, './td[6]').text)
        pe_ratios.append(row.find_element(By.XPATH, './td[10]').text)
    except:
        continue

# Create DataFrame
df = pd.DataFrame({
    "Symbol": symbols,
    "Name": names,
    "Price": prices,
    "Change ($)": changes,
    "Change (%)": changes_percent,
    "P/E Ratio": pe_ratios
})

# Get current timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Save to CSV with timestamp
filename = f'Top_25_Gainers_{timestamp}.csv'
df.to_csv(filename, index=False)

print(f"Saved as {filename}")

# Close browser
driver.quit()

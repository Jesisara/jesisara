from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_indeed(job_title, location, pages=1):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    all_jobs = []

    for page in range(pages):
        start = page * 10
        url = f"https://in.indeed.com/jobs?q={job_title.replace(' ', '+')}&l={location.replace(' ', '+')}&start={start}"
        driver.get(url)
        
        
        time.sleep(5)
        

        card_selectors = [
            "div.job_seen_beacon",
            "div.cardOutline",
            "div.jobsearch-SerpJobCard",
            "div[data-jk]",
            "div.slider_container",
            "div.result"
        ]
        
        cards = []
        for selector in card_selectors:
            try:
                cards = driver.find_elements(By.CSS_SELECTOR, selector)
                if cards:
                    print(f"Found {len(cards)} cards using selector: {selector}")
                    break
            except:
                continue
        
        if not cards:
            print("No job cards found. The page structure may have changed.")
            continue

        print(f"Found {len(cards)} cards on page {page+1}")

        for card in cards:
        
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, 'h2.jobTitle a, h2.jobTitle span, a.jcs-JobTitle, h2 a')
                title = title_elem.text.strip()
            except:
                title = ''

            
            try:
                company = card.find_element(By.CSS_SELECTOR, 'span[data-testid="company-name"], .companyName, span.companyName').text.strip()
            except:
                company = ''

            
            salary = ''
            try:
                
                try:
                    metadata_sections = card.find_elements(By.CSS_SELECTOR, 'div.metadata, div.attribute_snippet')
                    for metadata in metadata_sections:
                        text = metadata.text.strip()
                        if any(word in text.lower() for word in ['₹', 'rs', 'salary', 'pay', 'compensation']):
                            salary = text
                            break
                except:
                    pass
                
        
                if not salary:
                    salary_selectors = [
                        'div.salary-snippet-container',
                        'div[data-testid="attribute_snippet_testid"]',
                        'span.salary-snippet',
                        'div.estimated-salary-container',
                        'span.estimated-salary',
                        'div.metadata.salary-snippet-container'
                    ]
                    
                    for selector in salary_selectors:
                        try:
                            salary_elem = card.find_element(By.CSS_SELECTOR, selector)
                            if salary_elem and salary_elem.text.strip():
                                salary = salary_elem.text.strip()
                                break
                        except:
                            continue
                
            
                if not salary:
                    card_text = card.text.lower()
                    salary_keywords = ['₹', 'rs', 'salary', 'pay', 'compensation', 'per year', 'per month', 'lpa']
                    if any(keyword in card_text for keyword in salary_keywords):
                        
                        lines = card.text.split('\n')
                        for line in lines:
                            if any(keyword in line.lower() for keyword in salary_keywords):
                                salary = line.strip()
                                break
            except:
                salary = ''

        
            try:
                link = card.find_element(By.CSS_SELECTOR, 'h2 a, a.jcs-JobTitle').get_attribute('href')
            except:
                link = ''

            all_jobs.append({
                'Title': title,
                'Company': company,
                'Salary': salary,
                'Job Link': link
            })

    driver.quit()

    df = pd.DataFrame(all_jobs)
    filename = f"indeed_jobs_{int(time.time())}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Saved {len(all_jobs)} jobs to {filename}")
    return df

if __name__ == "__main__":
    job_title = input("Enter job title: ")
    location = input("Enter location: ")
    pages = int(input("How many pages to scrape? "))
    scrape_indeed(job_title, location, pages)

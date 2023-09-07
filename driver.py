from selenium import webdriver


class Driver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("log-level=3")
        self.driver = webdriver.Chrome(options=options)

    def close(self):
        self.driver.close()
        self.driver.quit()

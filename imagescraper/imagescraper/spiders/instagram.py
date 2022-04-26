import time, pickle

import scrapy

from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class InstagramSpider(scrapy.Spider):
	name = 'instagram'
	allowed_domains = ['instagram.com']

	basic_url = 'https://www.instagram.com/explore/tags/'
	current_tag = 0

	def start_requests(self):
		if self.is_login == 'True':
			yield SeleniumRequest(url='https://www.instagram.com/', callback=self.login)
		else:
			yield SeleniumRequest(url='https://www.instagram.com/', callback=self.load_cookies)

	def login(self, response):
		driver = response.request.meta['driver']

		time.sleep(3)
		driver.find_element(By.XPATH, '//input[@name="username"]').send_keys(self.username)
		driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(self.password)
		driver.find_element(By.XPATH, '//div[@class="             qF0y9          Igw0E     IwRSH      eGOV_       acqo5   _4EzTm    bkEs3                          CovQj                  jKUp7          DhRcB                                                    "]').click()
		time.sleep(5)

		pickle.dump(driver.get_cookies(), open('cookies.pkl','wb'))

		yield SeleniumRequest(url=f"{self.basic_url}{self.tags.split(',')[self.current_tag]}/", callback=self.parse)

	def load_cookies(self, response):
		driver = response.request.meta['driver']

		cookies = pickle.load(open('cookies.pkl', 'rb'))
		for cookie in cookies:
			driver.add_cookie(cookie)

		time.sleep(2)

		yield SeleniumRequest(url=f"{self.basic_url}{self.tags.split(',')[self.current_tag]}/", callback=self.parse)

	def parse(self, response):
		driver = response.request.meta['driver']
		prev_scroll_h = list(range(5))

		while len(set(prev_scroll_h)) != 1:
			for img_el in driver.find_elements(By.XPATH, '//div[@class="KL4Bh"]/img'):
				yield {'image_urls': [img_el.get_attribute('src')]}

			driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL, Keys.END)
			time.sleep(3)

			prev_scroll_h.append(driver.execute_script('return document.body.scrollHeight'))
			prev_scroll_h = prev_scroll_h[-5:]

		self.current_tag += 1
		if self.current_tag < len(self.tags.split(',')):
			yield SeleniumRequest(url=f"{self.basic_url}{self.tags.split(',')[self.current_tag]}/", callback=self.parse)

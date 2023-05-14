from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import csv

class CarInfoProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = []
        self.potential_cars = []

        with open(self.filepath, 'r') as file:
            self.data = file.readlines()

        # process raw data
        for ln, line in enumerate(self.data):
            line = line.strip()
            if line[0:2] == "CR":
                # name of car
                name = self.data[ln - 1][2:-2]

                # VIN
                vin = self.data[ln + 1][2:19]

                # ODO
                odoLine = self.data[ln + 2][7:]
                odo = ""
                for c in odoLine:
                    if c == ",":
                        pass
                    elif c != " ":
                        odo += c
                    else:
                        break

                # Lights
                for i in range(len(self.data[ln])):
                    if self.data[ln][i:i+9] == "Light(s):":
                        lights = self.data[ln][i+10:i+13]
                        break

                self.potential_cars.append((name, vin, odo, lights))


    # def __del__(self):
    #     self.driver.quit()
    #     self.f.close()

    def get_car_amount(self):
        return len(self.potential_cars)

    def process_car_info(self, car_num):
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

        options = webdriver.ChromeOptions()

        # specify headless mode
        options.add_argument('headless')
        # specify the desired user agent
        options.add_argument(f'user-agent={user_agent}')
        
        self.driver = webdriver.Chrome(chrome_options=options)

        self.driver.get('https://www.carfax.com/value/')
        self.driver.implicitly_wait(5)

        zip_box = self.driver.find_element(By.ID, 'zip')
        zip_box.send_keys('19355')

        vin_box = self.driver.find_element(By.ID, 'vin')
        vin_box.send_keys(self.potential_cars[car_num][1])

        submit = self.driver.find_element(By.CLASS_NAME, 'vehicle-input-form__input__submit')
        submit.click()

        prices = self.driver.find_element(By.CLASS_NAME, 'results__prices__list')

        actions = ActionChains(self.driver)
        actions.pause(2)
        actions.perform()

        chunk = prices.get_attribute('innerHTML')

        self.driver.quit()

        dollars = []

        for cn, c in enumerate(chunk):
            if c == "$":
                dollars.append(chunk[cn:cn+8])

        value1 = re.sub('[^0-9]', '', dollars[0])
        value2 = re.sub('[^0-9]', '', dollars[1])
        value3 = re.sub('[^0-9]', '', dollars[2])

        entry = f'Name: {self.potential_cars[car_num][0]} \nVIN: {self.potential_cars[car_num][1]} \nMileage: {self.potential_cars[car_num][2]} \nLights: {self.potential_cars[car_num][3]} \nRetail Value: {value1} \nPrivate Party Value: {value2}\nTrade-In Value {value3} \n \n'
        # entry = [self.potential_cars[car_num][0], self.potential_cars[car_num][1], self.potential_cars[car_num][2], self.potential_cars[car_num][3], value1, value2, value3]

        return entry


    # def process_car_info(self):
    #     cars = []
    #     with open(self.filepath, 'r') as file:
    #         cars = file.readlines()

    #     potential_cars = []

    #     for ln, line in enumerate(cars):
    #         line = line.strip()
    #         if line[0:2] == "CR":
    #             # name of car
    #             name = cars[ln - 1][2:-2]

    #             # VIN
    #             vin = cars[ln + 1][2:19]

    #             # ODO
    #             odoLine = cars[ln + 2][7:]
    #             odo = ""
    #             for c in odoLine:
    #                 if c == ",":
    #                     pass
    #                 elif c != " ":
    #                     odo += c
    #                 else:
    #                     break

    #             # self.driver.get('https://www.carfax.com/value/')
    #             # self.driver.implicitly_wait(5)

    #             # zip_box = self.driver.find_element(By.ID, 'zip')
    #             # zip_box.send_keys('19355')

    #             # vin_box = self.driver.find_element(By.ID, 'vin')
    #             # vin_box.send_keys(vin)

    #             # submit = self.driver.find_element(By.CLASS_NAME, 'vehicle-input-form__input__submit')
    #             # submit.click()

    #             # prices = self.driver.find_element(By.CLASS_NAME, 'results__prices__list')

    #             # actions = ActionChains(self.driver)
    #             # actions.pause(2)
    #             # actions.perform()

    #             # chunk = prices.get_attribute('innerHTML')

    #             # dollars = []
    #             # for cn, c in enumerate(chunk):
    #             #     if c == "$":
    #             #         dollars.append(chunk[cn:cn+8])

    #             # value1 = re.sub('[^0-9]', '', dollars[0])
    #             # value2 = re.sub('[^0-9]', '', dollars[1])
    #             # value3 = re.sub('[^0-9]', '', dollars[2])

    #             value1 = "1"
    #             value2 = "2"
    #             value3 = "3"

    #             potential_cars.append((name, vin, odo, value1, value2, value3))
    #             self.writer.writerow([name, vin, odo, value1, value2, value3])

    #     return potential_cars
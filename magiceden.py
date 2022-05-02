import requests
import base64
import time
import os
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from selenium_stealth import stealth

def mint(values, is_windows):

    def select_wallet():
        print("Status - Selecting wallet on ME")

        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div/div/header/nav/div[2]/div[2]/div/button[2]')))
        select_wallet = driver.find_element(
            By.XPATH, '//*[@id="root"]/div/div/div/header/nav/div[2]/div[2]/div/button[2]')
        webdriver.ActionChains(driver).move_to_element(select_wallet).click(select_wallet).perform()

        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[4]/div[1]/div/ul/li/button')))
        phantom_button = driver.find_element(
            By.XPATH, '/html/body/div[4]/div[1]/div/ul/li/button')
        webdriver.ActionChains(driver).move_to_element(phantom_button).click(phantom_button).perform()


        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Connect')]")))
        connect = driver.find_element(
            By.XPATH, "//button[contains(text(),'Connect')]")
        webdriver.ActionChains(driver).move_to_element(connect).click(connect).perform()


        original_window = driver.current_window_handle

        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Connect')]")))
        popup_connect = driver.find_element(
            By.XPATH, "//button[contains(text(),'Connect')]")
        webdriver.ActionChains(driver).move_to_element(popup_connect).click(popup_connect).perform()
        driver.switch_to.window(main_window)

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'I understand')]")))
        agree = driver.find_element(
            By.XPATH, "//button[contains(text(),'I understand')]")
        webdriver.ActionChains(driver).move_to_element(agree).click(agree).perform()

        print("Status - Finished Selecting Wallet on ME")

    def close_popup():
        print("Status - Closing Popup")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[@class='wallet-adapter-modal-button-close']")))
        closePopupButton = driver.find_element(
            By.XPATH, "//button[@class='wallet-adapter-modal-button-close']")
        webdriver.ActionChains(driver).move_to_element(closePopupButton).click(closePopupButton).perform()
        print("Status - Finished Closing Popup")
        time.sleep(5)

    def avait_mint():
        print("Status - Waiting for Mint, maximum time wait is 24h, after that please restart bot")
        WebDriverWait(driver, 60 * 60 * 24).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Mint your token!')]")))
        mint_your_token = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Mint your token!')]")
        driver.execute_script("arguments[0].click();", mint_your_token)

        original_window = driver.current_window_handle
        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Approve')]")))
        approve = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Approve')]")
        approve.click()

    def innit_wallet():
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])

        print("Event - switch window")
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Use Secret Recovery Phrase')]")))
        recovery_phrase = driver.find_element(
            By.XPATH, "//button[contains(text(),'Use Secret Recovery Phrase')]")
        webdriver.ActionChains(driver).move_to_element(recovery_phrase).click(recovery_phrase).perform()

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//textarea[@placeholder='Secret phrase']")))

        password_input = driver.find_element(By.XPATH, "//textarea[@placeholder='Secret phrase']").send_keys(values[1])
        import_button = driver.find_element(By.XPATH, "//button[@class='sc-bdfBQB bzlPNH']").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']")))
        password1 = driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys(values[2])
        password2 = driver.find_element(By.XPATH, "//input[@placeholder='Confirm Password']").send_keys(values[2])
        check_box = driver.find_element(By.XPATH, "//input[@type='checkbox']").click()
        submit = driver.find_element(By.XPATH, "//button[@type='submit']").click()

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Continue')]")))
        continue_ = driver.find_element(By.XPATH, "//button[contains(text(),'Continue')]")
        driver.execute_script("arguments[0].click();", continue_)

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Finish')]")))
        finish = driver.find_element(By.XPATH, "//button[contains(text(),'Finish')]")

        driver.execute_script("arguments[0].click();", finish)
        print("Status - Finished Initializing wallet")
        main_window = driver.window_handles[0]
        driver.switch_to.window(main_window)

        return main_window










    options = Options()

    options.add_extension('Phantom.crx')
    options.add_argument('--disable-gpu')

    prefs = {"profile.managed_default_content_settings.images":2}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(executable_path='YOUR PATH TO CHROME DRIVER', options=options)
    print('Successfully found chrome driver')

    stealth(driver,
            languages=["en-US", 'en'],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get(values[0])

    main_window = innit_wallet()

    select_wallet()

    close_popup()

    avait_mint()









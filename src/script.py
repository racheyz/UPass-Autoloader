import time
import winsdk
import asyncio

from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from winsdk.windows.ui.notifications.management import UserNotificationListener
from winsdk.windows.ui.notifications import NotificationKinds
from winsdk.windows.ui.notifications import KnownNotificationBindings
from winsdk.windows import foundation

from pyautogui import hotkey, press



driver = webdriver.Chrome()
driver.get('https://upassbc.translink.ca/')

dropdown = Select(driver.find_element(By.ID, 'PsiId'))
dropdown.select_by_value('ubc')

go = driver.find_element(By.ID, 'goButton')
go.click()

username = driver.find_element(By.ID, 'username')
username.send_keys("rzhao20")

password = driver.find_element(By.ID, 'password')
password.send_keys('Ocean1812?')

loginAction = ActionChains(driver)

loginAction.move_to_element(password)
loginAction.move_by_offset(-150, 41.3)
loginAction.click()
loginAction.perform()

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Other options')))
options = driver.find_element(By.LINK_TEXT, 'Other options')
options.click()

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "(//li[@data-testid='test-id-sms'])[2]")))
duomessage = driver.find_element(By.XPATH, "(//li[@data-testid='test-id-sms'])[2]")

# clearing notification center before sending code
hotkey('win', 'n')
press('tab')
press('tab')
press('enter')
hotkey('win', 'n')

duomessage.click()

# waiting time for notificaiton
time.sleep(15)


# retrieving duo verification code
listener = UserNotificationListener.current

async def getNotif():
    notification = await listener.get_notifications_async(NotificationKinds.TOAST)
    print(len(notification))
    for n in notification:
        binding = n.notification.visual.get_binding(KnownNotificationBindings.toast_generic)
        text = binding.get_text_elements()
        bodyText = '\n'.join([t.text for t in text[1:]])
        if ("UBC MFA passcode" in bodyText):
            temp = bodyText[-7:]
            return temp
        
    return "no code found"

async def main():
    temp = await getNotif()
    return temp

code = asyncio.run(main())


passcodeinput = driver.find_element(By.ID, 'passcode-input')
passcodeinput.send_keys(code)

verify = driver.find_element(By.XPATH, "//button[@type='submit']")
verify.click()

dontTrustBtn = driver.find_element(By.ID, 'dont-trust-browser-button')
dontTrustBtn.click()

checkbox = driver.find_element(By.ID, 'chk_1')
checkbox.click()


time.sleep(200)


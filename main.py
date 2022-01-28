from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import random
import time
import os


USERNAME = os.getenv("USERNAME")
INSTA_PASS = os.getenv("PASSWORD")
WEB_DRIVER_PATH = os.getenv("WEB_DRIVER_PATH")
INSTA_LINK = "https://www.instagram.com/"
ACCOUNT_TO_FOLLOW_FOLLOWERS = "google/"     # Página do instagram de quem irá seguir os seguidores.
NUM_TO_FOLLOW = 30  # O número de perfis para seguir.


class InstaFollower:
    def __init__(self):
        self.service = Service(WEB_DRIVER_PATH)
        self.driver = WebDriver(service=self.service)

    def login(self):
        """Faz o login no Instagram."""
        self.driver.get(INSTA_LINK)
        time.sleep(2)
        login_input = self.driver.find_elements(By.CSS_SELECTOR, ".f0n8F  input")
        login_input[0].send_keys(USERNAME)
        login_input[1].send_keys(INSTA_PASS)
        time.sleep(1)
        self.driver.find_elements(By.CSS_SELECTOR, ".qF0y9 button")[1].click()
        time.sleep(5)

    def find_followers(self):
        """Acessa a página com os seguidores para seguir."""
        self.driver.get(f"{INSTA_LINK}{ACCOUNT_TO_FOLLOW_FOLLOWERS}")
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, ".k9GMp .Y8-fY  a").click()
        time.sleep(3)

    def follow(self):
        """Segue os seguidores."""
        for n in range(NUM_TO_FOLLOW):
            to_follow_list = self.driver.find_elements(By.CSS_SELECTOR, ".PZuss button")
            self.driver.execute_script("arguments[0].scrollIntoView();", to_follow_list[n])
            try:
                to_follow_list[n].click()
            # Quando clicka em seguir alguém que já segue ou que já pediu para seguir, surge um pop-up questionando
            # se quer deixar de seguir ou cancelar a solicitação de follow. Tal pop-up irá interceptar o click
            # de follow do próximo perfil.
            except ElementClickInterceptedException:
                time.sleep(1)
                try:
                    # Caso tenhamos clickado em unfollow, este é o xpath do botão para cancelar esta ação:
                    self.driver.find_element(By.XPATH, "/html/body/div[7]/div/div/div/div[3]/button[2]").click()
                    # Caso tenhamos clickado em cancelar o pedido de solicitação de follow,
                    # este é o xpath do botão para cancelar esta ação:
                except NoSuchElementException:
                    self.driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div[3]/button[2]").click()
            finally:
                time.sleep(random.randint(1, 5))   # O tempo de espera entre seguir um perfil e outro.
        self.driver.quit()


insta_follower = InstaFollower()
insta_follower.login()
insta_follower.find_followers()
insta_follower.follow()


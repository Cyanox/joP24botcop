import time
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from const import LOGIN, PASSWORD, URL, PRICE_MAX, PRICE_CAT, NB_PLACE
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Configurer les options de Firefox
firefox_options = Options()

# Désactiver l'infobulle indiquant que le navigateur est contrôlé par Selenium
firefox_options.set_preference("dom.webdriver.enabled", False)
firefox_options.set_preference('useAutomationExtension', False)

# Désactiver le flag WebDriver
firefox_options.set_preference("webdriver.firefox.driver", "")

# Modifier l'User-Agent pour un user-agent classique
firefox_options.set_preference("general.useragent.override",
                               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0")

# D'autres options de confidentialité pour éviter la détection
firefox_options.set_preference("privacy.trackingprotection.enabled", True)
firefox_options.set_preference("privacy.resistFingerprinting", True)
firefox_options.set_preference("network.http.sendRefererHeader", 0)

# Initialiser le WebDriver avec les options configurées
driver = webdriver.Firefox(options=firefox_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
firefox_options.set_preference("media.peerconnection.enabled", False)  # Désactiver WebRTC
firefox_options.set_preference("network.http.sendRefererHeader", 0)  # Désactiver l'envoi du referer
driver.execute_script("delete window['navigator']['webdriver']")


def log_in():
    driver.get("https://connect.paris2024.org/oidc/OP_LoginPage.php")
    time.sleep(5)
    email_box = driver.find_element(By.CSS_SELECTOR, "#gigya-textbox-18778297769559624")
    email_box.send_keys(LOGIN)
    time.sleep(3)
    email_box.send_keys(Keys.RETURN)
    time.sleep(5)
    email_box = driver.find_element(By.CSS_SELECTOR, "#gigya-password-29367844582377896")
    email_box.send_keys(PASSWORD)
    email_box.send_keys(Keys.RETURN)
    time.sleep(10)
    return


def check_availability():
    panier = False
    while not panier:
        driver.get(URL)

        time.sleep(3)
        try:
            offers = driver.find_elements(By.CSS_SELECTOR,
                                          "#EventDetailsAndListingCard > div.Card.Card-onEventDetailsPage.Card-isMobileCard.EventDetail-Listing.js-EventDetail-Listing > div.EventEntryList.js-EventEntryList.EventEntryList-clearFloat.u-flexboxSortingContainer.js-EventEntryList-noSeatmap  > div[data-offer-id]")
        except:
            print("Pas trouvé :(")
            pass
        else:
            for offer in offers:
                float(offer.get_attribute("data-splitting-possibility-prices"))
                if float(offer.get_attribute("data-splitting-possibility-prices")) == NB_PLACE and (float(
                        offer.get_attribute("data-splitting-possibility-prices")) < PRICE_MAX or float(
                        offer.get_attribute("data-splitting-possibility-prices")) == PRICE_CAT):
                    try:
                        driver.execute_script("arguments[0].click();", offer)
                    except:
                        pass
                    else:
                        time.sleep(2)
                        try:
                            button = driver.find_element(By.CSS_SELECTOR,
                                                         "#detailCSectionForm > div.p24-detailC-ButtonContainer > button > div > span.p-btn-text.p-font.p-font-size-s-l.p24-detailC-ButtonText")
                        except:
                            pass
                        else:
                            driver.execute_script("arguments[0].click();", button)
                        finally:

                            try:
                                time.sleep(3)
                                driver.find_element(By.CSS_SELECTOR, 'div[class~="ErrorMessage"]')
                            except NoSuchElementException:
                                print("Done")
                                open_window()

                                panier = True
                                break

                            else:
                                pass
    time.sleep(7200)


def open_window():
    print('Fenêtre')
    # Créer une fenêtre principale
    root = tk.Tk()
    root.title("Paris 2024 Tickets")  # Titre de la fenêtre

    # Ajuster la taille de la fenêtre
    root.geometry("400x200")

    # Placer la fenêtre au-dessus des autres
    root.attributes("-topmost", True)
    root.focus_force()

    # Créer un label pour le message "Trouvé"
    label = tk.Label(root, text="Trouvé !")
    label.pack(pady=20)  # Espacement vertical

    # Lancer la boucle principale pour afficher la fenêtre
    root.mainloop()


def main():
    # log_in()
    check_availability()
    time.sleep(7200)
    driver.close()


if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import time

import requests as req

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# CHROME
from webdriver_manager.chrome import ChromeDriverManager  

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains #Double_click

st.set_page_config(page_title='Comunio Primas', page_icon="⚽", layout="wide", initial_sidebar_state="auto")

def calculo_primas(user, prima_por_punto, prima_once):

    opciones=Options()
    # Se pueden añadir muchas más, como entrar en modo incógnito, tener un adblock, etc --> Buscar en google.
    opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
    opciones.add_experimental_option('useAutomationExtension', False)
    prefs = {"credentials_enable_service": False,
    "profile.password_manager_enabled": False}
    opciones.add_experimental_option("prefs", prefs)
    opciones.headless=False
    PATH=ChromeDriverManager().install() 
    #PATH = 'chromedriver.exe'
    
    url = 'https://www.comuniate.com/abonos_primas.php'
    driver=webdriver.Chrome(PATH, options=opciones)
    driver.get(url)
    
    try:
        # cookies
        driver.find_element("xpath",'//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
        time.sleep(1)

    except:
        None
    
    driver.find_element("xpath",'//*[@id="login"]').send_keys(user)
    driver.find_element("xpath",'//*[@id="puntos"]').send_keys(prima_por_punto)
    driver.find_element("xpath",'//*[@id="ideal"]').send_keys(prima_once)
    
    driver.find_element("xpath",'//*[@id="formulario_abonos"]/div[9]/button').click()
    
    time.sleep(5)  
    soup=bs(driver.page_source, 'html.parser')   
    yeh=soup.find_all('td')
    lista_nombres = [e.text.strip() for x in yeh for e in x.find_all('span')]
    lista_dinero = [e.text.strip() for x in yeh for e in x.find_all('strong')]

    nombres = [lista_nombres[e] for e in range(0,len(lista_nombres), 3)]
    dinero = [int(lista_dinero[e][0:lista_dinero[e].find('€')].replace('.', '')) for e in range(0,len(lista_dinero))]

    
    return nombres, dinero

def comunio(user, password, prima_por_punto, prima_once, mensaje, tipo_prima): 
    opciones=Options()
    # Se pueden añadir muchas más, como entrar en modo incógnito, tener un adblock, etc --> Buscar en google.
    opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
    opciones.add_experimental_option('useAutomationExtension', False)
    prefs = {"credentials_enable_service": False,
    "profile.password_manager_enabled": False}
    opciones.add_experimental_option("prefs", prefs)
    opciones.headless=False
    PATH=ChromeDriverManager().install() 
    #PATH = 'chromedriver.exe'
    # Saco los valores de nonbres y dinero de la funcion de comuniate
    nombres_dinero = calculo_primas(user, prima_por_punto, prima_once)
    nombres, dinero = nombres_dinero[0], nombres_dinero[1]
    
    if tipo_prima == 'Penalizar':
        dinero = [-e for e in dinero]
    
    url = 'https://www.comunio.es/setup/clubs/rewardsAndDisciplinary'
    driver=webdriver.Chrome(PATH, options=opciones)
    driver.get(url)

    time.sleep(10)
    

    driver.find_element("xpath",'//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]/span').click()

    time.sleep(1)
    
    driver.find_element("xpath", '//*[@id="above-the-fold-container"]/div[2]/div[1]/div[2]/a[1]/span').click()
    
    
    driver.find_element("xpath",'//*[@id="input-login"]').send_keys(user)
    driver.find_element("xpath",'//*[@id="input-pass"]').send_keys(password)    
    driver.find_element("xpath",'//*[@id="login-btn-modal"]/span').click()
    
    time.sleep(3)
    
    
    for i in range(0,len(nombres)):
        
        driver.find_element("xpath",'//*[@id="user-selection"]/div[2]/div').click()
        time.sleep(1)
        driver.find_element("xpath",'//*[@id="user-selection"]/div[3]/div[' + str(i + 1) + ']/span[2]').click()
        time.sleep(1)
        nombre = driver.find_element("xpath",'//*[@id="user-selection"]/div[1]/span').text
        dic = dict(zip(nombres, dinero))
        dinero_sorted = [e[1] for e in sorted(dic.items())]
        dinero_nombre = dinero_sorted[i]
        driver.find_element("xpath",'//*[@id="amount-input"]').send_keys(dinero_nombre)
        driver.find_element("xpath",'//*[@id="reason-textarea"]').send_keys(mensaje)
        

        driver.find_element("xpath",'//*[@id="submit-btn"]/div[2]').click()
        time.sleep(1)
        driver.refresh()
        time.sleep(3)

    st.success(" Ta to pagao", icon = '💰')
    
st.header("Comunio Payment")

user = st.text_input("User Comunio: ")
password = st.text_input("Password Comunio", type  = 'password')
tipo_prima = st.selectbox("Bonificar o Castigar: ", ['Bonificar', 'Penalizar'])
prima_por_punto = st.text_input("Prima por punto hecho: ", '30000')
prima_once = st.text_input("Prima por jugador en el once ideal: ", '100000')
mensaje = st.text_input("Mensaje pago: ", 'Paid')

pago = st.button("Pagar 💸")

if pago:
    comunio(user, password, prima_por_punto, prima_once, mensaje, tipo_prima)


    



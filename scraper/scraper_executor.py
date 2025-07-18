from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

import time

# Atualize com o caminho real do driver e da URL
URL_TJSP = "https://esaj.tjsp.jus.br/cpopg/open.do"
EXECUTAVEL = "./" 

class ScraperExecutor:
    def __init__(self):
        self.service = Service(executable_path=f"{EXECUTAVEL}msedgedriver")
        #self.service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

    def carregar_pagina(self, filtro: int, documento: str) -> str:
        options = Options()
        #options.add_argument("-headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--remote-debugging-port=9222")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        navegador = webdriver.Chrome(options=options)
        navegador.get(URL_TJSP)

        try:
            select_el = navegador.find_element('xpath', '//*[@id="cbPesquisa"]')
            select_ob = Select(select_el)

            if filtro in [0, 1, 3]:
                select_ob.select_by_value('DOCPARTE')
                navegador.find_element('xpath', '//*[@id="campo_DOCPARTE"]').send_keys(documento)
            elif filtro == 2:
                select_ob.select_by_value('NMPARTE')
                navegador.find_element('xpath', '//*[@id="pesquisarPorNomeCompleto"]').click()
                navegador.find_element('xpath', '//*[@id="campo_NMPARTE"]').send_keys(documento)

            navegador.find_element('xpath', '//*[@id="botaoConsultarProcessos"]').click()
            time.sleep(3)

            return navegador.page_source

        except Exception as e:
            print(f"[ERRO SELENIUM] {e}")
            raise
        finally:
            navegador.quit()

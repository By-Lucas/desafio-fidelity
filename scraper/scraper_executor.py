import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

from bs4 import BeautifulSoup as bs

# URL do TJSP
URL_TJSP = "https://esaj.tjsp.jus.br/cpopg/open.do"
EXECUTABLE_PATH = "./msedgedriver.exe"

class ScraperExecutor:
    def __init__(self):
        self.service = EdgeService(executable_path=EXECUTABLE_PATH)

    def load_search_page(self, filter_type: int, document: str) -> str:
        options = Options()
        options.add_argument("--disable-gpu")
        #options.add_argument("-headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--remote-debugging-port=9222")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Edge(service=self.service, options=options)
        driver.get(URL_TJSP)

        try:
            select_el = driver.find_element(By.XPATH, '//*[@id="cbPesquisa"]')
            select_ob = Select(select_el)

            if filter_type in [0, 1, 3]:
                select_ob.select_by_value('DOCPARTE')
                driver.find_element(By.XPATH, '//*[@id="campo_DOCPARTE"]').send_keys(document)
            elif filter_type == 2:
                select_ob.select_by_value('NMPARTE')
                driver.find_element(By.XPATH, '//*[@id="pesquisarPorNomeCompleto"]').click()
                driver.find_element(By.XPATH, '//*[@id="campo_NMPARTE"]').send_keys(document)

            driver.find_element(By.XPATH, '//*[@id="botaoConsultarProcessos"]').click()
            time.sleep(5)  # Ajuste para aguardar o carregamento da página

            return driver.page_source

        except Exception as e:
            print(f"[SELENIUM ERROR] {e}")
            raise
        finally:
            driver.quit()
    
    def extract_processes_data(self, driver) -> list[dict]:
        soup = bs(driver.page_source, "html.parser")
        items = soup.select("ul.unj-list-row > li")

        base_url = "https://esaj.tjsp.jus.br"
        results = []

        for item in items:
            try:
                link_tag = item.select_one(".linkProcesso")
                process_number = link_tag.get_text(strip=True) if link_tag else None
                relative_url = link_tag['href'] if link_tag else None
                full_url = base_url + relative_url if relative_url else None

                name_div = item.select_one(".nomeParte")
                participant_name = name_div.get_text(strip=True) if name_div else None

                if process_number and full_url:
                    print(f"🔗 Visiting: {full_url}")
                    driver.get(full_url)
                    time.sleep(3)

                    parsed = self.parse_process_detail(driver.page_source)
                    parsed["codigo_processo"] = process_number
                    parsed["nome_completo"] = participant_name or parsed.get("nome_completo")

                    results.append(parsed)

            except Exception as e:
                print(f"[Erro ao processar item]: {e}")
                continue

        return results

    def load_detail_page(self, url: str) -> dict:
        """
        Abre a URL do processo e extrai os dados detalhados da página.
        """
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        navegador = webdriver.Edge(service=self.service, options=options)
        navegador.get(url)

        try:
            time.sleep(5)
            html = navegador.page_source
            soup = bs(html, "html.parser")

            # Aqui você pode ajustar os dados detalhados que deseja extrair:
            return {
                "classe": soup.select_one(".classeProcesso") and soup.select_one(".classeProcesso").text.strip(),
                "assunto": soup.select_one(".assuntoPrincipalProcesso") and soup.select_one(".assuntoPrincipalProcesso").text.strip(),
                "distribuicao": soup.select_one(".dataLocalDistribuicaoProcesso") and soup.select_one(".dataLocalDistribuicaoProcesso").text.strip()
            }

        except Exception as e:
            print(f"[Erro ao carregar detalhes do processo]: {e}")
            return {}
        finally:
            navegador.quit()

    def parse_process_detail(self, html: str) -> dict:
        soup = bs(html, 'html.parser')

        def safe_text(selector):
            el = soup.select_one(selector)
            return el.text.strip() if el else None

        # Extração direta
        foro_vara = safe_text('div.local span.valor') or ""
        foro, vara = (foro_vara.split(" - ", 1) + [None])[:2]

        return {
            "classe": safe_text('div.classe span.valor'),
            "assunto": safe_text('div.assunto span.valor'),
            "data_distribuicao": safe_text('div.dataDistribuicao span.valor'),
            "foro": foro,
            "vara": vara,
            "nome_completo": safe_text('div.nomeParte span'),
            "codigo_processo": None  # preenchido depois
        }

    def get_html_from_url(self, url: str) -> str:
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        navegador = webdriver.Edge(service=self.service, options=options)
        navegador.get(url)
        time.sleep(5)
        html = navegador.page_source
        navegador.quit()
        return html

    def extract_all_pages_data(self, filter_type: int, document: str) -> list[dict]:
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Edge(service=self.service, options=options)
        driver.get(URL_TJSP)

        all_data = []

        try:
            select_el = driver.find_element(By.XPATH, '//*[@id="cbPesquisa"]')
            select_ob = Select(select_el)

            if filter_type in [0, 1, 3]:
                select_ob.select_by_value('DOCPARTE')
                driver.find_element(By.XPATH, '//*[@id="campo_DOCPARTE"]').send_keys(document)
            elif filter_type == 2:
                select_ob.select_by_value('NMPARTE')
                driver.find_element(By.XPATH, '//*[@id="pesquisarPorNomeCompleto"]').click()
                driver.find_element(By.XPATH, '//*[@id="campo_NMPARTE"]').send_keys(document)

            driver.find_element(By.XPATH, '//*[@id="botaoConsultarProcessos"]').click()
            time.sleep(3)

            page_index = 1

            while True:
                print(f"\n📄 Página {page_index}")
                page_data = self.extract_processes_data(driver)
                all_data.extend(page_data)

                try:
                    next_btn = driver.find_element(By.CSS_SELECTOR, 'a.unj-pagination__next')
                    if "disabled" in next_btn.get_attribute("class"):
                        break
                    next_btn.click()
                    time.sleep(3)
                    page_index += 1
                except NoSuchElementException:
                    print("✅ Sem mais páginas.")
                    break

        except Exception as e:
            print(f"[Erro na paginação]: {e}")
        finally:
            driver.quit()

        return all_data

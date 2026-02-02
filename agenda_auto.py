'''Código com mensagem automatica 1 hora antes do agendamento, Favor não mexer!!'''
import urllib.parse
import os

import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def inicializar(url, headless=True):
    # Inicializa o navegador Chrome com opção de modo headless
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    navegador = webdriver.Chrome(options=options)
    navegador.maximize_window()
    # Abre a página da web
    navegador.get(url)
    return navegador

def login(navegador, número, senha):
    try:
        # Preenche e envia o formulário de login
        navegador.find_element(By.NAME, "email").send_keys(número)
        navegador.find_element(By.NAME, "password").send_keys(senha)
        
        # Espera até que o botão de login esteja visível e clicável
        WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "m_login_signin_submit"))
        )
        
        navegador.find_element(By.ID, "m_login_signin_submit").click()
        
        print("Login realizado com sucesso.")
    except TimeoutException:
        print("Erro: Tempo de espera excedido durante o login.")
    except Exception as e:
        print(f"Erro durante o login: {e}")

def espera_agendamento(navegador):
    navegador.refresh()
    print('Espera agendamento')
    agendamentos = WebDriverWait(navegador, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.fc-time-grid-event'))
        )
    return agendamentos

def converter_horario(horario):
    print('converter horario')
    horario_str = horario[0]
    hora, minuto = map(int, horario_str.split(':'))
    return (hora, minuto, 0)

def obter_agendamento(agendamentos, navegador):
    print('obter agendamento')
    print(len(agendamentos))
    for agendamento in range(0, len(agendamentos)-1):
            lista_horario = list()
            # Rola a página para o agendamento atual (exceto o primeiro)
            if agendamento > 0:
                navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", agendamentos[agendamento])
            # Clica no agendamento para abrir o pop-up
            agendamentos[agendamento].click()

            try:
                # Espera até que o widget (pop-up) esteja visível
                widget = WebDriverWait(navegador, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.popover.fade.show.bs-popover-bottom')))
            except TimeoutException:
                # Se o widget inferior não for encontrado, tenta o widget superior
                widget = WebDriverWait(navegador, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.popover.fade.show.bs-popover-top')))
            try:
                # Espera até que o elemento do número de celular esteja visível
                div_celular = WebDriverWait(widget, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".m-widget4__sub.label-spotlight-blue.client-phone.ng-star-inserted")))
                # Extrai o texto do número de celular e remove espaços em branco extras
                numero_celular = div_celular.text.strip()
            except:
                print('Erro: Número de celular não encontrado.')
                navegador.quit()
                exit()

            try:
                # Espera até que o elemento <h2> esteja presente na página
                nome_cliente_element = widget.find_element(By.XPATH, ".//h2")
                nome_cliente = nome_cliente_element.text
            except Exception as e:
                print(f"Erro: {e}")
                nome_cliente = "Cliente"

            try:
                horarios = widget.find_elements(By.CSS_SELECTOR, "span.font-blue")
                for horario in horarios:
                    lista_horario.append(horario.text)
            except Exception as e:
                print(f'Erro {e}')
            sleep(3)
            agendamentos[agendamento].click()

            hora_alvo = converter_horario(lista_horario)
            hora_alvo = datetime.time(*hora_alvo)
            '''while datetime.datetime.now().time() < hora_alvo:
                sleep(1) # para não sobrecarregar a CPU '''
            
            msg = f'Olá {nome_cliente}. Você tem um horário agendado hoje, {hoje.strftime("%d-%m-%y")}, às {lista_horario[0]}. Podemos confirmar?'
            print(hora_alvo)

            hora_alvo_menos_50 = (datetime.datetime.combine(datetime.date.today(), hora_alvo) - datetime.timedelta(minutes=50)).time()
            hora_alvo_menos_30 = (datetime.datetime.combine(datetime.date.today(), hora_alvo) - datetime.timedelta(minutes=30)).time()
            if hora_alvo_menos_50 < hora < hora_alvo_menos_30:
                mandar_msg(msg, navegador_whats, numero_celular)
            else:
                continue
    return msg, numero_celular, hora_alvo
    
def mandar_msg(msg, navegador_whats, numero_celular):
            print('mandar mensagem')
            msg_code = urllib.parse.quote(msg)
            link = f'https://web.whatsapp.com/send?phone={f"55{numero_celular}"}&text={msg_code}'
            navegador_whats.get(link)
            WebDriverWait(navegador_whats, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div/p')))

            try:
                campo_mensagem = WebDriverWait(navegador_whats, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div/p'))
                )
                campo_mensagem.send_keys(Keys.ENTER)
                sleep(2)
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")

def inicializar_whats():
    navegador_whats = webdriver.Chrome()
    navegador_whats.get('https://web.whatsapp.com/')

    # Espera o WhatsApp Web carregar
    WebDriverWait(navegador_whats, 30).until(EC.presence_of_element_located((By.ID, "side")))
    return navegador_whats

# Credenciais de login - usar variáveis de ambiente ou prompt (NÃO COMITAR credenciais)

número = os.getenv('AGENDA_USER') or input('Login (ou defina AGENDA_USER): ')
senha = os.getenv('AGENDA_PASS') or input('Senha (ou defina AGENDA_PASS): ')

url = 'https://www.appsalonsoft.com.br/#/agenda'

hoje = datetime.date.today()

navegador = inicializar(url, headless=False)
login(navegador, número, senha)
navegador_whats = inicializar_whats()

while True:
    agendamentos = espera_agendamento(navegador)
    if len(agendamentos) > 1:
        hora =  datetime.datetime.now().time()
        msg, numero_celular, hora_alvo = obter_agendamento(agendamentos, navegador)
        
    sleep(60)
    
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from difflib import get_close_matches
import re
from datetime import datetime
import requests  # Biblioteca para enviar requisições HTTP

# Baixar os recursos necessários
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Função para encontrar sinônimos em português
def get_synonyms(word):
    synonyms = set(lemma.name() for syn in wn.synsets(word, lang='por') for lemma in syn.lemmas('por'))
    return synonyms

# Função de similaridade semântica e correspondência de palavras próximas
def aval_similar_words(user_input, keywords):
    user_words = word_tokenize(user_input)
    for word in user_words:
        close_matches = get_close_matches(word, keywords, n=1, cutoff=0.8)
        if close_matches:
            return True
        synonyms = get_synonyms(word)
        if any(get_close_matches(syn, keywords, n=1, cutoff=0.8) for syn in synonyms):
            return True
    return False

# Função para enviar a requisição HTTP
def send_request(start_date, end_date, first_report_date, frequency, frequency_details):
    url = "http://example.com/api/agendar-relatorio"  # Substitua pela URL da API real
    payload = {
        "start_date": start_date,
        "end_date": end_date,
        "first_report_date": first_report_date,
        "frequency": frequency,
        "frequency_details": frequency_details
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx
        return response.json()  # Retorna a resposta em formato JSON
    except requests.exceptions.RequestException as e:
        return f"Erro ao enviar a requisição: {e}"

# Função para validar datas
def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%d%m%Y")
        return True
    except ValueError:
        return False

# Função para validar horas
def validate_hour(hour_str):
    try:
        datetime.strptime(hour_str, "%H%M").time()
        return True
    except ValueError:
        return False

# Funções de resposta
def handle_report_query(user_input):
    if 'relatório' in user_input or aval_similar_words(user_input, ['relatório', 'csv', 'documento']):
        return "Você pode agendar relatórios em CSV. Para isso, informe o período desejado, a data para o primeiro relatório e a frequência de geração."
    return None

def handle_scheduling(user_input):
    if 'agendar' in user_input or aval_similar_words(user_input, ['agendar', 'marcar', 'programar']):
        return "Para agendar um relatório, forneça a data inicial, data final, data do primeiro relatório e a frequência desejada (diária, semanal ou mensal)."
    return None

def handle_frequency(user_input):
    if 'frequência' in user_input or aval_similar_words(user_input, ['frequência', 'periodicidade']):
        return "Você pode escolher entre diferentes frequências: diária, semanal ou mensal. Qual você prefere?"
    return None

def handle_frequency_details(frequency):
    if frequency == 'diária':
        return "Você deseja gerar o relatório a cada uma ou a cada duas horas?"
    elif frequency == 'semanal':
        return "Quais dias da semana você deseja gerar o relatório e a cada quantas horas?"
    elif frequency == 'mensal':
        return "Quais meses e dias dos meses você deseja gerar o relatório e a cada quantas horas?"
    return "Frequência não reconhecida. Escolha entre diária, semanal ou mensal."

def handle_dates(user_input):
    if 'data inicial' in user_input or 'data final' in user_input or 'primeira data' in user_input:
        start_date_input = input("Chatbot: Por favor, informe a data inicial do agendamento (exemplo: 01012024): ").strip()
        if not validate_date(start_date_input):
            return "Data inicial inválida. Por favor, informe a data no formato ddmmaaaa."

        end_date_input = input("Chatbot: Agora, informe a data final do agendamento (exemplo: 31122024): ").strip()
        if not validate_date(end_date_input):
            return "Data final inválida. Por favor, informe a data no formato ddmmaaaa."

        first_report_date_input = input("Chatbot: Por fim, informe a data para gerar o primeiro relatório (exemplo: 01012024): ").strip()
        if not validate_date(first_report_date_input):
            return "Data do primeiro relatório inválida. Por favor, informe a data no formato ddmmaaaa."

        frequency = input("Chatbot: Qual é a frequência desejada (diária/semanal/mensal): ").strip().lower()
        if frequency not in ['diária', 'semanal', 'mensal']:
            return "Frequência não reconhecida. Escolha entre diária, semanal ou mensal."

        frequency_details = input(handle_frequency_details(frequency)).strip()

        if frequency == 'diária' and frequency_details not in ['uma', 'duas']:
            return "Para frequência diária, escolha entre a cada uma ou a cada duas horas."

        if frequency == 'semanal':
            days = input("Chatbot: Quais dias da semana (exemplo: segunda-feira, quarta-feira): ").strip()
            if not re.match(r'^(\\w+)(, \\w+)*$', days):
                return "Dias da semana inválidos. Informe os dias como 'segunda-feira, quarta-feira'."
            hours = input("Chatbot: A cada quantas horas (uma ou duas): ").strip().lower()
            if hours not in ['uma', 'duas']:
                return "Para frequência semanal, escolha entre a cada uma ou a cada duas horas."

            frequency_details = {"days": days, "hours": hours}

        if frequency == 'mensal':
            months = input("Chatbot: Quais meses (exemplo: janeiro, fevereiro): ").strip()
            days_of_month = input("Chatbot: Quais dias do mês (exemplo: 1, 15): ").strip()
            hours = input("Chatbot: A cada quantas horas (uma ou duas): ").strip().lower()
            if hours not in ['uma', 'duas']:
                return "Para frequência mensal, escolha entre a cada uma ou a cada duas horas."

            frequency_details = {"months": months, "days_of_month": days_of_month, "hours": hours}

        # Enviar a requisição após validar as datas e frequência
        response = send_request(start_date_input, end_date_input, first_report_date_input, frequency, frequency_details)
        return (f"Agendamento definido:\n"
                f"Data inicial: {start_date_input}\n"
                f"Data final: {end_date_input}\n"
                f"Primeira data do relatório: {first_report_date_input}\n"
                f"Frequência: {frequency}\n"
                f"Detalhes da frequência: {frequency_details}\n"
                f"Resposta da API: {response}")
    return None

def handle_notification(user_input):
    if 'mensagem' in user_input or aval_similar_words(user_input, ['mensagem', 'notificação']):
        return "Você pode receber uma notificação quando o relatório estiver pronto. Deseja habilitar isso (sim/não)?"
    return None

def handle_cancellation(user_input):
    if 'cancelar' in user_input or aval_similar_words(user_input, ['cancelar', 'remover']):
        return "Para cancelar um agendamento, informe o ID do agendamento que você deseja remover."
    return None

def handle_help(user_input):
    if 'ajuda' in user_input or aval_similar_words(user_input, ['ajuda', 'suporte', 'assistência']):
        return "Estou aqui para ajudar com o agendamento de relatórios. Se precisar de mais informações ou assistência, pergunte."
    return None

# Função principal do chatbot
def chatbot():
    print("Olá! Eu sou o chatbot. Pergunte-me sobre o agendamento de relatórios em CSV e eu tentarei ajudar.")

    # Variáveis para armazenar o estado do agendamento
    state = 'inicial'
    frequency = None
    start_date = None
    end_date = None
    first_report_date = None

    while True:
        user_input = input("Você: ").strip().lower()

        if user_input in ['sair', 'exit', 'quit']:
            print("Chatbot: Até mais!")
            break

        if state == 'inicial':
            if 'relatório' in user_input:
                print("Chatbot: Você pode agendar relatórios em CSV. Para isso, informe o período desejado, a data para o primeiro relatório e a frequência de geração.")
            elif 'agendar' in user_input:
                state = 'datas'
                print("Chatbot: Para agendar um relatório, forneça a data inicial, data final, data do primeiro relatório e a frequência desejada (diária, semanal ou mensal).")
            elif 'frequência' in user_input:
                print(handle_frequency(user_input))
            else:
                print("Chatbot: Desculpe, não entendi sua solicitação. Tente perguntar sobre agendamento de relatórios, datas ou frequência.")

        elif state == 'datas':
            print(handle_dates(user_input))

if __name__ == '__main__':
    chatbot()

import requests
from pywebio import input, output, start_server
from db import save_vacancy

experience_options = [
    {"id": "noExperience", "name": "Нет опыта"},
    {"id": "between1And3", "name": "От 1 года до 3 лет"},
    {"id": "between3And6", "name": "От 3 до 6 лет"},
    {"id": "moreThan6", "name": "Более 6 лет"}
]

employment_options = [
    {"id": "full", "name": "Полная занятость"},
    {"id": "part", "name": "Частичная занятость"},
    {"id": "project", "name": "Проектная работа"},
    {"id": "volunteer", "name": "Волонтерство"},
    {"id": "probation", "name": "Стажировка"}
]


def get_vacancies(keyword, experience, employment):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": keyword,
        "experience": experience,
        "employment": employment,
        "area": 1,  # Specify the desired area ID (1 is Moscow)
        "per_page": 100,  # Number of vacancies per page
    }
    headers = {
        "User-Agent": "Your User Agent",  # Replace with your User-Agent header
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        vacancies = data.get("items", [])
        num_vacancies = len(vacancies)

        if num_vacancies > 0:
            for i, vacancy in enumerate(vacancies):
                # Extract relevant information from the vacancy object
                vacancy_id = vacancy.get("id")
                vacancy_title = vacancy.get("name")
                vacancy_url = vacancy.get("alternate_url")
                company_name = vacancy.get("employer", {}).get("name")

                vacancy_data = {
                    "id": vacancy_id,
                    "title": vacancy_title,
                    "url": vacancy_url,
                    "company": company_name,
                    "experience": experience,
                    "employment": employment
                }

                save_vacancy(vacancy_data)  # Save to MongoDB

                output.put_text(f"🆔ID: {vacancy_id}")
                output.put_text(f"✍️Title: {vacancy_title}")
                output.put_text(f"🏦Company: {company_name}")
                output.put_text(f"🖥URL: {vacancy_url}")
                output.put_text("")  # Add an empty line for separation

                if i < num_vacancies - 1:
                    output.put_text("✨✨✨✨✨")  # Add separation line
        else:
            output.put_text("No vacancies found.")
    else:
        output.put_text(f"Request failed with status code: {response.status_code}")

def search_vacancies():
    keyword = input.input("Enter a keyword to search for vacancies:", type=input.TEXT)

    experience = input.select("Select your experience level:",
                              options=[(opt["name"], opt["id"]) for opt in experience_options])

    employment = input.select("Select employment type:",
                              options=[(opt["name"], opt["id"]) for opt in employment_options])

    output.clear()
    output.put_text("Searching for vacancies...")
    get_vacancies(keyword, experience, employment)

if __name__ == '__main__':
    start_server(search_vacancies, port=8080)

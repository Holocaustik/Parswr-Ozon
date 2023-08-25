import openai

# Установите ваш API-ключ OpenAI
openai.api_key = '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'


def communicate_with_gpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    if len(response.choices) > 0:
        return response.choices[0].text.strip()
    return None


# Основной цикл программы
while True:
    user_input = input("Вы: ")
    if user_input.lower() == 'выход':
        break

    # Отправка запроса к GPT
    response = communicate_with_gpt(user_input)

    if response:
        print("GPT: " + response)
    else:
        print("Произошла ошибка при связи с GPT.")

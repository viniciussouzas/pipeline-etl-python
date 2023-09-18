import pandas as pd
import requests
import json
import openai

openai.api_key = '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'
sdw_api_url = 'https://sdw-2023-prd.up.railway.app'

# extract
df = pd.read_csv('userIds.csv')
user_ids = df['UserID'].tolist()


def get_user(id):
  response = requests.get(f'{sdw_api_url}/users/{id}')

  if response.status_code == 200:
    return response.json() 
  else:
    None

users = [user for id in user_ids if (user := get_user(id)) is not None]

#transform
def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista sobre o universo Marvel e seus super-heróis."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre os poderes e habilidades de algum super-herói (máximo de 200 caracteres)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "description": news
  })

# load
def update_user(user):
  response = requests.put(f"{sdw_api_url}/users/{user['id']}", json=user)
  if response.status_code == 200:
    return True
  else:
    return False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")

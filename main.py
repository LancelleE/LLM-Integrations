from dotenv import dotenv_values

CONFIG = dotenv_values('.env')

print(CONFIG['CLAUDE_API_KEY'])

"""
Main module of this little workaround about LLMs.
"""
from dotenv import dotenv_values

CONFIG = dotenv_values('.env')
if __name__ == '__main__':
    if CONFIG['CLAUDE_API_KEY']:
        print('Claude OK, enjoy !')
    else:
        print('Please provide a .env file, with a Claude API key, formatted like in .env-example')

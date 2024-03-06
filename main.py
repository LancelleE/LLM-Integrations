"""
Main module of this little workaround about LLMs.
"""
from dotenv import dotenv_values

CONFIG = dotenv_values('.env')
if __name__ == '__main__':
    for provider in CONFIG:
        print(f'{provider} : OK !')

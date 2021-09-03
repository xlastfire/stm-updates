import re
import requests as req

import os

try:
    from credentials import USERNAME, PASSWORD
    
    if USERNAME.strip() == '' or PASSWORD.strip()  == '':
        print('Empty credentials in credentials.py!')
        print('Exiting..')
        exit(0)
        
except ModuleNotFoundError:
    print('Cannot find credentials.py\n Read the README.md')
    exit(1)

try:
    from bs4 import BeautifulSoup as Soup
    
except ModuleNotFoundError:
    print('Cannot import soup!. Trying to install...')

    os.system('pip install beautifulsoup4')

    try:
        from bs4 import BeautifulSoup as Soup
    except ModuleNotFoundError:
        print('Something error!. Exiting...')
        exit(1)



url = 'http://stm.eng.ruh.ac.lk/src/login.php'

PREFIX = 'http://stm.eng.ruh.ac.lk/src/'

login_url = 'http://stm.eng.ruh.ac.lk/src/redirect.php'
login_data = {'login_username_1': USERNAME,
              'login_username_2': 'engug.ruh.ac.lk',
              'secretkey': PASSWORD,
              'news_go': 'Sign in'}

page1 = 'http://stm.eng.ruh.ac.lk/src/webmail.php'
page2 = 'http://stm.eng.ruh.ac.lk/src/right_main.php'


def de_emojify(text):
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


def main():
    to_console = False

    output_path = 'emails.txt'
    f = open(output_path, 'w', encoding='utf-8')
    
    f.write('=' * 100)
    if to_console:
        print('=' * 100)

    with req.Session() as s:
        s.get(url)
        s.post(login_url, data=login_data)
        for_cook = s.get(page1)
        cook = for_cook.cookies
        r = s.get(page2)

    soup = Soup(r.content, 'html.parser')

    rows = soup.find_all('tr', attrs={'valign': 'top'})

    print(f'Found {len(rows)} emails')
    index = 0
    for row in rows:
        status = 'Read'
        row_content = row.contents
        sender_name = row_content[3].text
        sender_email = row_content[3]['title']
        sent_time = row_content[5].text
        email_link = PREFIX + row_content[9].a['href']
        try:
            description = row_content[9].contents[0].contents[0].a['title']
        except AttributeError:
            description = row_content[9].contents[0].contents[0]
        except TypeError:
            status = 'Unread'
            try:
                description = row_content[9].contents[0].contents[0]['title']
            except KeyError:
                description = row_content[9].contents[0].contents[0].contents[0]

        result = f'''
Status       - {status}
Description  - {description}
Name         - {sender_name}
From         - {sender_email}
Time         - {sent_time}
Email        - {email_link}
'''
        
        if to_console:
            try:
                print(result)
            except UnicodeEncodeError:
                print(f'{" "*19}######## Cannot print here due to encoding characters ########')
                print(f'{" "*25}######## Check emails.txt after execution ########')


        try:
            f.write(result)
        except UnicodeEncodeError:
            f.write(de_emojify(result))

        f.write('-' * 100)
        if to_console:
            print('-' * 100)

        page(email_link, s, f, cook, to_console)

        f.write('=' * 100)
        f.write('\n\n\n')

        if to_console:
            print('=' * 100)
            print('\n\n\n')
        index += 1

        if not to_console:
            print(f'Saved {index} email...')

    f.close()



def page(page_url, session, f, cook, to_console):

    r = session.get(page_url, cookies=cook)
    soup = Soup(r.content, 'html.parser')

    description_content = soup.contents[2].contents[3].contents[7].contents[2].contents[0].contents[1].text
    items = description_content.split('\n')

    subject = items[1]
    sender_name = items[3].replace('" <', ' - ').replace('>', '').replace('"', '')
    date = items[5]
    cc = items[9].replace('" <', ' - ').replace('>', '').replace('"', '')
    priority = items[11]

    msg = soup.contents[2].contents[3].contents[8].contents[1].contents[0].text

    email_content = f'''
Subject      - {subject}
Sender       - {sender_name}
Date         - {date}
CC           - {cc}
Priority     - {priority}

Content      - {msg}
'''
    if to_console:
        try:
            print(email_content)
        except UnicodeEncodeError:
            print(f'{" "*19}######## Cannot print here due to encoding characters ########')
            print(f'{" "*25}######## Check emails.txt after execution ########')

    try:
        f.write(email_content)
    except UnicodeEncodeError:
        f.write(de_emojify(email_content))


if __name__ == '__main__':
    os.system('cls')
    main()
    print('Done!')

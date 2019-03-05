# encoding: utf-8
# mathilda 2.0 - 05/03/2019 - python 2.x

import telepot, sys, time
from subprocess import call
import urllib
from urlparse import urlparse
import requests
import os
from bs4 import BeautifulSoup

call(['clear']) # clear terminal log
reload(sys)
sys.setdefaultencoding('utf8') # force utf-8

def handle(msg):

    def response(id, response):
        bot.sendMessage(id, response, reply_to_message_id=chat_msgid, parse_mode='Markdown')

    (content_type, chat_type, chat_id) = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    msg_id = msg['message_id']

    if content_type == 'new_chat_member': # New user on chat
        user_user = '@' + msg['from']['username']
        bot.sendMessage(chat_id, 'Welcome to the club, {0}!'.format(user_user), reply_to_message_id=msg_id, parse_mode='Markdown')
    else: # Can use others content_type values like text, document, media, etc
        pass

    try:

        id = msg['from']['id']
        msg_id = msg['message_id']
        chat_id = msg['chat']['id']
        message = msg['text'].split() # message parse the message into elements
        message2 = msg['text'] # message2 its the raw text
        len_msg = len(message) # count the elements in the message, useful for control commands syntaxe
        user_user = msg['from']['first_name']

    except Exception as e:
        print(e)
        pass

    if ('mathilda') in message2 or ('Mathilda') in message2:
        if ('search_pdf') in message2:

            query = message2.replace('mathilda', '')
            query = query.replace('search_pdf', '')
            query = query
            print query

            search = ('%s filetype:pdf' % (query))
            page = requests.get("https://www.google.com/search?q={}&num=5".format(search))
            soup = BeautifulSoup(page.content, "html5lib")
            links = soup.findAll('a')
            payload = ''

            for link in links:
                link_href = link.get('href')
                if "url?q=" in link_href and not "webcache" in link_href:
                    payload+='Link: `'+link.get('href').split("?q=")[1].split("&sa=U")[0]+'`\n'
            if payload:
                bot.sendMessage(chat_id, '{0}'.format(payload), reply_to_message_id=msg_id, parse_mode='Markdown')


        if ('pastebin_raw') in message2:

            query = message[-2]
            num_result = int(message[-1])

            print(query)
            print(num_result)
            print(len_msg)

            if len_msg == 4:
                bot.sendMessage(chat_id, '[+] `Crawling...`\n\n[+] **Query**: `{}`\n[+] **Site**: `pastebin.com`\n[+] **Num. Results**: `{}`'.format(query, num_result), reply_to_message_id=msg_id, parse_mode='Markdown')

                search = ("intext:'{}' inurl:'pastebin.com'".format(query))
                page = requests.get('https://www.google.com/search?q=%s&num=%d' % (search, num_result))
                soup = BeautifulSoup(page.content, 'html5lib')
                links = soup.findAll('a')
                filer = ''

                for link in links:
                    link_href = link.get('href')
                    if ('url?q=') in link_href and not ('webcache') in link_href:
                        grabber = link.get('href').split("?q=")[1].split("&sa=U")[0]
                        x = urlparse(grabber)
                        data = urllib.urlopen("https://pastebin.com/raw{0}".format(x[2])).read()
                        filer += ('[+] URL: {}\n\n{}\n============================================================\n\n'.format(grabber, data))

                if filer:
                    file = ('pastebin.log')
                    call(['rm', '%s' % (file)])
                    with open(file, 'a') as raw_write:
                        raw_write.write(filer)
                        bot.sendDocument(chat_id, open(file, 'rb'), reply_to_message_id=msg_id)
            else:
                bot.sendMessage(chat_id, '[-] Invalid Syntaxe. Usage: `Mathilda pastebin_raw QUERY NUM.RESULTS`', reply_to_message_id=msg_id, parse_mode='Markdown')

    print('%s: %s' % (user_user, message2))


bot = telepot.Bot('760224003:AAGBSYwMcnKvP0kRX3rc4g52y7_NlZQFHW8')
bot.message_loop(handle)
print('Online!')

while True:
    pass

######################################################
# Python Script - Description of the Script
######################################################
# Author: abaye
# Date: 15/05/2023
# Description: הורדת מערכת טלפונית של ימות המשיח באופן מלא או חלקי תוך שמירה על הירארכיית התיקיות.
# Instructions:
#   1. בהפעלה תתבקשו להזין מספר מערכת וסיסמה.
#   2. בשאלה השלישית תשאלו האם אתם רוצים להוריד את כל המערכת או רק תיקייה ספציפית, להורדה של כל המערכת יש ללחוץ אנטר בלבד, להורדת תיקיה ספציפית ותיקיות המשנה שלה, יש להזין אותה כך: "3/2" ואז ללחוץ אנטר.
#   3. כעת ייפתח לכם חלון שבו תתבקשו לבחור תיקיה שאליה ירדו הקבצים, וזהו זה יתחיל לרוץ...
# Contact Information:
#   - Email: ca@abaye.ml
#   - GitHub: github.com/abaye123
#   - Link: 
######################################################


import requests
import json
import os
import tkinter as tk
from tkinter import filedialog


def format_file_size(size):
    size_mb = size / (1024 * 1024)
    if size_mb < 0.01:
        formatted_size = '{} bytes'.format(size)
    else:
        formatted_size = '{:.2f} MB'.format(size_mb).rstrip('0').rstrip('.')
    return formatted_size


def download_file(url, destination):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f'Error downloading file from {url}: {str(e)}')


def process_item(item, parent_path):
    if item['fileType'] == 'DIR' or item['fileType'] == 'EXT':
        dir_path = os.path.join(os.path.expanduser(
            '~'), new_folder_path, parent_path, item['name'])
        try:
            os.makedirs(dir_path, exist_ok=True)
        except OSError as e:
            print(f'Error creating directory {dir_path}: {str(e)}')
            return

        response = requests.get(
            f'https://call2all.co.il/ym/api/GetIvrTree?path={item["what"]}&token={token}')
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f'Error fetching items for {item["what"]}: {str(e)}')
            return

        data = json.loads(response.text)
        if data['responseStatus'] == 'OK':
            sub_items = data['items']
            for sub_item in sub_items:
                process_item(sub_item, os.path.join(parent_path, item['name']))
        else:
            print(
                f'Error fetching items for {item["what"]}: {data["responseStatus"]}')
    else:
         if item['fileType'] == fileType or fileType == '':
            if item['fileType'] ==  'AUDIO':
                item_what = item["what"][:-3] + "txt"
                filename = item['name'][:-3] + "txt"
                file_url = f'https://call2all.co.il/ym/api/DownloadFile?path={item_what}&token={token}'
                download_path = os.path.join(os.path.expanduser(
                    '~'), new_folder_path, parent_path, filename)
                try:
                    download_file(file_url, download_path)
                    size_mb = format_file_size(item['size'])
                    print('\033[33mDownloaded:\033[0m', '\033[34m', filename, '\033[33mwhat\033[0m:',
                        '\033[34m', item_what, ' \033[33mSize\033[0m:', '\033[34m', size_mb, '\033[0m')
                except Exception as e:
                    print(f'Error downloading file {filename}: {str(e)}')
            
            file_url = f'https://call2all.co.il/ym/api/DownloadFile?path={item["what"]}&token={token}'
            filename = item['name']
            download_path = os.path.join(os.path.expanduser(
                '~'), new_folder_path, parent_path, filename)
            try:
                download_file(file_url, download_path)
                size_mb = format_file_size(item['size'])
                print('\033[33mDownloaded:\033[0m', '\033[34m', filename, '\033[33mwhat\033[0m:',
                    '\033[34m', item['what'], ' \033[33mSize\033[0m:', '\033[34m', size_mb, '\033[0m')
            except Exception as e:
                print(f'Error downloading file {filename}: {str(e)}')

while True:
    user = input('\033[33mהזן את מספר המערכת: \033[0m')
    password = input('\033[33mהזן את הסיסמה: \033[0m')

    url = f'https://call2all.co.il/ym/api/Login?path=ivr2:/&username={user}&password={password}'
    response = requests.get(url)

    try:
        response.raise_for_status()
        data = json.loads(response.text)

        if data['responseStatus'] == 'OK':
            token = data['token']
            break
        else:
            print(f'Response status is not OK: {data}')
            print('\033[33mPlease try again:\033[0m\n')
    except requests.exceptions.RequestException as e:
        print(f'Error fetching items: {str(e)}')
        print('\033[33mPlease try again:\033[0m\n')

paths = input('\033[33mהזן נתיב הורדה מותאם אישית, בפורמט "2" או "9/1", להורדת המערכת כולה השאר ריק: \033[0m')
fileType = input('\033[33mהזן פורמט קובץ רצוי להורדה, יש להשתמש באותיות גדולות, להורדת כל סוגי הקבצים השאר ריק: \033[0m')

root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory()

if folder_path:
    new_folder_path = os.path.join(folder_path, user, paths)
    print("Selected folder path with: ", new_folder_path)
    
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    else:
        print("Directory already exists.")
else:
    print("No folder selected.")


print(new_folder_path)
print('Download starter...')

response = requests.get(f'https://call2all.co.il/ym/api/GetIvrTree?path=ivr2:{paths}/&token={token}')
try:
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f'Error fetching items: {str(e)}')
    exit(1)

data = json.loads(response.text)

if data['responseStatus'] == 'OK':
    items = data['items']
    for item in items:
        process_item(item, '')

requests.get(f'https://call2all.co.il/ym/api/Logout?token={token}')

print('\033[31mההורדה הושלמה בהצלחה!:\033[31m\n')

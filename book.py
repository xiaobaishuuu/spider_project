from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time,base64,os
from PIL import Image

chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

book_id = '1594'
ori_url = 'https://sjrc.club/yy2/zh-HK/read?id='
path = f'C:\\Users\\OWNER\\Documents\\script\\python\\project\\book\\{book_id}'

username = 'yy219008@yy2.edu.hk'
password = '7dYOwlaz'

driver.get(ori_url+book_id)
driver.implicitly_wait(10)

def login(username,password):
    input_box = driver.find_elements(By.CLASS_NAME, 'q-field__native')
    input_box[0].send_keys(username)
    input_box[1].send_keys(password)
    login_button = driver.find_element(By.TAG_NAME, 'button')
    login_button.click()

def get_img(page):
    time.sleep(1)
    canvas = driver.find_element(By.TAG_NAME,'canvas')
    url = driver.execute_script('return arguments[0].toDataURL("image/png");',canvas)
    header, encoded = url.split(',', 1)
    image_data = base64.b64decode(encoded)
    with open(f'{path}\\{page}.png', 'wb') as f:
        print(f'downloading page_{page}.png {header}')
        f.write(image_data)
        return image_data

def page_operating(ratio = 300):
    driver.implicitly_wait(60)
    driver.find_element(By.XPATH,"//div[contains(@class,'tw-items-center tw-justify-between')]/div[2]/div[4]").click()
    setting = driver.find_element(By.XPATH,"//div[contains(@class,'tw-w-24 tw-h-24 tw-rounded-4 tw-border tw-border-solid tw-border-#CFD7D5 tw-flex tw-justify-center tw-items-center tw-cursor-pointer hover:tw-bg-#F5F7F7')][2]")
    for i in range((ratio - 100)//25): setting.click()
    next_page = driver.find_element(By.XPATH,"//div[contains(@class,'tw-w-48 tw-h-48 tw-flex tw-justify-center tw-items-center tw-cursor-pointer tw-ml-4')]")
    page = 1
    os.makedirs(path)
    prev = None
    while True:
        curr = get_img(page)
        if prev != curr:
            next_page.click()
            page += 1
            prev = curr
        else:
            os.remove(f'{path}\\{page}.png')
            return

def convert_images_to_pdf(image_file):
    os.chdir(image_file)
    images = []
    file_lis = sorted(os.listdir(image_file),key=lambda x:int(x.split('.')[0]))
    output_path = f'{book_id}.pdf'
    con = 0
    for image_path in file_lis:
        if image_path.endswith(('.jpg', '.png')):
            image = Image.open(image_path)
            images.append(image.convert("RGB"))
            con += 1
            print('making PDF:',image_path)
    images[0].save(output_path, save_all=True, append_images=images[1:])

if __name__ == '__main__':
    login(username,password)
    page_operating()
    convert_images_to_pdf(path)
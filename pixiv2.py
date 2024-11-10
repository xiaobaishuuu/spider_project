import requests
import urllib.parse
import json,jsonpath
import os
import sys

if getattr(sys,'frozen',False):
    ABS_PATH = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    ABS_PATH = os.path.dirname(os.path.abspath(__file__))
ABS_PATH = ABS_PATH.replace('\dist','')

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Referer':'https://www.pixiv.net/',
    }
VERSION = '82d3db204a8e8b7e2f627b893751c3cc6ef300fb'
ORIGINAL_URL = 'https://www.pixiv.net/tags/%E5%B0%91%E5%A5%B3/illustrations?p=1&type=illust&ratio=0.5'

def get_json_data(url,headers,path:str) -> list:
    content = requests.get(url=url,headers=headers).text
    obj = json.loads(content)
    return jsonpath.jsonpath(obj,path)

def get_art_id(keyword,start_page=1,end_page=1) -> list:
    # https://www.pixiv.net/ajax/search/illustrations/%E5%B0%91%E5%A5%B3?word=%E5%B0%91%E5%A5%B3&order=date_d&mode=all&p=1&s_mode=s_tag_full&type=illust&ratio=0.5&lang=zh&version=82d3db204a8e8b7e2f627b893751c3cc6ef300fb
    art_id_list = []
    keyword = urllib.parse.quote(keyword)
    for page in range(start_page,end_page+1):
        url = f'https://www.pixiv.net/ajax/search/illustrations/{keyword}?word={keyword}&order=date_d&mode=all&p={page}&s_mode=s_tag_full&type=illust&ratio=0.5&lang=zh&version={VERSION}'
        data = get_json_data(url=url,headers=HEADERS,path='$..data..id')
        if not data and page == 1:
            print('no relevant image available')
            input()
        elif data:
            art_id_list.extend(data)
        else:
            print(f'no relevant image after {page} page')
            break
    return art_id_list

def get_img_src(art_id) -> list:
    # https://www.pixiv.net/ajax/illust/110538270/pages?lang=zh&version=82d3db204a8e8b7e2f627b893751c3cc6ef300fb
    url = f'https://www.pixiv.net/ajax/illust/{art_id}/pages?lang=zh&version={VERSION}'
    return get_json_data(url=url,headers=HEADERS,path='$..original')

# def get_recomendation(keyword):
#     # https://www.pixiv.net/ajax/search/illustrations/%E7%BE%8E%E5%B0%91%E5%A5%B3?word=%E7%BE%8E%E5%B0%91%E5%A5%B3&order=date_d&mode=all&p=1&s_mode=s_tag_full&type=illust&ratio=0.5&lang=zh&version=82d3db204a8e8b7e2f627b893751c3cc6ef300fb
#     url = f'https://www.pixiv.net/ajax/search/illustrations/{keyword}?word={keyword}&order=date_d&mode=all&p=1&s_mode=s_tag_full&type=illust&ratio=0.5&lang=zh&version={VERSION}'
#     return get_json_data(url=url,headers=HEADERS,path='$..relatedTags')[0]

if __name__ == '__main__':
    keyword = input('关键字 keyword:')
    start_page = int(input('起始页面:'))
    end_page = int(input('终止页面:'))

    art_id_list = get_art_id(keyword,start_page,end_page)
    # ==========================================================================
    # 此功能為下載後提供推薦標簽，用於複製粘貼
    # recommend_list = get_recomendation(keyword)
    # for recommend in recommend_list:
    #     print(recommend,end=' ')
    # ==========================================================================
    # for loop主页所有id并获得作品链接
    for art_id in art_id_list:
        src_list = get_img_src(art_id=art_id)
        # 通过单个作品链接获取全作品链接
        for i in range(len(src_list)):
            src = src_list[i]
            with open(file=f'{ABS_PATH}/img/{art_id}_{i}.jpg',mode='wb') as fp:
                content = requests.get(url=src,headers=HEADERS).content
                fp.write(content)
                print(f'完成 {art_id}_{i}.jpg')
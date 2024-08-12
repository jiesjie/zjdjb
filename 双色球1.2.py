"""
双色球   每日任务
https://rf24-h1.cwlo.com.cn/?inviterId=211&from=qr  这个有邀请
https://rf24-h1.cwlo.com.cn/?from=wx_friend    这个没有邀请


不知道怎么时候过期  要等水   9点30左右
Authorization#备注
"""
import requests
import os
import time
import random
from urllib.parse import urlencode

#本地测试用 
os.environ['srqxhh1'] = '''

'''
blsytxt = 1   # 设置变量 / 文本
def create_headers(an):
    headers = {
    "Connection": "keep-alive",
    #"Content-Length": "8",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Android WebView\";v=\"126\"",
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    #"sec-ch-ua-mobile": "?1",
    "Authorization": an,
    "User-Agent": "Mozilla/5.0 (Linux; Android 11; MI 9 SE Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260093 MMWEBSDK/20240501 MMWEBID/4353 MicroMessenger/8.0.50.2701(0x28003255) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    #"sec-ch-ua-platform": "\"Android\"",
    #"Origin": "https://rf24-h1.cwlo.com.cn",
    #"X-Requested-With": "com.tencent.mm",
    #"Sec-Fetch-Site": "same-site",
    #"Sec-Fetch-Mode": "cors",
    #"Sec-Fetch-Dest": "empty",
    #"Referer": "https://rf24-h1.cwlo.com.cn/",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}
    return headers

# 环境变量和文件变量的获取
def get_variable(source, var_name='srqxhh', file_path='srqxhh.txt'):
    if source == 'env':
        value = os.getenv(var_name)
    else:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                value = file.read().strip()
        except FileNotFoundError:
            print(f'文件{file_path}未找到，请检查。')
            return None
    if not value:
        print(f'{var_name}未设置或为空，请检查。')
        return None
    accounts = value.strip().split('\n')
    print(f'-----------本次账号运行数量：{len(accounts)}-----------')
    return accounts


# 请求封装  请求体版
def post_request(url, headers, data=None, json_data=None):
    try:
        if json_data:
            response = requests.post(url, headers=headers, json=json_data)
        else:
            response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")
    return None

# 查询阳光和提交ID
def process_sun(an):
    sun_data = post_request('https://rf24-serv.cwlo.com.cn/api/user/sun/list', create_headers(an), json_data={'last_id': ''})
    if sun_data and sun_data.get('code') == 0:
        for item in sun_data.get('data', {}).get('list', []):
            tjid(an, item.get('id'))

def tjid(an, id_value):
    data = {'id': id_value}
    result = post_request('https://rf24-serv.cwlo.com.cn/api/user/sun/status', create_headers(an), data=data)
    if result and result.get('code') == 0:
        print(f"{result.get('msg')}, 收获阳光数量: {result.get('data', {}).get('sun')}")

# 捐献花朵和抽奖
def donate_and_lottery(an):
    donation = post_request('https://rf24-serv.cwlo.com.cn/api/welfare/donation', create_headers(an))
    if donation:
        if donation.get('code') == 0:
            print(f"消息: {donation.get('msg')}, 抽奖次数: {donation.get('data', {}).get('lottery_count', '无抽奖次数信息')}")
        elif donation.get('code') == 70101:
            bind_welfare(an)
        elif donation.get('code') == 70100:
            print(f"消息: {donation.get('msg')}")

def bind_welfare(an):
    data = urlencode({"province": "广东省"})
    result = post_request('https://rf24-serv.cwlo.com.cn/api/welfare/bind', create_headers(an), data=data)
    if result and result.get('code') == 0:
        print(f"福利绑定成功: {result.get('msg')}")

def lottery_draw(an):
    result = post_request('https://rf24-serv.cwlo.com.cn/api/lottery/start', create_headers(an))
    if result:
        if result.get('code') == 0:
            print(f"抽奖成功：{result.get('msg')}\n抽奖编号: {result.get('data', {}).get('lottery_sn')}\n剩余抽奖次数: {result.get('data', {}).get('lottery_count')}")
            time.sleep(random.uniform(2.1, 3.8))
            lottery_draw(an)
        elif result.get('code') == 80002:
            print(f"抽奖失败：{result.get('msg')}")

# 查询用户信息
def process_user_info(an):
    result = post_request('https://rf24-serv.cwlo.com.cn/api/user/info', create_headers(an))
    if result and result.get('code') == 0:
        user_data = result.get('data', {}).get('user', {})
        print(f"今日首次登录: {user_data.get('today_first_login')}, 用户ID: {user_data.get('user_id')}, 福利ID: {user_data.get('welfare_id')},\n捐献花朵: {user_data.get('donate_flower')}, 总花朵数量: {user_data.get('total_flower')}, 阳光数量: {user_data.get('sun')},\n花朵数量: {user_data.get('flower')},  抽奖次数: {user_data.get('lottery_count')}, ")
        if user_data.get('flower') > 0:
            donate_and_lottery(an)
        if user_data.get('lottery_count') > 0:
            lottery_draw(an)

jbxmmz = "双色球·送你一朵小红花 "
jbxmbb = "1.2"
gxsj = "2024年8月11日00:51:28"

# 主函数
def main():
    print(f'-----------{jbxmmz} {jbxmbb}版 {gxsj}-----------')
    print(f'------脚本作者: QGh3amllamll  ')
    tokens = get_variable('env') if blsytxt == 1 else get_variable('file')
    if not tokens:
        print(f'未获取 Authorization#备注  到账号数据，请检查。')
        return

    for token in tokens:
        parts = token.strip().split('#')
        if len(parts) < 1:
            print("令牌格式不正确。跳过处理。")
            continue
        an = parts[0]
        account_no = parts[1] if len(parts) > 1 else ""
        print(f'------{account_no} -------')

        process_sun(an)
        process_user_info(an)

if __name__ == "__main__":
    main()

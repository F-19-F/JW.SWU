import requests
import re
import time
import getpass


def Login(username, password):
    session = requests.session()
    Normal_headers = {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/90.0.4430.212Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    res = session.get(url='http://jw.swu.edu.cn/sso/zllogin', headers=Normal_headers,timeout=2)
    #Find login params
    lt = re.findall(
        '<input type="hidden" name="lt" value="(.*?)"/>', res.text)[0]
    Params = {
        'username': username,
        'password': password,
        'lt': lt,
        'execution': 'e1s1',
        '_eventId': 'submit',
        'isQrSubmit': 'false',
        'qrValue': ''
    }
    Post_Headers = {
        "Connection":"keep-alive",
        "Cache-Control":"max-age=0",
        "sec-ch-ua":"\"Google Chrome\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"",
        "sec-ch-ua-mobile":"?0",
        "sec-ch-ua-platform":"\"Windows\"",
        "Upgrade-Insecure-Requests":"1",
        "Origin":"https://uaaap.swu.edu.cn",
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site":"same-origin",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-User":"?1",
        "Sec-Fetch-Dest":"document",
        "Referer":"https://uaaap.swu.edu.cn/cas/login?service=http%3A%2F%2Fjw.swu.edu.cn%2Fsso%2Fzllogin",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9"
    }
    res = session.post(url='https://uaaap.swu.edu.cn/cas/login?service=http%3A%2F%2Fjw.swu.edu.cn%2Fsso%2Fzllogin'.format(session.cookies.get('36501JSESSIONID')),
                       data=Params,
                       headers=Post_Headers,
                       allow_redirects=False,
                       timeout=2
                       )
    if 'Location' in res.headers:
        url = res.headers['Location']
        pass
    else:
        return (None,None)
    nextheaders={
        "Host":"jw.swu.edu.cn",
        "Connection":"keep-alive",
        "Cache-Control":"max-age=0",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9"
    }
    #forwarding to jw.swu.edu.cn
    res = session.get(url=url,headers=nextheaders)
    num=re.findall('uid=(.*?)&',res.history[2].url)[0]#get snum
    return session,num


def GetInfo(session, username):
    info_headers = {
        "Host": "jw.swu.edu.cn",
        "Connection": "keep-alive",
        "Accept": "text/html, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    res = session.get(url='http://jw.swu.edu.cn/jwglxt/xtgl/index_cxYhxxIndex.html?xt=jw&localeKey=zh_CN&_={}&gnmkdm=index&su={}'.format(
        str(int(time.time()*1000)), username), headers=info_headers)
    class_info = re.findall('<p>(.*?)</p>', res.text)[0]
    name = re.findall('<h4 class="media-heading">(.*?)</h4>', res.text)[0]
    return class_info,name


if __name__ == '__main__':
    print("一站式网上办事大厅-->教务系统")
    username = input("学号:")
    password = getpass.getpass("密码:")
    session,num = Login(username, password)
    if session:
        print(GetInfo(session, username))

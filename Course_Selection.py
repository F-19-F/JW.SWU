#######################################
#######################################
#######################################
HOST = 'jw.swu.edu.cn'
USERNAME = '学号'
PASSWORD = '密码'
#要选的课程列表
TARGETS = ["课程一","课程二"]
#######################################
#######################################
#######################################
#######################################


from Login import Login
import re
import time
headers = {
    "Host": HOST,
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/90.0.4430.212Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}


class CS:
    #session 登录教务系统的会话
    def __init__(self, session,num):
        self.num=num
        Init_headers = headers
        Init_headers['X-Requested-With'] = 'XMLHttpRequest'
        Init_headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        #发送进入选课界面的请求
        session.post(url='http://{}/jwglxt/xtgl/index_cxBczjsygnmk.html?gnmkdm=index&su={}'.format(
            HOST, self.num), headers=Init_headers, data={'gndm': 'N253512'})
        res = session.get(
            url='http://{}/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su={}'.format(HOST, self.num), headers=headers)
        #判断是否在选课时段
        status = re.findall(
            '<div class="nodata"><span>(.*?)</span></div>', res.text)
        if len(status) > 0:
            #print(status[0])
            self.status = -1
            return
        #分析参数
        params = dict(re.findall(
            '<input type="hidden" name="(.*?)" id=".*?" value="(.*?)"/>', res.text))
        first_postdata = {
            'xkkz_id': params['firstXkkzId'],
            'xszxzt': params['xszxzt'],
            'kspage': '0',
            'jspage': '0'
        }
        res = session.post(url='http://{}/jwglxt/xsxk/zzxkyzb_cxZzxkYzbDisplay.html?gnmkdm=N253512&su={}'.format(
            HOST, self.num), headers=Init_headers, data=first_postdata)
        #寻找后续需要的参数
        params1 = dict(re.findall(
            '<input type="hidden" name="(.*?)" id=".*?" value="(.*?)"/>', res.text))
        #合并参数
        params.update(params1)
        self.params = params
        self.session = session
        self.status=0
    #todo conditon 条件筛选
    def GetCourses(self, condition=None):
        post_headers = headers
        post_headers['X-Requested-With'] = 'XMLHttpRequest'
        post_headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        post_headers['Origin'] = HOST
        post_headers['Referer'] = 'http://{}/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su={}'.format(
            HOST, self.num)
        post_params = {}
        #基本参数
        post_params.update({
            'rwlx': self.params['rwlx'],
            'xkly': self.params['xkly'],
            'bklx_id': self.params['bklx_id'],
            'xqh_id': self.params['xqh_id'],
            'jg_id': self.params['jg_id_1'],
            'zyh_id': self.params['zyh_id'],
            'zyfx_id': self.params['zyfx_id'],
            'njdm_id': self.params['njdm_id'],
            'bh_id': self.params['bh_id'],
            'xbm': self.params['xbm'],
            'xslbdm': self.params['xslbdm'],
            'ccdm': self.params['ccdm'],
            'xsbj': self.params['xsbj'],
            'sfkknj': self.params['sfkknj'],
            'sfkkzy': self.params['sfkkzy'],
            'kzybkxy': self.params['kzybkxy'],
            'sfznkx': self.params['sfznkx'],
            'zdkxms': self.params['zdkxms'],
            'sfkxq': self.params['sfkxq'],
            'sfkcfx': self.params['sfkcfx'],
            'kkbk': self.params['kkbk'],
            'kkbkdj': self.params['kkbkdj'],
            'sfkgbcx': self.params['sfkgbcx'],
            'sfrxtgkcxd': self.params['sfrxtgkcxd'],
            'tykczgxdcs': self.params['tykczgxdcs'],
            'xkxnm': self.params['xkxnm'],
            'xkxqm': self.params['xkxqm'],
            'kklxdm': self.params['firstKklxdm'],
            'rlkz': self.params['rlkz'],
            'xkzgbj': self.params['xkzgbj'],
            'kspage': 1,  # 默认值，后面会自主更新
            'jspage': 10,  # 默认值，后面会自主更新
            'jxbzb': self.params['jxbzb']
        })
        url = 'http://{}/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su={}'.format(
            HOST, self.num)
        res = self.session.post(
            url=url, headers=post_headers, data=post_params)
        jsonret=res.json()['tmpList']
        sum=[]
        sum+=jsonret
        #判断是否存在更多课程
        if len(jsonret) == 0:
            return []
        while int(jsonret[-1]['kcrow'])-int(jsonret[0]['kcrow'])+1 >= 10:
            post_params['kspage']=post_params['kspage']+10
            post_params['jspage']=post_params['jspage']+10
            res = self.session.post(url=url, headers=post_headers, data=post_params)
            jsonret=res.json()['tmpList']
            sum+=jsonret
        return sum
    #course_info 要选的课程信息，是GetCourses返回列表的子集
    def SelectCourse(self, course_info):
        post_headers = headers
        post_headers['X-Requested-With'] = 'XMLHttpRequest'
        post_headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        post_headers['Origin'] = HOST
        post_headers['Referer'] = 'http://{}/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su={}'.format(
            HOST, self.num)
        post_params = {
            'rwlx': self.params['rwlx'],
            'xkly': self.params['xkly'],
            'bklx_id': self.params['bklx_id'],
            'xqh_id': self.params['xqh_id'],
            'jg_id': self.params['jg_id_1'],
            'zyh_id': self.params['zyh_id'],
            'zyfx_id': self.params['zyfx_id'],
            'njdm_id': self.params['njdm_id'],
            'bh_id': self.params['bh_id'],
            'xbm': self.params['xbm'],
            'xslbdm': self.params['xslbdm'],
            'ccdm': self.params['ccdm'],
            'xsbj': self.params['xsbj'],
            'sfkknj': self.params['sfkknj'],
            'sfkkzy': self.params['sfkkzy'],
            'kzybkxy': self.params['kzybkxy'],
            'sfznkx': self.params['sfznkx'],
            'zdkxms': self.params['zdkxms'],
            'sfkxq': self.params['sfkxq'],
            'sfkcfx': self.params['sfkcfx'],
            'kkbk': self.params['kkbk'],
            'kkbkdj': self.params['kkbkdj'],
            'xkxnm': self.params['xkxnm'],
            'xkxqm': self.params['xkxqm'],
            'kklxdm': self.params['firstKklxdm'],
            'rlkz': self.params['rlkz'],
            'xkkz_id': self.params['firstXkkzId']
        }
        print("选择课程:{}".format(course_info['kcmc']))
        post_params['kch_id'] = course_info['kch_id']
        post_params['cxbj'] = course_info['cxbj']
        post_params['fxbj'] = course_info['fxbj']
        res = self.session.post(url='http://{}/jwglxt/xsxk/zzxkyzbjk_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su={}'.format(
            HOST, self.num), data=post_params, headers=post_headers)
        target = res.json()[0]
        do_jxb_id=target['do_jxb_id']#do_jxb_id,这个参数比较特殊
        #有子课程的课程
        if course_info['jxbzls'] == '2':#jxb_ids=target['do_jxb_id']+'%2C'+实践课jxb_id
            html_api='http://jw.swu.edu.cn/jwglxt/xsxk/zzxkyzb_xkZyZzxkYzbZjxb.html?jxb_id={jxb_id}&do_jxb_id={do_jxb_id}&jxbzls={jxbzls}&rlkz={rlkz}&fxbj={fxbj}&cxbj={cxbj}&rlzlkz={rlzlkz}&rwlx={rwlx}&syqz={syqz}&time={time}&gnmkdm=N253512&su={num}'.format(
                jxb_id=course_info['jxb_id'],
                do_jxb_id=target['do_jxb_id'],
                jxbzls='2',
                rlkz=self.params['rlkz'],
                fxbj=course_info['fxbj'],
                cxbj=course_info['cxbj'],
                rlzlkz=self.params['rlzlkz'],
                rwlx=self.params['rwlx'],
                syqz='100',
                time=str(int(time.time()*1000)),
                num=self.num
            )
            h_headers = headers
            h_headers['X-Requested-With'] = 'XMLHttpRequest'
            h_headers['Origin'] = HOST
            h_headers['Accept'] = 'text/html, */*; q=0.01'
            h_headers['Referer'] = 'http://{}/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su={}'.format(
                HOST, self.num)
            self.session.post(url=html_api,headers=h_headers)
            post_params={
                'xkxnm':self.params['xkxnm'],
                'xkxqm':self.params['xkxqm'],
                'xkly':self.params['xkly'],
                'jxb_id':target['do_jxb_id'],
                'jxbzls':course_info['jxbzls'],
                'rlkz':self.params['rlkz'],
                'rlzlkz':self.params['rlzlkz'],
                'rwlx':self.params['rwlx'],
                'syqz':'100',#默认100
                'zyfx_id':self.params['zyfx_id'],
                'bh_id':self.params['bh_id'],
                'zyh_id':self.params['zyh_id'],
                'njdm_id':self.params['njdm_id'],
                'sfkknj':self.params['sfkknj'],
                'sfkkzy':self.params['sfkkzy'],
                'zh':'',
                'sfznkx':self.params['sfznkx'],
                'kklxdm':course_info['kklxdm'],
                'xh_id':self.num,
                'bklx_id':self.params['bklx_id'],
                'kkbk':self.params['kkbk'],
                'kkbkdj':self.params['kkbkdj'],
                'fxbj':course_info['fxbj'],
                'cxbj':course_info['cxbj']
            }
            res=self.session.post(url='http://{}/jwglxt/xsxk/zzxkyzb_xkZyDisplayZzxkYzbZjxb.html?gnmkdm=N253512&su={}'.format(HOST,self.num),data=post_params,headers=post_headers)
            res=res.json()
            if len(res)>1:
                t=res[1]
            do_jxb_id+='%2C'
            do_jxb_id+=t['do_jxb_id']
        #准备参数，进行最终选课请求的发送
        post_params = {
            'jxb_ids': do_jxb_id,
            'kch_id': course_info['kch_id'],#课程相关参数
            'kcmc': "({}){}+-+{}+学分".format(course_info['kch'], course_info['kcmc'], course_info['xf']),#不变
            'rwlx': self.params['rwlx'],#全局参数
            'rlkz': self.params['rlkz'],#全局参数
            'rlzlkz': self.params['rlzlkz'],#全局参数
            'sxbj': '1',  # 固定值
            'xxkbj': course_info['xxkbj'],
            'qz': '0',  # 固定值
            'cxbj': course_info['cxbj'],
            'xkkz_id': self.params['firstXkkzId'],
            'njdm_id': self.params['njdm_id'],#全局参数
            'zyh_id': self.params['zyh_id'],
            'kklxdm': course_info['kklxdm'],#全局参数
            'xklc': self.params['xklc'],#选课轮次
            'xkxnm': self.params['xkxnm'],#选课学年名
            'xkxqm': self.params['xkxqm'],#选课学期名
        }
        res = self.session.post(url='http://{}/jwglxt/xsxk/zzxkyzbjk_xkBcZyZzxkYzb.html?gnmkdm=N253512&su={}'.format(
            HOST, self.num), data=post_params, headers=post_headers)
        res = res.json()
        if res['flag'] == '1':
            print("选课成功!!!")
            return True
        elif res['flag'] == '-1':
            print("该课程现已满员")
        elif res['flag'] == '0':
            print(res['msg'])
        return False
def CheckName(name:str):
    for i in TARGETS:
        if i in name:
            return True
        else:
            return False

if __name__ == '__main__':
    needloop = True
    s,num = Login(USERNAME, PASSWORD)
    if not s:
        exit(-1)
    XK=CS(s,num)
    if XK.status < 0:
        exit(-1)
    while needloop:
        courses = XK.GetCourses()
        for c in courses:
            if CheckName(c['kcmc']):
                if XK.SelectCourse(c):
                    TARGETS.remove(c['kcmc'])
                    if len(TARGETS) == 0:
                        needloop = False
                        break
        time.sleep(0.8)

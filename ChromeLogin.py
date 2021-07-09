from Login import Login,GetInfo
import getpass
import selenium.webdriver
from webdriver_manager.chrome import ChromeDriverManager
#pip3 install selenium webdriver_manager
if __name__=='__main__':
    print("一站式网上办事大厅-->教务系统")
    username = input("学号:")
    password = getpass.getpass("密码:")
    session=None
    while not session:
        try:
            session,num = Login(username, password)
        except:
            pass
    if session:
        GetInfo(session, username)
        cookies=session.cookies.get_dict()
        scookies=[]
        for i in cookies:
            one={
                'name':i,
                'value':cookies[i],
                'domain':'jw.swu.edu.cn'
            }
            scookies.append(one)
    driver=selenium.webdriver.Chrome(ChromeDriverManager().install())
    driver.get("http://jw.swu.edu.cn")
    driver.delete_all_cookies()
    for i in scookies:
        driver.add_cookie(i)
    driver.refresh()

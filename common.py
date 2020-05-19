import pymysql

import requests
from json import JSONDecodeError

import re
import os

class RunMethod():
    def post_main(self,url,data,header=None):
        res=None
        if header !=None:
            res=requests.post(url=url,data=data,headers=header)
            #res=requests.post(url=url,data=data,header=header)
        else:
            res=requests.post(url=url,data=data)
        #return res.json()  #返回的是一个字典
        return res
    def get_main(self,url,data=None,header=None):
        res=None
        if header!=None:
            res=requests.get(url=url,params=data,headers=header,verify=False)
        else:
            res=requests.get(url=url,params=data,verify=False)
        #return res.json()
        return res
    def run_main(self,method,url,data=None,header=None):
        res=None
        if method=='post':
            res=self.post_main(url,data,header)
        else:
            res=self.get_main(url,data,header)
        #return json.dumps(res,ensure_ascii=False)
        #return json.dumps(res,sort_keys=True,indent=4,ensure_ascii=False)  #json格式化
        return res


#获取cookie的方法
def get_cookie():
    url = "http://m.imooc.com/passport/user/login"
    data = {
        "username": "15192727132",
        "password": "weiwei07093312",
        "verify": "",
        # "remember":"1",
        # "pwencode":"1",
        # "browser_key":"a2e9fce148b4ca819dddfe864425f980",
        "referer": "https://www.imooc.com"
    }
    res = requests.post(url, data).json()
    print(res)
    response_url = res['data']['url'][0]
    request_url = response_url + "&callback=jQuery19102848013151016324_1588836131776&_=1588836131778"
    res2 = requests.get(request_url).cookies
    cookie_dict = requests.utils.dict_from_cookiejar(res2)
    print("cookie_dict:",cookie_dict)
    return cookie_dict

class RunTest():
    def __init__(self,username):
        self.db=OpenationDbInterface()
        #self.data=self.db.select_data()
        self.run_method = RunMethod()
        #self.username=username
        self.data=self.db.select_data2(username)
        #self.db2=OpenationDbInterface1()



    def str_to_dict(self,in_str):
        out_dict=eval(in_str)
        return out_dict

    def go_to_run(self):
        for i in range(len(self.data)):
            print("======i=========",i)
            data=self.data[i]
            # print(data)
            method=data['exe_mode']
            # print("method:",method)
            url=data['url']
            # print("url: ",url)
            url_param=data['params']
            url_param_dict={}
            print("url_param:",url_param)
            if url_param !=None:  #如果请求参数不为空，则要转为字典格式
                print("请求参数不为空")
                url_param_dict=self.str_to_dict(url_param)

            # print("url_param_dict: ",url_param_dict)
            # print("type(url_param_dict)",type(url_param_dict))

            header=data['header']
            if header != None:
                print("========")
                header_dict={}

                header_dict=self.str_to_dict(header)
            else:
                header_dict=""
            # print("header_dict:",header_dict)
            # print("type(header_dict)",type(header_dict))
            cookie=data['cookie']
            print("Cook:",cookie)
            if cookie ==None:
                res=self.run_method.run_main(method,url,url_param_dict,header_dict)
            else:
                #res=self.run_method.run_main(method,url,url_param_dict,header_dict,)
                res=requests.get(url=url,cookies=get_cookie(),verify=False)
                #res=self.run_method.run_main(method,url,url_param_dict,header_dict,get_cookie())

            print("result====="+str(i)+"=====:",res.text)
            key_param_flag, all_param_flag,real_expect_params=self.check_result(data,res)
            print(key_param_flag,all_param_flag)
            id=data['id']
            name_interface=data['name_interface']
            exe_mode=data['exe_mode']
            url_interface=data['url']
            print("url -----i----"+str(i)+url)
            #result_interface=data['result_interface']
            header_interface=data['header']
            params_interface=data['params']
            result_interface=res.text
            expect_params=data['expect_params']
            result_expect_params=data['expect_params_value']
            result_code=key_param_flag
            complete_params=data['complete_params']
            result_complete_params=all_param_flag
            username=data['username']

            self.db.insert_value_result(id_test=id,username=username,interface_name=name_interface,exe_mode=exe_mode,url=url_interface,
                                        header=header,cookie=cookie,params=params_interface,result=res.text,expect_params=expect_params,expect_params_value=result_expect_params,
                                        real_expect_params=real_expect_params,result_code=result_code,complete_params=complete_params,
                                        real_complete_params='xxx',result_complete_params=result_complete_params)
            # insert_value_result(self, id_test, username, interface_name, exe_mode, url, header, cookie, params, result,
            #                     expect_params, expect_params_value, real_expect_params, result_code, complete_params,
            #                     real_complete_params, result_complete_params):
            #在这个地方将结果保存到mysql中


            # write_excel(self.filename,id,name_interface,exe_mode,url_interface,header_interface,params_interface,
            #             result_interface,expect_params,result_expect_params,result_code,
            #             complete_params,result_complete_params)
            # result_head = ['id', 'name_interface', 'exe_mode', 'url_interface', 'header_interface', 'params_interface',
            #                'result_interface', 'expect_params', 'result_expect_params', 'result_code',
            #                'complete_params', 'result_complete_params']
            # res_dict=self.str_to_dict(res.text)
            # print(res_dict)
            # print(type(res_dict))
    def check_result(self,in_result,in_res):
        key_param_flag=True
        all_param_flag=True
        real_expect_params=''
        try:
            res = in_res.json()
        except JSONDecodeError:  #抛出异常，无法转换为json列表格式
            expect_params = in_result['expect_params']
            result_expect_params = in_result['real_expect_params']
            complete_params = in_result['complete_params']
            complete_params_list = re.split(',', complete_params)
            res=in_res.text
            for i in complete_params_list:
                if i not in res:
                    all_param_flag=False
            return key_param_flag, all_param_flag,real_expect_params

        else:
            expect_params=in_result['expect_params']
            # print("expect_params: ",expect_params)
            expect_params_value=in_result['expect_params_value']
            # print("result_expect_params: ",result_expect_params)
            complete_params=in_result['complete_params']
            # print("complete_params: ",complete_params)
            # print("type(complete_params)",type(complete_params))
            complete_params_list=re.split(',',complete_params)
            # print("complete_params_list",complete_params_list)
            # print("type(complete_params_list)",type(complete_params_list))
            #print(res)
            # print("type(res):",type(res))
            # print(res['result'])
            # print("type(res['result']):",type(res['result']))
            temp_dict={}
            temp_list=[]
            tmp=res
            #real_expect_params=''
            for k,v in tmp.items():
                # print("k:",k)
                # print("V:",v)
                if k==expect_params:
                    #print("找到了这个k和v",k,v)
                    if v!=expect_params_value:
                        real_expect_params=v  #实际请求到的该参数的值，需要返回
                        key_param_flag=False
                if (type(v).__name__=='dict'): #判断是否是字典
                    temp_list.append(k)
                    for kk,vv in v.items():
                        temp_dict[kk]=vv
                        temp_list.append(kk)
                else:
                    temp_dict[k]=v
                    temp_list.append(k)
            # print("=================")
            # print(temp_dict)
            # print("list+++++++")
            # print(temp_list)

            #判断complete_params_list 列表的元素是否都在temp_list里面
            # print("complete_params_list:",complete_params_list)
            # print("temp_list: ",temp_list)
            d=[False for c in complete_params_list if c not in temp_list]
            if d:
                print('complete_params_list not in temp_list')
                all_param_flag=False
            else:
                print('complete_params_list in temp_list')
            return key_param_flag,all_param_flag,real_expect_params
    def test_data(self):
        print(self.data)



class OpenationDbInterface(object):
    def __init__(self,host_db='123.57.45.250',user_db='root',pwssword='123456',name_db='test_interface',port_db=3306,link_type=0):
        """
        :param host_db: 数据库主机
        :param user_db: 用户名
        :param pwssword: 密码
        :param name_db: 数据库名称
        :param port_db: 端口号
        :param link_type: 连接类型，用于实在输出是元组还是字典（试了一下是列表）,默认列表
        返回游标
        """
        print("执行初始化")
        try:
            if link_type==0:
                self.conn=pymysql.connect(host=host_db,user=user_db,passwd=pwssword,db=name_db,port=port_db,charset='utf8',cursorclass=pymysql.cursors.DictCursor,autocommit =True)
            else:
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=pwssword, db=name_db, port=port_db,
                                    charset='utf8',autocommit =True)   #返回元组
        except pymysql.Error as e:
            print("创建数据库链接失败|MySql Error %d :%s" %(e.args[0],e.args[1]))
    def select_data(self,sql="select * from interface_test"):
        cursor=self.conn.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        cursor.close()
        self.close_db()
        return result
    def select_data2(self,username):
        cursor = self.conn.cursor()
        sql="select * from interface_test where username = '"+username+"'"
        print("sql: ",sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        self.close_db()
        return result

    def close_db(self):
        if self.conn != None:
            self.conn.close()

        # def ping(self, reconnect=True):
        #     """Check if the server is alive"""
        #     if self._sock is None:
        #         if reconnect:
        #             self.connect()
        #             reconnect = False
        #         else:
        #             raise err.Error("Already closed")
        #     try:
        #         self._execute_command(COMMAND.COM_PING, "")
        #         return self._read_ok_packet()
        #     except Exception:
        #         if reconnect:
        #             self.connect()
        #             return self.ping(False)
        #         else:
        #             raise

    def insert_value(self,username,interface_name,exe_mode,interface_url,header,cookie,params,expect_params,expect_params_value,complete_params):
        print("数据库中拆入值:"+username+interface_name+exe_mode,interface_url+header+cookie+params+expect_params+expect_params_value+complete_params)
        if username==None:
            print("is None")
        else:
            print("不是None")
            print(type(username))
            print(len(username))
        if len(username)==0:
            username='NULL'
        else:
            username='"' + username +'"'
        if len(interface_name)==0:
            interface_name='NULL'
        else:
            interface_name='"' + interface_name +'"'

        if len(exe_mode)==0:
            exe_mode='NULL'
        else:
            exe_mode='"' + exe_mode +'"'

        if len(interface_url)==0:
            interface_url='NULL'
        else:
            interface_url='"' + interface_url +'"'

        if len(header)==0:
            header='NULL'
        else:
            header='"' + header +'"'

        if len(cookie)==0:
            cookie='NULL'
        else:
            cookie='"' + cookie +'"'

        if len(params)==0:
            params='NULL'
        else:
            params = '"' + params + '"'

        if len(expect_params)==0:
            expect_params='NULL'
        else:
            expect_params = '"' + expect_params + '"'

        if len(expect_params_value)==0:
            expect_params_value='NULL'
        else:
            expect_params_value = '"' + expect_params_value + '"'

        if len(complete_params)==0:
            complete_params='NULL'
        else:
            complete_params = '"' + complete_params + '"'

        sql="INSERT INTO interface_test (username,name_interface,exe_mode,url,header,cookie,params,expect_params,expect_params_value,complete_params)" \
            " VALUES ("+username+","+interface_name+","+exe_mode+","+interface_url+","+header+","+cookie+","+params+","+expect_params+","+expect_params_value+","+complete_params+")"
        print("插入的sql:  ",sql)

        cursor = self.conn.cursor()
        cursor.execute(sql)
        #cursor.commit()

        cursor.close()
        self.close_db()

    def insert_value_result(self,id_test,username,interface_name,exe_mode,url,header,cookie,params,result,expect_params,expect_params_value,real_expect_params,result_code,complete_params,real_complete_params,result_complete_params):
        #id_test不需要处理，不可能为空
        # if len(id_test)==0:
        #     id_test='NULL'
        # else:
        #     id_test='"' + id_test +'"'
        id_test=str(id_test)
        if len(username)==0:
            username='NULL'
        else:
            username='"' + username +'"'
        if len(interface_name)==0:
            interface_name='NULL'
        else:
            interface_name='"' + interface_name +'"'

        if len(exe_mode)==0:
            exe_mode='NULL'
        else:
            exe_mode='"' + exe_mode +'"'

        if len(url)==0:
            interface_url='NULL'
        else:
            url='"' + url +'"'

        if header is None or len(header)==0 :
            header='NULL'
        else:
            header='"' + header +'"'

        if cookie is None or len(cookie)==0:
            cookie='NULL'
        else:
            cookie='"' + cookie +'"'
        if params is None or len(params)==0:
            params='NULL'
        else:
            params = '"' + params + '"'

        if result is None or len(result)==0:
            result='NULL'
        else:
            result="'"+result+"'"
            #result = '"' + result + '"'

        if expect_params is None or len(expect_params)==0:
            expect_params='NULL'
        else:
            expect_params = '"' + expect_params + '"'

        if expect_params_value is None or len(expect_params_value)==0:
            expect_params_value='NULL'
        else:
            expect_params_value = '"' + expect_params_value + '"'
        if real_expect_params is None or len(real_expect_params)==0:
            real_expect_params='NULL'
        else:
            real_expect_params = '"' + real_expect_params + '"'
        #result是bool型，不需要处理
        # if result_code is None or len(result_code)==0:
        #     result_code='NULL'
        # else:
        #     result_code = '"' + result_code + '"'
        result_code=str(result_code)


        if complete_params is None or len(complete_params)==0:
            complete_params='NULL'
        else:
            complete_params = '"' + complete_params + '"'
        if real_complete_params is None or len(real_complete_params)==0:
            real_complete_params='NULL'
        else:
            real_complete_params = '"' + real_complete_params + '"'

        #result_complete_params 传入的是bool，不要用处理
        # if result_complete_params is None or len(result_complete_params)==0:
        #     result_complete_params='NULL'
        # else:
        #     result_complete_params = '"' + result_complete_params + '"'
        result_complete_params=str(result_complete_params)

        sql = "INSERT INTO interface_result (id_test,username,name_interface,exe_mode,url,header,cookie,params,result,expect_params,expect_params_value,real_expect_params,result_code,complete_params,real_complete_params,result_complete_params)" \
              " VALUES (" +id_test+","+ username + "," + interface_name + "," + exe_mode + "," + url + "," + header + "," + cookie + "," + params + ","+result+"," + expect_params + "," + expect_params_value + "," +real_expect_params+","+result_code+","+ complete_params+"," +real_complete_params+","+result_complete_params+ ")"

        print("结果写入的sql:  ", sql)

        try:
            cursor=self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()
            cursor = self.conn.cursor()
            cursor.execute(sql)

        # cursor = self.conn.cursor()
        # cursor.execute(sql)
        cursor.close()
        self.close_db()

        #将结果保存到mysql中

class OpenationDbInterface1(object):
    def __init__(self,host_db='123.57.45.250',user_db='root',pwssword='123456',name_db='test_interface',port_db=3306,link_type=0):
        """
        :param host_db: 数据库主机
        :param user_db: 用户名
        :param pwssword: 密码
        :param name_db: 数据库名称
        :param port_db: 端口号
        :param link_type: 连接类型，用于实在输出是元组还是字典（试了一下是列表）,默认列表
        返回游标
        """
        print("执行初始化")
        try:
            if link_type==0:
                self.conn=pymysql.connect(host=host_db,user=user_db,passwd=pwssword,db=name_db,port=port_db,charset='utf8',cursorclass=pymysql.cursors.DictCursor,autocommit =True)
            else:
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=pwssword, db=name_db, port=port_db,
                                    charset='utf8',autocommit =True)   #返回元组
        except pymysql.Error as e:
            print("创建数据库链接失败|MySql Error %d :%s" %(e.args[0],e.args[1]))


    def close_db(self):
        if self.conn != None:
            self.conn.close()


    def insert_value_result(self,id_test,username,interface_name,exe_mode,url,header,cookie,params,result,expect_params,expect_params_value,real_expect_params,result_code,complete_params,real_complete_params,result_complete_params):
        #id_test不需要处理，不可能为空
        # if len(id_test)==0:
        #     id_test='NULL'
        # else:
        #     id_test='"' + id_test +'"'
        id_test=str(id_test)
        if len(username)==0:
            username='NULL'
        else:
            username='"' + username +'"'
        if len(interface_name)==0:
            interface_name='NULL'
        else:
            interface_name='"' + interface_name +'"'

        if len(exe_mode)==0:
            exe_mode='NULL'
        else:
            exe_mode='"' + exe_mode +'"'

        if len(url)==0:
            interface_url='NULL'
        else:
            url='"' + url +'"'

        if header is None or len(header)==0 :
            header='NULL'
        else:
            header='"' + header +'"'

        if cookie is None or len(cookie)==0:
            cookie='NULL'
        else:
            cookie='"' + cookie +'"'
        if params is None or len(params)==0:
            params='NULL'
        else:
            params = '"' + params + '"'

        if result is None or len(result)==0:
            result='NULL'
        else:
            result="'"+result+"'"
            #result = '"' + result + '"'

        if expect_params is None or len(expect_params)==0:
            expect_params='NULL'
        else:
            expect_params = '"' + expect_params + '"'

        if expect_params_value is None or len(expect_params_value)==0:
            expect_params_value='NULL'
        else:
            expect_params_value = '"' + expect_params_value + '"'
        if real_expect_params is None or len(real_expect_params)==0:
            real_expect_params='NULL'
        else:
            real_expect_params = '"' + real_expect_params + '"'
        #result是bool型，不需要处理
        # if result_code is None or len(result_code)==0:
        #     result_code='NULL'
        # else:
        #     result_code = '"' + result_code + '"'
        result_code=str(result_code)


        if complete_params is None or len(complete_params)==0:
            complete_params='NULL'
        else:
            complete_params = '"' + complete_params + '"'
        if real_complete_params is None or len(real_complete_params)==0:
            real_complete_params='NULL'
        else:
            real_complete_params = '"' + real_complete_params + '"'

        #result_complete_params 传入的是bool，不要用处理
        # if result_complete_params is None or len(result_complete_params)==0:
        #     result_complete_params='NULL'
        # else:
        #     result_complete_params = '"' + result_complete_params + '"'
        result_complete_params=str(result_complete_params)

        sql = "INSERT INTO interface_result (id_test,username,name_interface,exe_mode,url,header,cookie,params,result,expect_params,expect_params_value,real_expect_params,result_code,complete_params,real_complete_params,result_complete_params)" \
              " VALUES (" +id_test+","+ username + "," + interface_name + "," + exe_mode + "," + url + "," + header + "," + cookie + "," + params + ","+result+"," + expect_params + "," + expect_params_value + "," +real_expect_params+","+result_code+","+ complete_params+"," +real_complete_params+","+result_complete_params+ ")"

        print("结果写入的sql:  ", sql)

        try:
            cursor=self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()
            cursor = self.conn.cursor()
            cursor.execute(sql)


        # cursor = self.conn.cursor()
        # cursor.execute(sql)
        # cursor.close()
        # self.close_db()

        #将结果保存到mysql中




class Run():
    def __init__(self):
        pass
    def myrun(self,name):
        #这里是执行的主入口，这里要完成用例读取，用例执行，用例写入
        print("获取到的用户名称是：",name)


if __name__=="__main__":
    go_test = RunTest("cmx")
    go_test.go_to_run()
    #
    #db2=OpenationDbInterface1()
    # #db2.insert_value('1','1','1','1','1','1','1','1','1','1')
    #db2.insert_value_result('1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1')



    #res2=db2.select_data()

    # run=Run()
    # run.myrun("xxx")
    # # sql2="select * from interface_test"
    # # res2=db2.select_data(sql2)
    # print(res2)
    # # for i in range(len(res2)):
    # #     print(res2[i])
    # #     print(type(res2[i]))
    # #     print(len(res2[i]))
    # #     print("++++")
"""
数据依赖,依赖case
"""
import json
from jsonpath_rw import parse
from util.operation_excel import OperationExcel
from util.runmethod import RunMethod
from data.get_data import GetData


class DependentData:
    def __init__(self, case_id):
        self.case_id = case_id
        self.oper_excel = OperationExcel()
        self.method = RunMethod()
        self.data = GetData()

    # 通过case_id去获取依赖case_id的整行数据
    def get_case_line_data(self):
        rows_data = self.oper_excel.get_rows_data(self.case_id)
        return rows_data

    # 执行依赖测试，获取结果
    def run_dependent(self):
        row_num = self.oper_excel.get_row_num(self.case_id)
        request_data = self.data.get_data_value(row_num)
        header = self.data.get_request_header(row_num)
        method = self.data.get_request_method(row_num)
        url = self.data.get_request_url(row_num)
        if header == 'write_Cookies':
            # header = {'Content-Type': 'application/json',
            #           "X-Lemonban-Media-Type": "lemonban.v2"}
            # header = OperationHeader.write_cookie()
            data = json.dumps(request_data)
            res = self.method.run_main(method, url, data, header, params=data)
        else:
            res = self.method.run_main(method, url, request_data, header, params=request_data)
        return res

    # 获取依赖字段的响应数据：通过执行依赖测试case来获取响应数据，响应中某个字段数据作为依赖key的value
    def get_value_for_key(self, row):
        newdepend = ''
        # 获取依赖的返回数据key，excel表中
        depend_data = self.data.get_depend_key(row)
        # 执行依赖case返回结果
        response_data = self.run_dependent()
        if ',' in depend_data:
            newdepend_data = depend_data.split(',')  # 切片，用，分割
            if len(newdepend_data) > 1:
                '''
                for index, item in enumerate(newdepend_data):
                    newdepend += str([match.value for match in parse(item).find(response_data)][0])+","
                这么写会在结尾强制加一个","导致报错,所以加一个判断
                '''
                for index, item in enumerate(newdepend_data):  # 遍历
                    if index == len(newdepend_data)-1:  # 如果是最后一次遍历，则不加","
                        newdepend = newdepend + str([match.value for match in parse(item).find(response_data)][0])
                    else:
                        '''
                        获取匹配的数据，返回list
                        [match.value for match in parse(strdata).find(jsondata)]
                        用法：
                        jsondata = {"addCar": {"product": [{"id": "1","price": "38"},{"id": "32", "price": "19"}]}}
                        获取product：
                        strdata = addCar.product
                        获取id：
                        strdata = addCar.product[*].id # 取所有id
                        strdata = addCar.product[0].id # 取第一个id
                        '''
                        newdepend = newdepend + str([match.value for match in parse(item).find(response_data)][0])+","  # 返回是列表所以用[0]
                return newdepend
        else:
            return [match.value for match in parse(depend_data).find(response_data)][0]

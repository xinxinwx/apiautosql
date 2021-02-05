"""
主函数
"""
import pytest
if __name__ == '__main__':
    # 要执行的测试模块
    case_path = 'test_api.py'
    # 函数的参数
    args = [
        '-s',  # 输出打印信息
        '-q',  # 减少测试的运行冗长，简化输出信息，与-v相反
        case_path,  # 执行文件的路径
        # '--reruns 3',  # 重试3次
        # '--reruns-delay=2'  # 延时2秒启动
        '--html=../html/report.html',  # 生成html报告的路径
        # '--self - contained - html'  # 把css样式合并到html里
        # '-–maxfail=1',  # 出现一个失败就终止(这个参数生成的报告不能用,不知为啥)
    ]
    pytest.main(args=args)

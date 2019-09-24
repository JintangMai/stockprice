#!=/usr/bin/python
# -*- coding:GBK -*-
import requests
'''
#
'''
import time
import sys
'''
# sys 
'''
import threading
# threading

from Queue import Queue
# Que
from optparse import OptionParser
# OptionParser

class Worker(threading.Thread):
#

    def __init__(self, work_queue, result_queue):


        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.start()

    def run(self):
    #  run

        while True:
            func, arg, code_index = self.work_queue.get()
            #  func, arg, code_index
            res = func(arg, code_index)
            self.result_queue.put(res)
            if self.result_queue.full():
                res = sorted([self.result_queue.get() for i in range(self.result_queue.qsize())], key=lambda s: s[0], reverse=True)
                # sorted()
                # Queue.get()
                # Queue.qsize()
                res.insert(0, ('0', u'名称\t\t', u'昨收\t', u'今开\t',u'现价\t',u'最高\t',u'最低\t',u'市值\t',u'成本\t',u'涨跌'))
                # list.insert()
                print '***** start *****'
                #print res[0][2]
                n=1
                for obj in res:

                    if n > 1:
                        shizhi =float(obj[4].encode("utf-8"))
                        print obj[1]+'\t'+obj[2]+'\t'+obj[3]+'\t'+obj[4]+'\t'+obj[5]+'\t'+obj[6]+'\t'+str(shizhi * 500)+ '\t' + str(42.88 * 500) + '\t' + str(shizhi*500 -42.88*500)
                    else:
                        print obj[1] + ' ' + obj[3] + ' ' + obj[2] + ' ' + obj[4] + ' ' + obj[5] + ' ' + obj[6] + ' ' + obj[7]+ ' ' + obj[8]+ ' ' + obj[9]
                    n = n+1
                print '***** end *****\n'
                print '*****'
                print time.asctime(time.localtime(time.time()))
                print '*****\n'
            self.work_queue.task_done()
            # ，Queue.task_done()


class Stock(object):
#

    def __init__(self, code, thread_num):
        self.code = code
        self.work_queue = Queue()
        self.threads = []
        self.__init_thread_poll(thread_num)

    def __init_thread_poll(self, thread_num):
        self.params = self.code.split(',')
        # parmas
        # self.params.extend(['s_sh000001', 's_sz399001'])
        #
        # extend()： ，append() ，extend()
        self.result_queue = Queue(maxsize=len(self.params[::-1]))
        for i in range(thread_num):
            self.threads.append(Worker(self.work_queue, self.result_queue))

    def __add_work(self, stock_code, code_index):
        self.work_queue.put((self.value_get, stock_code, code_index))
        # self.value_get

    def del_params(self):
        for obj in self.params:
            self.__add_work(obj, self.params.index(obj))

    def wait_all_complete(self):
        for thread in self.threads:
            if thread.isAlive():
            #
            #  start() ， run()
                thread.join()
                # join()
                #
                #  join()

    @classmethod
    #
    def value_get(cls, code, code_index):
        slice_num, value_num = 21, 3
        name, now = u'——无——', u'  ——无——'
        if code in ['s_sh000001', 's_sz399001']:
            slice_num = 23
            value_num = 1
        r = requests.get("http://hq.sinajs.cn/list=%s" % (code,))
        #
        res = r.text.split(',')
        if len(res) > 1:
            name, now = r.text.split(',')[0][slice_num:], r.text.split(',')[value_num]
            begin = r.text.split(',')[1]
            yesterday = r.text.split(',')[2]
            top = r.text.split(',')[4]
            bottom = r.text.split(',')[5]
        return code_index, name, begin, yesterday, now, top, bottom


if __name__ == '__main__':
#  import
    parser = OptionParser(description="Query the stock's value.", usage="%prog [-c] [-s] [-t]", version="%prog 1.0")
    #
    # %prog
    parser.add_option('-c', '--stock-code', dest='codes',
                      help="the stock's code that you want to query.")
    # 使用 add_option()
    # dest
    parser.add_option('-s', '--sleep-time', dest='sleep_time', default=6, type="int",
                      help='How long does it take to check one more time.')
    parser.add_option('-t', '--thread-num', dest='thread_num', default=1, type='int',
                      help="thread num.")
    options, args = parser.parse_args(args=sys.argv[1:])
    # ， parse_args()
    assert options.codes, "Please enter the stock code!"
    #
    if filter(lambda s: s[:-6] not in ('sh', 'sz', 's_sh', 's_sz'), options.codes.split(',')):
    #
        raise ValueError

    stock = Stock(options.codes, options.thread_num)

    while True:
        stock.del_params()
        time.sleep(options.sleep_time)
        # sleep()
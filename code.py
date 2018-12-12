"""
process_request
当返回不同类型的值的时候，行为也不一样：

返回值
None：  一切正常，继续执行其他的中间件链
Response ：  轻质调用其它Process_request和process_exception函数，也不再继续下载该请求，然后走
调用process_response的流程
Request: 不再继续调用其它process_request函数，交由调度器重新安排下载
IgnoreResquest： process_exception函数会被调用，如果没有此方法，则request.errback会被调用，
如果errback也没有，则此一场会被忽略，甚至连日志也没有。


process_response
在将下载结果返回给engine过程中被调用

返回值：
Response ：  急促调用其他中间件的Process_response
Request: 不再继续调用其它process_request函数，交由调度器重新安排下载
IgnoreResquest： 则request.errback会被调用,如果errback也没有，则此一场会被忽略，甚至连日志也没有。


process_exception
在下载过程中出现异常，或者在process_request中抛出IgnoreResques异常的时候调用
返回值：
Response ：  开始中间件连的process_response处理流程
Request: 不再继续调用其它process_request函数，交由调度器重新安排下载
IgnoreResquest： process_exception函数会被调用，如果没有此方法，则request.errback会被调用，
如果errback也没有，则此一场会被忽略，甚至连日志也没有。


from_crawler(cls,crawler)
如果存在该函数，则调用该函数创建中间件的实例，如果要写这个函数，一定要返回一个中间件的对象

"""

'''
内置中间件
请求rebot.txt文件，并解析其中的规则


'''
'''
getproxies():
获取环境变量的值
'''
import requests
import json
import os

# edd02de6d6402150514802d82505ba4b0b59314e186fc98f736255ab3156c029
# root:test
dingding = 'https://oapi.dingtalk.com/robot/send?access_token={}'
sonarUrl = '{}/api/measures/search?projectKeys={}&metricKeys=alert_status,bugs,reliability_rating,vulnerabilities,security_rating,code_smells,sqale_rating,duplicated_lines_density,coverage,ncloc,ncloc_language_distribution'
successPic = 'http://s1.ax1x.com/2020/10/29/BGMeTe.png'
errorPic = 'http://s1.ax1x.com/2020/10/29/BGMZwD.png'
messageUrl = '{}/dashboard?id={}'
headers = {
    "Content-Type": "application/json"
}
if __name__ == '__main__':
    if os.getenv('accessKey') is None:
        print('dingding accessKey not found')
        exit(1)
    if os.getenv('projectKeys') is None:
        print('projectKeys not found')
        exit(1)
    if os.getenv('sonarUrl') is None:
        print('sonarUrl not found')
        exit(1)
    if os.getenv('successImgUrl') is not None:
        successPic = os.getenv('errorImgUrl')
    if os.getenv('errorImgUrl') is not None:
        errorPic = os.getenv('errorImgUrl')
    dingding = dingding.format(os.getenv('accessKey'))
    sonarUrl = sonarUrl.format(os.getenv('sonarUrl'), os.getenv('projectKeys'))
    messageUrl = messageUrl.format(os.getenv('sonarUrl'), os.getenv('projectKeys'))
    req = requests.get(url=sonarUrl)
    jsons = json.loads(req.text)
    bugCount = 0
    vulnerabilitiesCount = 0
    codeSmellsCount = 0
    coverage = 0
    duplicatedLinesDensityCount = 0
    alertStatus = 0
    if jsons:
        list = jsons['measures']
        for metric in list:
            if metric['metric'] == 'bugs':
                bugCount = metric['value']
            if metric['metric'] == 'vulnerabilities':
                vulnerabilitiesCount = metric['value']
            if metric['metric'] == 'code_smells':
                codeSmellsCount = metric['value']
            if metric['metric'] == 'coverage':
                coverage = metric['value']
            if metric['metric'] == 'duplicated_lines_density':
                duplicatedLinesDensityCount = metric['value']
            if metric['metric'] == 'alert_status':
                alertStatus = metric['value']
    str = os.getenv('projectKeys') + '项目扫描结果:BUG数：{}个，漏洞数：{}个，异味数：{}个，覆盖率：{}%，重复率：{}%'.format(bugCount,
                                                                                              vulnerabilitiesCount,
                                                                                              codeSmellsCount,
                                                                                              coverage,
                                                                                              duplicatedLinesDensityCount)
    pic = successPic
    if alertStatus == 'ERROR':
        pic = errorPic

    msg = {
        'link': {
            "title": "Sonar质量检测报告",
            "text": str,
            "picUrl": pic,
            "messageUrl": messageUrl
        },
        "msgtype": 'link',
    }
    req = requests.post(url=dingding, data=json.dumps(msg), headers=headers)
    res = json.loads(req.text)
    if res:
        if res['errcode'] == 0:
            print('发送成功!请前往钉钉查看。')
        else:
            print('发送失败! 原因:' + req.text)

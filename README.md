# sonar-ding

Sonar-drone钉钉推送插件

在sonar执行完成后执行该插件即可

```yaml
#docker hub
docker pull yujian1996/sonar-ding:1
```



|   key   |   value   |
| ---- | ---- |
|  accessKey    |  钉钉机器人的accesskey    |
|   projectKeys   |   sonar项目的key  |
|   sonarUrl   |   sonar ip:port   |

指定环境变量即可
```shell
docker run -d --name py -e accessKey={key} -e projectKeys={projectkey} -e sonarUrl={sonarurl}   sonar-ding
```
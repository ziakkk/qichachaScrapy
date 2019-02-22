# qichachaScrapy

#### 项目介绍
企查查( https://www.qichacha.com ) 供应商信息采集  

#### 界面预览
![qcc_list](https://github.com/TonyK-T/github_images/blob/master/tycAndQcc/qcc_list.png)
![qcc_info_title](https://github.com/TonyK-T/github_images/blob/master/tycAndQcc/qcc_info_title.png)
![qcc_info_detail](https://github.com/TonyK-T/github_images/blob/master/tycAndQcc/qcc_info_detail.png)

#### 执行过程
![qcc_run](https://github.com/TonyK-T/github_images/blob/master/tycAndQcc/qcc_run.png)
![qcc_run2](https://github.com/TonyK-T/github_images/blob/master/tycAndQcc/qcc_run2.png)

#### 执行结果
![qcc_data](https://github.com/TonyK-T/github_images/blob/master/tycAndQcc/qcc_data.png)

#### 软件架构
软件架构说明  
1、Scrapy + Scrapy-redis 分布式爬取  
2、bloomfilter 过滤、redis sadd去重  
3、Selenium渲染js 和 滑块认证  
4、数据入mysql(sqlalchemy) ，数据入mongodb(motor异步)  
5、User-Agent代理，IP代理，cookies登录态  
6、scrapyd-client打包  
7、gerapy 爬虫管理平台  

#### 安装教程
安装Python库[Scrapy,scrapy-redis-bloomfilter,scrapyd ,scrapyd-client,Redis,sqlalchemy,motor]等等  
安装redis  
安装chrome  
安装mysql，mongodb  
搭建gerapy环境 - 略  

#### 懒人专享 一键docker
1、安装docker-略  
2、下载docker镜像：https://pan.baidu.com/s/1JU9xqbsDkYh-3ehhiuK1Jg  
3、加载镜像(耗时)：docker load -i  centos7:python3.tar    
4、创建并运行容器：docker  run -itd -p 8002:8001 -p 6802:6800  --privileged=true  centos7:python3  /usr/sbin/init  
5、访问gerapy管理部署爬虫： http://IP:8002/    

如果访问 http://IP:8002/ 报500，解决方式如下：  
  1.查看容器的CID：docker ps -a  
  2.进入容器命令行： docker exec -it  容器CID /bin/bash  
  3.容器命令行里重启gerapy服务：  
      ps -ef|grep gerapy   
      kill -9 gerapy进程ID  
      /gerapy/gerapy_start.sh    # 重启gerapy脚本    
 ![docker_python3](https://github.com/TonyK-T/github_images/blob/master/docker/docker_Python3.png)
 
#### 使用说明
1、纯脚本运行：Python run.py  
2、gerapy 爬虫管理平台： 部署、启动停止删除爬虫 -略  

#### gerapy管理平台
![qcc_gerapy_1](https://github.com/TonyK-T/github_images/blob/master/tycAndQcc/qcc_gerapy_1.png)
![qcc_gerapy_2](https://github.com/TonyK-T/github_images/blob/master/tycAndQcc/qcc_gerapy_2.png)
![qcc_gerapy_3](https://github.com/TonyK-T/github_images/blob/master/tycAndQcc/qcc_gerapy_3.png)

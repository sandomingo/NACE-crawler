# NACE-crawler


### 页面分析
BaseURL：http://www.nace.net/AF_MemberDirectory.asp

请求通过一个Http Post请求发送，提交表单内容到BaseURL，例如：
`
curl -d "keyword=&DList=54&Action=&Page=1&Page2=1&Submit1=Search" www.nace.net/AF_MemberDirectory.asp
`

Directory Categories: Audio/Visual
点击后搜索结果第一页

* 第一页：intpage=1, action=f
	* http://www.nace.net/af_memberdirectory.asp?keyword=&intpage=1&page=1&action=f&dlist=54
* 第二页：intpage=1, action=n
	* http://www.nace.net/af_memberdirectory.asp?keyword=&intpage=1&page=1&action=n&dlist=54
* 第三页：
	* http://www.nace.net/af_memberdirectory.asp?keyword=&intpage=2&page=1&action=n&dlist=54
* 第N页：intpage＝N－1，这里N是一个不知道的选项，可以先抓去页面内容，知道内容与前一个页面一致时，停止即可。
* 不同的Categories对应的是dlist不同的值

每个用户信息内容
* Company：font size＝“3”， <b> Tag
* Name：font size＝“2”， <b> Tag
* Position：<i> Tag
* Other Info
	* Address：
	* Phone/Fax/Email/Website：...
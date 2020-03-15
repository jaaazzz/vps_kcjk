

对于一些卖的比较火热的vps套餐，经常会出现缺货的情况，如搬瓦工的cn2基础款，virmach的大盘鸡，便宜鸡等。于是就写了一套vps主机存货监控程序，可以第一时间了解主机商vps补货情况，并发邮件通知你。自己用着还不错，现开源出来，大家有需要的可以试试。

<h1>vps补货监控工具简介</h1>
1目前支持搬瓦工、virmach、hostdare、hostodo、hostsolutions、kimsufi、ramnode、rfchost、soyoustart这几家主机商的vps存货监控。<br>
2支持监控vps产品缺货、补货、上架新品、下架产品<br>
3工具是基于python2.7开发、需要mysql数据库<br>
4需要配置自动发邮件的发件箱smtp<br>
5工具难免有缺点，代码可能不成熟，望轻喷<br>
<h1>vps补货监控通知效果图</h1>
 
<img src="https://www.vpsjxw.com/wp-content/uploads/2020/03/2020031508534964.png" />

<h1>工具安装步骤</h1>

1可运行在linux、windows上，推荐linux。<br>
2安装crontab、python2.7、mysql5.5+<br>
3将工具解压<br>
配置email_sender_class.py中的stmp，参考stmp配置+python脚本实现自动邮件通知<br>
数据库配置在db_conf.py中<br>
4crontab中写入<br>
*/10 * * * * python /root/vuf/start_bwh.py<br>
*/10 * * * * python /root/vuf/start_hostdare.py<br>
*/10 * * * * python /root/vuf/start_virmach.py<br>
*/10 * * * * python /root/vuf/start_vpsjxw.py<br>
表示每10秒钟执行一次监控工具<br>
<h1>欢迎进群讨论讨论，Q群283468775</h1>

from rest_framework.decorators import APIView
from rest_framework.response import Response

import time

class CollectedInfoSummaryData(APIView):
    def get(self, request, *args, **kwargs):
        response_data = {
            'code': 0,
            'data': {
                "totalInfo": 44586,
                "dailyNewInfo": 1674,
                "tags": ["数据泄露", "极端天气", "互联网政策", "网络攻击", "信息安全"]
            },
            'message': "成功"
        }
        return Response(response_data)

class DailyHighWeightInfo(APIView):
    def get(self, request, *args, **kwargs):
        response_data = {
            'code': 0,
            'data': {
                "list": [
                    {
                        'content': """小米应用包管理组件禁止部分软件安装

    经过频道抓包流量分析，确定了应用扫描拦截由 MIUI应用包安装管理器 组件提供，通过实现DNS上游屏蔽可以暂时无效化该功能［当前只针对于小米品牌手机］此操作无需你对手机系统文件进行任何更改

    屏蔽列表:

    api.installer.xiaomi.com［应用包扫描API］

    注: 该解决方案我们早已在 2 月份放出，本次组件更新也只是取消掉了继续安装按钮，但该选项在早些版本中也需要登录小米账号并经过三次授权才可用

    同时为了方便网友屏蔽小米云扫描，本频道整理了一下相关的域名，任意DNS或者广告屏蔽软件都可以直接订阅这个host

    https://raw.githubusercontent.com/LoopDns/Fuck-you-MIUI/main/MIhosts

    自行选择

    https://raw.githubusercontent.com/LoopDns/Fuck-you-MIUI/main/Fhosts""",
                        'tags': ["科技", "手机", "应用管理", "小米", "安全", "网络隐私", "软件屏蔽", "MIUI", "域名屏蔽", "DNS"],
                        'source': ["来源: Telegram", "二级来源: LoopDNS咨询播报"],
                        'meta': ["由AI进行总结生成", "原内容已无法追溯"]
                    },
                    {
                        'content': """OpenAI 在中国申请注册“GPT-5”商标，此前已在美国申请

    据国家知识产权局商标局官网显示，欧爱运营有限责任公司（OPENAI OPCO, LLC）已于上月下旬申请注册了两枚“GPT-5”商标，国际分类分别为 9 类和 42 类（科学仪器、设计研究），商标状态均为申请中。

    此前，据美国专利商标局（USPTO）信息显示，OpenAI 已经在上月 18 日申请注册“GPT-5”的商标。从商标信息来看，GPT-5 将提供文本生成、自然语言理解、语音转录、翻译、分析等功能。

    来源

    投稿：@ZaiHuaBot
    频道：@TestFlightCN""",
                        'tags': ["OpenAI","中国","商标注册","GPT-5","知识产权","美国","申请","科技公司","文本生成","自然语言理解","语音转录","翻译","分析","科学仪器","设计研究"],
                        'source': ["来源: Telegram", "二级来源: LoopDNS咨询播报"],
                        'meta': ["原内容已无法追溯"]
                    },
                    {
                    'content': """近期黑客针对宝塔面板管理员进行的钓鱼行动

在上次的宝塔漏洞风波过后，近期宝塔面版论坛再次出现用户反馈网站被挂马、劫持问题。[ 1 ] [ 2 ]

据网站esw.ink的一篇博文分析，被绑马的网站会被引入一份伪装成普通Bootstrap库、文件名为bootstrap_v10.js的恶意脚本。这场攻击专门针对中国用户。

同时，在宝塔论坛的众多反馈中，笔者还发现了这样一篇帖子（存档 ），帖子中求助者声称自己遇到“浏览器安全组件缺失,错误码 0x164B56A3”错误，所提供图片为宝塔面版运行时错误弹窗。

不难看出，这是明显的钓鱼行为。攻击者在入侵服务器后对用户展开钓鱼，诱导其运行木马软件。且这样的钓鱼是为宝塔面版精心设计的，详情弹窗疑点与钓鱼证据点击这里。

笔者建议宝塔面版用户近期应注意安全防范：通过将面版监听端口切换到高位随机端口、部署防火墙规则仅允许特定IP地址访问或使用Cloudflare ZeroTrust等服务保护面版入口端点，在无需使用面版时可尽量关闭面版以减少攻击面。

—— TG匿名网友""",
                    'tags': ["黑客攻击","钓鱼行动","宝塔面板","恶意脚本","网站安全","信息安全","服务器入侵","安全防护","网络攻击"],
                    'source': ["来源: Telegram", "二级来源: LoopDNS咨询播报"],
                    'meta': ["原内容已无法追溯"]
                },
                ],
            },
            'message': "成功"
        }
        return Response(response_data)

# MemAI-Flow

拓展mem.ai的内容，使它在中文生态更好用。

# 介绍

## 什么是Mem.ai

https://mem.ai
是OpenAI旗下基金投资的一个项目。使用Mem，你曾经拥有的每一个想法、创意和信息都可以轻松获取，有序且易于访问。使你拥有无限记忆！它使用OpenAI的模型来智能搜索或者提问，你在和模型对话时，除了模型知识，它还会优先从你记录的笔记中来回答问题。

它还有非常强大的创作能力，AI内容编辑等，建议去官网了解。

## 为什么需要MemAI-Flow

Mem在海外的生态非常完善，可以轻松保存笔记、链接、Twitter(X)上的内容，还提供了Zapier连接方式，同时也有API。

但是在国内，它不太容易轻松的收藏内容，尤其是我们习惯的微信、微博、知乎等。MemAI-Flow的目的就是让MemAI在国内生态更好用，让我们可以轻松的把国内信息源看到的内容，轻松同步到Mem，让它成为我们的超级记忆！我们不会重复造轮子，只做连接器。

# 功能

## 利用Cubox打通国内生态

https://cubox.pro 是国内公司开发的一款很好用的一站式信息收集、阅读、管理工具，网页, iOS, iPadOS, macOS, Android, Windows,
微信全端支持。利用它可以非常容易的把微信读到的文章，看到的微博等内容，轻松剪藏。

可它也有不足，AI能力一定是没有OpenAI投资的Mem强，所以我们只需要利用它的全端剪藏能力，然后把内容同步送进Mem。这既是MemAI-Flow当前的主要功能。

# 如何使用

你需要持续的运行MemAI-Flow，它才会及时自动把你剪藏的内容同步到Mem。建议部署在云服务器、NAS、树莓派等设备上，这样你可以随时随地剪藏，不用担心MemAI-Flow没有运行。
## 环境变量解释
| 环境变量 | 说明                                                                  |
| --- |---------------------------------------------------------------------|
| MEM_API_KEY | Mem的API Key，可以在[Manage my API Keys](https://mem.ai/sources/api) 中设置 |
| CUBOX_AUTH_CODE | Cubox的接口授权码，需要登录Web页面，抓包任何接口请求，从Headers中查看Authorization的值           |
| CUBOX_SYNC_INTERVAL | Cubox同步间隔，单位秒，默认300秒，即5分钟，建议不要太快爬取，避免给Cubox制造太多访问压力                 |

## 通过命令行运行
```bash
docker run -d --restart always --name memaiflow -p 8000:8000 -e MEM_API_KEY='' -e CUBOX_AUTH_CODE='' -e CUBOX_SYNC_INTERVAL=300 yipengfei/memai-flow:latest
```
## 通过docker-compose运行
```yaml
version: "3"

services:
  memaiflow:
    restart: always
    image: yipengfei/memai-flow:latest
    container_name: memaiflow
    ports:
      - 8000:8000
    environment:
      MEM_API_KEY: ''
      CUBOX_AUTH_CODE: ''
      CUBOX_SYNC_INTERVAL: 300
```

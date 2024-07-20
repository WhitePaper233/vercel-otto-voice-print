# Vercel OTTO 活字印刷 API

这是一个可以使用 [Vercel](https://vercel.com) 部署的 Otto 语音活字印刷项目

## 自行部署（推荐）
可注册一个 [Vercel](https://vercel.com) 账户 部署到自己的账户上（免费！）

### 一键部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/WhitePaper233/vercel-otto-voice-print)

## 使用主仓库部署的 API（不推荐 不保证稳定性）

### 请求 URL

`https://vercel-otto-voice-print.vercel.app/api`

### 请求参数

| 参数名    | 类型    | 是否必须 | 默认值 | 描述                   |
|---------|-------|------|-----|----------------------|
| content | string | 是   | -   | 需要转换为语音的文本内容。 |
| raw_mode | bool  | 否   | true | 是否使用原始句子模式。     |
| pitch   | float | 否   | 1.0 | 语音的音高。              |
| speed   | float | 否   | 1.0 | 语音的速度。              |
| norm    | bool  | 否   | true | 是否对音频进行标准化。     |

### 响应内容

成功请求后，服务器将返回生成的语音文件。

### 示例请求URL
`https://vercel-otto-voice-print.vercel.app/api?content="大家好啊 我是说的道理"`

## 感谢
- [sakaneko117 / HUOZI](https://github.com/sakaneko117/HUOZI) 提供了原素材及音频处理相关代码
- [hua-zhi-wan / otto-hzys](https://github.com/hua-zhi-wan/otto-hzys) 提供素材

## 免责条款

本项目（vercel-otto-voice-print）仅供学习和研究目的使用。项目维护者不对任何直接或间接由使用本项目引起的损失或损害承担责任。用户应自行承担使用本项目的所有风险。

本项目依赖的第三方服务（包括但不限于 Vercel 和 GitHub）可能受到其各自条款和政策的约束。用户在使用本项目时，也应遵守这些服务的条款和政策。

本项目维护者保留随时更改或停止本项目服务的权利，不需提前通知用户。若用户继续使用本项目，则视为接受修改。

本项目中提及的所有第三方品牌和产品名称均为其各自所有者的财产。本项目不隶属于这些公司，也未得到这些公司的赞助或认可。

最后，用户不应将本项目用于任何违法或不道德的活动。若用户的行为导致法律诉讼或其他争议，用户应自行承担所有责任。

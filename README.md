# zoe-wang.com

Ziyi “Zoe” Wang 的个人主页。纯静态网站（HTML + CSS + 原生 JS），托管在 GitHub Pages，绑定自定义域名 `www.zoe-wang.com`。

## 目录结构

```
index.html        首页（About / News / Publications / Background）
design.html       设计作品页
404.html          404 页面
css/style.css     全部样式（含浅色 / 深色主题变量）
js/main.js        交互：深色模式切换、手机菜单、新闻展开、论文筛选、图片灯箱
assets/img/       头像、论文配图（pubs/）、设计作品图（design/）、图标
_src/data.py      ★ 网站内容数据：个人信息、新闻、论文、设计栏目、教育与经历
_src/build.py     根据 data.py 生成三个 HTML 文件
CNAME             自定义域名（GitHub Pages 需要）
```

## 怎么更新内容（推荐方式）

1. 用任意编辑器打开 `_src/data.py`，修改 `NEWS`（新闻）、`PUBS`（论文）、`EDUCATION` / `EXPERIENCE`（背景）等列表。
   - 新增一篇论文：复制 `PUBS` 里的一段 `{...}`，改标题、作者、venue、链接、摘要；把配图放进 `assets/img/pubs/`，在 `"image"` 里写文件名。
   - 作者名后加 `*` 表示共同一作，加 `†` 表示通讯作者；`"tags"` 里加 `"first"`（一作）/ `"selected"`（精选）控制筛选标签。
   - 新增新闻：在 `NEWS` 最上面加一行 `("Sep 2026", '文字，可含 <a href="...">链接</a>')`。
2. 在项目根目录运行：

   ```bash
   python3 _src/build.py .
   ```

3. 提交并推送，GitHub Pages 会在 1 分钟左右自动更新：

   ```bash
   git add -A && git commit -m "Update news" && git push
   ```

不想跑脚本的话，也可以直接改 `index.html` / `design.html`（下次再用脚本生成时会被覆盖，注意二选一）。

## 设计作品页加图

把图片放进 `assets/img/design/`，按 `nio-11.jpg`、`bmw-08.jpg` 这样的编号命名，然后在 `_src/data.py` 的 `DESIGN_SECTIONS` 里把对应栏目的 `count` 改成新的数量。为了让图片按比例排版，再运行一次：

```bash
python3 _src/update_dims.py     # 需要安装 ImageMagick（brew install imagemagick）
python3 _src/build.py .
```

如果没装 ImageMagick，跳过第一步也能用，新图会按 4:3 比例占位。

## 本地预览

```bash
python3 -m http.server 8000
```

然后浏览器打开 http://localhost:8000 。

## 域名

域名 `zoe-wang.com` 注册在 Squarespace Domains，DNS 指向 GitHub Pages：

- `A` 记录（@）：185.199.108.153 / 185.199.109.153 / 185.199.110.153 / 185.199.111.153
- `CNAME` 记录（www）：`zoewang0213.github.io`

GitHub 仓库 Settings → Pages → Custom domain 填 `www.zoe-wang.com` 并勾选 Enforce HTTPS。

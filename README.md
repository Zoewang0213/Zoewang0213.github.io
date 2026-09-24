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
_src/update_dims.py   重新统计设计图尺寸（写入 _src/image_dims.json，供排版用）
robots.txt / sitemap.xml   搜索引擎用
CNAME             绑定自定义域名后由 GitHub 自动生成（见下方“域名”）
```

页面里的 canonical / Open Graph 链接默认写的是 `https://www.zoe-wang.com`。在域名切换完成之前如果想临时改成 GitHub 地址，可以这样构建：`SITE_URL=https://zoewang0213.github.io python3 _src/build.py .`

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

## 域名（把 zoe-wang.com 指到这个站）

域名 `zoe-wang.com` 注册在 Squarespace Domains（到期 2027-02），和 Squarespace 网站会员是两回事，会员过期域名照样能用。切换分两步：

**第一步：在 Squarespace 改 DNS**（Squarespace 后台 → Domains → zoe-wang.com → DNS Settings）

删除原来指向 Squarespace 的记录（`A` 198.185.159.x / 198.49.23.x，以及 `www` 的 `CNAME ext-sq.squarespace.com`），改成：

| 类型 | 主机 | 值 |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | zoewang0213.github.io |

**第二步：在 GitHub 绑定域名**（仓库 → Settings → Pages → Custom domain）

填 `www.zoe-wang.com`，点 Save；等 DNS check 通过后勾选 **Enforce HTTPS**。GitHub 会自动往仓库提交一个 `CNAME` 文件，之后 `zoewang0213.github.io` 会自动跳到 `www.zoe-wang.com`，`zoe-wang.com` 也会跳到 `www`。

DNS 生效通常几分钟到几小时。在此之前网站可以先用 https://zoewang0213.github.io 访问。

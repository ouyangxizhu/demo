from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 460
img = Image.new("RGB", (W, H), "#0B0F10")
d = ImageDraw.Draw(img)

# 背景网格
for x in range(0, W, 40):
    d.line([(x, 0), (x, H)], fill="#121A1C", width=1)
for y in range(0, H, 40):
    d.line([(0, y), (W, y)], fill="#121A1C", width=1)

# 左侧绿色竖条
d.rectangle([0, 0, 10, H], fill="#3BE38F")

font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
f_tag = ImageFont.truetype(font_path, 26)
f_title = ImageFont.truetype(font_path, 74)
f_sub = ImageFont.truetype(font_path, 32)
f_small = ImageFont.truetype(font_path, 24)

d.text((62, 70), ">_ LANGCHAIN 1.x  ·  MIDDLEWARE", font=f_tag, fill="#3BE38F")
d.text((60, 130), "一文读懂", font=f_title, fill="#F2F7F5")
d.text((60, 218), "LangChain 中间件", font=f_title, fill="#F2F7F5")
d.text((62, 330), "顺序篇｜钩子执行顺序的源码级拆解", font=f_sub, fill="#8FA3A0")
d.text((62, 386), "前置顺序进 · 包裹层层套 · 后置逆序出", font=f_small, fill="#3BE38F")

# 右侧装饰括号
d.text((W-120, 120), "{ }", font=ImageFont.truetype(font_path, 90), fill="#1C2A2A")

img.save(".workbuddy/publish_imgs/cover.jpg", "JPEG", quality=88)
print("ok")

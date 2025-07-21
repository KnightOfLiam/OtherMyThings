import urwid

# 1. 创建五个组件（四角+中心）
top_left = urwid.Text("↖ 左上角", align="left")
top_right = urwid.Text("右上角 ↗", align="right")
center = urwid.Text("★ 主内容 ★", align="center")
bottom_left = urwid.Text("↙ 左下角", align="left")
bottom_right = urwid.Text("右下角 ↘", align="right")

# 2. 顶部行：左右布局
top_row = urwid.Columns([
    # 左组件（固定宽度或自适应）
    ('weight', 1, urwid.Filler(top_left, top='top')),
    # 右组件（固定宽度或自适应）
    ('weight', 1, urwid.Filler(top_right, top='top'))
], dividechars=1)

# 3. 中间行：主内容居中
center_box = urwid.Filler(
    urwid.Padding(center, align='center', width=('relative', 80)),
    valign='middle',
    height=('relative', 60)
)

# 4. 底部行：左右布局
bottom_row = urwid.Columns([
    urwid.Filler(bottom_left, bottom='bottom'),
    urwid.Filler(bottom_right, bottom='bottom')
], dividechars=1)

# 5. 组合所有行
layout = urwid.Pile([
    ('pack', top_row),          # 顶部行（自动高度）
    ('weight', 1, center_box),  # 中间行（占据剩余空间）
    ('pack', bottom_row)        # 底部行（自动高度）
])

# 6. 添加边框（可选）
frame = urwid.LineBox(layout, title="五区域布局")

# 运行
loop = urwid.MainLoop(frame)
loop.run()

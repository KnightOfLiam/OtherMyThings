import urwid

# 创建左侧和右侧的文本控件
left_content = urwid.Text("左侧内容\n按L键更新")
right_content = urwid.Text("右侧内容\n按R键更新")

# 添加边框增强可视化
left_panel = urwid.LineBox(urwid.Filler(left_content, valign='top'), title="左侧面板")
right_panel = urwid.LineBox(urwid.Filler(right_content, valign='top'), title="右侧面板")

# 使用Columns实现水平布局
"""
urwid.Columns([
    ('fixed', 宽度, 控件),   # 固定宽度
    ('pack', 控件),         # 按内容自适应
    ('weight', 权重值, 控件) # 按比例分配剩余空间
])
"""
layout = urwid.Columns([
    ('fixed', 10, left_panel),  # 左侧占1份权重
    ('weight', 1, right_panel)  # 右侧占2份权重
], dividechars=1, focus_column=1)

# 键盘事件处理函数
def handle_input(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    elif key in ('l', 'L'):
        left_content.set_text("左侧内容已更新!\n" + str(urwid.get_encoding_mode()))
    elif key in ('r', 'R'):
        right_content.set_text("右侧内容已更新!\n" + str(urwid.get_encoding_mode()))
    elif key == 'enter':
        left_content.set_text("左侧内容")
        right_content.set_text("右侧内容")

# 创建调色板增强显示效果
palette = [
    ('header', 'white', 'dark blue'),
    ('body', 'black', 'light gray'),
    ('footer', 'white', 'dark red')
]

# 添加页脚说明
footer_text = urwid.Text(('footer', " 按 L/R 更新内容 | Q 退出 | Enter 重置 "), align='center')
main_frame = urwid.Frame(
    body=urwid.AttrMap(layout, 'body'),
    footer=urwid.AttrMap(footer_text, 'footer')
)

# 运行应用程序
loop = urwid.MainLoop(
    main_frame,
    # palette=palette,
    unhandled_input=handle_input,
    handle_mouse=False
)
loop.run()



# import urwid

# def on_click(button, data):
#     footer.set_text(f"点击了: {button.label} | 数据: {data}")

# # 创建带样式的按钮
# button1 = urwid.Button("保存", on_press=on_click, user_data="SAVE_DATA")
# button2 = urwid.Button("取消", on_press=on_click, user_data="CANCEL_DATA")

# # 应用焦点样式
# # styled_btns = [urwid.BoxAdapter(urwid.AttrMap(b, None, focus_map='standout'), height=1) for b in [button1, button2]]
# # styled_btns = [urwid.AttrMap(b, None, focus_map='standout') for b in [button1, button2]]
# # box_buttons = [
# #     urwid.BoxAdapter(urwid.AttrMap(button1, None, focus_map='standout'), height=1),
# #     urwid.BoxAdapter(urwid.AttrMap(button2, None, focus_map='standout'), height=1)
# # ]
# # 每个按钮用Filler包装并居中
# filled_buttons = [
#     urwid.Filler(urwid.AttrMap(button1, None, focus_map='standout'), 'middle', height=31),
#     urwid.Filler(urwid.AttrMap(button2, None, focus_map='standout'), 'middle', height=31)
# ]

# body = urwid.Columns(filled_buttons)

# # 布局
# footer = urwid.Text("等待操作...")
# layout = urwid.Frame(
#     body=urwid.Columns(filled_buttons),
#     footer=footer
# )

# urwid.MainLoop(layout).run()

# 下面是一个完整的Urwid实现方案，用于创建类似《骑马与砍杀：霸主》的百科菜单系统，支持层级导航和快捷键操作：

import urwid
from urwid import BoxAdapter

# 全局状态管理
class NavigationState:
    def __init__(self):
        self.view_stack = []  # 视图堆栈
        self.main_loop = None
    
    def push_view(self, view):
        """压入新视图"""
        self.view_stack.append(view)
        self.update_display()
    
    def pop_view(self):
        """返回上一级"""
        if len(self.view_stack) > 1:
            self.view_stack.pop()
            self.update_display()
    
    def back_to_main(self):
        """返回主界面"""
        if self.view_stack:
            self.view_stack = [self.view_stack]
            self.update_display()
    
    def update_display(self):
        """更新界面显示"""
        if self.main_loop and self.view_stack:
            self.main_loop.widget = self.view_stack[-1]

# 创建状态单例
nav_state = NavigationState()

# 自定义可点击文本部件
class ClickableText(urwid.Text):
    _selectable = True
    
    def __init__(self, label, callback, user_data=None):
        super().__init__(label)
        self.callback = callback
        self.user_data = user_data
        self.set_wrap_mode('clip')
    
    def keypress(self, size, key):
        if key == 'enter':
            self.activate()
            return None
        return key
    
    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press' and button == 1:
            self.activate()
            return True
        return False
    
    def activate(self):
        if callable(self.callback):
            self.callback(self.user_data)

# 弹窗容器
class MenuDialog(urwid.WidgetWrap):
    def __init__(self, title, content, width=60, height=20):
        # 标题栏 (带关闭按钮)
        close_btn = ClickableText("❌", lambda _: nav_state.back_to_main())
        header = urwid.Columns([
            urwid.Text(('title', title), align='center'),
            (4, urwid.AttrMap(close_btn, None, focus_map='close_btn_focus'))
        ])
        
        # 内容区域
        body = urwid.Filler(
            urwid.Padding(content, align='center', width=('relative', 90)),
            valign='top'
        )
        
        # 底部状态栏
        footer = urwid.Text(('footer', "ESC返回上级  Q关闭  ↑↓导航  Enter选择"), align='center')
        
        # 主框架
        frame = urwid.Frame(
            body=urwid.LineBox(
                urwid.Pile([
                    ('fixed', 1, urwid.AttrMap(header, 'header')),
                    ('weight', 1, body),
                    ('fixed', 1, urwid.AttrMap(footer, 'footer'))
                ]),
                title=title
            ),
            focus_part='body'
        )
        
        # 尺寸适配
        boxed = urwid.Padding(frame, align='center', width=width)
        super().__init__(BoxAdapter(urwid.Filler(boxed, valign='middle'), height))

# 创建百科条目视图
def create_encyclopedia_view(category):
    items = {
        "人物": ["领主", "同伴", "家族", "统治者"],
        "地点": ["城堡", "城镇", "村庄", "藏身处"],
        "王国": ["瓦兰迪亚", "斯特吉亚", "库赛特", "阿塞莱"],
        "百科": ["文化", "经济", "战争", "政策"]
    }
    
    # 创建可点击条目
    pile_contents = []
    for item in items.get(category, []):
        txt = ClickableText(
            f"→ {item}",
            lambda _, it=item: nav_state.push_view(
                create_detail_view(f"{category}:{it}")
            )
        )
        adapted_txt = BoxAdapter(txt, 1)  # 先适配高度
        attr_txt = urwid.AttrMap(adapted_txt, None, focus_map='item_focus')
        # 修复：直接添加适配后的按钮
        pile_contents.append(attr_txt)
        # pile_contents.append(
        #     BoxAdapter(urwid.AttrMap(txt, None, focus_map='item_focus'), 1)
        # )
    
    # 返回按钮
    back_btn = ClickableText("← 返回", lambda _: nav_state.pop_view())
    pile_contents.append(
        BoxAdapter(urwid.AttrMap(back_btn, None, focus_map='btn_focus'), 1)
    )
    
    # 内容容器
    content = urwid.ListBox(urwid.SimpleFocusListWalker(pile_contents))
    return MenuDialog(category, content)

# 创建详情视图
def create_detail_view(item_id):
    content_map = {
        "人物:领主": "领主是王国中的贵族，拥有自己的封地和军队...",
        "地点:城堡": "城堡是战略要地，提供驻军保护和资源生产...",
        "王国:瓦兰迪亚": "瓦兰迪亚王国以骑兵闻名，拥有强大的重装骑士...",
        "百科:文化": "不同文化有独特优势：\n- 帝国：城镇发展快\n- 斯特吉亚：雪地作战强\n- 库赛特：骑射优势"
    }
    
    content = urwid.Text(('detail', content_map.get(item_id, "内容未找到")), align='left')
    back_btn = ClickableText("← 返回", lambda _: nav_state.pop_view())
    
    adapted_btn = BoxAdapter(back_btn, 1)  # 先适配高度
    attr_btn = urwid.AttrMap(adapted_btn, None, focus_map='btn_focus')

    return MenuDialog(
        item_id,
        urwid.Pile([
            ('weight', 1, urwid.Filler(content, valign='top')),
            # ('fixed', 1, BoxAdapter(urwid.AttrMap(back_btn, None, focus_map='btn_focus'), 1))
            ('fixed', 1, attr_btn)  # 直接使用适配后部件
        ])
    )

# 主界面
def create_main_view():
    categories = ["peopel", "area", "knight", "baike"]
    
    # 创建分类按钮
    buttons = []
    for cat in categories:
        btn = ClickableText(
            f"📖 {cat}",
            lambda _, c=cat: nav_state.push_view(create_encyclopedia_view(c))
        )
        adapted_btn = BoxAdapter(btn, 1)  # 先适配高度
        attr_btn = urwid.AttrMap(adapted_btn, None, focus_map='category_focus')
        buttons.append(attr_btn)  # 直接添加适配后的按钮
        # buttons.append(
        #     BoxAdapter(urwid.AttrMap(btn, None, focus_map='category_focus'), 1)
        # )
    
    # 退出按钮
    exit_btn = ClickableText("🚪 退出", lambda _: nav_state.back_to_main())
    buttons.append(
        BoxAdapter(urwid.AttrMap(exit_btn, None, focus_map='exit_focus'), 1)
    )
    
    # 主布局
    content = urwid.ListBox(urwid.SimpleFocusListWalker(buttons))
    return MenuDialog("霸主百科", content, width=40, height=15)

# 全局按键处理
def handle_global_input(key):
    if key == 'esc':
        nav_state.pop_view()
        return True
    elif key == 'q':
        nav_state.back_to_main()
        return True
    return False

# 主程序
def main():
    # 创建主视图
    main_view = create_main_view()
    nav_state.view_stack = [main_view]
    
    # 创建主循环
    loop = urwid.MainLoop(
        main_view,
        handle_mouse=True,
        unhandled_input=handle_global_input,
        palette=[
            ('header', 'white', 'dark blue'),
            ('footer', 'light gray', 'black'),
            ('title', 'yellow,bold', ''),
            ('detail', 'light gray', ''),
            ('item_focus', 'black', 'light green'),
            ('category_focus', 'black', 'yellow'),
            ('btn_focus', 'black', 'light red'),
            ('exit_focus', 'white', 'dark red'),
            ('close_btn_focus', 'white', 'dark red')
        ]
    )
    
    # 设置全局状态
    nav_state.main_loop = loop
    loop.run()

if __name__ == '__main__':
    main()
# # ====== 修改 create_main_view 函数 ======
# def create_main_view():
#     buttons = []
#     for cat in categories:
#         btn = ClickableText(...)
#         # 修复：先创建BoxAdapter，再应用AttrMap
#         adapted_btn = BoxAdapter(btn, 1)  # 先适配高度
#         attr_btn = urwid.AttrMap(adapted_btn, None, focus_map='category_focus')
#         buttons.append(attr_btn)  # 直接添加

# # ====== 修改 create_encyclopedia_view 函数 ======
# def create_encyclopedia_view(category):
#     pile_contents = []
#     for item in items.get(category, []):
#         txt = ClickableText(...)
#         # 修复：调整包装顺序
#         adapted_txt = BoxAdapter(txt, 1)
#         attr_txt = urwid.AttrMap(adapted_txt, None, focus_map='item_focus')
#         pile_contents.append(attr_txt)  # 无需额外包装

# # ====== 修改 create_detail_view 函数 ======
# def create_detail_view(item_id):
#     back_btn = ClickableText(...)
#     # 修复：正确包装返回按钮
#     adapted_btn = BoxAdapter(back_btn, 1)
#     attr_btn = urwid.AttrMap(adapted_btn, None, focus_map='btn_focus')
#     return MenuDialog(
#         item_id,
#         urwid.Pile([
#             ('weight', 1, urwid.Filler(content, valign='top')),
#             ('fixed', 1, attr_btn)  # 直接使用适配后部件
#         ])
#     )

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

KV = '''
Screen

    MDDropDownItem:
        id: drop_item
        pos_hint: {'center_x': .5, 'center_y': .5}
        text: 'Item'
        on_release: app.menu.open()
'''


class Test(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        menu_items = [{"icon": "git", "text": f"Item {i}"} for i in range(5)]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.drop_item,
            items=menu_items,
            position="center",
            callback=self.set_item,
            width_mult=4,
        )

    def set_item(self, instance):
        self.screen.ids.drop_item.set_item(instance.text)
        self.menu.dismiss()

    def build(self):
        return self.screen

if __name__ == '__main__':
    Test().run()

import random
from pathlib import Path

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image


class ItemToRandomize(BoxLayout):

    def __init__(self, **kwargs):
        image_path = kwargs.pop('image_path')
        item_location = kwargs.pop('item_location')
        super().__init__(**kwargs)

        self.orientation = 'vertical'

        item = Image(source=image_path)
        self.location = Label(text=item_location)

        self.add_widget(item)
        self.add_widget(self.location)


class MyApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items_layout = GridLayout(cols=2)
        self.preparation_tokens = [str(i.absolute()) for i in Path("images/duel/preparation tokens").glob("**/*")]

    def build(self):
        token_locations = MyApp.get_random_location_of_items(len(self.preparation_tokens))

        for token, location in zip(self.preparation_tokens, token_locations):
            self.items_layout.add_widget(ItemToRandomize(image_path=token, item_location=str(location)))

        layout = BoxLayout(orientation='vertical')

        layout.add_widget(self.items_layout)

        btn_shuffle = Button(text='перемешать', size_hint_y=0.1)
        layout.add_widget(btn_shuffle)

        btn_shuffle.bind(on_release=self.on_shuffle)

        return layout

    def on_shuffle(self, button):
        self.shuffle()

    def shuffle(self):
        new_locations = MyApp.get_random_location_of_items(len(self.preparation_tokens))

        for i, j in zip(self.items_layout.children, new_locations):
            i.location.text = str(j)

    @staticmethod
    def get_random_location_of_items(items_amount):
        location_nums = [i for i in range(1, items_amount + 1)]
        random.shuffle(location_nums)
        return location_nums


if __name__ == '__main__':
    MyApp().run()

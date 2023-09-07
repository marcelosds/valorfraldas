from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from funcoes import mensagem, imagem

screen = ScreenManager()


class LoginScreen(Screen):
    pass

    def login(self):
        from funcoes import login
        login(self)

    def cria_usuario(self):
        from funcoes import cria_usuario
        cria_usuario(self)

    def send_password_reset_email(self):
        from funcoes import send_password_reset_email
        send_password_reset_email(self)


class LeituraScreen(Screen):
    pass


class ConfiguracaoScreen(Screen):
    pass

    def define_referencia(self):
        from funcoes import define_referencia
        define_referencia(self)



screen.add_widget(LoginScreen(name='login'))
screen.add_widget(LeituraScreen(name='leitura'))
screen.add_widget(ConfiguracaoScreen(name='configuracao'))


class LiveApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # auto reload path
    AUTORELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.mensagem = mensagem
        self.imagem = imagem
        return Builder.load_file("telas.kv")



# finally, run the app
if __name__ == "__main__":
    LiveApp().run()


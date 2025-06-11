from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy_garden.mapview import MapMarkerPopup, MapView
from kivy.uix.image import AsyncImage # Import adicionado para clareza
from kivy.uix.label import Label # Import adicionado para clareza
import random

Window.size = (360, 640)

class ProdutoCard(ButtonBehavior, BoxLayout):
    """
    Um card clicável para exibir informações de um produto.
    Inclui imagem, nome e preço.
    """
    nome = StringProperty('')
    imagem = StringProperty('')
    preco = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(150), dp(190))
        self.spacing = dp(5)
        self.padding = dp(8)
        # Adiciona o retângulo arredondado como background
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(1, 1, 1, 1) # Cor de fundo branca
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Adiciona os widgets internos ao card.
        # Estes widgets são adicionados programaticamente no build() do app,
        # mas a estrutura básica é definida aqui para clareza.
        # Em um cenário real, o KV do ProdutoCard definiria esses widgets diretamente.
        # self.add_widget(AsyncImage(source=self.imagem, size_hint=(1, 0.7)))
        # self.add_widget(Label(text=self.nome, size_hint=(1, 0.15), halign='center'))
        # self.add_widget(Label(text=self.preco, size_hint=(1, 0.15), color=(0, 0.5, 0, 1), halign='center'))

    def update_rect(self, *args):
        """
        Atualiza a posição e o tamanho do retângulo de fundo
        para corresponder ao card.
        """
        self.rect.pos = self.pos
        self.rect.size = self.size

class BoasVindasScreen(Screen):
    """Tela de boas-vindas inicial do aplicativo."""
    pass

class CadastroScreen(Screen):
    """Tela para registro de novos usuários."""
    pass

class LoginScreen(Screen):
    """Tela para login de usuários existentes."""
    pass

class HomeScreen(Screen):
    """
    Tela principal que exibe produtos e opções de navegação.
    """
    def busca_changed(self, instance, texto):
        """
        Método chamado quando o texto do campo de busca é alterado.
        Pode ser usado para implementar a filtragem de produtos.
        """
        # print(f"Busca alterada para: {texto}") # Para debug
        pass

class DetalhesProdutoScreen(Screen):
    """
    Tela para exibir detalhes de um produto selecionado.
    """
    nome = StringProperty('')
    imagem = StringProperty('')
    preco = StringProperty('')

    def on_pre_enter(self):
        """
        Método chamado antes da tela se tornar visível.
        Atualiza os widgets com os dados do produto selecionado.
        """
        self.ids.produto_nome.text = self.nome
        self.ids.produto_imagem.source = self.imagem
        self.ids.produto_preco.text = self.preco

class CarteiraScreen(Screen):
    """Tela que exibe o saldo da carteira do usuário."""
    pass

class MapaScreen(Screen):
    """
    Tela que exibe um mapa, permitindo buscar locais
    e simular preços de entrega.
    """
    def on_enter(self):
        """
        Método chamado quando a tela do mapa é exibida.
        Centraliza o mapa e adiciona um marcador padrão.
        """
        # Centraliza no local padrão (São Paulo)
        self.ids.mapview.center_on(-23.55052, -46.633308)
        self.adicionar_marcador(-23.55052, -46.633308)

    def adicionar_marcador(self, lat, lon):
        """
        Adiciona um marcador no mapa nas coordenadas fornecidas.
        Remove marcadores anteriores para exibir apenas um por vez.
        """
        # Remove marcadores anteriores
        marcadores = [w for w in self.ids.mapview.children if isinstance(w, MapMarkerPopup)]
        for m in marcadores:
            self.ids.mapview.remove_widget(m)

        marcador = MapMarkerPopup(lat=lat, lon=lon)
        self.ids.mapview.add_widget(marcador)

    def buscar_local(self):
        """
        Simula a busca por um local no mapa e atualiza os preços de entrega.
        """
        endereco = self.ids.local_input.text.strip()
        if endereco:
            # Simula lat/lon próximo ao local padrão
            # Para uma implementação real, usaria uma API de geocodificação
            lat = -23.55052 + random.uniform(-0.01, 0.01)
            lon = -46.633308 + random.uniform(-0.01, 0.01)
            self.ids.mapview.center_on(lat, lon)
            self.adicionar_marcador(lat, lon)

            # Simula preços de entrega com base em uma distância aleatória
            distancia_km = random.uniform(1.0, 8.0)
            preco_bike = 3.5 + distancia_km * 0.7
            preco_moto = 4.0 + distancia_km * 1.1
            self.ids.preco_bike.text = f"R$ {preco_bike:.2f}"
            self.ids.preco_moto.text = f"R$ {preco_moto:.2f}"

KV = '''
#:import dp kivy.metrics.dp

ScreenManager:
    BoasVindasScreen:
        name: 'boasvindas'
    CadastroScreen:
        name: 'cadastro'
    LoginScreen:
        name: 'login'
    HomeScreen:
        name: 'home'
    DetalhesProdutoScreen:
        name: 'detalhes'
    CarteiraScreen:
        name: 'carteira'
    MapaScreen:
        name: 'mapa'

<BoasVindasScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(25)
        padding: dp(30)
        canvas.before:
            Color:
                rgba: 0.05, 0.6, 0.45, 1 # Verde escuro
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "Bem-vindo de volta,\\n[b]Usuário[/b]"
            markup: True
            font_size: '26sp'
            halign: 'center'
            valign: 'middle'
            text_size: self.width, None

        Button:
            text: "Entrar"
            size_hint_y: None
            height: dp(50)
            background_color: 1,1,1,1
            color: 0,0,0,1
            on_press: app.root.current = 'login'

        Button:
            text: "Não tem uma conta? Cadastre-se"
            size_hint_y: None
            height: dp(40)
            background_color: 0,0,0,0 # Transparente
            color: 1,1,1,1
            on_press: app.root.current = 'cadastro'

<CadastroScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(15)
        padding: dp(25)

        Label:
            text: "Cadastro"
            font_size: '22sp'
            size_hint_y: None
            height: dp(50)

        TextInput:
            hint_text: "Nome de Usuário"
            size_hint_y: None
            height: dp(40)

        TextInput:
            hint_text: "Senha"
            password: True
            size_hint_y: None
            height: dp(40)

        TextInput:
            hint_text: "E-mail"
            size_hint_y: None
            height: dp(40)

        Button:
            text: "Cadastrar"
            size_hint_y: None
            height: dp(50)
            on_press: app.root.current = 'login' # Simula o cadastro e vai para login

        Button:
            text: "Voltar"
            size_hint_y: None
            height: dp(40)
            on_press: app.root.current = 'boasvindas'

<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(15)
        padding: dp(25)

        Label:
            text: "Entrar"
            font_size: '22sp'
            size_hint_y: None
            height: dp(50)

        TextInput:
            hint_text: "E-mail"
            size_hint_y: None
            height: dp(40)

        TextInput:
            hint_text: "Senha"
            password: True
            size_hint_y: None
            height: dp(40)

        Button:
            text: "Login"
            size_hint_y: None
            height: dp(50)
            on_press: app.root.current = 'home' # Simula login e vai para home

        Button:
            text: "Esqueceu a senha?"
            size_hint_y: None
            height: dp(40)
            background_color: 0,0,0,1 # Cor preta
            color: 1,1,1,1 # Texto branco

<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: dp(10)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: 0.9, 0.95, 0.9, 1 # Cinza claro
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: "Olá, Usuário!"
                color: 0,0.4,0,1 # Verde escuro
                font_size: '20sp'
                halign: 'left'
                valign: 'middle'
                text_size: self.size

        TextInput:
            id: input_busca
            hint_text: "Procurar produtos..."
            size_hint_y: None
            height: dp(45)
            padding: dp(10)
            multiline: False
            on_text: root.busca_changed(self, self.text) # Chama método Python

        Label:
            text: "Produtos em alta"
            font_size: '18sp'
            size_hint_y: None
            height: dp(30)
            padding: dp(10), 0

        ScrollView:
            size_hint_y: 1
            do_scroll_x: True
            do_scroll_y: False

            BoxLayout:
                id: box_produtos
                orientation: 'horizontal'
                size_hint_x: None
                width: self.minimum_width
                spacing: dp(10)
                padding: dp(10)

        # Barra inferior fixa:
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: dp(5)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: 0, 0.5, 0.2, 1 # Verde escuro
                Rectangle:
                    pos: self.pos
                    size: self.size

            Button:
                text: "Home"
                color: 1,1,1,1
                background_color: 0,0.7,0.3,1 # Verde claro
                on_press: app.root.current = 'home'

            Button:
                text: "Carteira"
                color: 1,1,1,1
                background_color: 0,0.5,0.2,1
                on_press: app.root.current = 'carteira'

            Button:
                text: "Mapa"
                color: 1,1,1,1
                background_color: 0,0.5,0.2,1
                on_press: app.root.current = 'mapa'

<DetalhesProdutoScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        Image:
            id: produto_imagem
            source: root.imagem # Bind com a propriedade da classe
            allow_stretch: True
            keep_ratio: True
            size_hint_y: 0.6
            canvas.before:
                Color:
                    rgba: 1,1,1,1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [20]

        Label:
            id: produto_nome
            text: root.nome # Bind com a propriedade da classe
            font_size: '24sp'
            size_hint_y: None
            height: dp(40)

        Label:
            id: produto_preco
            text: root.preco # Bind com a propriedade da classe
            font_size: '20sp'
            color: 0, 0.5, 0, 1 # Verde
            size_hint_y: None
            height: dp(40)

        Button:
            text: "Voltar"
            size_hint_y: None
            height: dp(50)
            on_press: app.root.current = 'home'

<CarteiraScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        Label:
            text: "Carteira"
            font_size: '22sp'
            size_hint_y: None
            height: dp(50)

        Label:
            text: "Saldo atual: R$ 123,45" # Valor fixo
            font_size: '18sp'

        Button:
            text: "Voltar"
            size_hint_y: None
            height: dp(50)
            on_press: app.root.current = 'home'

<MapaScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(5)
        spacing: dp(5)

        BoxLayout:
            size_hint_y: None
            height: dp(40)
            spacing: dp(5)

            TextInput:
                id: local_input
                hint_text: "Digite o local"
                multiline: False

            Button:
                text: "Buscar"
                size_hint_x: None
                width: dp(80)
                on_press: root.buscar_local() # Chama o método Python

        MapView:
            id: mapview
            lat: -23.55052 # Latitude padrão (São Paulo)
            lon: -46.633308 # Longitude padrão (São Paulo)
            zoom: 12

        BoxLayout:
            size_hint_y: None
            height: dp(60)
            spacing: dp(10)
            padding: dp(10)

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                Label:
                    text: "Preço Bike:"
                    size_hint_y: None
                    height: dp(20)
                Label:
                    id: preco_bike
                    text: "R$ 0,00"
                    color: 0, 0.5, 0, 1
                    font_size: '16sp' # Aumentei um pouco para legibilidade

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                Label:
                    text: "Preço Moto:"
                    size_hint_y: None
                    height: dp(20)
                Label:
                    id: preco_moto
                    text: "R$ 0,00"
                    color: 0, 0.5, 0, 1
                    font_size: '16sp' # Aumentei um pouco para legibilidade

            Button:
                text: "Voltar"
                size_hint_x: None
                width: dp(80)
                on_press: app.root.current = 'home'
'''

class InstacartApp(App):
    """
    Classe principal do aplicativo Kivy.
    Define a construção da interface e a lógica inicial.
    """
    def build(self):
        """
        Constrói a interface do usuário do aplicativo.
        Carrega o KV e adiciona produtos de exemplo à tela Home.
        """
        sm = Builder.load_string(KV)

        # Adiciona alguns produtos de exemplo na Home
        home = sm.get_screen('home')
        produtos = [
            {'nome': 'Maçã', 'imagem': 'https://png.pngtree.com/png-vector/20231226/ourmid/pngtree-big-apple-png-image_11383442.png', 'preco': 'R$ 4,50'},
            {'nome': 'Banana', 'imagem': 'https://static.vecteezy.com/system/resources/previews/038/154/598/non_2x/ai-generated-sliced-berry-bliss-raspberry-cut-out-with-transparency-free-png.png', 'preco': 'R$ 3,20'},
            {'nome': 'Laranja', 'imagem': 'https://superprix.vteximg.com.br/arquivos/ids/175259/Bebida-Energetica-Red-Bull-250ml.png?v=636299404178930000', 'preco': 'R$ 5,10'},
            {'nome': 'Pão', 'imagem': 'https://png.pngtree.com/png-clipart/20240320/original/pngtree-chili-pepper-illustration-png-image_14638300.png', 'preco': 'R$ 2,00'},
            {'nome': 'Leite', 'imagem': 'https://www.itambe.com.br/portal/Images/Produto/requeijotrad_full.png', 'preco': 'R$ 3,80'},
        ]

        box_produtos = home.ids.box_produtos
        for p in produtos:
            card = ProdutoCard(nome=p['nome'], imagem=p['imagem'], preco=p['preco'])

            # Limpa widgets existentes e adiciona os componentes internos do card
            # Esta parte está sendo feita programaticamente aqui para fins de exemplo
            # mas o ideal é que a própria classe ProdutoCard ou seu KV defina sua estrutura interna
            card.clear_widgets() # Garante que não haja widgets residuais
            img = AsyncImage(source=p['imagem'], size_hint=(1, 0.7))
            card.add_widget(img)
            card.add_widget(Label(text=p['nome'], size_hint=(1, 0.15), halign='center', color=(0,0,0,1))) # Adicionado cor preta para o texto
            card.add_widget(Label(text=p['preco'], size_hint=(1, 0.15), color=(0, 0.5, 0, 1), halign='center'))

            # Configura o on_press para navegar para a tela de detalhes
            def on_card_press(instance, produto=p):
                detalhes = sm.get_screen('detalhes')
                detalhes.nome = produto['nome']
                detalhes.imagem = produto['imagem']
                detalhes.preco = produto['preco']
                sm.current = 'detalhes'
            card.bind(on_press=on_card_press)
            box_produtos.add_widget(card)

        return sm

if __name__ == '__main__':
    InstacartApp().run()

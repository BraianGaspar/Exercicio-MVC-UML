import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


# ================== INTERFACE DO OBSERVADOR ==================
class Observer(ABC):
    """Interface para o padrão Observer"""

    @abstractmethod
    def update(self):
        """Método chamado quando o modelo muda"""
        pass


# ================== MODELO ==================
class ClickCounterModel:
    """Modelo que armazena e gerencia o estado do contador"""

    def __init__(self):
        self._count = 0
        self._observers = []

    def get_count(self):
        """Retorna o número atual de cliques"""
        return self._count

    def increment(self):
        """Incrementa o contador em 1"""
        self._count += 1
        self._notify_observers()

    def reset(self):
        """Reseta o contador para 0"""
        self._count = 0
        self._notify_observers()

    def add_observer(self, observer):
        """Adiciona um observador para notificações de mudança"""
        if not isinstance(observer, Observer):
            raise TypeError("Observador deve implementar a interface Observer")
        self._observers.append(observer)

    def remove_observer(self, observer):
        """Remove um observador da lista"""
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self):
        """Notifica todos os observadores sobre mudanças"""
        for observer in self._observers:
            observer.update()


# ================== VISUALIZAÇÃO ==================
class ClickCounterView(tk.Tk):
    """Visualização que exibe a interface gráfica"""

    def __init__(self):
        super().__init__()

        self.title("Contador de Cliques - Padrão MVC")
        self.geometry("400x300")
        self.resizable(False, False)

        # Centralizar janela
        self._center_window()

        # Configurar estilo
        self._configure_styles()

        # Frame principal
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Contador de Cliques",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=15)

        # Frame do display
        display_frame = ttk.Frame(main_frame, style="Display.TFrame")
        display_frame.pack(pady=20, padx=20, fill=tk.BOTH)

        # Display do contador
        self.count_display = ttk.Label(
            display_frame,
            text="0",
            font=("Arial", 56, "bold"),
            foreground="#0066cc",
            anchor=tk.CENTER
        )
        self.count_display.pack(pady=30)

        # Frame dos botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        # Botão Clique
        self.click_button = ttk.Button(
            button_frame,
            text="➕ Clique",
            command=self._on_click_pressed,
            style="Action.TButton",
            width=12
        )
        self.click_button.pack(side=tk.LEFT, padx=10)

        # Botão Resetar
        self.reset_button = ttk.Button(
            button_frame,
            text="🔄 Resetar",
            command=self._on_reset_pressed,
            style="Reset.TButton",
            width=12
        )
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Label de informação
        info_label = ttk.Label(
            main_frame,
            text="Pressione 'Clique' para incrementar | 'Resetar' para zerar",
            font=("Arial", 8),
            foreground="#666666"
        )
        info_label.pack(pady=5)

        # Listeners (callbacks)
        self._click_listener = None
        self._reset_listener = None

    def _center_window(self):
        """Centraliza a janela na tela"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _configure_styles(self):
        """Configura estilos personalizados"""
        style = ttk.Style()
        style.configure("Display.TFrame", relief=tk.RIDGE, borderwidth=2)
        style.configure("Action.TButton", font=("Arial", 10, "bold"))
        style.configure("Reset.TButton", font=("Arial", 10))

    def set_click_listener(self, callback):
        """Define o callback para o botão Clique"""
        self._click_listener = callback

    def set_reset_listener(self, callback):
        """Define o callback para o botão Resetar"""
        self._reset_listener = callback

    def _on_click_pressed(self):
        """Chamado quando o botão Clique é pressionado"""
        if self._click_listener:
            self._click_listener()

    def _on_reset_pressed(self):
        """Chamado quando o botão Resetar é pressionado"""
        if self._reset_listener:
            self._reset_listener()

    def update_display(self, count):
        """Atualiza a exibição do contador"""
        self.count_display.config(text=str(count))

        # Animação visual de feedback
        if count > 0:
            self.count_display.config(foreground="#0066cc")
        else:
            self.count_display.config(foreground="#999999")


# ================== CONTROLADOR ==================
class ClickCounterController(Observer):
    """Controlador que conecta modelo e visualização"""

    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Configura listeners na view
        self.view.set_click_listener(self._on_click)
        self.view.set_reset_listener(self._on_reset)

        # Registra como observador do modelo
        self.model.add_observer(self)

        # Atualiza a view com o estado inicial
        self.update()

    def _on_click(self):
        """Trata o evento de clique do botão"""
        print("👆 Botão 'Clique' pressionado")
        self.model.increment()

    def _on_reset(self):
        """Trata o evento de reset do botão"""
        print("🔄 Botão 'Resetar' pressionado")
        self.model.reset()

    def update(self):
        """Atualiza a visualização com dados do modelo (padrão Observer)"""
        count = self.model.get_count()
        print(f"📊 Atualizando view - Contador: {count}")
        self.view.update_display(count)

    def run(self):
        """Inicia a aplicação"""
        self.view.mainloop()


# ================== APLICAÇÃO PRINCIPAL ==================
def main():
    """Função principal que inicializa a aplicação"""
    print("=" * 60)
    print("         Aplicação Contador de Cliques - Padrão MVC")
    print("=" * 60)
    print("✓ Modelo: ClickCounterModel (gerencia o estado)")
    print("✓ Visualização: ClickCounterView (interface gráfica)")
    print("✓ Controlador: ClickCounterController (conecta M e V)")
    print("✓ Padrão Observer: Implementado para notificações")
    print("=" * 60)
    print()

    # Instancia os componentes MVC
    model = ClickCounterModel()
    view = ClickCounterView()
    controller = ClickCounterController(model, view)

    # Inicia a aplicação
    controller.run()


if __name__ == "__main__":
    main()

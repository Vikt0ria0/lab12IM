import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("")

        self.days = 0
        self.state = 0
        self.state0 = 0
        self.stateOld = 0
        self.P = [
            [0.6, 0.3, 0.1],
            [0.4, 0.2, 0.4],
            [0.1, 0.4, 0.5]]
        self.random = random.Random()

        # Создание фрейма для виджетов
        self.frame = tk.Frame(self)
        self.frame.pack(padx=10, pady=10)

        # Создание изображения
        self.image_label = tk.Label(self.frame)
        self.image_label.pack(pady=10)
        self.picter(self.state)

        # Создание кнопки Старт/ Стоп
        self.start_button = tk.Button(self.frame, text="Старт", command=self.start_simulation)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = tk.Button(self.frame, text="Стоп", command=self.stop_simulation)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        #день
        self.day_label = tk.Label(self.frame, text=f"День: {self.days}")
        self.day_label.pack(side=tk.LEFT, padx=10)

        # График
        self.fig = plt.Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("Дни")
        self.ax.set_ylabel("Состояние")

        # Создание канвы для отображения графика
        self.chart_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(pady=10)

        # Создание метки для вывода эмпирических вероятностей
        self.probability_label = tk.Label(self, text="")
        self.probability_label.pack(pady=10)

        # Флаг для отслеживания, запущена ли симуляция
        self.simulation_running = False

        # Список для хранения данных графика
        self.chart_data = []

    def start_simulation(self):
        if not self.simulation_running:
            self.simulation_running = True
            self.days = 0
            self.state = self.state0
            self.picter(self.state)
            self.chart_data = [(0, self.state)]
            self.update_chart()
            self.update_state()

    def stop_simulation(self):
        if self.simulation_running:
            self.simulation_running = False
            self.after_cancel(self.update_state)

    def update_state(self):
        if self.simulation_running:
            self.state = self.state_transition(self.state) #текущее состояние
            self.picter(self.state)
            self.days += 1
            self.day_label.config(text=f"День: {self.days}")
            self.chart_data.append((self.days, self.state))
            self.update_chart()
            self.update_probabilities()
            self.after(1000, self.update_state)

    def state_transition(self, old_state): #переход состояния
        a = self.random.random()
        sum = 0
        for i in range(3):
            sum += self.P[old_state][i]
            if a < sum:
                return i
        return -1

    def picter(self, state):
        image_path = {
            0: "1.png",
            1: "2.png",
            2: "3.jpg",
        }.get(state)
        if image_path:
            try:
                image = Image.open(image_path)
                image = image.resize((300, 200))  # Изменение размера изображения
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo
            except FileNotFoundError:
                messagebox.showerror("Ошибка", f"Изображение '{image_path}' не найдено.")

    def update_chart(self):
        # Получение данных
        x_values = [x for x, _ in self.chart_data]
        y_values = [y for _, y in self.chart_data]

        # Очистка предыдущего графика
        self.ax.clear()

        # Построение графика
        self.ax.plot(x_values, y_values)
        self.ax.set_xlabel("Дни")
        self.ax.set_ylabel("Состояние")

        # Обновление канвы
        self.chart_canvas.draw()

    def update_probabilities(self):
        # Подсчет эмпирических вероятностей
        counts = [0, 0, 0]
        for _, state in self.chart_data:
            counts[state] += 1
        total_days = len(self.chart_data)
        probabilities = [count / total_days for count in counts]

        # Формирование текста для метки
        probability_text = "Эмпирические вероятности:\n"
        probability_text += f"Состояние 0: {probabilities[0]:.2f}\n"
        probability_text += f"Состояние 1: {probabilities[1]:.2f}\n"
        probability_text += f"Состояние 2: {probabilities[2]:.2f}\n"

        # Обновление метки
        self.probability_label.config(text=probability_text)

if __name__ == "__main__":
    app = App()
    app.mainloop()

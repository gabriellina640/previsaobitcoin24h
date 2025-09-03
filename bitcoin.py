import requests
import numpy as np
import tkinter as tk
from tkinter import messagebox


class LinearRegression:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__correlation_coefficient = self.__correlacao()
        self.__inclination = self.__inclinacao()
        self.__intercept = self.__interceptacao()

    def __correlacao(self):
        covariacao = np.cov(self.x, self.y, bias=True)[0][1]
        variancia_x = np.var(self.x)
        variancia_y = np.var(self.y)
        return covariacao / np.sqrt(variancia_x * variancia_y)

    def __inclinacao(self):
        stdx = np.std(self.x)
        stdy = np.std(self.y)
        return self.__correlation_coefficient * (stdy / stdx)

    def __interceptacao(self):
        mediax = np.mean(self.x)
        mediay = np.mean(self.y)
        return mediay - self.__inclination * mediax

    def previsao(self, valor):
        return self.__intercept + (self.__inclination * valor)


def pegar_precos():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {'vs_currency': 'brl', 'days': '2'}
    response = requests.get(url, params=params, verify=False)
    data = response.json()
    todos_precos = [item[1] for item in data['prices']]
    return todos_precos[-24:]  # últimos 24 pontos (1 dia)


def calcular_previsao():
    precos_1_dia = pegar_precos()
    x = np.array(range(1, 25))
    y = np.array(precos_1_dia)
    
    
    lista_precos.delete(0, tk.END)
    for hora, preco in enumerate(precos_1_dia, start=1):
        lista_precos.insert(tk.END, f"Hora {hora}: R${preco:.2f}")
    
    
    lr = LinearRegression(x, y)
    previsao_hora_25 = lr.previsao(25)
    
    label_previsao.config(text=f"Previsão em 1 hora: R${previsao_hora_25:.2f}")


janela = tk.Tk()
janela.title("Previsão Bitcoin")
janela.geometry("400x500")


botao = tk.Button(janela, text="Calcular Previsão", command=calcular_previsao)
botao.pack(pady=10)


lista_precos = tk.Listbox(janela, width=50, height=20)
lista_precos.pack(pady=10)


label_previsao = tk.Label(janela, text="", font=("Arial", 14), fg="blue")
label_previsao.pack(pady=10)

janela.mainloop()

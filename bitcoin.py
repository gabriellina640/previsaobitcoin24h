import requests
import numpy as np

# --- PEGAR DADOS DO BITCOIN ---
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    'vs_currency': 'brl',
    'days': '2'  # pegar 2 dias para ter pelo menos 24 pontos por dia
}

# Ignorando verificação SSL para teste local
response = requests.get(url, params=params, verify=False)
data = response.json()

# Extrair preços
todos_precos = [item[1] for item in data['prices']]

# Pegar apenas os últimos 24 pontos para representar 1 dia
precos_1_dia = todos_precos[-24:]

# Criar eixo X para o dia (1 a 24 horas)
x = np.array(range(1, 25))
y = np.array(precos_1_dia)

# --- SUA CLASSE LINEARREGRESSION ---
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

# CRIAR MODELO E PREVER PRÓXIMA HORA 
lr = LinearRegression(x, y)
previsao_hora_25 = lr.previsao(25)

# Formatar preços do último dia com 2 casas decimais
precos_formatados = [f"{preco:.2f}" for preco in y]

print(f"Preços por hora do último dia: {precos_formatados}")
print(f"Previsão em uma hora: R${previsao_hora_25:.2f}")


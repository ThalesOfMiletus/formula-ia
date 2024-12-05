# **Documentação do Projeto - Fórmula IA: Simulação de corrida com Programação Genética**

## **Introdução**
Este projeto é uma simulação de carros autônomos que utilizam **programação genética** para aprender a atravessar uma pista repleta de obstáculos e alcançar uma linha de chegada. Cada carro possui um conjunto de "genes" que controla sua direção ao longo da pista, e os mais aptos são clonados para formar a próxima geração.

O objetivo do projeto é demonstrar os conceitos básicos de algoritmos genéticos em um ambiente visual interativo.

---

## **Funcionamento**
### **Componentes Principais**
1. **Carros:**
   - Cada carro é representado como um retângulo que se move automaticamente pela pista.
   - Os carros possuem genes que determinam seus movimentos (ângulos de curva em diferentes momentos).
   - Eles têm velocidade variável, aceleração e rotação.
   - Quando colidem com um obstáculo, saem da pista ou atingem a linha de chegada, são desativados.

2. **Pista:**
   - Uma faixa cinza reta com limites claros.
   - Contém **obstáculos fixos** que os carros devem evitar.
   - Inclui uma **linha de chegada vertical**, onde os carros completam a simulação.

3. **Algoritmo Genético:**
   - A cada geração, o carro mais apto (com maior pontuação) é identificado.
   - Todos os carros da próxima geração são clones do carro mais apto da geração atual.

---

### **Fluxo de Execução**
1. Inicialização:
   - Um número definido de carros (ex.: 400) é gerado com genes aleatórios.
   - Eles começam na mesma posição inicial na pista.

2. Simulação:
   - Cada carro segue seus genes para se mover pela pista.
   - A cada passo, os carros verificam:
     - Se colidiram com um obstáculo.
     - Se saíram da pista.
     - Se cruzaram a linha de chegada.

3. Avaliação:
   - A "aptidão" de cada carro é calculada com base em:
     - Proximidade da linha de chegada.
     - Se cruzaram a linha de chegada.
   - O melhor carro é identificado.

4. Geração:
   - Todos os carros da próxima geração são clones do melhor carro da geração atual.
   - O processo é repetido até que os carros aprendam a atravessar a pista.

---

## **Requisitos**
### **Bibliotecas Necessárias**
- `pygame`
- `sys`
- `random`
- `math`

### **Execução**
1. Instale o Python.
2. Instale o `requirements.txt` usando o comando:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o script:
   ```bash
   python formulaia.py
   ```

---

## **Estrutura do Código**
### **1. Configuração**
Define as cores, dimensões da tela, posição inicial dos carros, posição da linha de chegada e obstáculos.

### **2. Classe `Car`**
Representa cada carro da simulação. Principais métodos:
- `move`: Calcula o movimento com base na velocidade e ângulo.
- `auto_drive`: Direciona o carro com base em seus genes.
- `check_collision`: Verifica se o carro colidiu com um obstáculo ou saiu da pista.
- `check_finish`: Verifica se o carro cruzou a linha de chegada.
- `calculate_fitness`: Calcula a pontuação de aptidão com base na distância da linha de chegada.

### **3. Funções Genéticas**
- `calculate_fitness`: Avalia a aptidão de cada carro ao final de uma geração.
- `clone_best_car`: Clona o melhor carro para criar a próxima geração.

### **4. Pista e Obstáculos**
- `draw_track`: Desenha a pista, obstáculos e a linha de chegada.

---

## **Configurações Customizáveis**
1. **Número de Carros:**
   - Pode ser ajustado na variável `num_cars` na função `main()`.
   - Valor padrão: `400`.

2. **Obstáculos:**
   - Definidos na lista `OBSTACLES`.
   - Cada obstáculo é representado por um retângulo com coordenadas `(x, y, largura, altura)`.

3. **Atributos dos Carros:**
   - Velocidade inicial: Ajustada em `speed`.
   - Velocidade máxima: Ajustada em `max_speed`.
   - Taxa de mutação: Definida na função `mutate`.

---

## **Melhorias Futuras**
1. **Diversidade Genética:**
   - Introduzir variabilidade na próxima geração para explorar mais possibilidades.
   - Implementar cruzamentos e mutações em vez de clonar apenas um carro.

2. **Pistas Mais Complexas:**
   - Criar pistas com curvas ou rotas alternativas.
   - Adicionar variações no formato dos obstáculos.

3. **Feedback Visual:**
   - Exibir a trajetória de carros das gerações anteriores para observar o progresso.
   - Mostrar a aptidão de cada carro na tela.

4. **Outros Algoritmos:**
   - Experimentar métodos alternativos de aprendizado, como redes neurais.

---

## **Licença**
Este projeto é de uso livre para fins educacionais e não possui restrições de uso comercial. 

---

Se precisar expandir a documentação ou criar um README para um repositório GitHub, posso ajudar a refiná-la ainda mais! 🚗✨

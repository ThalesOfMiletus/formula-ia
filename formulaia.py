import pygame
import sys
import random
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1200, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação com Programação Genética - Obstáculos")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
OBSTACLE_COLOR = (139, 69, 19)  # Marrom
YELLOW = (255, 255, 0)

CAR_COLORS = [RED, BLUE, YELLOW, (0, 255, 0), (255, 0, 255)]

# Relógio para controle de FPS
clock = pygame.time.Clock()

# Linha de chegada ajustada
FINISH_LINE_START = (1100, 100)
FINISH_LINE_END = (1100, 300)

# Posição inicial dos carros
START_POSITION_X = 100
START_POSITION_Y = 200

# Obstáculos
OBSTACLES = [
    pygame.Rect(350, 140, 60, 100),  # Primeiro obstáculo
    pygame.Rect(700, 250, 50, 50),  # Segundo obstáculo
    pygame.Rect(900, 100, 50, 150),  # Terceiro obstáculo
]

# Configuração de fonte para texto
FONT = pygame.font.SysFont("Arial", 20)

# Classe para o carro
class Car:
    def __init__(self, x, y, angle, genes=None):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = random.uniform(8, 10)
        self.max_speed = random.uniform(10, 20)
        self.acceleration = random.uniform(0.1, 0.5)
        self.rotation_speed = random.uniform(20, 30)
        self.fitness = 0
        self.alive = True
        self.finished = False
        self.color = random.choice(CAR_COLORS)

        self.genes = genes if genes else [random.uniform(-45, 45) for _ in range(20)]

    def move(self):
        if self.speed < self.max_speed:
            self.speed += self.acceleration
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

    def auto_drive(self, step):
        if step < len(self.genes):
            self.angle += self.genes[step]
        self.move()

    def check_collision(self):
        if not (0 <= self.x < WIDTH and 100 <= self.y <= 300):
            self.alive = False
        else:
            for obstacle in OBSTACLES:
                if obstacle.collidepoint(self.x, self.y):
                    self.alive = False

    def check_finish(self):
        if FINISH_LINE_START[0] - 10 <= self.x <= FINISH_LINE_START[0] + 10:
            if FINISH_LINE_START[1] <= self.y <= FINISH_LINE_END[1] and not self.finished:
                self.fitness += 1000
                self.alive = False
                self.finished = True

    def calculate_fitness(self):
        # Aptidão baseada na distância mínima à linha de chegada
        distance_x = abs(self.x - FINISH_LINE_START[0])
        distance_y = max(0, abs(self.y - (FINISH_LINE_START[1] + FINISH_LINE_END[1]) / 2))
        proximity = math.sqrt(distance_x**2 + distance_y**2)  # Distância mínima à linha de chegada

        # Fitness básico: recompensa pela proximidade da linha de chegada
        self.fitness += max(0, 1000 - proximity)

        # Penalização por colisões
        if not self.alive:
            self.fitness -= 100

        # Recompensa por se manter na pista
        if 100 <= self.y <= 300:
            self.fitness += 50

        # Recompensa por distância percorrida em x
        self.fitness += self.x / WIDTH * 100


    def draw(self, screen):
        # Desenha o carro como um retângulo rotacionado
        car_surface = pygame.Surface((30, 20), pygame.SRCALPHA)  # Tamanho maior
        car_surface.fill(self.color)  # Cor do carro
        rotated_car = pygame.transform.rotate(car_surface, -self.angle)
        car_rect = rotated_car.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_car, car_rect.topleft)

# Função para seleção genética com clonagem do melhor carro
def genetic_selection(cars, num_cars):
    # Verifica se algum carro terminou a corrida
    finished_cars = [car for car in cars if car.finished]

    if finished_cars:
        # Seleciona o primeiro carro que terminou para clonagem
        best_car = finished_cars[0]
        print(f"Carro terminou a corrida! Clonando para a próxima geração.")
        # Cria a próxima geração clonando o carro que terminou
        next_generation = [Car(START_POSITION_X, START_POSITION_Y, 0, genes=best_car.genes) for _ in range(num_cars)]
    else:
        # Se nenhum carro terminou, aplica seleção genética normal
        cars = sorted(cars, key=lambda c: c.fitness, reverse=True)
        next_generation = [Car(START_POSITION_X, START_POSITION_Y, 0, genes=cars[0].genes)]  # Clona o melhor

        # Seleciona os melhores carros para reprodução
        selected = cars[:num_cars // 2]

        for _ in range(num_cars - 1):
            parent1, parent2 = random.sample(selected, 2)
            child_genes = crossover(parent1.genes, parent2.genes)
            child_genes = mutate(child_genes)
            next_generation.append(Car(START_POSITION_X, START_POSITION_Y, 0, genes=child_genes))

    return next_generation



def crossover(genes1, genes2):
    return [g1 if random.random() < 0.7 else g2 for g1, g2 in zip(genes1, genes2)]

def mutate(genes):
    mutation_rate = 0.3
    return [gene + random.uniform(-10, 10) if random.random() < mutation_rate else gene for gene in genes]

def draw_track(render):
    if render:
        screen.fill(GREEN)
        pygame.draw.rect(screen, GRAY, (0, 100, WIDTH, 200))
        pygame.draw.line(screen, WHITE, FINISH_LINE_START, FINISH_LINE_END, 5)
        for obstacle in OBSTACLES:
            pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle)

def draw_info(screen, generation, finished_cars, best_fitness, closest_proximity):
    text_gen = FONT.render(f"Geração: {generation}", True, WHITE)
    text_finished = FONT.render(f"Carros que terminaram: {finished_cars}", True, WHITE)
    text_best = FONT.render(f"Melhor Fitness: {best_fitness:.2f}", True, WHITE)
    text_proximity = FONT.render(f"Proximidade mais próxima: {closest_proximity:.2f}", True, WHITE)

    screen.blit(text_gen, (10, 10))
    screen.blit(text_finished, (10, 40))
    screen.blit(text_best, (10, 70))
    screen.blit(text_proximity, (10, 100))

def main(render=True):
    num_cars = 800
    cars = [Car(START_POSITION_X, START_POSITION_Y, 0) for _ in range(num_cars)]
    generation = 1
    step = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if render:
            draw_track(render)

        for car in cars:
            if car.alive:
                car.auto_drive(step)
                car.check_collision()
                car.check_finish()
                if render:
                    car.draw(screen)

        finished_cars = sum(car.finished for car in cars)
        best_fitness = max(car.fitness for car in cars)

        # Verifica se há carros vivos antes de calcular a proximidade
        if any(car.alive for car in cars):
            closest_proximity = min(
                math.sqrt(abs(car.x - FINISH_LINE_START[0])**2 + abs(car.y - (FINISH_LINE_START[1] + FINISH_LINE_END[1]) / 2)**2)
                for car in cars if car.alive
            )
        else:
            closest_proximity = float('inf')  # Valor padrão

        if all(not car.alive for car in cars) or step > 300:
            for car in cars:
                if car.alive:
                    car.calculate_fitness()

            print(f"Geração: {generation}, Carros que terminaram: {finished_cars}, Melhor Fitness: {best_fitness:.2f}, Proximidade mais próxima: {closest_proximity:.2f}")

            cars = genetic_selection(cars, num_cars)
            step = 0
            generation += 1

        if render:
            draw_info(screen, generation, finished_cars, best_fitness, closest_proximity)
            pygame.display.flip()
            clock.tick(60)

        step += 1


if __name__ == "__main__":
    main(render=True)

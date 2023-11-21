# Importação de bibliotecas necessárias
import random                               # Biblioteca para geração de números aleatórios
import time                                 # Biblioteca para manipulação de tempo
from spade.agent import Agent               # Módulo para criação de agentes no SPADE
from spade.behaviour import CyclicBehaviour # Módulo para comportamentos cíclicos no SPADE
from spade.message import Message           # Módulo para manipulação de mensagens no SPADE
import asyncio                              # Biblioteca para programação assíncrona em Python
import spade                                # Biblioteca SPADE para desenvolvimento de sistemas multiagentes
import pygame                               # Biblioteca para a interface gráfica do projeto
from queue import PriorityQueue             # Implementação de uma fila de prioridade em Python
from collections import defaultdict         # Implementação de um dicionário padrão em Python (defaultdict)

# Seed the random number generator with the current system time
random.seed(time.time())

# Inicialização de constantes e estruturas de dados
SIZE = 30  # Tamanho do mapa
traffic_lights_grid = [[None for _ in range(SIZE)] for _ in range(SIZE)]    # Grade para armazenar informações sobre semáforos
vehicles_grid = [[None for _ in range(SIZE)] for _ in range(SIZE)]          # Grade para armazenar informações sobre veículos
lanes_grid = [[None for _ in range(SIZE)] for _ in range(SIZE)]             # Grade para armazenar informações sobre faixas de tráfego
intersections_grid = [[None for _ in range(SIZE)] for _ in range(SIZE)]     # Grade para armazenar informações sobre interseções
emergency_grid = [[None for _ in range(SIZE)] for _ in range(SIZE)]         # Grade para armazenar informações sobre situações de emergência

message_dict = defaultdict(list) # Dicionário padrão para armazenar listas de mensagens associadas a ids

analise_times = []  # Lista para armazenar tempos de espera para análise de estatísticas
clock = 1           # Variável para contar o tempo
media_max=[]         # Lisra para armazenar a média máxima de espera

class Map:
    def __init__(self):
        # Inicializa os atributos do mapa
        self.zoom_level = 1
        self.offset_x = 0
        self.offset_y = 0
        self.previous_media = 0
        self.maxTimeMedia = 0


    def zoom_in(self):
        # Aumenta o zoom do mapa no display pygame
        self.zoom_level *= 1.2


    def zoom_out(self):
        # Diminui o zoom do mapa no display pygame
        self.zoom_level /= 1.2


    def pan(self, dx, dy):
        # Move o mapa no display pygame com o rato
        self.offset_x += dx
        self.offset_y += dy


    def update_traffic_lights(self, x, y, info):
        # Atualiza as luzes de trânsito na posição (x, y) com as informações fornecidas
        traffic_lights_grid[x][y] = info


    def update_vehicles(self, x, y, info):
        # Atualiza os veículos na posição (x, y) com as informações fornecidas
        vehicles_grid[x][y] = info


    def update_lanes(self, x, y, info):
        # Método para atualizar as faixas na posição (x, y) com a informação dada
        if lanes_grid[x][y] is None:
            lanes_grid[x][y] = []
        lanes_grid[x][y].append(info)


    def update_intersections(self, x, y, info):
        # Método para atualizar as interseções na posição (x, y) com a informação dada
        intersections_grid[x][y] = info


    def update_emergency(self, x, y, info):
        # Método para atualizar situações de emergência na posição (x, y) com a informação dada
        emergency_grid[x][y] = info    


    def IsThereTrafficLight(self, x, y):
        # Método para verificar se há um semáforo na posição (x, y)
        if traffic_lights_grid[x][y] is not None or traffic_lights_grid[x][y] != 0:
            return traffic_lights_grid[x][y]
        return False


    def IsThereCar(self, x, y):
        # Método para verificar se há um carro na posição (x, y)
        if vehicles_grid[x][y] is None or vehicles_grid[x][y]  == 0:
            return False
        return vehicles_grid[x][y]
    
    
    def isThereEmergency(self, x, y):
        # Método para verificar se há uma situação de emergência na posição (x, y)
        if emergency_grid[x][y] is None or emergency_grid[x][y] == 0 or emergency_grid[x][y] == 1:
            return False
        return emergency_grid[x][y]


    def WhatsNextLane(self, x, y):
        # Método para mostrar os movimentos disponíveis para o carro na posição (x, y)
        if lanes_grid[x][y] is not None:
            lanes = []
            for i in range(len(env.lanes)):
                for k in range(len(lanes_grid[x][y])):
                    if env.lanes[i].lane_id == lanes_grid[x][y][k]:
                        lanes.append(env.lanes[i].next_position(x,y))
                        break
            return lanes
    
    
    def route_greedy(self, from_x, from_y, to_x, to_y):
        # Método para encontrar o caminho mais eficiente pelo algoritmo greedy para o veículo de emergência
        class Node:
            # Classe interna para representar um nó na busca do caminho
            def __init__(self, greedy, parent, position):
                self.parent = parent
                self.position = position
                self.greedy = greedy

            
            def __eq__(self, other):
                return self.position == other.position
            

            def CalcularCusto(self, to_x, to_y):
                # Calcula o custo (distância de Manhattan) do nó até o ponto de destino
                return self.greedy.ManhattanDistance(self.position[0], self.position[1], to_x, to_y)
            

            def __lt__(self, other):
            
                return self.CalcularCusto(to_x, to_y) < other.CalcularCusto(to_x, to_y)
            

            def __gt__(self, other):
                return self.CalcularCusto(to_x, to_y) > other.CalcularCusto(to_x, to_y)
            

            def __le__(self, other):
                return self.CalcularCusto(to_x, to_y) <= other.CalcularCusto(to_x, to_y)
            

            def __ge__(self, other):
                return self.CalcularCusto(to_x, to_y) >= other.CalcularCusto(to_x, to_y)
            

            def __ne__(self, other):
                return self.position != other.position
            

            def __repr__(self):
                return f"{self.position} - g: {self.CalcularCusto(to_x, to_y)}"
            
            
            def __str__(self):
                return f"{self.position} - g: {self.CalcularCusto(to_x, to_y)}"
            

            def __hash__(self):
                return hash(self.position)
            

            def return_parent(self):
                return self.parent


        def return_path(current_node):
            # Retorna o caminho a ser percorrido pelo veículo de emergência
            path = []
            result = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.return_parent()
            path = path[::-1]
            for i in range(len(path)):
                result.append(path[i])
            print(result)
            return result
        

        def search(start, end):
            # Método de busca para encontrar o caminho mais eficiente pelo meio de uma fila de prioridade
            q = PriorityQueue()             # Cria uma fila de prioridade para armazenar os nós a serem explorados
            visited = set()                 # Conjunto para rastrear nós já visitados durante a busca
            no = Node(self, None, start)    # Cria o nó de origem
            q.put(no)                       # Adiciona o nó de origem à fila de prioridade

            while not q.empty():
                atual = q.get()                                                         # Obtém o nó com menor custo da fila de prioridade
                if atual.position == end:                                               # Se o nó atual atingir o destino, retorna o caminho percorrido
                    return return_path(atual)
                if atual.position not in visited:
                    visited.add(atual.position)                                          # Marca o nó atual como visitado
                    nextmoves = self.WhatsNextLane(atual.position[0], atual.position[1]) # Obtém os movimentos disponíveis
                    if nextmoves is not None:
                        for i in range(len(nextmoves)):
                            if nextmoves[i] is not None and nextmoves[i] not in visited:
                                no = Node(self, atual, nextmoves[i])                     # Cria um novo nó para o próximo movimento
                                q.put(no)                                                # Adiciona o novo nó à fila de prioridade para explorar

        return search((from_x, from_y), (to_x, to_y)) # Inicia a busca com os pontos de origem e destino
     
    
    def ManhattanDistance(self, from_x, from_y, to_x, to_y):
        # Calcula a distância de Manhattan entre dois pontos
        return abs(from_x - to_x) + abs(from_y - to_y)
    

    async def statiscs(self):
        # Atualiza estatísticas periodicamente (a cada segundo)
        global analise_times
        global clock
        global media_max
        while True:
            maximo=0
            for element in analise_times:
                if element>maximo:
                    maximo=element
            if maximo>0:
                media_max.append(maximo) # Adiciona o valor máximo de tempos de espera à lista
                
            for max in media_max:
                if max == 0:
                    media_max.remove(max)
                self.maxTimeMedia+=max # Soma os valores máximos de tempos de espera
            
            if len(media_max) > 0:
                self.maxTimeMedia = self.maxTimeMedia / len(media_max) # Calcula a média dos valores máximos de tempos de espera


            media = float(len(analise_times) / len(env.cars))
            # media igual ao anterior a dividir por dois
            if self.previous_media != 0:
                # Calcula a média ponderada considerando o valor anterior
                media = (media / clock) + (self.previous_media *  (clock - 1)  / clock )
            self.previous_media = media
            analise_times = []
            clock += 1
            await asyncio.sleep(1)

    async def draw_map(self):
        # Inicializa e atualiza a interface gráfica do ambiente
        pygame.init()
        screen_width, screen_height = 1100, 700
        CHAT_WIDTH, _ = 400, screen_height
        GAME_WIDTH, GAME_HEIGHT = screen_width - CHAT_WIDTH, screen_height
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        pygame.display.set_caption('Traffic Simulation')

        # Definição das cores utilizadas
        lane_color = (70, 70, 70)                       # Gray
        intersection_color = (50, 50, 50)               # Dark Gray
        car = (255, 255, 255)                           # White
        greenback = (0, 200, 100)                       # Green background
        Emergency_vehicle_grid_color_blue = (0, 0, 255) # Blue
        Emergency_color = (255, 165, 0)                 # Orange
        RED = (255, 0, 0)                               # Red
        BLACK = (0, 0, 0)                               # Black

        # Cores dos semáforos
        traffic_light_colors = {
            'Green': (60, 255, 60),
            'Yellow': (255, 255, 0),
            'Red': (255, 0, 0),
            'Intermitent': (255, 165, 0)  # Orange for Intermitent
        }

        # Configuração das fontes e cores de texto
        font = pygame.font.SysFont('Arial', 16)
        font1 = pygame.font.SysFont('Arial', 14)
        font2 = pygame.font.SysFont('Arial', 12)
        font_heading = pygame.font.SysFont('Arial', 23, True)

        chat_scroll = 0
        running = True
        dragging = False
        prev_mouse_pos = None
        last_click_time = 0
        double_click_threshold = 500

        siren = 0
        while running:
            # Lida com eventos do pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.VIDEORESIZE:
                    # Atualiza as dimensões da janela do pygame
                    screen_width, screen_height = event.w, event.h
                    GAME_WIDTH, GAME_HEIGHT = screen_width - CHAT_WIDTH, screen_height
                    # Atualiza o display do pygame
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        env.zoom_in()  # Zoom in
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        env.zoom_out() # Zoom out
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Lida com eventos de clique do rato
                    mouse_pos = pygame.mouse.get_pos() # Posição do rato
                    if GAME_WIDTH < mouse_pos[0] < screen_width:
                        # Se o clique for na área do chat
                        if event.button == 4:
                            # Scroll da comunicação dos agentes para cima
                            chat_scroll = max(chat_scroll - 1, 0)
                        elif event.button == 5:
                            # Scroll da comunicação dos agentes para baixo
                            chat_scroll += 1
                    else:
                        if event.button == 1:
                            # Clique esquerdo
                            if pygame.time.get_ticks() - last_click_time < double_click_threshold:
                                env.zoom_in()
                            else:
                                dragging = True
                                prev_mouse_pos = pygame.mouse.get_pos()
                        last_click_time = pygame.time.get_ticks()
                        # Zoom in e zoom out com o scroll do rato
                        if event.button == 4:
                            # Scroll up
                            env.zoom_out()
                        elif event.button == 5:
                            # Scroll down
                            env.zoom_in()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = False
                        prev_mouse_pos = None

            # Lógica de deslocamento e zoom do ambiente
            if dragging:
                new_mouse_pos = pygame.mouse.get_pos()
                if prev_mouse_pos is not None:
                    delta_x = prev_mouse_pos[0] - new_mouse_pos[0] 
                    delta_y = prev_mouse_pos[1] - new_mouse_pos[1]
                    env.pan(delta_x, delta_y)
                prev_mouse_pos = new_mouse_pos

            screen.fill(greenback)

            # Desenha o display com o zoom e deslocamento
            cell_size = int(GAME_WIDTH // (SIZE * env.zoom_level))
            for x in range(SIZE):
                for y in range(SIZE):
                    draw_x = int((x * cell_size) - env.offset_x)
                    draw_y = int((y * cell_size) - env.offset_y)

                    if lanes_grid[x][y] is not None:
                        pygame.draw.rect(screen, lane_color, (draw_x, draw_y, cell_size, cell_size))
                    if intersections_grid[x][y] is not None:
                        pygame.draw.rect(screen, intersection_color, (draw_x, draw_y, cell_size, cell_size))

                    if traffic_lights_grid[x][y] is not None:
                        tl_id = traffic_lights_grid[x][y]
                        color = 'Red'
                        for tl in env.traffic_lights:   # Procura o semáforo com o id correspondente
                            if tl.id == tl_id:
                                color = tl.get_color()  # Obtém a cor do semáforo
                                break
                        pygame.draw.rect(screen, traffic_light_colors[color], (draw_x, draw_y, cell_size, cell_size)) # Desenha o semáforo com a cor correspondente

                    if emergency_grid[x][y] is not None and emergency_grid[x][y] == 1: 
                        pygame.draw.rect(screen, Emergency_color, (draw_x, draw_y, cell_size, cell_size)) # Desenha o local de socorrimento
                        
                    if vehicles_grid[x][y] is not None and vehicles_grid[x][y] != 0:
                        pygame.draw.ellipse(screen, car, (draw_x+2, draw_y+2, cell_size-5, cell_size-5)) # Desenha o veículo
                    
                    
                    if emergency_grid[x][y] is not None and emergency_grid[x][y] != 0 and emergency_grid[x][y] != 1:
                        # Desenha o veículo de emergência a piscar azul e vermelho
                        if siren == 0:
                            pygame.draw.ellipse(screen, Emergency_vehicle_grid_color_blue, (draw_x, draw_y, cell_size, cell_size))
                            siren = 1
                        else:
                            pygame.draw.ellipse(screen, RED, (draw_x, draw_y, cell_size, cell_size))
                            siren = 0
            
            # Desenha a área do chat
            pygame.draw.rect(screen, (255, 255, 255), (GAME_WIDTH, 0, CHAT_WIDTH, screen_height))

            # Desenha o cabeçalho do chat
            pygame.draw.rect(screen, (100, 100, 100), (GAME_WIDTH, 0, CHAT_WIDTH, 40))

            # Desenha a linha divisória entre o cabeçalho do chat e o corpo do chat
            pygame.draw.line(screen, (0, 0, 0), (GAME_WIDTH, 40), (GAME_WIDTH + CHAT_WIDTH, 40), 3)

            # Desenha a linha divisória entre o mapa e o chat
            pygame.draw.line(screen, (0, 0, 0), (GAME_WIDTH, 0), (GAME_WIDTH, GAME_HEIGHT), 3)

            y = 10
            current_scroll = chat_scroll
            text = font_heading.render("Inbox of Agents", True, (255,255,255))
            screen.blit(text, (GAME_WIDTH + 40, y))
            y+= 45
            # Desenha as mensagens recebidas pelos agentes
            for agent in message_dict:
                if current_scroll > 0:
                    current_scroll -= 1
                    continue
                text = font.render(agent, True, (0, 0, 0))
                screen.blit(text, (GAME_WIDTH + 30, y))

                # Desenha o icone do agente
                if agent.startswith("tlagent"):
                    pygame.draw.rect(screen, RED, pygame.Rect(GAME_WIDTH + 10, y, 10, 10))
                elif agent.startswith("vehicle"):
                    pygame.draw.circle(screen, BLACK, (GAME_WIDTH + 10 , y), 5)
                elif agent.startswith("emergencyvehicle"):
                    pygame.draw.circle(screen,Emergency_vehicle_grid_color_blue , (GAME_WIDTH + 10 , y), 8)
                elif agent.startswith("intersection"):
                    pygame.draw.rect(screen, BLACK, pygame.Rect(GAME_WIDTH + 10 , y, 10, 10))
                elif agent.startswith("centralcontrol"):
                    pygame.draw.rect(screen,Emergency_color, pygame.Rect(GAME_WIDTH + 10 , y, 10, 10))

                y += 26

                for message in message_dict[agent]:
                    if current_scroll > 0:
                        current_scroll -= 1
                        continue
                    if message != '' or message is not None:
                        text = font2.render(message, True, (0, 0, 0))
                        screen.blit(text, (GAME_WIDTH + 50, y))
                        y += 26
            
            # Desenha a linha divisória na posicao y
            pygame.draw.line(screen, (0, 0, 0), (GAME_WIDTH, y), (GAME_WIDTH + CHAT_WIDTH, y), 3)

            # Desenha o cabeçalho das estatísticas
            pygame.draw.rect(screen, (200, 200, 200), (GAME_WIDTH, y, CHAT_WIDTH, screen_height))
            y += 15

            # Desenha a linha divisória entre o chat e as estatísticas
            pygame.draw.line(screen, (0, 0, 0), (GAME_WIDTH, 0), (GAME_WIDTH, GAME_HEIGHT), 3)

            text = font_heading.render("Statistics", True, (0, 0, 0))
            screen.blit(text, (GAME_WIDTH + 10, y))
            y += 34
            text = font1.render(f"Average time stopped by a traffic light: {format(self.previous_media, '.3f')} s", True, (0, 0, 0))
            screen.blit(text, (GAME_WIDTH + 20, y))
            y += 26
            global analise_times
            text = font1.render(f"Waiting times of a vehicle(s) by a traffic light: {analise_times}", True, (0, 0, 0))
            screen.blit(text, (GAME_WIDTH + 20, y))
            y += 26
            text = font1.render(f"Maximum average time stopped by a traffic light: {format(self.maxTimeMedia, '.3f')} s", True, (0, 0, 0))
            screen.blit(text, (GAME_WIDTH + 20, y))
            y += 26
            text = font1.render(f"Number of seconds since the beggining: {clock}", True, (0, 0, 0))
            screen.blit(text, (GAME_WIDTH + 20, y))

            pygame.display.flip()
            await asyncio.sleep(0.1)

        pygame.quit()
    


class TrafficLight(Agent):
    # Inicialização do agente semáforo
    def __init__(self, id, intersection, colorfront, colorleft, road, cordX, cordY):
        Agent.__init__(self, id, "password")
        self.id = id
        self.colorfront = colorfront
        self.colorleft = colorleft
        self.intersection = intersection
        self.road = road
        self.cordX = cordX
        self.cordY = cordY
        self.map = Map()
        self.map.update_traffic_lights(cordX, cordY, id)


    async def setup(self):
        # Configuração inicial do agente TrafficLight
        b = self.TrafficLight(self, self.map)
        self.add_behaviour(b)
        await self.behaviours[0].run()


    class TrafficLight(CyclicBehaviour):
        def __init__(self, agent, map):
            super().__init__()
            self.agent = agent
            self.map = map


        async def receiveMessage(self):
            # Método para receber mensagens
            msg = await self.receive(timeout = 0.01) 
            if msg:
                print(f"Traffic light {self.agent.id} received the message with content: {msg.body} from {msg.sender}")
                message_dict[str(self.agent.id).lower()] = []
                message_dict[str(self.agent.id).lower()].append(f"{msg.body} from {msg.sender}") 
                waiting_times = eval(msg.body)
                return waiting_times
            else:
                return None


        async def send_score(self, score):
            # Método para enviar pontuações para a interseção
            receiver = self.agent.intersection.id
            msg = Message(to = receiver , sender = self.agent.id) 
            msg.set_metadata("performative", "inform")
            msg.body = str(score)
            # print(f"Sending score to {receiver} from {self.agent.id}")
            await self.send(msg)


        async def run(self):
            # Método principal do comportamento cíclico do semáforo
            while True:
                waiting_times = await self.receiveMessage()
                score={'points': 0, 'car_platoon': 0}
                if waiting_times is not None:
                    score = self.agent.heuristic(waiting_times)
                if (self.agent.get_color() == 'Red' or self.agent.get_color() == 'Yellow'): 
                    await self.send_score(score)
                await asyncio.sleep(1)


    def heuristic(self, waiting_times):
        # Função de heurística para calcular pontuações com base nos tempos de espera dos veículos
        points = 0
        sum = 0
        length = len(waiting_times)
        for i in range(len(waiting_times)):
            sum += waiting_times[i]       # Soma dos tempos de espera
        points = (3 * length) + (1 * sum) # Pontuação com base na soma dos tempos de espera e com um peso maior no número de veículos
        reactiontime = 2 * length         # Tempo de reação com base no número de veículos
        return {'points': points, 'car_platoon': reactiontime}
        

    def change(self, new_colorfront, new_colorleft):
        # Método para alterar as cores do semáforo
        self.colorfront = new_colorfront
        self.colorleft = new_colorleft


    def asking_to_change(self, waiting_time):
        # Método para decidir se o semáforo deve mudar com base no tempo de espera
        if self.colorfront == "Red":
            if waiting_time >= 4:
                self.waiting = True
                return True
        self.waiting = False
        return False
        

    def get_color(self):
        # Método para obter a cor atual do semáforo
        if self.colorfront == "Green":
            return "Green"
        elif self.colorfront == "Yellow":
            return "Yellow"
        else:
            return 'Red'



class Intersection(Agent):
    # Inicialização do agente interseção
    def __init__(self, name, road1, road2, road3, road4, x, y):
        Agent.__init__(self, name, "password")
        self.id = name
        self.road1 = road1
        self.road2 = road2
        self.road3 = road3
        self.road4 = road4
        self.tlights = [] # Lista para armazenar os semáforos associados à interseção
        self.scores= {'tf1': {'points': 0, 'car_platoon': 0}, 'tf2': {'points': 0, 'car_platoon': 0},
                      'tf3': {'points': 0, 'car_platoon': 0}, 'tf4': {'points': 0, 'car_platoon': 0}}
        self.x = x
        self.y = y
        self.map = Map()
        self.addcoord()


    def add_tlight(self, tlight):
        # Método para adicionar um semáforo à lista de semáforos
        self.tlights.append(tlight)


    def addcoord(self):
         # Método para atualizar as coordenadas da interseção no mapa
        for i in range(len(self.x)):
            self.map.update_intersections(self.x[i], self.y[i], self.name)


    def change(self, color1, color2):
        # Método para alterar as cores dos semáforos com base nas cores fornecidas
        if color1 == 'Green':
            color1left = 'Intermitent'
        elif color1 == 'Yellow':
            color1left = 'Yellow'
        else :
            color1left = 'Red'

        if color2 == 'Green':
            color2left = 'Intermitent'
        elif color2 == 'Yellow':
            color2left = 'Yellow'
        else :
            color2left = 'Red'
            
        for i in range(len(self.tlights)):
            if self.tlights[i].road == self.road1 or self.tlights[i].road == self.road3:
                self.tlights[i].change(color1, color1left)
                print(f"Traffic Light Agent {self.tlights[i].id}: Front: {color1}; Left: {color1left}")

            elif self.tlights[i].road == self.road2 or self.tlights[i].road == self.road4:
                self.tlights[i].change(color2, color2left)
                print(f"Traffic Light Agent {self.tlights[i].id}: Front: {color2}; Left: {color2left}")


    def askedChange(self):
        # Método para verificar se algum semáforo está à espera de mudar de cor
        for i in range(len(self.tlights)):
            if self.tlights[i].waiting == True:
                self.tlights[i].waiting = False
                return {'boolVal': True,'id': self.tlights[i].id}


    def find_tlight(self, id):
        # Método para encontrar um semáforo com base no id
        for i in range(len(self.tlights)):
            if str(self.tlights[i].id).lower() == str(id).lower():
                return self.tlights[i]


    def find_tlight_by_score(self, score):
        # Método para encontrar um semáforo com base na pontuação
        if score == 'tf1' and len(self.tlights) > 0 and self.road1 is not None: 
            tlight=self.find_tlight_by_road(self.road1.name)
            return tlight
        elif score == 'tf2' and len(self.tlights) > 1 and self.road2 is not None:
            tlight=self.find_tlight_by_road(self.road2.name)
            return tlight
        elif score == 'tf3' and len(self.tlights) > 2 and self.road3 is not None:
            tlight=self.find_tlight_by_road(self.road3.name)
            return tlight
        elif score == 'tf4' and len(self.tlights) > 3 and self.road4 is not None:
            tlight=self.find_tlight_by_road(self.road4.name)
            return tlight
        else:
            return None


    def find_tlight_by_road(self, road):
        # Método para encontrar um semáforo com base na estrada em que se encontra
        for tl in self.tlights:
            if str(tl.road.name).lower() == str(road).lower():
                return tl


    def tlight_with_more_points(self):
        # Método para encontrar o semáforo com mais pontos
        max_points = 0
        tlight_to_change = None
        reaction_time = 0
        for score in self.scores: # Procura o semáforo com mais pontos
            if self.scores[score]['points'] >= max_points:
                max_points = self.scores[score]['points']
                tlight_to_change = self.find_tlight_by_score(score)
                reaction_time = self.scores[score]['car_platoon']
        return {'tlight': tlight_to_change, 'reaction_time': reaction_time} # Retorna o semáforo com mais pontos


    def clear_scores(self):
        # Método para limpar as pontuações
        for score in self.scores:
            self.scores[score]['points'] = 0
            self.scores[score]['car_platoon'] = 0


    async def setup(self):
        # Configuração inicial do agente Intersection
        b = self.Intersection(self)
        self.add_behaviour(b)
        await self.behaviours[0].run()


    class Intersection(CyclicBehaviour):
        def __init__(self, agent):
            super().__init__()
            self.agent = agent
        

        async def change_by_tlight(self, tlight):
            # Método para alterar as cores dos semáforos com base no semáforo fornecido
            if tlight is not None:
                if tlight.road == self.agent.road1 or tlight.road == self.agent.road3:
                    if (tlight.colorfront == 'Yellow') and (tlight.colorleft == 'Yellow'):
                        self.agent.change('Red', 'Green')
                    
                    elif (tlight.colorfront == 'Red') and (tlight.colorleft == 'Intermitent'):
                        self.agent.change('Red', 'Yellow')
                        await asyncio.sleep(2)
                        self.agent.change('Green', 'Red')

                    elif (tlight.colorfront == 'Red') and (tlight.colorleft == 'Red'):
                        self.agent.change('Red', 'Yellow')
                        await asyncio.sleep(2)
                        self.agent.change('Green', 'Red')

                elif tlight.road == self.agent.road2 or tlight.road == self.agent.road4:
                    if (tlight.colorfront == 'Yellow') and (tlight.colorleft == 'Yellow'):
                        self.agent.change('Green', 'Red')
                    
                    elif (tlight.colorfront == 'Red') and (tlight.colorleft == 'Intermitent'):
                        self.agent.change('Yellow', 'Red')
                        await asyncio.sleep(2)
                        self.agent.change('Red', 'Green')

                    elif (tlight.colorfront == 'Red') and (tlight.colorleft == 'Red'):
                        self.agent.change('Yellow', 'Red')
                        await asyncio.sleep(2)
                        self.agent.change('Red', 'Green')


        async def receiveMessage(self):
            # Método para receber mensagens
            msg = await self.receive(timeout = 0.01)
            if msg:
                print(f"{self.agent.id} receive message from {msg.sender} with content: {msg.body} --")
                message_dict[str(self.agent.id).lower()].append(f"{msg.body} from {msg.sender}")
                scores = {'sender': msg.sender, 'body': eval(msg.body)}
                await self.arrange_scores(scores)
            else:
                pass
            

        async def arrange_scores(self, scores):
            # Método para organizar as pontuações recebidas
            tlight = self.agent.find_tlight(scores['sender'])
            if tlight is not None:
                if str(tlight.road.name).lower() == str(self.agent.road1.name).lower():
                    self.agent.scores['tf1']['points'] += scores['body']['points']
                    self.agent.scores['tf1']['car_platoon'] = max(self.agent.scores['tf1']['car_platoon'],scores['body']['car_platoon'])
                elif str(tlight.road.name).lower() == str(self.agent.road2.name).lower():
                    self.agent.scores['tf2']['points'] += scores['body']['points']
                    self.agent.scores['tf2']['car_platoon'] = max(self.agent.scores['tf2']['car_platoon'],scores['body']['car_platoon'])
                elif str(tlight.road.name).lower() == str(self.agent.road3.name).lower():
                    self.agent.scores['tf3']['points'] += scores['body']['points']
                    self.agent.scores['tf3']['car_platoon'] = max(self.agent.scores['tf3']['car_platoon'],scores['body']['car_platoon'])
                elif str(tlight.road.name).lower() == str(self.agent.road4.name).lower():
                    self.agent.scores['tf4']['points'] += scores['body']['points']
                    self.agent.scores['tf4']['car_platoon'] = max(self.agent.scores['tf4']['car_platoon'],scores['body']['car_platoon'])
            #await self.print_scores()
                    

        async def print_scores(self):
            # Método para imprimir as pontuações
            print("+---------------------------------------------+")
            print(f"| {self.agent.road1.name} | {self.agent.road2.name}              |")
            print(f"| {self.agent.id} Scores:                  |")
            for road in self.agent.scores:
                print(f"|Road {road}: {self.agent.scores[road]['points']} points                           |")
            print("+---------------------------------------------+")


        async def run(self):
            # Método principal do comportamento cíclico da interseção
            time = 0 
            while True:
                if time == 0:
                    message_dict[str(self.agent.id).lower()]=[]
                await self.receiveMessage()
                await self.receiveMessage()
                await self.receiveMessage()
                await self.receiveMessage()
                if (time > 0):
                    time -= 1
                    self.agent.clear_scores()
                    await asyncio.sleep(1)
                    continue
                tlight_to_change = None
                tlight_to_change = self.agent.tlight_with_more_points()
                if tlight_to_change is not None and tlight_to_change['tlight'] is not None:
                    time = tlight_to_change['reaction_time']
                    if (time > 10):
                        time = 10
                    tlight_to_change = tlight_to_change['tlight']
                    await self.change_by_tlight(tlight_to_change)
                    self.agent.clear_scores()
                    continue
                else:
                    pass
                await asyncio.sleep(1)



class Car(Agent):
    # Inicialização do agente veículo
    def __init__(self, car_id, x, y):
        Agent.__init__(self, car_id, "password")
        self.car_id = car_id
        self.x = x
        self.y = y
        self.map = Map()
        self.map.update_vehicles(x, y, car_id)


    async def setup(self):
        # Configuração inicial do agente Car
        class CarInteraction(CyclicBehaviour):
            def __init__(self, agent, msg, map):
                super().__init__()
                self.agent = agent
                self.msg = msg
                self.map = map
                self.car_id = agent.car_id
                self.set_agent(agent)


            def move(self, x, y):
                # Método para atualizar a posição do veículo no mapa
                self.agent.x = int(x)
                self.agent.y = int(y)
                self.agent.map.update_vehicles(self.agent.x, self.agent.y, self.car_id)


            def travel(self):
                # Método para calcular o próximo movimento do veículo (escolha aleatória)
                whatsnextlanes = self.map.WhatsNextLane(self.agent.x, self.agent.y)
                if whatsnextlanes is not None:
                    nextmove = random.choice(whatsnextlanes)
                    return nextmove
                return None


            def IsThereTrafficLight(self, nextmove):
                # Método para verificar se há um semáforo na próxima posição
                if self.map.IsThereTrafficLight(nextmove[0], nextmove[1]) is not False:
                    tl_id = self.map.IsThereTrafficLight(nextmove[0], nextmove[1])
                    for tl in env.traffic_lights:
                        if tl.id == tl_id:
                            if tl.get_color() == 'Red':
                                # Se o semáforo estiver vermelho, o carro espera
                                while tl.get_color() == 'Red':
                                    return {'isThere': True, 'id': tl.id}
                                break
                            elif tl.get_color() == 'Yellow':
                                # Se o semáforo estiver amarelo, o carro espera
                                while tl.get_color() == 'Yellow':
                                    return {'isThere': True, 'id': tl.id}
                                break
                            else:
                                # Se o semáforo estiver verde, o carro passa
                                return {'isThere': False, 'id': tl.id}
                            

            def IsThereCarRight(self, nextmove):
                # # Método para verificar se há um carro à direita do próximo movimento
                vector = (nextmove[0] - self.agent.x, nextmove[1] - self.agent.y)
                newxplus = nextmove[0] + 1
                newyplus = nextmove[1] + 1
                newxminus = nextmove[0] - 1
                newyminus = nextmove[1] - 1

                # Determina a direção do movimento com base no vetor
                if vector == (0, 1):
                    # a ir para cima (mas visualmente para baixo)
                    if (newxminus < 0): return False
                    if self.map.IsThereCar(nextmove[0] - 1, nextmove[1]) is not False and self.map.isThereEmergency(nextmove[0] - 1, nextmove[1]) is not False:
                        return True
                elif vector == (0, -1):
                    # a ir para baixo (mas visualmente para cima)
                    if (newxplus >= SIZE): return False
                    if self.map.IsThereCar(nextmove[0] + 1, nextmove[1]) is not False and self.map.isThereEmergency(nextmove[0] + 1, nextmove[1]) is not False:
                        return True
                elif vector == (1, 0):
                    # a ir para a direita
                    if (newyplus >= SIZE): return False
                    if self.map.IsThereCar(nextmove[0], nextmove[1] + 1) is not False and self.map.isThereEmergency(nextmove[0], nextmove[1] + 1) is not False:
                        return True
                elif vector == (-1, 0):
                    # ir para a esquerda
                    if (newyminus < 0): return False
                    if self.map.IsThereCar(nextmove[0], nextmove[1] - 1) is not False and self.map.isThereEmergency(nextmove[0], nextmove[1] - 1) is not False:
                        return True    

                # Verifica se há um carro na posição do próximo movimento
                if self.map.IsThereCar(nextmove[0], nextmove[1]) is not False:
                    return True
                return False
            
            
            async def run(self):
                # Método principal do comportamento cíclico do veículo
                waiting_time = 0
                while True:
                    nextmove = self.travel()
                    if nextmove is not None:
                        is_there_traffic_light = self.IsThereTrafficLight(nextmove)
                        if is_there_traffic_light is not None and is_there_traffic_light['isThere'] is not True or is_there_traffic_light is None:
                            if self.map.IsThereCar(nextmove[0], nextmove[1]) == False and self.map.isThereEmergency(nextmove[0], nextmove[1]) == False:
                                waiting_time = 0
                                if self.IsThereCarRight(nextmove) is not True:
                                    pastx = self.agent.x
                                    pasty = self.agent.y
                                    self.move(nextmove[0], nextmove[1])
                                    self.map.update_vehicles(pastx, pasty, 0)
                                    await asyncio.sleep(1)
                                    continue
                                else:
                                    # Carro espera que o carro à direita se mova
                                    #print(f"Car {self.car_id} is waiting for the car(s) passing by")
                                    await asyncio.sleep(1)
                                    continue
                            elif self.map.IsThereCar(nextmove[0], nextmove[1]) is not False or self.map.isThereEmergency(nextmove[0], nextmove[1]) is not False:
                                waiting_time += 1
                                carAhead = self.map.IsThereCar(nextmove[0], nextmove[1])
                                #print(f"Car {self.agent.car_id} is waiting for the car {carAhead} to move")
                                if carAhead is not False:
                                    await self.reporting_waiting_time(waiting_time, carAhead)
                                #print(f"Car {self.car_id} is waiting for the car in front to move")
                                await asyncio.sleep(1)
                                continue
                        elif is_there_traffic_light is not None and is_there_traffic_light['isThere'] is True:
                            # Carro espera pelo semáforo mudar de cor para passar
                            #print(f"Car {self.car_id} is waiting for the traffic light to change")
                            waiting_time += 1
                            await self.reporting_waiting_time(waiting_time, is_there_traffic_light['id'])
                            await asyncio.sleep(1)
                            continue
                    else:
                        # Aguarda quando não é encontrado um caminho 
                        #print(f"No road finded, car {self.agent.car_id} is waiting")
                        await asyncio.sleep(1)
                        continue


            async def receiveMessage(self):
                # Método para receber mensagens
                msg = await self.receive(timeout = 0.01) 
                if msg:
                    print(f"{self.agent.car_id} received a message with content: {msg.body} from {msg.sender}")
                    message_dict[str(self.agent.car_id).lower()]=[]
                    message_dict[str(self.agent.car_id).lower()].append(f"{msg.body} from {msg.sender}")
                    mensagem = eval(msg.body)
                    return mensagem
                else:
                    return None

                
            async def reporting_waiting_time(self, waiting_time, agentDestination):
                # Método para enviar o tempo de espera para o agente de destino
                global analise_times
                msg = Message(to = agentDestination, sender = self.car_id)
                previous_cars = await self.receiveMessage()
                if previous_cars is not None:
                    previous_cars.append(waiting_time)
                else:
                    previous_cars = []
                    previous_cars.append(waiting_time)
                if (agentDestination.startswith("TLAgent")):
                    for element in previous_cars:
                        analise_times.append(element)
                    
                msg.set_metadata("performative", "inform")
                msg.body = str(previous_cars)
                #print(str(msg.sender) + " ->->->->->->->->-> " + str(msg.to) + "   Body: " + str(msg.body))
                await self.send(msg)
 
        # Adiciona o comportamento ao agente
        self.add_behaviour(CarInteraction(self, None, self.map))
        await self.behaviours[0].run()



class EmergencyVehicle(Agent):
    # Inicialização do agente veículo de emergência
    def __init__(self, id, x, y):
        Agent.__init__(self, id, "password")
        self.id = id
        self.x = x
        self.y = y
        self.map = Map()
        self.map.update_emergency(x, y, id)


    def move(self, x, y):
        # Atualiza a posição do veículo de emergência no mapa
        self.map.update_emergency(self.x, self.y, 0)
        self.x = x
        self.y = y
        self.map.update_emergency(self.x, self.y, self.id)


    def IsThereTrafficLight(self, nextmove):
        # Verifica se há um semáforo na próxima posição
        if self.map.IsThereTrafficLight(nextmove[0], nextmove[1]) is not False:
            # check if there is a traffic light in the next position
            tl_id = self.map.IsThereTrafficLight(nextmove[0], nextmove[1])
            for tl in env.traffic_lights:
                if tl.id == tl_id:
                    if tl.get_color() == 'Red':
                        return True
                    elif tl.get_color() == 'Yellow':
                        return True
                    else:
                        return False


    def isThereCarRight(self, nextmove):
        # Verifica se há um carro à direita do próximo movimento
        vector = (nextmove[0] - self.x, nextmove[1] - self.y)
        newxplus = nextmove[0] + 1
        newyplus = nextmove[1] + 1
        newxminus = nextmove[0] - 1
        newyminus = nextmove[1] - 1

        if vector == (0, 1):
            # a ir para cima (mas visualmente para baixo)
            if (newxminus < 0): return False
            if self.map.IsThereCar(nextmove[0] - 1, nextmove[1]) is not False and self.map.isThereEmergency(nextmove[0] - 1, nextmove[1]) is not False:
                return True
        elif vector == (0, -1):
            # a ir para baixo (mas visualmente para cima)
            if (newxplus >= SIZE): return False
            if self.map.IsThereCar(nextmove[0] + 1, nextmove[1]) is not False and self.map.isThereEmergency(nextmove[0] + 1, nextmove[1]) is not False:
                return True
        elif vector == (1, 0):
            # a ir para a direita
            if (newyplus >= SIZE): return False
            if self.map.IsThereCar(nextmove[0], nextmove[1] + 1) is not False and self.map.isThereEmergency(nextmove[0], nextmove[1] + 1) is not False:
                return True
        elif vector == (-1, 0):
            # ir para a esquerda
            if (newyminus < 0): return False
            if self.map.IsThereCar(nextmove[0], nextmove[1] - 1) is not False and self.map.isThereEmergency(nextmove[0], nextmove[1] - 1) is not False:
                return True
        
        # Verifica se há um carro na próxima posição e se há uma emergência      
        if self.map.IsThereCar(nextmove[0], nextmove[1]) is not False and self.map.isThereEmergency(nextmove[0], nextmove[1]) is not False:
            return True
        return False
    

    def emergency_call(self):
        # Gera uma chamada de emergência em uma posição aleatória
        x = random.randint(0, SIZE-1)
        y = random.randint(0, SIZE-1)
        while lanes_grid[x][y] is None:
            x = random.randint(0, SIZE-1)
            y = random.randint(0, SIZE-1)
        self.map.update_emergency(x, y, 1)
        return (x, y)


    async def setup(self):
        # Configuração inicial do agente EmergencyVehicle
        b = self.EmergencyInteraction(self, env.central_control.id)
        self.add_behaviour(b)
        await self.behaviours[0].run()

    
    class EmergencyInteraction(CyclicBehaviour):
        def __init__(self, agent, central_control):
            super().__init__()
            self.agent = agent
            self.central_control = central_control


        async def send_route(self, route):
            # Envia a rota para o agente de controle central
            receiver = str(self.central_control)
            msg = Message(to = receiver , sender = self.agent.id)
            msg.set_metadata("performative", "inform")
            msg.body = str(route)
            #print(f"Sending route to {receiver} from {self.agent.id}")
            await self.send(msg)


        async def send_position(self):
            # Envia a posição atual para o agente de controle central
            receiver = str(self.central_control)
            msg = Message(to = receiver , sender = self.agent.id)
            msg.set_metadata("performative", "inform")
            msg.body = str((self.agent.x, self.agent.y))
            #print(f"Sending position to {receiver} from {self.agent.id}")
            await self.send(msg)


        async def run(self):
            # Método principal do comportamento cíclico do veículo de emergência
            flag = 0
            route = []
            while True:
                await asyncio.sleep(0.5)
                if flag == 0:
                    x, y = self.agent.emergency_call()
                    print ( f"Emergency at {x}, {y}. Emergency Vehicle {self.agent.id} dispatched")
                    if x is not None and y is not None:
                        print (f"planning route to {x}, {y}")
                        route = []
                        route = self.agent.map.route_greedy(self.agent.x, self.agent.y, x, y)
                        print ("planning complete")
                        flag = 1
                        await self.send_route(route)
                    x, y = None, None
                if flag == 1:
                    pen=0
                    i = 1
                    while i < len(route):
                        if pen==1:
                            pen=0
                            i -= 1
                        newx = route[i][0]
                        newy = route[i][1]
                        if (i + 1) < len(route):
                            nextPosition = (route[i][0], route[i][1])
                            tlightahead = not self.agent.IsThereTrafficLight(nextPosition)
                        else :
                            tlightahead = True
                        if self.agent.map.IsThereCar(newx, newy) is False and self.agent.map.isThereEmergency(newx, newy) is False and self.agent.isThereCarRight(route[i]) is False and tlightahead is True:
                            self.agent.move(newx, newy)
                            await self.send_position()
                            await asyncio.sleep(0.5)
                        else:
                            await self.send_position()
                            await asyncio.sleep(1)
                            pen=1
                        i += 1
                    flag = 0                        
                print (f"Emergency Vehicle {self.agent.id} arrived at the destination to help")
                await asyncio.sleep(1)



class CentralControl(Agent):
    # Inicialização do agente de controle central
    def __init__(self, id):
        Agent.__init__(self, id, "password")
        self.id = id
        self.map = Map()
  

    async def setup(self):
        # Configuração inicial do agente CentralControl
        b = self.CentralControlInteraction(self)
        self.add_behaviour(b)
        await self.behaviours[0].run()


    class CentralControlInteraction(CyclicBehaviour):
        def __init__(self, agent):
            super().__init__()
            self.agent = agent


        async def receiveMessage(self):
            # Método para receber mensagens
            msg = await self.receive(timeout = 0.1)
            if msg:
                print(f"Central Control {self.agent.id} received a message with content: {msg.body}")
                message_dict[str(self.agent.id).lower()] = []
                message_dict[str(self.agent.id).lower()].append(f"{msg.body} from {msg.sender}")
                mensagem = eval(msg.body)
                return mensagem
            else:
                return None


        async def receive_position(self):
            # Método para receber a posição atual do veículo de emergência
            msg = await self.receive(timeout = 0.1)
            if msg:
                print(f"Central Control {self.agent.id} received a message with content: {msg.body} from {msg.sender}")
                message_dict[str(self.agent.id).lower()] = []
                message_dict[str(self.agent.id).lower()].append(f"{msg.body} from {msg.sender}")
                mensagem = eval(msg.body)
                return mensagem
            else:
                return None


        async def alert_TLight(self, tlight, distance):
            # Método para alertar o semáforo mais próximo do veículo de emergência
            msg = Message(to = tlight, sender = self.agent.id)
            msg.set_metadata("performative", "inform")
            toSend = [100, 100, 100, 100] # 100 é o valor máximo, então se o semáforo receber 100, não mudará de cor
            for _ in range(distance):
                toSend[0] += 100 
            msg.body = str(toSend)
            await self.send(msg)


        async def run(self):
            # Método principal do comportamento cíclico do agente de controle central
            while True:
                # aguarda a receção de uma rota
                route = await self.receiveMessage()
                if route is not None:
                    i = 1
                    while i < len(route):
                        if isinstance(route[i], (list, tuple)) and len(route[i]) >= 2:
                            x = route[i][0]
                            y = route[i][1]
                            # Recebe a posição do veículo de emergência e verifica se está perto de um semáforo
                            position = await self.receive_position()
                            if self.agent.map.IsThereTrafficLight(x, y) is not None:
                                if position is not None:
                                    if position[0] == x and position[1] == y:
                                        i += 1
                                        continue
                                    # A distância é igual ao número de índices entre o veículo de emergência e o semáforo, então encontre o índice do semáforo na rota menos a posição do veículo de emergência
                                    try:
                                        distance =  route.index((x, y)) - route.index(position)
                                    except ValueError:
                                        print(f"Position {position} not found in route")
                                        distance = 8
                                    # Se a distância for menor ou igual a 8, o veículo de emergência está perto do semáforo, então alerte o semáforo
                                    if distance <= 8:
                                        tl_id = self.agent.map.IsThereTrafficLight(x, y)
                                        if tl_id is not None:
                                            await self.alert_TLight(tl_id, 8 - distance)
                                    
                                    await asyncio.sleep(0.5)
                                    continue
                                continue
                                #print(f" --------- Central Control {self.agent.id} found a traffic light {tl_id} at {x}, {y}")
                            i += 1
                        else:
                            break
                await asyncio.sleep(0.4)
                    


class Lane:
    def __init__(self, lane_id):
        # Inicialização de uma faixa de trânsito
        self.lane_id = lane_id
        self.cars = [] # lista de carros na faixa de trânsito
        self.lane = [] # lista de coordenadas da faixa de trânsito
        self.map = Map()


    def add_car(self, car):
        # Adiciona um carro à faixa de trânsito
        self.cars.append(car)


    def add_lane(self, *args):
        # Adiciona coordenadas à faixa de trânsito
        for lane_coord in args:
            self.lane.append(lane_coord)
            x, y = lane_coord
            self.map.update_lanes(x, y, self.lane_id)


    def next_position(self, x, y):
        # Retorna a próxima posição na faixa de trânsito com base na posição atual
        for i in range(len(self.lane)):
            if int(self.lane[i][0]) == int(x) and int(self.lane[i][1]) == int(y):
                if (i + 1) == len(self.lane):
                    return None
                lanes = self.lane[i + 1]
                return lanes



class Road:
    def __init__(self, name, num_lanes):
        # Inicialização de uma estrada
        self.name = name
        self.lanes = [Lane(i) for i in range(num_lanes)]
        self.map = Map()


    def add_lane(self, lane):
        # Adiciona uma faixa de trânsito à estrada
        self.lanes.append(lane)



class Environment:
    def __init__(self):
        # Inicialização do ambiente
        self.zoom_level = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # Inicialização das estradas
        road_1 = Road("Road_1", 2)
        road_2 = Road("Road_2", 2)
        road_3 = Road("Road_3", 2)
        road_4 = Road("Road_4", 2)
        road_5 = Road("Road_5", 2)
        road_6 = Road("Road_6", 2)
        road_7 = Road("Road_7", 2)

        # Inicialização das faixas de trânsito
        lane1 = Lane(1)
        lane2 = Lane(2)
        lane3 = Lane(3)
        lane4 = Lane(4)
        lane5 = Lane(5)
        lane6 = Lane(6)
        lane7 = Lane(7)
        lane8 = Lane(8)
        lane9 = Lane(9)
        lane10 = Lane(10)
        lane11 = Lane(11)
        lane12 = Lane(12)
        lane13 = Lane(13)
        lane14 = Lane(14)


        lane1.add_lane((5,7), (6,7), (6,6), (6,5), (6,4), (6,3), (6,2), (6,1), (6,0), (5,0), (4,0), (3,0), (2,0), (1,0), (0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9), (0,10), (0,11), (0,12), (0,13), (0,14), (0,15), (0,16), (0,17), (1,17), (2,17), (3,17), (4,17), (5,17), (6,17), (6,16))
        lane2.add_lane((6,16), (5,16), (4,16), (3,16), (2,16), (1,16), (1,15), (1,14), (1,13), (1,12), (1,11), (1,10), (1,9), (1,8), (1,7), (1,6), (1,5), (1,4), (1,3), (1,2), (1,1), (2,1), (3,1), (4,1), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7))

        lane3.add_lane((13,7), (13,6), (12,6), (11,6), (10,6), (9,6), (8,6), (7,6), (6,6), (5,6), (5,7))
        lane4.add_lane((5,6), (5,7), (6,7), (7,7), (8,7), (9,7),(10,7), (11,7), (12,7), (13,7))

        lane5.add_lane((28, 12), (29, 12), (29, 11), (29, 10), (29, 9), (29, 8), (29, 7), (29, 6), (29, 5), (29, 4), (29, 3), (29, 2), (29, 1), (29, 0), (28, 0), (27, 0), (26, 0), (25, 0), (24, 0), (23, 0), (22, 0), (21, 0), (20, 0), (19, 0), (18, 0), (17, 0), (16, 0), (15, 0), (14, 0), (13, 0), (12, 0), (12, 1), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (13, 12), (14, 12), (15, 12), (16, 12), (17, 12), (18, 12), (19, 12))
        lane6.add_lane((19,12), (19,11), (18,11), (17,11), (16,11), (15,11), (14,11), (13,11), (13,10), (13,9), (13,8), (13,7), (13,6), (13,5), (13,4), (13,3), (13,2), (13,1), (14,1), (15,1), (16,1), (17,1), (18,1), (19,1), (20,1), (21,1), (22,1), (23,1), (24,1), (25,1), (26,1), (27,1), (28,1), (28,2), (28,3), (28,4), (28,5), (28,6), (28,7), (28,8), (28,9), (28,10), (28,11), (28,12))

        lane7.add_lane((29, 11), (28, 11), (27, 11), (26, 11), (25, 11), (24, 11), (23, 11), (22, 11), (21, 11), (20, 11), (19, 11), (18, 11))
        lane8.add_lane((18,11), (18,12), (19,12), (20,12), (21,12), (22,12), (23,12), (24,12), (25,12), (26,12), (27,12), (28,12), (29,12), (29,11))

        lane9.add_lane((5,17), (6,17), (6,16), (6,15), (6,14), (6,13), (6,12), (6,11), (6,10), (6,9), (6,8), (6,7), (6,6), (5,6))
        lane10.add_lane((5,6), (5,7), (5,8), (5,9), (5,10), (5,11), (5,12), (5,13), (5,14), (5,15), (5,16), (5,17))

        lane11.add_lane((19, 11), (18, 11), (18, 12), (18, 13), (18, 14), (18, 15), (18, 16), (17, 16), (16, 16), (15, 16), (14, 16), (13, 16), (12, 16), (11, 16), (10, 16), (9, 16), (8, 16), (7, 16), (6, 16), (5, 16), (5, 17))
        lane12.add_lane((5,17), (6,17), (7,17), (8,17), (9,17), (10,17), (11,17), (12,17), (13,17), (14,17), (15,17), (16,17), (17,17), (18,17), (19,17), (19,16), (19,15), (19,14), (19,13), (19,12), (19,11))

        lane13.add_lane((29, 11), (28, 11), (28, 12), (28, 13), (28, 14), (28, 15), (28, 16), (28, 17), (28, 18), (28, 19), (28, 20), (28, 21), (28, 22), (28, 23), (28, 24), (28, 25), (28, 26), (28, 27), (27, 27), (26, 27), (25, 27), (24, 27), (23, 27), (22, 27), (21, 27), (20, 27), (19, 27), (18, 27), (17, 27), (16, 27), (15, 27), (14, 27), (13, 27), (12, 27), (11, 27), (10, 27), (9, 27), (8, 27), (7, 27), (6, 27), (6, 26), (6, 25), (6, 24), (6, 23), (6, 22), (6, 21), (6, 20), (6, 19), (6, 18), (6, 17), (6, 16), (5, 16))
        lane14.add_lane((5,16), (5,17), (5,18), (5,19), (5,20), (5,21), (5,22), (5,23), (5,24), (5,25), (5,26), (5,27), (5,28), (6,28), (7,28), (8,28), (9,28), (10,28), (11,28), (12,28), (13,28), (14,28), (15,28), (16,28), (17,28), (18,28), (19,28), (20,28), (21,28), (22,28), (23,28), (24,28), (25,28), (26,28), (27,28), (28,28), (29,28), (29,27), (29,26), (29,25), (29,24), (29,23), (29,22), (29,21), (29,20), (29,19), (29,18), (29,17), (29,16), (29,15), (29,14), (29,13), (29,12), (29,11))

        road_1.add_lane(lane1)
        road_1.add_lane(lane2)
        road_2.add_lane(lane3)
        road_2.add_lane(lane4)
        road_3.add_lane(lane5)
        road_3.add_lane(lane6)
        road_4.add_lane(lane7)
        road_4.add_lane(lane8)
        road_5.add_lane(lane9)
        road_5.add_lane(lane10)
        road_6.add_lane(lane11)
        road_6.add_lane(lane12)
        road_7.add_lane(lane13)
        road_7.add_lane(lane14)

        # Inicialização das interseções
        intersection_1 = Intersection("Intersection_1@localhost", road_1, road_2, road_5, None, (5, 5, 6, 6), (6, 7, 6, 7))
        intersection_2 = Intersection("Intersection_2@localhost", road_2, road_3, None, None, (12, 12, 13, 13), (6, 7, 6, 7))
        intersection_3 = Intersection("Intersection_3@localhost", road_1, road_5, road_6, road_7, (5, 5, 6, 6), (16, 17, 16, 17))
        intersection_4 = Intersection("Intersection_4@localhost", road_3, road_6, road_4, None, (18, 18, 19, 19), (11, 12, 11, 12))
        intersection_5 = Intersection("Intersection_5@localhost", road_3, road_4, road_7, None, (28, 28, 29, 29), (11, 12, 11, 12))

        self.roads = [road_1, road_2, road_3, road_4, road_5, road_6, road_7]

        self.intersections = [intersection_1, intersection_2, intersection_3, intersection_4, intersection_5]

        self.lanes = [lane1, lane2, lane3, lane4, lane5, lane6, lane7, lane8, lane9, lane10, lane11, lane12, lane13, lane14]

        # Inicialização dos semáforos
        trafficLight1 = TrafficLight("TLAgent-1@localhost", intersection_1, 'Green', 'Intermitent', road_1, 5, 5)
        trafficLight2 = TrafficLight("TLAgent-2@localhost", intersection_1, 'Red', 'Intermitent', road_2, 7, 6)
        trafficLight3 = TrafficLight("TLAgent-3@localhost", intersection_1, 'Green', 'Intermitent', road_5, 6, 8)
        trafficLight4 = TrafficLight("TLAgent-4@localhost", intersection_2, 'Red', 'Intermitent', road_2, 11, 7)
        trafficLight5 = TrafficLight("TLAgent-5@localhost", intersection_2, 'Green', 'Intermitent', road_3, 12, 5)
        trafficLight6 = TrafficLight("TLAgent-6@localhost", intersection_2, 'Green', 'Intermitent', road_3, 13, 8)
        trafficLight7 = TrafficLight("TLAgent-7@localhost", intersection_3, 'Red', 'Intermitent', road_1, 4, 17)
        trafficLight8 = TrafficLight("TLAgent-8@localhost", intersection_3, 'Green', 'Intermitent', road_5, 5, 15)
        trafficLight9 = TrafficLight("TLAgent-9@localhost", intersection_3, 'Red', 'Intermitent', road_6, 7, 16)
        trafficLight10 = TrafficLight("TLAgent-10@localhost", intersection_3, 'Green', 'Intermitent', road_7, 6, 18)
        trafficLight11 = TrafficLight("TLAgent-11@localhost", intersection_4, 'Green', 'Intermitent', road_3, 17, 12)
        trafficLight12 = TrafficLight("TLAgent-12@localhost", intersection_4, 'Red', 'Intermitent', road_6, 19, 13)
        trafficLight13 = TrafficLight("TLAgent-13@localhost", intersection_4, 'Green', 'Intermitent', road_4, 20, 11)
        trafficLight14 = TrafficLight("TLAgent-14@localhost", intersection_5, 'Green', 'Intermitent', road_4, 27, 12)
        trafficLight15 = TrafficLight("TLAgent-15@localhost", intersection_5, 'Red', 'Intermitent', road_3, 28, 10)
        trafficLight16 = TrafficLight("TLAgent-16@localhost", intersection_5, 'Red', 'Intermitent', road_7, 29, 13)

        intersection_1.add_tlight(trafficLight1)
        intersection_1.add_tlight(trafficLight2)
        intersection_1.add_tlight(trafficLight3)
        intersection_2.add_tlight(trafficLight4)
        intersection_2.add_tlight(trafficLight5)
        intersection_2.add_tlight(trafficLight6)
        intersection_3.add_tlight(trafficLight7)
        intersection_3.add_tlight(trafficLight8)
        intersection_3.add_tlight(trafficLight9)
        intersection_3.add_tlight(trafficLight10)
        intersection_4.add_tlight(trafficLight11)
        intersection_4.add_tlight(trafficLight12)
        intersection_4.add_tlight(trafficLight13)
        intersection_5.add_tlight(trafficLight14)
        intersection_5.add_tlight(trafficLight15)
        intersection_5.add_tlight(trafficLight16)

        self.traffic_lights = [trafficLight1, trafficLight2, trafficLight3, trafficLight4, trafficLight5, trafficLight6, trafficLight7, trafficLight8, trafficLight9, trafficLight10, trafficLight11, trafficLight12, trafficLight13, trafficLight14, trafficLight15, trafficLight16]

        # Inicialização dos veículos
        self.car1 = Car("Vehicle-1@localhost", 0, 0)
        self.car2 = Car("Vehicle-2@localhost", 2, 1)
        self.car3 = Car("Vehicle-3@localhost", 5, 4)
        self.car4 = Car("Vehicle-4@localhost", 28, 13)
        self.car5 = Car("Vehicle-5@localhost", 29, 5)
        self.car6 = Car("Vehicle-6@localhost", 6, 9)
        self.car7 = Car("Vehicle-7@localhost", 13, 16)
        self.car8 = Car("Vehicle-8@localhost", 28, 3)
        self.car9 = Car("Vehicle-9@localhost", 6, 24)
        self.car10 = Car("Vehicle-10@localhost", 5, 28)
        self.car11 = Car("Vehicle-11@localhost", 12, 10)
        self.car12 = Car("Vehicle-12@localhost", 13, 2)
        self.car13 = Car("Vehicle-13@localhost", 20, 0)
        self.car14 = Car("Vehicle-14@localhost", 27, 1)
        self.car15 = Car("Vehicle-15@localhost", 6, 20)
        self.car16 = Car("Vehicle-16@localhost", 5, 2)
        self.car17 = Car("Vehicle-17@localhost", 0, 17)
        self.car18 = Car("Vehicle-18@localhost", 11, 16)
        self.car19 = Car("Vehicle-19@localhost", 24, 11)
        self.car20 = Car("Vehicle-20@localhost", 27, 12)

        self.cars = [self.car1, self.car2, self.car3, self.car4, self.car5, self.car6, self.car7, self.car8, self.car9, self.car10,self.car11, self.car12, self.car13, self.car14, self.car15, self.car16, self.car17, self.car18, self.car19, self.car20]
        
        # Inicialização do agente de controle central
        self.central_control = CentralControl("CentralControl@localhost")

        # Inicialização do veículo de emergência
        self.emergency1 = EmergencyVehicle("EmergencyVehicle-1@localhost", 18,11)

        self.emergency_vehicles = [self.emergency1]

        self.map = Map()

        self.create_message()

    # Método para criar uma mensagem
    def create_message(self):
        message_dict[str(self.central_control.id).lower()].append('')
        
        for intersection in self.intersections:
            message_dict[str(intersection.id).lower()].append('')

        for tlight in self.traffic_lights:
            message_dict[str(tlight.id).lower()].append('')

        for car in self.cars:
            message_dict[str(car.car_id).lower()].append('')
        
        for emergency in self.emergency_vehicles:
            message_dict[str(emergency.id).lower()].append('')
    

    # Método para aumentar o zoom do ambiente
    def zoom_in(self):
        self.zoom_level *= 1.1


    # Método para diminuir o zoom do ambiente
    def zoom_out(self):
        self.zoom_level /= 1.1

    # Método para mover o ambiente
    def pan(self, delta_x, delta_y):
        self.offset_x += delta_x
        self.offset_y += delta_y

    # Método para adicionar uma estrada
    def add_road(self, road):
        self.roads.append(road)

    # Método para adicionar uma interseção
    def add_intersection(self, intersection):
        self.intersections.append(intersection)


    # Método para exibir o ambiente
    def display(self):
        for road in self.roads:
            print(f"{road.name}: ", end='')
            for lane in road.lanes:
                print(f" Lane {lane.lane_id}", end='')
            print()

        print("Intersections: ")
        for intersection in self.intersections:
            print(f"{intersection.name} - Traffic Light: ", end='')
            for tlight in intersection.tlights:
                print(f"{tlight.id} ", end='')
            print()


if __name__ == "__main__":
    env = Environment()
    env.display()


    async def main():
        simulation_task = asyncio.create_task(env.map.draw_map())
        analysis_task = asyncio.create_task(env.map.statiscs())

        await asyncio.gather(*[ agent.start() for agent in env.cars ],*[intersection.start() for intersection in env.intersections], *[tlight.start() for tlight in env.traffic_lights],env.central_control.start(), *[emergencyV.start() for emergencyV in env.emergency_vehicles ] , simulation_task, analysis_task)
        await spade.wait_until_finished(*[ agent for agent in env.cars ])
    spade.run(main())

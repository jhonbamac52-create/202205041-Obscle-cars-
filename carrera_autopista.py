import pygame
import random
import math

pygame.init()

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
ANCHO = 900
ALTO = 600

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Turbo Highway")

reloj = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (15, 15, 20)
GRIS = (70, 70, 75)
GRIS_CLARO = (120, 120, 125)
VERDE = (30, 150, 70)
ROJO = (220, 50, 50)
AZUL = (40, 120, 255)
AMARILLO = (255, 210, 30)
NARANJA = (255, 130, 20)
MORADO = (150, 70, 220)

# Fuentes
fuente_grande = pygame.font.SysFont("Arial", 55, bold=True)
fuente = pygame.font.SysFont("Arial", 30, bold=True)
fuente_pequena = pygame.font.SysFont("Arial", 22)

# -----------------------------
# VARIABLES DE LA CARRETERA
# -----------------------------

ANCHO_CARRETERA = 600
X_CARRETERA = (ANCHO - ANCHO_CARRETERA) // 2

CARRILES = [
    X_CARRETERA + 100,
    X_CARRETERA + 300,
    X_CARRETERA + 500
]

# -----------------------------
# JUGADOR
# -----------------------------

jugador = pygame.Rect(CARRILES[1] - 30, ALTO - 120, 60, 100)

velocidad = 7
velocidad_maxima = 15

turbo = 100
puntuacion = 0
monedas = 0

# -----------------------------
# OBJETOS
# -----------------------------

enemigos = []
monedas_obj = []

contador_enemigos = 0
contador_monedas = 0

juego_terminado = False
pausa = False

# -----------------------------
# ESTRELLAS / AMBIENTE
# -----------------------------

estrellas = []

for i in range(80):
    estrellas.append([
        random.randint(0, ANCHO),
        random.randint(0, ALTO),
        random.randint(1, 3)
    ])

# -----------------------------
# FUNCIONES
# -----------------------------

def texto(texto, fuente, color, x, y):
    imagen = fuente.render(texto, True, color)
    pantalla.blit(imagen, (x, y))


def boton(texto_boton, x, y, ancho, alto):
    rect = pygame.Rect(x, y, ancho, alto)

    pygame.draw.rect(pantalla, (35, 35, 45), rect, border_radius=12)
    pygame.draw.rect(pantalla, AZUL, rect, 3, border_radius=12)

    imagen = fuente.render(texto_boton, True, BLANCO)

    pantalla.blit(
        imagen,
        (
            x + ancho // 2 - imagen.get_width() // 2,
            y + alto // 2 - imagen.get_height() // 2
        )
    )

    return rect


def dibujar_carretera():

    # Fondo
    pantalla.fill((20, 110, 50))

    # Zona exterior
    pygame.draw.rect(
        pantalla,
        (35, 130, 60),
        (0, 0, ANCHO, ALTO)
    )

    # Carretera
    pygame.draw.rect(
        pantalla,
        (55, 55, 60),
        (X_CARRETERA, 0, ANCHO_CARRETERA, ALTO)
    )

    # Bordes
    pygame.draw.rect(
        pantalla,
        BLANCO,
        (X_CARRETERA, 0, 8, ALTO)
    )

    pygame.draw.rect(
        pantalla,
        BLANCO,
        (X_CARRETERA + ANCHO_CARRETERA - 8, 0, 8, ALTO)
    )

    # Líneas de los carriles
    for x in [X_CARRETERA + 200, X_CARRETERA + 400]:

        for y in range(-50, ALTO, 80):

            pygame.draw.rect(
                pantalla,
                BLANCO,
                (x, y, 8, 45)
            )


def dibujar_jugador():

    # Sombra
    pygame.draw.ellipse(
        pantalla,
        (20, 20, 20),
        (jugador.x - 5, jugador.y + 85, 70, 20)
    )

    # Carro
    pygame.draw.rect(
        pantalla,
        AZUL,
        jugador,
        border_radius=12
    )

    # Ventanas
    pygame.draw.rect(
        pantalla,
        (150, 220, 255),
        (jugador.x + 10, jugador.y + 15, 40, 25),
        border_radius=5
    )

    pygame.draw.rect(
        pantalla,
        (150, 220, 255),
        (jugador.x + 10, jugador.y + 48, 40, 22),
        border_radius=5
    )

    # Luces
    pygame.draw.circle(
        pantalla,
        AMARILLO,
        (jugador.x + 10, jugador.y + 8),
        5
    )

    pygame.draw.circle(
        pantalla,
        AMARILLO,
        (jugador.x + 50, jugador.y + 8),
        5
    )

    # Llantas
    pygame.draw.rect(
        pantalla,
        NEGRO,
        (jugador.x - 6, jugador.y + 20, 8, 25)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (jugador.x + 58, jugador.y + 20, 8, 25)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (jugador.x - 6, jugador.y + 65, 8, 25)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (jugador.x + 58, jugador.y + 65, 8, 25)
    )


def crear_enemigo():

    carril = random.choice(CARRILES)

    colores = [
        ROJO,
        NARANJA,
        MORADO,
        (30, 200, 150)
    ]

    color = random.choice(colores)

    enemigo = {
        "rect": pygame.Rect(carril - 30, -120, 60, 100),
        "color": color
    }

    enemigos.append(enemigo)


def dibujar_enemigo(enemigo):

    rect = enemigo["rect"]
    color = enemigo["color"]

    pygame.draw.rect(
        pantalla,
        color,
        rect,
        border_radius=12
    )

    # Ventanas
    pygame.draw.rect(
        pantalla,
        (180, 220, 230),
        (rect.x + 10, rect.y + 15, 40, 25),
        border_radius=5
    )

    pygame.draw.rect(
        pantalla,
        (180, 220, 230),
        (rect.x + 10, rect.y + 50, 40, 22),
        border_radius=5
    )

    # Llantas
    pygame.draw.rect(
        pantalla,
        NEGRO,
        (rect.x - 6, rect.y + 20, 8, 25)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (rect.x + 58, rect.y + 20, 8, 25)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (rect.x - 6, rect.y + 65, 8, 25)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (rect.x + 58, rect.y + 65, 8, 25)
    )


def crear_moneda():

    carril = random.choice(CARRILES)

    moneda = pygame.Rect(
        carril - 15,
        -30,
        30,
        30
    )

    monedas_obj.append(moneda)


def dibujar_moneda(moneda):

    pygame.draw.circle(
        pantalla,
        AMARILLO,
        moneda.center,
        15
    )

    pygame.draw.circle(
        pantalla,
        NARANJA,
        moneda.center,
        10
    )

    texto(
        "$",
        fuente_pequena,
        BLANCO,
        moneda.x + 9,
        moneda.y + 1
    )


def reiniciar():

    global velocidad
    global turbo
    global puntuacion
    global monedas
    global enemigos
    global monedas_obj
    global contador_enemigos
    global contador_monedas
    global juego_terminado
    global pausa

    jugador.x = CARRILES[1] - 30
    jugador.y = ALTO - 120

    velocidad = 7
    turbo = 100
    puntuacion = 0
    monedas = 0

    enemigos = []
    monedas_obj = []

    contador_enemigos = 0
    contador_monedas = 0

    juego_terminado = False
    pausa = False


def dibujar_hud():

    # Panel superior
    pygame.draw.rect(
        pantalla,
        (20, 20, 25),
        (0, 0, ANCHO, 65)
    )

    texto(
        f"Puntos: {puntuacion}",
        fuente_pequena,
        BLANCO,
        20,
        18
    )

    texto(
        f"Monedas: {monedas}",
        fuente_pequena,
        AMARILLO,
        180,
        18
    )

    texto(
        f"Velocidad: {velocidad}",
        fuente_pequena,
        BLANCO,
        350,
        18
    )

    # Barra turbo
    texto(
        "TURBO",
        fuente_pequena,
        BLANCO,
        580,
        18
    )

    pygame.draw.rect(
        pantalla,
        (60, 60, 60),
        (660, 20, 180, 20),
        border_radius=8
    )

    pygame.draw.rect(
        pantalla,
        AZUL,
        (660, 20, int(180 * turbo / 100), 20),
        border_radius=8
    )


def pantalla_menu():

    while True:

        pantalla.fill((12, 15, 30))

        # Título
        texto(
            "TURBO HIGHWAY",
            fuente_grande,
            AZUL,
            250,
            80
        )

        texto(
            "CARRERA INFINITA",
            fuente,
            BLANCO,
            315,
            150
        )

        jugar = boton(
            "JUGAR",
            300,
            230,
            300,
            60
        )

        instrucciones = boton(
            "INSTRUCCIONES",
            300,
            310,
            300,
            60
        )

        salir = boton(
            "SALIR",
            300,
            390,
            300,
            60
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                return False

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if jugar.collidepoint(evento.pos):
                    reiniciar()
                    return True

                if instrucciones.collidepoint(evento.pos):
                    pantalla_instrucciones()

                if salir.collidepoint(evento.pos):
                    pygame.quit()
                    return False

        pygame.display.update()
        reloj.tick(60)


def pantalla_instrucciones():

    esperando = True

    while esperando:

        pantalla.fill((12, 15, 30))

        texto(
            "INSTRUCCIONES",
            fuente_grande,
            AZUL,
            280,
            60
        )

        instrucciones = [
            "← →  Cambiar de carril",
            "↑     Acelerar",
            "↓     Reducir velocidad",
            "ESPACIO  Activar TURBO",
            "",
            "Evita los carros enemigos.",
            "Recoge monedas para conseguir puntos.",
            "El turbo consume la barra azul.",
            "",
            "La velocidad aumenta con el tiempo.",
            "¡Intenta conseguir la mayor puntuación!"
        ]

        y = 145

        for linea in instrucciones:

            texto(
                linea,
                fuente_pequena,
                BLANCO,
                180,
                y
            )

            y += 35

        volver = boton(
            "VOLVER",
            330,
            510,
            240,
            55
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                return

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if volver.collidepoint(evento.pos):
                    esperando = False

        pygame.display.update()
        reloj.tick(60)


def pantalla_game_over():

    esperando = True

    while esperando:

        pantalla.fill((15, 10, 20))

        texto(
            "¡ACCIDENTE!",
            fuente_grande,
            ROJO,
            300,
            100
        )

        texto(
            f"Puntuación: {puntuacion}",
            fuente,
            BLANCO,
            330,
            190
        )

        texto(
            f"Monedas: {monedas}",
            fuente,
            AMARILLO,
            350,
            235
        )

        jugar = boton(
            "JUGAR OTRA VEZ",
            280,
            320,
            340,
            60
        )

        menu = boton(
            "MENÚ",
            330,
            400,
            240,
            60
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                return False

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if jugar.collidepoint(evento.pos):
                    reiniciar()
                    return True

                if menu.collidepoint(evento.pos):
                    return False

        pygame.display.update()
        reloj.tick(60)


# -----------------------------
# JUEGO PRINCIPAL
# -----------------------------

def jugar():

    global velocidad
    global turbo
    global puntuacion
    global monedas
    global contador_enemigos
    global contador_monedas
    global pausa
    global juego_terminado
    global enemigos

    ejecutando = True

    while ejecutando:

        reloj.tick(60)

        # -------------------------
        # EVENTOS
        # -------------------------

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                return False

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    return False

                if evento.key == pygame.K_p:
                    pausa = not pausa

        # -------------------------
        # PAUSA
        # -------------------------

        if pausa:

            pantalla.fill((10, 10, 20))

            texto(
                "PAUSA",
                fuente_grande,
                BLANCO,
                350,
                180
            )

            texto(
                "Presiona P para continuar",
                fuente,
                AZUL,
                250,
                280
            )

            texto(
                "ESC para volver al menú",
                fuente_pequena,
                BLANCO,
                320,
                340
            )

            pygame.display.update()
            continue

        # -------------------------
        # CONTROLES
        # -------------------------

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            jugador.x -= 8

        if teclas[pygame.K_RIGHT]:
            jugador.x += 8

        if teclas[pygame.K_UP]:
            velocidad += 0.08

        if teclas[pygame.K_DOWN]:
            velocidad -= 0.12

        # Limitar velocidad
        if velocidad < 4:
            velocidad = 4

        if velocidad > velocidad_maxima:
            velocidad = velocidad_maxima

        # Turbo
        if teclas[pygame.K_SPACE] and turbo > 0:

            velocidad += 0.18
            turbo -= 0.8

        else:

            if turbo < 100:
                turbo += 0.15

        # Limitar carro dentro de la carretera
        if jugador.left < X_CARRETERA:
            jugador.left = X_CARRETERA

        if jugador.right > X_CARRETERA + ANCHO_CARRETERA:
            jugador.right = X_CARRETERA + ANCHO_CARRETERA

        # -------------------------
        # GENERAR ENEMIGOS
        # -------------------------

        contador_enemigos += 1

        intervalo = max(
            25,
            int(70 - velocidad * 3)
        )

        if contador_enemigos >= intervalo:

            crear_enemigo()
            contador_enemigos = 0

        # -------------------------
        # GENERAR MONEDAS
        # -------------------------

        contador_monedas += 1

        if contador_monedas >= 80:

            crear_moneda()
            contador_monedas = 0

        # -------------------------
        # MOVER ENEMIGOS
        # -------------------------

        for enemigo in enemigos:

            enemigo["rect"].y += int(velocidad)

        # -------------------------
        # MOVER MONEDAS
        # -------------------------

        for moneda in monedas_obj:

            moneda.y += int(velocidad)

        # -------------------------
        # ELIMINAR OBJETOS
        # -------------------------

        enemigos = [
            enemigo
            for enemigo in enemigos
            if enemigo["rect"].top < ALTO + 100
        ]

        monedas_obj[:] = [
            moneda
            for moneda in monedas_obj
            if moneda.top < ALTO + 50
        ]

        # -------------------------
        # COLISIONES
        # -------------------------

        for enemigo in enemigos:

            if jugador.colliderect(enemigo["rect"]):

                juego_terminado = True

        # Monedas
        for moneda in monedas_obj[:]:

            if jugador.colliderect(moneda):

                monedas += 1
                puntuacion += 100

                monedas_obj.remove(moneda)

        # -------------------------
        # PUNTUACIÓN
        # -------------------------

        puntuacion += int(velocidad / 4)

        # Aumentar dificultad
        if puntuacion % 500 == 0:

            velocidad += 0.01

        # -------------------------
        # DIBUJAR
        # -------------------------

        dibujar_carretera()

        for moneda in monedas_obj:
            dibujar_moneda(moneda)

        for enemigo in enemigos:
            dibujar_enemigo(enemigo)

        dibujar_jugador()

        dibujar_hud()

        pygame.display.update()

        # -------------------------
        # GAME OVER
        # -------------------------

        if juego_terminado:

            resultado = pantalla_game_over()

            if resultado:

                reiniciar()

            else:

                return False

    return False


# -----------------------------
# PROGRAMA
# -----------------------------

while True:

    resultado = pantalla_menu()

    if resultado is False:
        break

    resultado = jugar()

    if resultado is False:
        continue

pygame.quit()
import pygame
import random
import math

pygame.init()

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
ANCHO = 900
ALTO = 600

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Turbo Highway")

reloj = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (15, 15, 20)
GRIS = (70, 70, 75)
GRIS_CLARO = (120, 120, 125)
VERDE = (30, 150, 70)
ROJO = (220, 50, 50)
AZUL = (40, 120, 255)
AMARILLO = (255, 210, 30)
NARANJA = (255, 130, 20)
MORADO = (150, 70, 220)

# Fuentes
fuente_grande = pygame.font.SysFont("Arial", 55, bold=True)
fuente = pygame.font.SysFont("Arial", 30, bold=True)
fuente_pequena = pygame.font.SysFont("Arial", 22)

# -----------------------------
# VARIABLES DE LA CARRETERA
# -----------------------------

ANCHO_CARRETERA = 600
X_CARRETERA = (ANCHO - ANCHO_CARRETERA) // 2

CARRILES = [
    X_CARRETERA + 100,
    X_CARRETERA + 300,
    X_CARRETERA + 500
]

# -----------------------------
# JUGADOR
# -----------------------------

jugador = pygame.Rect(CARRILES[1] - 30, ALTO - 120, 60, 100)

velocidad = 7
velocidad_maxima = 15

turbo = 100
puntuacion = 0
monedas = 0

# -----------------------------
# OBJETOS
# -----------------------------

enemigos = []
monedas_obj = []

contador_enemigos = 0
contador_monedas = 0

juego_terminado = False
pausa = False

# -----------------------------
# ESTRELLAS / AMBIENTE
# -----------------------------

estrellas = []

for i in range(80):
    estrellas.append([
        random.randint(0, ANCHO),
        random.randint(0, ALTO),
        random.randint(1, 3)
    ])

# -----------------------------
# FUNCIONES
# -----------------------------

def texto(texto, fuente, color, x, y):
    imagen = fuente.render(texto, True, color)
    pantalla.blit(imagen, (x, y))


def boton(texto_boton, x, y, ancho, alto):
    rect = pygame.Rect(x, y, ancho, alto)

    pygame.draw.rect(pantalla, (35, 35, 45), rect, border_radius=12)
    pygame.draw.rect(pantalla, AZUL, rect, 3, border_radius=12)

    imagen = fuente.render(texto_boton, True, BLANCO)

    pantalla.blit(
        imagen,
        (
            x + ancho // 2 - imagen.get_width() // 2,
            y + alto // 2 - imagen.get_height() // 2
        )
    )

    return rect


def dibujar_carretera():

    # Fondo
    pantalla.fill((20, 110, 50))

    # Zona exterior
    pygame.draw.rect(
        pantalla,
        (35, 130, 60),
        (0, 0, ANCHO, ALTO)
    )

    # Carretera
    pygame.draw.rect(
        pantalla,
        (55, 55, 60),
        (X_CARRETERA, 0, ANCHO_CARRETERA, ALTO)
    )

    # Bordes
    pygame.draw.rect(
        pantalla,
        BLANCO,
        (X_CARRETERA, 0, 8, ALTO)
    )

    pygame.draw.rect(
        pantalla,
        BLANCO,
        (X_CARRETERA + ANCHO_CARRETERA - 8, 0, 8, ALTO)
    )

    # Líneas de los carriles
    for x in [X_CARRETERA + 200, X_CARRETERA + 400]:

        for y in range(-50, ALTO, 80):

            pygame.draw.rect(
                pantalla,
                BLANCO,
                (x, y, 8, 45)
            )


def dibujar_jugador():

    # Sombra
    pygame.draw.ellipse(
        pantalla,
        (20, 20, 20),
        (jugador.x - 5, jugador.y + 85, 70, 20)
    )

    # Carro
    pygame.draw.rect(
        pantalla,
        AZUL,
        jugador,
        border_radius=12
    )

    # Ventanas
    pygame.draw.rect(
        pantalla,
        (150, 220, 255),
        (jugador.x + 10, jugador.y + 15, 40, 25),
        border_radius=5
    )

    pygame.draw.rect(
        pantalla,
        (150, 220, 255),
        (jugador.x + 10, jugador.y + 48, 40, 22),
        border_radius=5
    )

    # Luces
    pygame.draw.circle(
        pantalla,
        AMARILLO,
        (jugador.x + 10, jugador.y + 8),
        5
    )

    pygame.draw.circle(
        pantalla,
        AMARILLO,
        (jugador.x + 50, jugador.y + 8),
        5
    )

    # Llantas
    pygame.draw.rect(
        pantalla,
        NEGRO,
        (jugador.x - 6, jugador.y + 20, 8, 25)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (jugador.x + 58, jugador.y + 20, 8, 25)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (jugador.x - 6, jugador.y + 65, 8, 25)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (jugador.x + 58, jugador.y + 65, 8, 25)
    )


def crear_enemigo():

    carril = random.choice(CARRILES)

    colores = [
        ROJO,
        NARANJA,
        MORADO,
        (30, 200, 150)
    ]

    color = random.choice(colores)

    enemigo = {
        "rect": pygame.Rect(carril - 30, -120, 60, 100),
        "color": color
    }

    enemigos.append(enemigo)


def dibujar_enemigo(enemigo):

    rect = enemigo["rect"]
    color = enemigo["color"]

    pygame.draw.rect(
        pantalla,
        color,
        rect,
        border_radius=12
    )

    # Ventanas
    pygame.draw.rect(
        pantalla,
        (180, 220, 230),
        (rect.x + 10, rect.y + 15, 40, 25),
        border_radius=5
    )

    pygame.draw.rect(
        pantalla,
        (180, 220, 230),
        (rect.x + 10, rect.y + 50, 40, 22),
        border_radius=5
    )

    # Llantas
    pygame.draw.rect(
        pantalla,
        NEGRO,
        (rect.x - 6, rect.y + 20, 8, 25)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (rect.x + 58, rect.y + 20, 8, 25)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (rect.x - 6, rect.y + 65, 8, 25)
    )

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (rect.x + 58, rect.y + 65, 8, 25)
    )


def crear_moneda():

    carril = random.choice(CARRILES)

    moneda = pygame.Rect(
        carril - 15,
        -30,
        30,
        30
    )

    monedas_obj.append(moneda)


def dibujar_moneda(moneda):

    pygame.draw.circle(
        pantalla,
        AMARILLO,
        moneda.center,
        15
    )

    pygame.draw.circle(
        pantalla,
        NARANJA,
        moneda.center,
        10
    )

    texto(
        "$",
        fuente_pequena,
        BLANCO,
        moneda.x + 9,
        moneda.y + 1
    )


def reiniciar():

    global velocidad
    global turbo
    global puntuacion
    global monedas
    global enemigos
    global monedas_obj
    global contador_enemigos
    global contador_monedas
    global juego_terminado
    global pausa

    jugador.x = CARRILES[1] - 30
    jugador.y = ALTO - 120

    velocidad = 7
    turbo = 100
    puntuacion = 0
    monedas = 0

    enemigos = []
    monedas_obj = []

    contador_enemigos = 0
    contador_monedas = 0

    juego_terminado = False
    pausa = False


def dibujar_hud():

    # Panel superior
    pygame.draw.rect(
        pantalla,
        (20, 20, 25),
        (0, 0, ANCHO, 65)
    )

    texto(
        f"Puntos: {puntuacion}",
        fuente_pequena,
        BLANCO,
        20,
        18
    )

    texto(
        f"Monedas: {monedas}",
        fuente_pequena,
        AMARILLO,
        180,
        18
    )

    texto(
        f"Velocidad: {velocidad}",
        fuente_pequena,
        BLANCO,
        350,
        18
    )

    # Barra turbo
    texto(
        "TURBO",
        fuente_pequena,
        BLANCO,
        580,
        18
    )

    pygame.draw.rect(
        pantalla,
        (60, 60, 60),
        (660, 20, 180, 20),
        border_radius=8
    )

    pygame.draw.rect(
        pantalla,
        AZUL,
        (660, 20, int(180 * turbo / 100), 20),
        border_radius=8
    )


def pantalla_menu():

    while True:

        pantalla.fill((12, 15, 30))

        # Título
        texto(
            "TURBO HIGHWAY",
            fuente_grande,
            AZUL,
            250,
            80
        )

        texto(
            "CARRERA INFINITA",
            fuente,
            BLANCO,
            315,
            150
        )

        jugar = boton(
            "JUGAR",
            300,
            230,
            300,
            60
        )

        instrucciones = boton(
            "INSTRUCCIONES",
            300,
            310,
            300,
            60
        )

        salir = boton(
            "SALIR",
            300,
            390,
            300,
            60
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                return False

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if jugar.collidepoint(evento.pos):
                    reiniciar()
                    return True

                if instrucciones.collidepoint(evento.pos):
                    pantalla_instrucciones()

                if salir.collidepoint(evento.pos):
                    pygame.quit()
                    return False

        pygame.display.update()
        reloj.tick(60)


def pantalla_instrucciones():

    esperando = True

    while esperando:

        pantalla.fill((12, 15, 30))

        texto(
            "INSTRUCCIONES",
            fuente_grande,
            AZUL,
            280,
            60
        )

        instrucciones = [
            "← →  Cambiar de carril",
            "↑     Acelerar",
            "↓     Reducir velocidad",
            "ESPACIO  Activar TURBO",
            "",
            "Evita los carros enemigos.",
            "Recoge monedas para conseguir puntos.",
            "El turbo consume la barra azul.",
            "",
            "La velocidad aumenta con el tiempo.",
            "¡Intenta conseguir la mayor puntuación!"
        ]

        y = 145

        for linea in instrucciones:

            texto(
                linea,
                fuente_pequena,
                BLANCO,
                180,
                y
            )

            y += 35

        volver = boton(
            "VOLVER",
            330,
            510,
            240,
            55
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                return

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if volver.collidepoint(evento.pos):
                    esperando = False

        pygame.display.update()
        reloj.tick(60)


def pantalla_game_over():

    esperando = True

    while esperando:

        pantalla.fill((15, 10, 20))

        texto(
            "¡ACCIDENTE!",
            fuente_grande,
            ROJO,
            300,
            100
        )

        texto(
            f"Puntuación: {puntuacion}",
            fuente,
            BLANCO,
            330,
            190
        )

        texto(
            f"Monedas: {monedas}",
            fuente,
            AMARILLO,
            350,
            235
        )

        jugar = boton(
            "JUGAR OTRA VEZ",
            280,
            320,
            340,
            60
        )

        menu = boton(
            "MENÚ",
            330,
            400,
            240,
            60
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                return False

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if jugar.collidepoint(evento.pos):
                    reiniciar()
                    return True

                if menu.collidepoint(evento.pos):
                    return False

        pygame.display.update()
        reloj.tick(60)


# -----------------------------
# JUEGO PRINCIPAL
# -----------------------------

def jugar():

    global velocidad
    global turbo
    global puntuacion
    global monedas
    global contador_enemigos
    global contador_monedas
    global pausa
    global juego_terminado

    ejecutando = True

    while ejecutando:

        reloj.tick(60)

        # -------------------------
        # EVENTOS
        # -------------------------

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                return False

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    return False

                if evento.key == pygame.K_p:
                    pausa = not pausa

        # -------------------------
        # PAUSA
        # -------------------------

        if pausa:

            pantalla.fill((10, 10, 20))

            texto(
                "PAUSA",
                fuente_grande,
                BLANCO,
                350,
                180
            )

            texto(
                "Presiona P para continuar",
                fuente,
                AZUL,
                250,
                280
            )

            texto(
                "ESC para volver al menú",
                fuente_pequena,
                BLANCO,
                320,
                340
            )

            pygame.display.update()
            continue

        # -------------------------
        # CONTROLES
        # -------------------------

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            jugador.x -= 8

        if teclas[pygame.K_RIGHT]:
            jugador.x += 8

        if teclas[pygame.K_UP]:
            velocidad += 0.08

        if teclas[pygame.K_DOWN]:
            velocidad -= 0.12

        # Limitar velocidad
        if velocidad < 4:
            velocidad = 4

        if velocidad > velocidad_maxima:
            velocidad = velocidad_maxima

        # Turbo
        if teclas[pygame.K_SPACE] and turbo > 0:

            velocidad += 0.18
            turbo -= 0.8

        else:

            if turbo < 100:
                turbo += 0.15

        # Limitar carro dentro de la carretera
        if jugador.left < X_CARRETERA:
            jugador.left = X_CARRETERA

        if jugador.right > X_CARRETERA + ANCHO_CARRETERA:
            jugador.right = X_CARRETERA + ANCHO_CARRETERA

        # -------------------------
        # GENERAR ENEMIGOS
        # -------------------------

        contador_enemigos += 1

        intervalo = max(
            25,
            int(70 - velocidad * 3)
        )

        if contador_enemigos >= intervalo:

            crear_enemigo()
            contador_enemigos = 0

        # -------------------------
        # GENERAR MONEDAS
        # -------------------------

        contador_monedas += 1

        if contador_monedas >= 80:

            crear_moneda()
            contador_monedas = 0

        # -------------------------
        # MOVER ENEMIGOS
        # -------------------------

        for enemigo in enemigos:

            enemigo["rect"].y += int(velocidad)

        # -------------------------
        # MOVER MONEDAS
        # -------------------------

        for moneda in monedas_obj:

            moneda.y += int(velocidad)

        # -------------------------
        # ELIMINAR OBJETOS
        # -------------------------

        enemigos = [
            enemigo
            for enemigo in enemigos
            if enemigo["rect"].top < ALTO + 100
        ]

        monedas_obj[:] = [
            moneda
            for moneda in monedas_obj
            if moneda.top < ALTO + 50
        ]

        # -------------------------
        # COLISIONES
        # -------------------------

        for enemigo in enemigos:

            if jugador.colliderect(enemigo["rect"]):

                juego_terminado = True

        # Monedas
        for moneda in monedas_obj[:]:

            if jugador.colliderect(moneda):

                monedas += 1
                puntuacion += 100

                monedas_obj.remove(moneda)

        # -------------------------
        # PUNTUACIÓN
        # -------------------------

        puntuacion += int(velocidad / 4)

        # Aumentar dificultad
        if puntuacion % 500 == 0:

            velocidad += 0.01

        # -------------------------
        # DIBUJAR
        # -------------------------

        dibujar_carretera()

        for moneda in monedas_obj:
            dibujar_moneda(moneda)

        for enemigo in enemigos:
            dibujar_enemigo(enemigo)

        dibujar_jugador()

        dibujar_hud()

        pygame.display.update()

        # -------------------------
        # GAME OVER
        # -------------------------

        if juego_terminado:

            resultado = pantalla_game_over()

            if resultado:

                reiniciar()

            else:

                return False

    return False


# -----------------------------
# PROGRAMA
# -----------------------------

while True:

    resultado = pantalla_menu()

    if resultado is False:
        break

    resultado = jugar()

    if resultado is False:
        continue

pygame.quit()
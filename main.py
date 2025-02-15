import pygame
import random
import numpy as np
import streamlit as st
from pygame.surfarray import array3d

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Game variables
snake = [(100, 100), (90, 100), (80, 100)]
direction = "RIGHT"
food = (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
        random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)
score = 0
speed = 10
level = 1

# Streamlit UI
st.title("🐍 Streamlit Snake Game")
st.write("Use the buttons to control the snake!")

# Initialize pygame display (off-screen)
screen = pygame.Surface((WIDTH, HEIGHT))

# Streamlit buttons for controlling the snake
col1, col2, col3 = st.columns(3)
if col1.button("⬅️ Left") and direction != "RIGHT":
    direction = "LEFT"
if col2.button("⬆️ Up") and direction != "DOWN":
    direction = "UP"
if col3.button("⬇️ Down") and direction != "UP":
    direction = "DOWN"
if st.button("➡️ Right") and direction != "LEFT":
    direction = "RIGHT"

# Main game loop
def game_step():
    global direction, score, food, level, speed, snake

    # Move snake
    head_x, head_y = snake[0]
    if direction == "UP":
        head_y -= CELL_SIZE
    elif direction == "DOWN":
        head_y += CELL_SIZE
    elif direction == "LEFT":
        head_x -= CELL_SIZE
    elif direction == "RIGHT":
        head_x += CELL_SIZE

    # Collision with walls
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        return None

    # Insert new head
    snake.insert(0, (head_x, head_y))

    # Check if food is eaten
    if snake[0] == food:
        score += 10
        food = (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)
    else:
        snake.pop()

    # Draw everything on pygame screen
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))
    for pos in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

    return screen

# Run a game step
pygame_screen = game_step()

# Convert pygame surface to a NumPy array
if pygame_screen:
    img = np.rot90(np.fliplr(array3d(pygame_screen)))
    st.image(img, caption=f"Score: {score} | Level: {level}", use_container_width=True)
else:
    st.write("**Game Over! Refresh to restart.**")

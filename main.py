import streamlit as st
import numpy as np
import pygame
import random
from pygame.surfarray import array3d

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
WHITE, GREEN, RED, BLACK, BLUE, ORANGE, PURPLE, GRAY = (
    (255, 255, 255), (0, 255, 0), (255, 0, 0),
    (0, 0, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128), (128, 128, 128)
)

LEVEL_THRESHOLDS = {1: 0, 2: 50, 3: 100, 4: 150}  # Scores for level-ups
OBSTACLE_COUNT = {1: 0, 2: 3, 3: 6, 4: 10}  # Number of obstacles per level

# Initialize game state in session
if "snake" not in st.session_state:
    st.session_state.snake = [(100, 100), (90, 100), (80, 100)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                             random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
    st.session_state.score = 0
    st.session_state.running = True
    st.session_state.level = 1
    st.session_state.speed = 5
    st.session_state.obstacles = []  # Initialize empty obstacles

# Streamlit UI
st.title("🐍 Streamlit Snake Game with Levels & Obstacles")
st.write("Use the buttons below to control the snake!")

# Game controls using buttons
col1, col2, col3 = st.columns(3)
if col1.button("⬅️ Left") and st.session_state.direction != "RIGHT":
    st.session_state.direction = "LEFT"
if col2.button("⬆️ Up") and st.session_state.direction != "DOWN":
    st.session_state.direction = "UP"
if col3.button("⬇️ Down") and st.session_state.direction != "UP":
    st.session_state.direction = "DOWN"
if st.button("➡️ Right") and st.session_state.direction != "LEFT":
    st.session_state.direction = "RIGHT"

# Initialize pygame surface (off-screen rendering)
screen = pygame.Surface((WIDTH, HEIGHT))

def update_level():
    """Updates level based on score and increases speed."""
    for lvl, threshold in LEVEL_THRESHOLDS.items():
        if st.session_state.score >= threshold:
            st.session_state.level = lvl
            st.session_state.speed = 5 + (lvl - 1) * 2  # Increase speed

            # Add new obstacles as the level increases
            obstacle_count = OBSTACLE_COUNT[lvl]
            st.session_state.obstacles = [
                (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                 random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
                for _ in range(obstacle_count)
            ]

def game_step():
    """Runs one step of the snake game."""
    if not st.session_state.running:
        return None

    update_level()  # Check if level needs to be updated

    # Move snake
    head_x, head_y = st.session_state.snake[0]
    if st.session_state.direction == "UP":
        head_y -= CELL_SIZE
    elif st.session_state.direction == "DOWN":
        head_y += CELL_SIZE
    elif st.session_state.direction == "LEFT":
        head_x -= CELL_SIZE
    elif st.session_state.direction == "RIGHT":
        head_x += CELL_SIZE

    # Collision with walls
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        st.session_state.running = False
        return None

    # Collision with obstacles
    if (head_x, head_y) in st.session_state.obstacles:
        st.session_state.running = False
        return None

    # Insert new head
    st.session_state.snake.insert(0, (head_x, head_y))

    # Check if food is eaten
    if st.session_state.snake[0] == st.session_state.food:
        st.session_state.score += 10
        st.session_state.food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                                 random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
    else:
        st.session_state.snake.pop()  # Remove last segment

    # Set background color based on level
    level_colors = {1: BLACK, 2: BLUE, 3: ORANGE, 4: PURPLE}
    bg_color = level_colors.get(st.session_state.level, BLACK)

    # Draw everything
    screen.fill(bg_color)
    pygame.draw.rect(screen, RED, pygame.Rect(st.session_state.food[0], st.session_state.food[1], CELL_SIZE, CELL_SIZE))

    # Draw obstacles
    for obs in st.session_state.obstacles:
        pygame.draw.rect(screen, GRAY, pygame.Rect(obs[0], obs[1], CELL_SIZE, CELL_SIZE))

    # Draw the snake
    for pos in st.session_state.snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

    return screen

# Run one game step
pygame_screen = game_step()

# Convert pygame screen to NumPy array for Streamlit
if pygame_screen:
    img = np.rot90(np.fliplr(array3d(pygame_screen)))
    st.image(img, caption=f"Score: {st.session_state.score} | Level: {st.session_state.level}", use_container_width=True)
else:
    st.write("**Game Over! Refresh to restart.**")

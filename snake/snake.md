# Key Components:

## Snake Class:
- Manages the snake's behavior, including its movement, direction, and growth.
- Handles collisions (with the snake's body) and resets when needed.
- Listens for key inputs (arrow keys) to change the snake's direction.

## Food Class:
- Randomly places food on the grid.
- When the snake "eats" the food (collides with the food position), the snake grows, and the score increases.

## Grid Drawing Function:
- Draws a grid pattern on the game surface for visual clarity.

## Main Game Loop:
- Handles the game's main logic:
  - Snake movement.
  - Food collision detection.
  - Rendering the snake, food, and score on the screen.
  - Key event handling.
- The game runs at a controlled frame rate (`clock.tick(10)`), limiting the speed to 10 frames per second.

# Pygame Setup:
- `pygame.init()` initializes Pygame.
- A screen surface is set up to display the game with a size of 480x480 pixels.
- The snake and food are drawn onto a surface that is then rendered to the screen using `blit()`.

## Snake Movement:
- The snake moves in a grid, and its position wraps around the screen edges due to the modulus (`%`) operations used in the `move()` method.
- Snake's direction can be changed using the arrow keys, but it cannot reverse direction directly.

## Food:
- The food's position is randomized and aligned with the grid size using `random.randint()`.
- When the snake "eats" the food (head position equals the food position), the snake grows, and the food respawns in a new location.

## Score:
- The player's score is displayed at the top of the screen, increasing each time the snake eats the food.

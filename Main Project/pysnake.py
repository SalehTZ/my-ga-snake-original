import random
import time
import pygame


# LEFT -> button_direction = 0
# RIGHT -> button_direction = 1
# DOWN ->button_direction = 2
# UP -> button_direction = 3

class Directions:
    UP = 3
    DOWN = 2
    RIGHT = 1
    LEFT = 0


display_width = 250
display_height = 250
white = (255, 255, 255)


class SnakeGame:
    # ================================== SnakeGame class functions =======================================
    def __init__(self, random_seed, pop_size):
        self.snakes = []
        for i in range(0, pop_size):
            self.snakes.insert(i, self.Snakes(i, random_seed))

        pygame.init()
        self.display = pygame.display.set_mode((display_width, display_height))
        self.clock = pygame.time.Clock()

    def play_game(self, populations, game_speed):
        scores_list = []

        j = 0  # directions index   max = dna_size
        while True:
            if len(self.snakes) != 0:
                self.display.fill(white)
                for snake in self.snakes:
                    crashed, score = snake.move(populations[snake.index].genes[j - 1], self.display)
                    if crashed:
                        del self.snakes[snake.index]
                        for k in range(snake.index, len(self.snakes)):
                            self.snakes[k].index -= 1
                        scores_list.insert(snake.index, score)
                j += 1

            else:
                break
            pygame.display.update()
            self.clock.tick(game_speed)

        return scores_list

    # ======================================== Snakes class ==============================================
    class Snakes:
        def __init__(self, index, random_seed):
            self.index = index
            self.snake_start = []
            self.snake_position = []
            self.apple_position = []
            self.last_direction = Directions.LEFT
            self.score = 0
            random.seed(random_seed)

            self.head_color = (0, 0, 0)
            self.body_color = (255, 0, 0)
            self.apple_color = self.head_color

            self.random_color()
            self.starting_positions()

        def random_color(self):
            r = random.randrange(0, 100)
            g = random.randrange(0, 100)
            b = random.randrange(0, 100)

            self.head_color = (r + self.index, g + self.index, b + self.index)
            self.apple_color = self.head_color

            self.body_color = (r + 10, g + 10, b + 10)

        def display_snake(self, display):
            pygame.draw.rect(display, self.head_color, pygame.Rect(self.snake_start[0], self.snake_start[1], 10, 10))
            for position in self.snake_position[1:]:
                pygame.draw.rect(display, self.body_color, pygame.Rect(position[0], position[1], 10, 10))

        def display_apple(self, display):
            pygame.draw.rect(display, self.apple_color,
                             pygame.Rect(self.apple_position[0], self.apple_position[1], 10, 10))

        def starting_positions(self):
            self.snake_start = [100, 100]
            self.snake_position = [[100, 100], [90, 100], [80, 100]]
            self.apple_position = [random.randrange(1, display_width / 10) * 10,
                                   random.randrange(1, display_height / 10) * 10]
            self.score = 0

        def generate_snake(self, button_direction, last_direction):
            snake_moved = True
            current_direction = 0
            if button_direction == Directions.RIGHT and last_direction != Directions.LEFT:
                self.snake_start[0] += 10
                current_direction = Directions.RIGHT
            elif button_direction == Directions.LEFT and last_direction != Directions.RIGHT:
                self.snake_start[0] -= 10
                current_direction = Directions.LEFT
            elif button_direction == Directions.DOWN and last_direction != Directions.UP:
                self.snake_start[1] += 10
                current_direction = Directions.DOWN
            elif button_direction == Directions.UP and last_direction != Directions.DOWN:
                self.snake_start[1] -= 10
                current_direction = Directions.UP
            else:
                snake_moved = False

            if self.snake_start == self.apple_position:  # if snake hits apple
                self.collision_with_apple()
                self.snake_position.insert(0, list(self.snake_start))

            elif snake_moved:
                self.snake_position.insert(0, list(self.snake_start))
                self.snake_position.pop()

            elif not snake_moved:
                current_direction = last_direction

            return current_direction

        def collision_with_apple(self):
            # regenerate apple
            self.apple_position = [random.randrange(1, display_width / 10) * 10,
                                   random.randrange(1, display_height / 10) * 10]
            self.score += 100
            # return self.score

        def collision_with_boundaries(self):
            if self.snake_start[0] >= display_width or self.snake_start[0] < 0 \
                    or self.snake_start[1] >= display_height or self.snake_start[1] < 0:
                self.score += -5
                return True
            else:
                return False

        def collision_with_self(self):
            snake_start = self.snake_position[0]
            if snake_start in self.snake_position[1:]:
                self.score += -1
                return True
            else:
                return False

        def game_logic(self):
            crashed = self.collision_with_self()
            if crashed:
                return True

            crashed = self.collision_with_boundaries()
            if crashed:
                return True

            return False

        def move(self, direction, display):
            self.display_apple(display)
            self.display_snake(display)

            self.last_direction = self.generate_snake(direction, self.last_direction)

            crashed = self.game_logic()

            return crashed, self.score

import pygame
from options import Options as Opt
from state import State
from player import Player
from seeder import seed_players


Opt.set_default_window_position()
state = State()

seed_players(200, state.players_sprites, state.field)


class EventHandler():

    def mousemotion_handler(self, event):
        if event.type == pygame.MOUSEMOTION:
            state.mouse.pos = event.pos

            state.move_field = set()
            if Opt.width*Opt.move_area > event.pos[0]:
                state.move_field.add(state.field.move_left)
            if (Opt.width - Opt.width*Opt.move_area) < event.pos[0]:
                state.move_field.add(state.field.move_right)
            if Opt.height*Opt.move_area > event.pos[1]:
                state.move_field.add(state.field.move_top)
            if (Opt.height - Opt.height*Opt.move_area) < event.pos[1]:
                state.move_field.add(state.field.move_bot)

    def mousebuttondown_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            state.new_items.add(Player)


class Game(EventHandler):

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("My Game")

    def main_loop(self):
        running = True
        while running:
            state.update()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                self.mousemotion_handler(event)
                self.mousebuttondown_handler(event)

            for move in state.move_field:
                move()

            self.draw()
            pygame.display.flip()

        pygame.quit()

    def draw(self):
        state.screen.fill(Opt.bg)
        state.interface_sprites.draw(state.screen)
        state.players_sprites.draw(state.field.image)
        state.clock.tick(Opt.fps)


if __name__ == "__main__":
    g = Game()
    g.main_loop()

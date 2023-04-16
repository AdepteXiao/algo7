from random import randrange, randint, choice, sample

import pygame as pg

# BLUE = (70, 130, 180)
WHITE = (224, 255, 255)
WIDTH, HEIGHT = 930, 630
CELL_SIZE = 10
DEPTH = 2
COLOR = (70, 130, 180)


class Cell:
    def __init__(self, surface, x, y, c_type):
        self.x = x
        self.y = y
        self.surf = surface
        self.c_type = c_type
        self.rect = pg.Rect(
            self.x * CELL_SIZE,
            self.y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        # self.cord_txt = pg.font.Font(None, 13) \
        #     .render(f'({self.x}, {self.y})', True, (180, 0, 0))

    def render(self):
        col = COLOR if self.c_type == "wall" else WHITE
        pg.draw.rect(self.surf, col, self.rect)
        # self.surf.blit(self.cord_txt, (self.rect.x + 2, self.rect.centery - 2))

    def __repr__(self):
        wall_type = "maze_wall" if self.x == WIDTH or \
                                   self.y == HEIGHT or \
                                   self.x == 0 or \
                                   self.y == 0 else "wall"
        return f"Cell({self.x}, {self.y}, " \
               f"{wall_type if self.c_type == 'wall' else self.c_type})"


class Map:

    def __init__(self, surface, width, height):
        self.width = width
        self.height = height
        self.cells = []
        self.surface = surface
        self.gen_space()

    def gen_space(self):
        for y in range(0, self.height):
            line = []
            for x in range(0, self.width):
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    line.append(Cell(self.surface, x, y, "wall"))
                else:
                    line.append(Cell(self.surface, x, y, "way"))
            self.cells.append(line)

    def generate_piece(self):
        if self.width <= 1 or self.height <= 1:
            return
        # TODO: проверка на наличие прохода в данных координатах
        coord_y = randrange(2, self.height - 1, 2)
        coord_x = randrange(2, self.width - 1, 2)
        print(f'x: {coord_x}, y: {coord_y}')
        x_wall_1, x_wall_2, y_wall_1, y_wall_2 = [], [], [], []
        for i in range(1, self.width - 1):
            cell = self.cells[coord_y][i]
            cell.c_type = "wall"
            if i < coord_x:
                x_wall_1.append([coord_y, i])
            elif i > coord_x:
                x_wall_2.append([coord_y, i])
        print(f'x1: {x_wall_1}, \nx2: {x_wall_2}')

        for i in range(1, self.height - 1):
            cell = self.cells[i][coord_x]
            cell.c_type = "wall"
            if i < coord_y:
                y_wall_1.append([i, coord_x])
            elif i > coord_y:
                y_wall_2.append([i, coord_x])
        print(f'y1: {y_wall_1}, \ny2: {y_wall_2}')

        rand_walls = sample(
            [x_wall_1, x_wall_2, y_wall_1, y_wall_2], 3)
        print(f'rand_walls: {rand_walls}')
        for wall in rand_walls:
            cell = randint(0, len(wall) - 1)
            x, y = wall[cell][1], wall[cell][0]
            print(f'coord x: {x}, coord y: {y}')
            print(wall)
            cell = self.cells[y][x]
            cell.c_type = "way"

    def dividing(self):

        def divide_cur(m_rect, depth=1):

            if m_rect.w <= 2 or m_rect.h <= 2 or depth == DEPTH:
                return
            # print(m_rect)
            x2 = m_rect.x + m_rect.w
            y2 = m_rect.y + m_rect.h
            x_can, y_can = [], []

            for y in range(m_rect.y, y2):
                for x in range(m_rect.x, x2):
                    if x == m_rect.x or y == m_rect.y or x == x2 or y == y2:
                        if x % 2 == 0 and y % 2 == 0:
                            if m_rect.x < x < x2 - 1:
                                x_can.append(x)
                            if m_rect.y < y < y2 - 1:
                                y_can.append(y)

            # print(x_can, y_can)

            if x_can == [] or y_can == []:
                return
            wall_x, wall_y = choice(x_can), choice(y_can)
            # print(wall_x, wall_y)
            # print()

            top, bot, left, right = [], [], [], []
            for y in range(m_rect.y + 1, y2):
                for x in range(m_rect.x + 1, x2):
                    if x == wall_x or y == wall_y:
                        self.cells[y][x].c_type = "wall"
                        if x < wall_x:
                            left.append(self.cells[y][x])
                        elif x > wall_x:
                            right.append(self.cells[y][x])
                        elif y < wall_y:
                            top.append(self.cells[y][x])
                        elif y > wall_y:
                            bot.append(self.cells[y][x])
            # print("\t" * depth, top, bot, left, right, sep="\n")
            to_hole = sample([top, bot, left, right], k=3)
            for wall in to_hole:
                hole = choice(wall)
                hole.c_type = "way"
                holes.append(hole)

            top_left = pg.Rect(
                m_rect.x,
                m_rect.y,
                wall_x - m_rect.x,
                wall_y - m_rect.y
            )
            top_right = pg.Rect(
                wall_x,
                m_rect.y,
                m_rect.w - top_left.w,
                top_left.h
            )
            bot_left = pg.Rect(
                m_rect.x,
                m_rect.y + top_left.h,
                top_left.w,
                m_rect.h - top_left.h
            )
            bot_right = pg.Rect(
                wall_x,
                wall_y,
                top_right.w,
                bot_left.h
            )
            # print([top_left, top_right, bot_left, bot_right])
            # num = 1
            # global COLOR
            for cur_rect in [top_left, top_right, bot_left, bot_right]:
                # num += 1
                # COLOR = (num * 10, 130, 180)
                divide_cur(cur_rect, depth=depth + 1)

        holes = []
        divide_cur(pg.Rect(0, 0, self.width - 1, self.height - 1))

        for cell in holes:
            list_of_statements = [
                self.cells[cell.y + 1][cell.x].c_type == 'wall',
                self.cells[cell.y - 1][cell.x].c_type == 'wall',
                self.cells[cell.y][cell.x + 1].c_type == 'wall',
                self.cells[cell.y][cell.x - 1].c_type == 'wall']
            mirror = [self.cells[cell.y - 1][cell.x],
                      self.cells[cell.y + 1][cell.x],
                      self.cells[cell.y][cell.x - 1],
                      self.cells[cell.y][cell.x + 1]]
            if sum(list_of_statements) == 3:
                for i, state in enumerate(list_of_statements):
                    if not state:
                        mirror[i].c_type = 'way'
                        print(f'done: {mirror[i]}')
                        break
            if sum(list_of_statements) == 4:
                for c in sample(mirror, 1):
                    c.c_type = 'way'
                    print(f'changed: {c}')
        print(holes)

    def render(self):
        for line in self.cells:
            for cell in line:
                cell.render()

    def reset(self):
        self.gen_space()


def main():
    global DEPTH
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    m_w, m_h = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
    print(m_w, m_h)
    tile_map = Map(screen, m_w, m_h)
    tile_map.dividing()
    tile_map.render()
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    tile_map = Map(screen, m_w, m_h)
                    tile_map.dividing()
                if event.key == pg.K_UP:
                    DEPTH += 1
                    tile_map = Map(screen, m_w, m_h)
                    tile_map.dividing()

        tile_map.render()
        pg.display.flip()


if __name__ == '__main__':
    main()

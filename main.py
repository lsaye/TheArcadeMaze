import pygame
import sys
import random
import time
import math

#  CONSTANTS
SCREEN_W, SCREEN_H = 800, 600
FPS = 60
TITLE = "The Arcade Maze"

# Colours (retro palette)
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
NEON_GREEN = (57,  255, 20)
NEON_BLUE  = (0,   200, 255)
NEON_PINK  = (255, 20,  147)
GOLD       = (255, 215, 0)
DARK_GRAY  = (20,  20,  30)
MID_GRAY   = (60,  60,  80)
RED        = (220, 50,  50)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 140, 0)
PURPLE      = (180, 0,  255)

# Game states
STATE_MAIN_MENU    = "main_menu"
STATE_STORY        = "story"
STATE_TOKEN_RAIN   = "token_rain"
STATE_MAZE_RUN     = "maze_run"
STATE_BEAT_THE_BEAT = "beat_the_beat"
STATE_WIN          = "win"
STATE_LOSE         = "lose"
STATE_END          = "end"

# Token Rain settings
TOKEN_GOAL        = 15
TOKEN_TIME_LIMIT  = 30
TOKEN_SPAWN_RATE  = 45
PLAYER_SPEED      = 5
TOKEN_FALL_SPEED  = 3

# Maze Run settings
TILE          = 36           # pixel size of each maze cell
MAZE_COLS     = 19
MAZE_ROWS     = 13
MAZE_OFFSET_X = (SCREEN_W - MAZE_COLS * TILE) // 2   # = 58
MAZE_OFFSET_Y = (SCREEN_H - MAZE_ROWS * TILE) // 2   # = 66
MAZE_SPEED    = 3

# Beat the Beat settings
BTB_LANES      = 4
BTB_KEYS       = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]
BTB_LABELS     = ["A", "S", "D", "F"]
BTB_COLORS     = [NEON_PINK, NEON_BLUE, NEON_GREEN, NEON_YELLOW]
BTB_HIT_Y      = SCREEN_H - 100   # y-position of the hit line
BTB_NOTE_SPEED = 4
BTB_SPAWN_RATE = 55              # frames between note spawns
BTB_GOAL       = 12              # correct hits needed to win
BTB_TIME_LIMIT = 40              # seconds
BTB_HIT_WINDOW = 30             # pixel tolerance for a "hit"
BTB_LANE_W     = 90
BTB_LANE_START = (SCREEN_W - BTB_LANES * BTB_LANE_W) // 2

# STORY TEXT
STORY_INTRO = [
    {
        "speaker": "Narrator",
        "lines": [
            "Late one night, Jeffrey wandered into an old game shop\n"
            "tucked between two forgotten buildings.",

            "At the very back, half-hidden by dusty curtains,\n"
            "sat a glowing arcade cabinet unlike any Jeffrey had seen.",

            "A single coin slot pulsed with golden light.",
        ]
    },
    {
        "speaker": "Jeffrey",
        "lines": [
            "\"One coin... what's the worst that could happen?\"",
        ]
    },
    {
        "speaker": "Narrator",
        "lines": [
            "The screen FLASHED. The room VANISHED.\n"
            "Jeffrey was no longer in the shop.",

            "He stood inside a vast digital world,\n"
            "walls of glowing circuitry stretched in every direction.",

            "A floating message blinked before him:",
        ]
    },
    {
        "speaker": "ARCADE SYSTEM",
        "lines": [
            "\"WELCOME, PLAYER ONE.\n"
            " BEAT EVERY REALM TO EARN YOUR ESCAPE.\"",
        ]
    },
]

STORY_BEFORE_GAME1 = [
    {
        "speaker": "Narrator",
        "lines": [
            "Jeffrey stepped into the first realm.\n"
            "Golden tokens began raining from a pixelated sky.",
        ]
    },
    {
        "speaker": "ARCADE SYSTEM",
        "lines": [
            "\"REALM 1: TOKEN RAIN\n"
            " Collect " + str(TOKEN_GOAL) + " tokens before time runs out.\n"
            " Use LEFT / RIGHT arrow keys to move.\"",
        ]
    },
]

STORY_AFTER_GAME1 = [
    {
        "speaker": "Jeffrey",
        "lines": [
            "\"Yes! The door, it's opening!\"",
        ]
    },
    {
        "speaker": "Narrator",
        "lines": [
            "A bright doorway shimmered into existence at the end of the hall.\n"
            "Jeffrey sprinted toward it, unsure what waited on the other side.",

            "The arcade was not done with him yet.\n"
            "But for now, one realm down.",
        ]
    },
    {
        "speaker": "ARCADE SYSTEM",
        "lines": [
            "\"REALM 1 CLEARED.  ENTERING REALM 2...\"",
        ]
    },
]

STORY_BEFORE_GAME2 = [
    {
        "speaker": "Narrator",
        "lines": [
            "Jeffrey stumbled through the glowing doorway and found himself\n"
            "standing at the entrance of a massive digital maze.",

            "Neon walls twisted in every direction.\n"
            "Dead ends lurked around every corner.",
        ]
    },
    {
        "speaker": "ARCADE SYSTEM",
        "lines": [
            "\"REALM 2: MAZE RUN\n"
            " Find the exit hidden deep within the maze.\n"
            " Use ARROW KEYS to move. Reach the glowing portal!\"",
        ]
    },
]

STORY_AFTER_GAME2 = [
    {
        "speaker": "Jeffrey",
        "lines": [
            "\"There it is — the portal! I made it through!\"",
        ]
    },
    {
        "speaker": "Narrator",
        "lines": [
            "The exit portal pulsed with blinding light.\n"
            "Jeffrey dove through it without a second thought.",

            "The maze collapsed behind him in a cascade\n"
            "of dissolving pixels.",
        ]
    },
    {
        "speaker": "ARCADE SYSTEM",
        "lines": [
            "\"REALM 2 CLEARED.  ONE FINAL REALM AWAITS...\"",
        ]
    },
]

STORY_BEFORE_GAME3 = [
    {
        "speaker": "Narrator",
        "lines": [
            "Jeffrey landed in the Core Room — the beating heart\n"
            "of the arcade machine itself.",

            "A giant panel of glowing buttons dominated the wall.\n"
            "Colored circles pulsed in hypnotic patterns.",
        ]
    },
    {
        "speaker": "ARCADE SYSTEM",
        "lines": [
            "\"REALM 3: BEAT THE BEAT\n"
            " Match the rhythm. Hit the keys when the circles\n"
            " reach the line.  A / S / D / F\"",
        ]
    },
    {
        "speaker": "Jeffrey",
        "lines": [
            "\"This is it. Beat the machine and I go home.\"",
        ]
    },
]

STORY_AFTER_GAME3 = [
    {
        "speaker": "ARCADE SYSTEM",
        "lines": [
            "\"...SYSTEM OVERLOADED.\n"
            " INITIATING ESCAPE SEQUENCE.\"",
        ]
    },
    {
        "speaker": "Narrator",
        "lines": [
            "The Core Room shuddered. Pixels crumbled from the walls.\n"
            "A blinding column of white light erupted from the floor.",

            "Jeffrey felt himself lifted — pulled upward through\n"
            "layer after layer of circuitry and code.",

            "And then... silence.",

            "He was lying on the floor of the old game shop.\n"
            "The arcade cabinet sat dark and quiet in the corner.",
        ]
    },
    {
        "speaker": "Jeffrey",
        "lines": [
            "\"...Was any of that real?\"",
        ]
    },
    {
        "speaker": "Narrator",
        "lines": [
            "He looked at his hand.\n"
            "A single golden token rested in his palm.",
        ]
    },
]

# MAZE LAYOUT
# 1 = wall, 0 = open path, S = start, E = exit
# 15 cols x 13 rows
RAW_MAZE = [
    "###################",
    "#S#   # #   #   # #",
    "# # # # # # # # # #",
    "#   # #   # #   # #",
    "### # ##### ### # #",
    "#   #     #   # # #",
    "# ######### # # # #",
    "#   #     # #   # #",
    "#   #   #   #     #",
    "#   #   #   #     #",
    "# ##### # ### ### #",
    "#       #       #E#",
    "###################",
]

def _parse_maze(raw):
    """Convert raw string maze into a 2D list and locate start/exit."""
    grid   = []
    start  = (1, 1)
    exit_  = (0, 0)
    for r, row in enumerate(raw):
        cells = []
        for c, ch in enumerate(row):
            if ch == "S":
                start = (c, r)
                cells.append(0)
            elif ch == "E":
                exit_ = (c, r)
                cells.append(0)
            elif ch == "#":
                cells.append(1)
            else:
                cells.append(0)
        grid.append(cells)
    return grid, start, exit_

MAZE_GRID, MAZE_START, MAZE_EXIT = _parse_maze(RAW_MAZE)

# HELPER
def draw_text_wrapped(surface, text, font, color, rect, line_spacing=6):
    words_by_line = []
    for paragraph in text.split("\n"):
        words_by_line.append(paragraph.split(" "))

    x, y    = rect.topleft
    space_w = font.size(" ")[0]

    for word_list in words_by_line:
        line_words = []
        line_w     = 0
        for word in word_list:
            word_w = font.size(word)[0]
            if line_w + word_w + space_w > rect.width and line_words:
                line_surf = font.render(" ".join(line_words), True, color)
                surface.blit(line_surf, (x, y))
                y += font.get_height() + line_spacing
                line_words = [word]
                line_w     = word_w + space_w
            else:
                line_words.append(word)
                line_w += word_w + space_w
        if line_words:
            line_surf = font.render(" ".join(line_words), True, color)
            surface.blit(line_surf, (x, y))
            y += font.get_height() + line_spacing
        y += line_spacing

    return y

# SPRITES  — Token Rain
class Player(pygame.sprite.Sprite):
    """Jeffrey: the player-controlled character (Token Rain)."""
    WIDTH  = 30
    HEIGHT = 44

    def __init__(self, x, y):
        super().__init__()
        self.image = self._build_sprite()
        self.rect  = self.image.get_rect(midbottom=(x, y))

    def _build_sprite(self):
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 220, 180), (9, 0, 12, 12))
        pygame.draw.rect(surf, (80, 40, 0),     (9, 0, 12, 4))
        pygame.draw.rect(surf, NEON_BLUE,        (7, 12, 16, 16))
        pygame.draw.rect(surf, (40, 40, 120),    (7,  28, 6, 12))
        pygame.draw.rect(surf, (40, 40, 120),    (17, 28, 6, 12))
        pygame.draw.rect(surf, (60, 40, 20),     (5,  39, 8, 5))
        pygame.draw.rect(surf, (60, 40, 20),     (17, 39, 8, 5))
        pygame.draw.rect(surf, NEON_BLUE,        (1,  13, 6, 10))
        pygame.draw.rect(surf, NEON_BLUE,        (23, 13, 6, 10))
        return surf

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_W, SCREEN_H))


class Token(pygame.sprite.Sprite):
    """A falling golden token."""
    RADIUS = 14

    def __init__(self):
        super().__init__()
        self.image = self._build_sprite()
        x = random.randint(self.RADIUS, SCREEN_W - self.RADIUS)
        self.rect  = self.image.get_rect(center=(x, -self.RADIUS))
        self.speed = TOKEN_FALL_SPEED + random.uniform(-0.5, 1.2)

    def _build_sprite(self):
        r    = self.RADIUS
        surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, GOLD,          (r, r), r)
        pygame.draw.circle(surf, (200, 160, 0), (r, r), r, 2)
        font = pygame.font.SysFont("arial", r, bold=True)
        s    = font.render("$", True, (160, 120, 0))
        surf.blit(s, s.get_rect(center=(r, r)))
        return surf

    def update(self):
        self.rect.y += int(self.speed)
        if self.rect.top > SCREEN_H:
            self.kill()

# SPRITES — Maze Run
class MazePlayer(pygame.sprite.Sprite):
    """Jeffrey: top-down sprite for Maze Run."""
    SIZE = 22

    def __init__(self, col, row):
        super().__init__()
        self.image = self._build_sprite()
        self.grid_col  = col
        self.grid_row  = row
        # pixel position (centre of cell)
        self.px = float(MAZE_OFFSET_X + col * TILE + TILE // 2)
        self.py = float(MAZE_OFFSET_Y + row * TILE + TILE // 2)
        self.rect = self.image.get_rect(center=(int(self.px), int(self.py)))
        # movement state
        self.move_dx   = 0
        self.move_dy   = 0
        self.moving    = False

    def _build_sprite(self):
        s = self.SIZE
        surf = pygame.Surface((s, s), pygame.SRCALPHA)
        # body circle
        pygame.draw.circle(surf, NEON_BLUE, (s // 2, s // 2), s // 2)
        # face
        pygame.draw.circle(surf, (255, 220, 180), (s // 2, s // 2 - 2), s // 4)
        # direction indicator (arrow pointing up by default)
        pts = [(s // 2, 2), (s // 2 - 4, s // 2 - 2), (s // 2 + 4, s // 2 - 2)]
        pygame.draw.polygon(surf, WHITE, pts)
        return surf

    def try_move(self, dx, dy, grid):
        """Attempt to move one cell; returns True if movement started."""
        if self.moving:
            return False
        new_col = self.grid_col + dx
        new_row = self.grid_row + dy
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
            if grid[new_row][new_col] == 0:
                self.grid_col = new_col
                self.grid_row = new_row
                self.move_dx  = dx
                self.move_dy  = dy
                self.moving   = True
                return True
        return False

    def update(self):
        if self.moving:
            target_x = float(MAZE_OFFSET_X + self.grid_col * TILE + TILE // 2)
            target_y = float(MAZE_OFFSET_Y + self.grid_row * TILE + TILE // 2)
            self.px += (target_x - self.px) * 0.25
            self.py += (target_y - self.py) * 0.25
            if abs(self.px - target_x) < 1 and abs(self.py - target_y) < 1:
                self.px     = target_x
                self.py     = target_y
                self.moving = False
            self.rect.center = (int(self.px), int(self.py))

# SPRITES — Beat the Beat
class BeatNote(pygame.sprite.Sprite):
    """A falling rhythm note in a specific lane."""
    RADIUS = 22

    def __init__(self, lane):
        super().__init__()
        self.lane  = lane
        self.color = BTB_COLORS[lane]
        self.image = self._build_sprite()
        cx = BTB_LANE_START + lane * BTB_LANE_W + BTB_LANE_W // 2
        self.rect = self.image.get_rect(center=(cx, -self.RADIUS))

    def _build_sprite(self):
        r    = self.RADIUS
        surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, self.color,  (r, r), r)
        pygame.draw.circle(surf, WHITE,       (r, r), r, 2)
        font = pygame.font.SysFont("couriernew", r - 2, bold=True)
        lbl  = font.render(BTB_LABELS[self.lane], True, DARK_GRAY)
        surf.blit(lbl, lbl.get_rect(center=(r, r)))
        return surf

    def update(self):
        self.rect.y += BTB_NOTE_SPEED
        if self.rect.top > SCREEN_H:
            self.kill()

# MAIN GAME CLASS
class ArcadeMazeGame:
    """Main game controller — state machine + mini-game logic."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.clock  = pygame.time.Clock()

        # fonts
        self.font_title  = pygame.font.SysFont("couriernew", 48, bold=True)
        self.font_large  = pygame.font.SysFont("couriernew", 28, bold=True)
        self.font_medium = pygame.font.SysFont("couriernew", 20)
        self.font_small  = pygame.font.SysFont("couriernew", 16)

        # sounds
        self.sfx_catch  = self._gen_beep(880,  80)
        self.sfx_win    = self._gen_beep(1200, 300)
        self.sfx_lose   = self._gen_beep(200,  400)
        self.sfx_hit    = self._gen_beep(660,  60)
        self.sfx_miss   = self._gen_beep(150,  120)
        self.sfx_step   = self._gen_beep(440,  40)

        self._reset_state()

    def _gen_beep(self, freq, duration_ms):
        import array
        sample_rate = 44100
        n_samples   = int(sample_rate * duration_ms / 1000)
        buf         = array.array("h", [0] * n_samples)
        amplitude   = 4000
        for i in range(n_samples):
            t       = i / sample_rate
            buf[i]  = int(amplitude * math.sin(2 * math.pi * freq * t))
        return pygame.mixer.Sound(buffer=buf)

    def _reset_state(self):
        self.state = STATE_MAIN_MENU

        # story
        self.story_queue      = []
        self.story_index      = 0
        self.story_line_index = 0
        self.next_state       = None

        # token rain
        self.player      = None
        self.all_sprites = pygame.sprite.Group()
        self.token_group = pygame.sprite.Group()
        self.score       = 0
        self.spawn_timer = 0
        self.game_start  = 0.0

        # maze run
        self.maze_player    = None
        self.maze_grid      = None
        self.maze_exit      = None
        self.key_held       = {}

        # beat the beat
        self.btb_notes      = pygame.sprite.Group()
        self.btb_all        = pygame.sprite.Group()
        self.btb_score      = 0
        self.btb_misses     = 0
        self.btb_spawn_t    = 0
        self.btb_start      = 0.0
        self.btb_flash      = {}    
        self.btb_feedback   = []    


    def _start_story(self, story_beats, next_state):
        self.story_queue      = story_beats
        self.story_index      = 0
        self.story_line_index = 0
        self.next_state       = next_state
        self.state            = STATE_STORY

    def _current_story_line(self):
        beat = self.story_queue[self.story_index]
        return beat["speaker"], beat["lines"][self.story_line_index]

    def _advance_story(self):
        beat = self.story_queue[self.story_index]
        if self.story_line_index < len(beat["lines"]) - 1:
            self.story_line_index += 1
        elif self.story_index < len(self.story_queue) - 1:
            self.story_index      += 1
            self.story_line_index  = 0
        else:
            self.state = self.next_state
            if   self.next_state == STATE_TOKEN_RAIN:
                self._init_token_rain()
            elif self.next_state == STATE_MAZE_RUN:
                self._init_maze_run()
            elif self.next_state == STATE_BEAT_THE_BEAT:
                self._init_beat_the_beat()

    def _init_token_rain(self):
        self.all_sprites = pygame.sprite.Group()
        self.token_group = pygame.sprite.Group()
        self.player      = Player(SCREEN_W // 2, SCREEN_H - 30)
        self.all_sprites.add(self.player)
        self.score       = 0
        self.spawn_timer = 0
        self.game_start  = time.time()

    def _init_maze_run(self):
        import copy
        self.maze_grid   = copy.deepcopy(MAZE_GRID)
        self.maze_exit   = MAZE_EXIT
        sc, sr           = MAZE_START
        self.maze_player = MazePlayer(sc, sr)
        self.key_held    = {}

    def _init_beat_the_beat(self):
        self.btb_notes   = pygame.sprite.Group()
        self.btb_all     = pygame.sprite.Group()
        self.btb_score   = 0
        self.btb_misses  = 0
        self.btb_spawn_t = 0
        self.btb_start   = time.time()
        self.btb_flash   = {i: 0 for i in range(BTB_LANES)}
        self.btb_feedback = []

    def run(self):
        while True:
            self.clock.tick(FPS)
            self._handle_events()
            self._update()
            self._draw()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:

                if self.state == STATE_MAIN_MENU:
                    if event.key == pygame.K_RETURN:
                        self.story_queue = STORY_INTRO + STORY_BEFORE_GAME1
                        self.next_state  = STATE_TOKEN_RAIN
                        self._start_story(self.story_queue, STATE_TOKEN_RAIN)
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

                elif self.state == STATE_STORY:
                    if event.key != pygame.K_ESCAPE:
                        self._advance_story()

                elif self.state == STATE_BEAT_THE_BEAT:
                    self._handle_btb_keydown(event.key)

                elif self.state in (STATE_WIN, STATE_LOSE):
                    if event.key == pygame.K_r:
                        self._reset_state()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

                elif self.state == STATE_END:
                    if event.key == pygame.K_r:
                        self._reset_state()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

    def _update(self):
        if self.state == STATE_TOKEN_RAIN:
            self._update_token_rain()
        elif self.state == STATE_MAZE_RUN:
            self._update_maze_run()
        elif self.state == STATE_BEAT_THE_BEAT:
            self._update_beat_the_beat()

    def _update_token_rain(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        self.spawn_timer += 1
        if self.spawn_timer >= TOKEN_SPAWN_RATE:
            t = Token()
            self.token_group.add(t)
            self.all_sprites.add(t)
            self.spawn_timer = 0

        self.token_group.update()

        caught = pygame.sprite.spritecollide(self.player, self.token_group, True)
        if caught:
            self.score += len(caught)
            for _ in caught:
                try: self.sfx_catch.play()
                except: pass
            if self.score >= TOKEN_GOAL:
                try: self.sfx_win.play()
                except: pass
                self._start_story(STORY_AFTER_GAME1, STATE_MAZE_RUN)

        elapsed = time.time() - self.game_start
        if elapsed >= TOKEN_TIME_LIMIT and self.score < TOKEN_GOAL:
            try: self.sfx_lose.play()
            except: pass
            self.state = STATE_LOSE

    def _update_maze_run(self):
        keys     = pygame.key.get_pressed()
        mp       = self.maze_player
        moved    = False

        if not mp.moving:
            dirs = {
                pygame.K_UP:    (0, -1),
                pygame.K_DOWN:  (0,  1),
                pygame.K_LEFT:  (-1, 0),
                pygame.K_RIGHT: (1,  0),
            }
            for k, (dx, dy) in dirs.items():
                if keys[k]:
                    if mp.try_move(dx, dy, self.maze_grid):
                        moved = True
                        try: self.sfx_step.play()
                        except: pass
                        break

        mp.update()

        # check win
        if (mp.grid_col, mp.grid_row) == self.maze_exit:
            try: self.sfx_win.play()
            except: pass
            self._start_story(STORY_AFTER_GAME2, STATE_BEAT_THE_BEAT)

    def _handle_btb_keydown(self, key):
        if key not in BTB_KEYS:
            return
        lane  = BTB_KEYS.index(key)
        notes = [n for n in self.btb_notes if n.lane == lane]
        # find closest note in hit window
        best  = None
        best_dist = 9999
        for note in notes:
            dist = abs(note.rect.centery - BTB_HIT_Y)
            if dist < BTB_HIT_WINDOW and dist < best_dist:
                best      = note
                best_dist = dist

        cx = BTB_LANE_START + lane * BTB_LANE_W + BTB_LANE_W // 2
        if best is not None:
            best.kill()
            self.btb_score += 1
            self.btb_flash[lane] = 12
            try: self.sfx_hit.play()
            except: pass
            self.btb_feedback.append(["NICE!", NEON_GREEN, cx, BTB_HIT_Y - 30, 30])
        else:
            try: self.sfx_miss.play()
            except: pass
            self.btb_feedback.append(["MISS", RED, cx, BTB_HIT_Y - 30, 30])

    def _update_beat_the_beat(self):
        # spawn notes
        self.btb_spawn_t += 1
        if self.btb_spawn_t >= BTB_SPAWN_RATE:
            lane = random.randint(0, BTB_LANES - 1)
            note = BeatNote(lane)
            self.btb_notes.add(note)
            self.btb_all.add(note)
            self.btb_spawn_t = 0

        # count notes that fall past the hit line as misses
        for note in list(self.btb_notes):
            if note.rect.top > BTB_HIT_Y + BTB_HIT_WINDOW + 10:
                note.kill()
                self.btb_misses += 1

        self.btb_notes.update()

        # flash cooldown
        for lane in range(BTB_LANES):
            if self.btb_flash[lane] > 0:
                self.btb_flash[lane] -= 1

        # feedback TTL
        self.btb_feedback = [f for f in self.btb_feedback if f[4] > 0]
        for f in self.btb_feedback:
            f[4] -= 1

        # win
        if self.btb_score >= BTB_GOAL:
            try: self.sfx_win.play()
            except: pass
            self._start_story(STORY_AFTER_GAME3, STATE_END)

        # lose (time)
        elapsed = time.time() - self.btb_start
        if elapsed >= BTB_TIME_LIMIT and self.btb_score < BTB_GOAL:
            try: self.sfx_lose.play()
            except: pass
            self.state = STATE_LOSE

    def _draw(self):
        if   self.state == STATE_MAIN_MENU:
            self._draw_main_menu()
        elif self.state == STATE_STORY:
            self._draw_story()
        elif self.state == STATE_TOKEN_RAIN:
            self._draw_token_rain()
        elif self.state == STATE_MAZE_RUN:
            self._draw_maze_run()
        elif self.state == STATE_BEAT_THE_BEAT:
            self._draw_beat_the_beat()
        elif self.state == STATE_WIN:
            self._draw_result(won=True)
        elif self.state == STATE_LOSE:
            self._draw_result(won=False)
        elif self.state == STATE_END:
            self._draw_end()
        pygame.display.flip()

    # Main Menu
    def _draw_main_menu(self):
        self.screen.fill(DARK_GRAY)
        self._draw_scanlines()
        title1 = self.font_title.render("THE ARCADE", True, NEON_GREEN)
        title2 = self.font_title.render("MAZE",       True, NEON_PINK)
        self.screen.blit(title1, title1.get_rect(center=(SCREEN_W // 2, 160)))
        self.screen.blit(title2, title2.get_rect(center=(SCREEN_W // 2, 220)))
        if (pygame.time.get_ticks() // 600) % 2 == 0:
            prompt = self.font_medium.render("PRESS ENTER TO START", True, WHITE)
            self.screen.blit(prompt, prompt.get_rect(center=(SCREEN_W // 2, 360)))
        quit_txt = self.font_small.render("ESC  to quit", True, MID_GRAY)
        self.screen.blit(quit_txt, quit_txt.get_rect(center=(SCREEN_W // 2, 420)))
        pygame.draw.rect(self.screen, NEON_GREEN, (20, 20, SCREEN_W - 40, SCREEN_H - 40), 2)

    # Story Screen
    def _draw_story(self):
        self.screen.fill(DARK_GRAY)
        self._draw_scanlines()
        speaker, line = self._current_story_line()
        spk_surf = self.font_large.render(speaker, True, NEON_PINK)
        pygame.draw.rect(self.screen, MID_GRAY,  (40, 360, SCREEN_W - 80, 40))
        pygame.draw.rect(self.screen, NEON_PINK, (40, 360, SCREEN_W - 80, 40), 2)
        self.screen.blit(spk_surf, (60, 368))
        pygame.draw.rect(self.screen, (10, 10, 20), (40, 400, SCREEN_W - 80, 140))
        pygame.draw.rect(self.screen, NEON_GREEN,   (40, 400, SCREEN_W - 80, 140), 2)
        draw_text_wrapped(self.screen, line, self.font_medium, WHITE,
                          pygame.Rect(60, 415, SCREEN_W - 120, 100))
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            cont = self.font_small.render("[ Press any key to continue ]", True, NEON_GREEN)
            self.screen.blit(cont, cont.get_rect(bottomright=(SCREEN_W - 50, 535)))
        total_lines = sum(len(b["lines"]) for b in self.story_queue)
        done_lines  = sum(len(self.story_queue[i]["lines"]) for i in range(self.story_index)) \
                      + self.story_line_index + 1
        prog = self.font_small.render(f"{done_lines}/{total_lines}", True, MID_GRAY)
        self.screen.blit(prog, (50, 540))

    # Token Rain
    def _draw_token_rain(self):
        self.screen.fill((5, 5, 25))
        for i in range(0, SCREEN_H, 40):
            alpha = max(0, 40 - i // 15)
            s = pygame.Surface((SCREEN_W, 40), pygame.SRCALPHA)
            s.fill((0, 100, 255, alpha))
            self.screen.blit(s, (0, i))
        self._draw_scanlines()
        pygame.draw.rect(self.screen, MID_GRAY,  (0, SCREEN_H - 30, SCREEN_W, 30))
        pygame.draw.line(self.screen, NEON_BLUE, (0, SCREEN_H - 30), (SCREEN_W, SCREEN_H - 30), 2)
        self.all_sprites.draw(self.screen)
        elapsed   = time.time() - self.game_start
        time_left = max(0, TOKEN_TIME_LIMIT - elapsed)
        hud_bg = pygame.Surface((SCREEN_W, 50), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 160))
        self.screen.blit(hud_bg, (0, 0))
        score_txt = self.font_medium.render(f"Tokens: {self.score} / {TOKEN_GOAL}", True, GOLD)
        time_txt  = self.font_medium.render(f"Time: {time_left:.1f}s", True,
                                            RED if time_left < 8 else NEON_GREEN)
        instr_txt = self.font_small.render("← → Arrow keys to move", True, MID_GRAY)
        self.screen.blit(score_txt, (20,  10))
        self.screen.blit(time_txt,  (SCREEN_W - 200, 10))
        self.screen.blit(instr_txt, (SCREEN_W // 2 - instr_txt.get_width() // 2, 30))
        bar_w = int((self.score / TOKEN_GOAL) * (SCREEN_W - 40))
        pygame.draw.rect(self.screen, MID_GRAY, (20, 52, SCREEN_W - 40, 8))
        pygame.draw.rect(self.screen, GOLD,     (20, 52, bar_w,         8))

    # Maze Run
    def _draw_maze_run(self):
        self.screen.fill((5, 5, 25))
        self._draw_scanlines()

        # draw maze tiles
        for r, row in enumerate(self.maze_grid):
            for c, cell in enumerate(row):
                px = MAZE_OFFSET_X + c * TILE
                py = MAZE_OFFSET_Y + r * TILE
                rect = pygame.Rect(px, py, TILE, TILE)
                if cell == 1:
                    # wall — filled + inner glow border
                    pygame.draw.rect(self.screen, (10, 30, 60),  rect)
                    pygame.draw.rect(self.screen, NEON_BLUE,     rect, 1)
                else:
                    # floor
                    pygame.draw.rect(self.screen, (8, 8, 20), rect)

        # draw exit portal with pulsing gold/pink glow (contrasts dark floor)
        ec, er = self.maze_exit
        ex = MAZE_OFFSET_X + ec * TILE
        ey = MAZE_OFFSET_Y + er * TILE
        pulse = abs(math.sin(pygame.time.get_ticks() / 350))
        inner_r = int(55 + pulse * 180)
        inner_g = int(pulse * 100)
        inner_b = int(pulse * 200)
        pygame.draw.rect(self.screen, (inner_r, inner_g, inner_b),
                         pygame.Rect(ex + 2, ey + 2, TILE - 4, TILE - 4))
        border_color = GOLD if (pygame.time.get_ticks() // 250) % 2 == 0 else NEON_PINK
        pygame.draw.rect(self.screen, border_color,
                         pygame.Rect(ex, ey, TILE, TILE), 3)
        lbl = self.font_small.render("EXIT", True, WHITE)
        self.screen.blit(lbl, lbl.get_rect(center=(ex + TILE // 2, ey + TILE // 2)))

        # draw start marker
        sc, sr = MAZE_START
        sx = MAZE_OFFSET_X + sc * TILE
        sy = MAZE_OFFSET_Y + sr * TILE
        pygame.draw.rect(self.screen, (30, 60, 30),
                         pygame.Rect(sx + 3, sy + 3, TILE - 6, TILE - 6))

        # draw player
        self.screen.blit(self.maze_player.image, self.maze_player.rect)

        # HUD: title above maze, instructions below
        title_txt = self.font_medium.render("REALM 2: MAZE RUN", True, NEON_BLUE)
        instr_txt = self.font_small.render("Arrow keys to move  |  Reach the EXIT portal", True, MID_GRAY)
        # Centre title in the space above the maze
        title_y = (MAZE_OFFSET_Y - title_txt.get_height()) // 2
        self.screen.blit(title_txt, title_txt.get_rect(center=(SCREEN_W // 2, max(title_y, 8))))
        # Centre instructions in the space below the maze
        instr_y = MAZE_OFFSET_Y + MAZE_ROWS * TILE + (SCREEN_H - (MAZE_OFFSET_Y + MAZE_ROWS * TILE) - instr_txt.get_height()) // 2
        self.screen.blit(instr_txt, instr_txt.get_rect(center=(SCREEN_W // 2, instr_y)))
        pygame.draw.rect(self.screen, NEON_BLUE, (20, 20, SCREEN_W - 40, SCREEN_H - 40), 2)

    # Beat the Beat
    def _draw_beat_the_beat(self):
        self.screen.fill((10, 5, 25))
        self._draw_scanlines()

        # lane backgrounds
        for i in range(BTB_LANES):
            lx = BTB_LANE_START + i * BTB_LANE_W
            flash = self.btb_flash[i]
            bg_color = (*BTB_COLORS[i][:3], 30 + flash * 10)
            lane_surf = pygame.Surface((BTB_LANE_W - 4, SCREEN_H), pygame.SRCALPHA)
            lane_surf.fill((BTB_COLORS[i][0], BTB_COLORS[i][1], BTB_COLORS[i][2],
                            20 + flash * 8))
            self.screen.blit(lane_surf, (lx + 2, 0))
            # lane divider
            pygame.draw.line(self.screen, MID_GRAY, (lx, 0), (lx, SCREEN_H))

        # hit line
        pygame.draw.line(self.screen, WHITE, (BTB_LANE_START, BTB_HIT_Y),
                         (BTB_LANE_START + BTB_LANES * BTB_LANE_W, BTB_HIT_Y), 3)

        # hit targets (static circles at hit line)
        for i in range(BTB_LANES):
            cx = BTB_LANE_START + i * BTB_LANE_W + BTB_LANE_W // 2
            r  = BeatNote.RADIUS
            flash = self.btb_flash[i]
            color = BTB_COLORS[i] if flash == 0 else WHITE
            pygame.draw.circle(self.screen, color, (cx, BTB_HIT_Y), r, 3)
            lbl = self.font_medium.render(BTB_LABELS[i], True, BTB_COLORS[i])
            self.screen.blit(lbl, lbl.get_rect(center=(cx, BTB_HIT_Y + r + 14)))

        # notes
        self.btb_notes.draw(self.screen)

        # feedback popups
        for f in self.btb_feedback:
            text, color, fx, fy, ttl = f
            alpha = min(255, ttl * 10)
            pop_surf = self.font_medium.render(text, True, color)
            self.screen.blit(pop_surf, pop_surf.get_rect(center=(fx, fy)))

        # HUD
        elapsed   = time.time() - self.btb_start
        time_left = max(0, BTB_TIME_LIMIT - elapsed)
        hud_bg = pygame.Surface((SCREEN_W, 50), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 180))
        self.screen.blit(hud_bg, (0, 0))
        score_txt = self.font_medium.render(f"Hits: {self.btb_score} / {BTB_GOAL}", True, NEON_GREEN)
        time_txt  = self.font_medium.render(f"Time: {time_left:.1f}s", True,
                                            RED if time_left < 10 else NEON_PINK)
        title_txt = self.font_small.render("REALM 3: BEAT THE BEAT", True, NEON_PINK)
        self.screen.blit(score_txt, (20, 8))
        self.screen.blit(time_txt,  (SCREEN_W - 210, 8))
        self.screen.blit(title_txt, (SCREEN_W // 2 - title_txt.get_width() // 2, 30))

        # progress bar
        bar_w = int((self.btb_score / BTB_GOAL) * (SCREEN_W - 40))
        pygame.draw.rect(self.screen, MID_GRAY, (20, 52, SCREEN_W - 40, 8))
        pygame.draw.rect(self.screen, NEON_PINK, (20, 52, bar_w,         8))

    # Win / Lose
    def _draw_result(self, won):
        self.screen.fill(DARK_GRAY)
        self._draw_scanlines()
        if won:
            msg, color, sub = "YOU WIN!", NEON_GREEN, f"You caught all {TOKEN_GOAL} tokens!"
        else:
            msg, color, sub = "GAME OVER", RED, "You ran out of time!"
        msg_surf = self.font_title.render(msg,  True, color)
        sub_surf = self.font_large.render(sub,  True, WHITE)
        r_surf   = self.font_medium.render("R  to retry    ESC  to quit", True, MID_GRAY)
        self.screen.blit(msg_surf, msg_surf.get_rect(center=(SCREEN_W // 2, 220)))
        self.screen.blit(sub_surf, sub_surf.get_rect(center=(SCREEN_W // 2, 300)))
        self.screen.blit(r_surf,   r_surf.get_rect(  center=(SCREEN_W // 2, 400)))

    # End Screen
    def _draw_end(self):
        self.screen.fill(DARK_GRAY)
        self._draw_scanlines()
        t = pygame.time.get_ticks()
        # animated colour shift
        r = int(abs(math.sin(t / 800)) * 200 + 55)
        g = int(abs(math.sin(t / 600 + 1)) * 200 + 55)
        b = int(abs(math.sin(t / 1000 + 2)) * 200 + 55)
        lines = [
            ("ALL REALMS CLEARED!", (r, g, b),    self.font_large,  200),
            ("Jeffrey escapes the arcade...",  WHITE,        self.font_medium, 270),
            ("...or did he?",                  MID_GRAY,     self.font_medium, 310),
            ("R  to restart    ESC  to quit",  MID_GRAY,     self.font_medium, 430),
        ]
        for text, color, font, y in lines:
            surf = font.render(text, True, color)
            self.screen.blit(surf, surf.get_rect(center=(SCREEN_W // 2, y)))
        pygame.draw.rect(self.screen, NEON_PINK, (20, 20, SCREEN_W - 40, SCREEN_H - 40), 2)

    # Scanlines
    def _draw_scanlines(self):
        scanline = pygame.Surface((SCREEN_W, 2), pygame.SRCALPHA)
        scanline.fill((0, 0, 0, 40))
        for y in range(0, SCREEN_H, 4):
            self.screen.blit(scanline, (0, y))

# ENTRY POINT
if __name__ == "__main__":
    game = ArcadeMazeGame()
    game.run()

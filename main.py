import pygame
import sys
import random
import time

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

# Game states
STATE_MAIN_MENU   = "main_menu"
STATE_STORY       = "story"
STATE_TOKEN_RAIN  = "token_rain"
STATE_WIN         = "win"
STATE_LOSE        = "lose"
STATE_END         = "end"

# Token Rain settings
TOKEN_GOAL        = 15   
TOKEN_TIME_LIMIT  = 30   
TOKEN_SPAWN_RATE  = 45  
PLAYER_SPEED      = 5
TOKEN_FALL_SPEED  = 3

# STORY
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
            "\"REALM 1 CLEARED.\n",
        ]
    },
]

# HELPER 
def draw_text_wrapped(surface, text, font, color, rect, line_spacing=6):
    """
    Draws text wrapped to fit inside 'rect'.
    Supports manual newlines (\\n) in the text string.
    Returns the y-position after the last drawn line.
    """
    words_by_line = []
    for paragraph in text.split("\n"):
        words_by_line.append(paragraph.split(" "))

    x, y = rect.topleft
    space_w = font.size(" ")[0]
    max_x   = rect.right

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

#  PLAYER SPRITE
class Player(pygame.sprite.Sprite):
    """Jeffrey: the player-controlled character."""

    WIDTH  = 30
    HEIGHT = 44

    def __init__(self, x, y):
        super().__init__()
        self.image = self._build_sprite()
        self.rect  = self.image.get_rect(midbottom=(x, y))

    #drawing Jeffrey
    def _build_sprite(self):
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)

        # head
        pygame.draw.rect(surf, (255, 220, 180), (9, 0, 12, 12))
        # hair
        pygame.draw.rect(surf, (80, 40, 0),     (9, 0, 12, 4))
        # body
        pygame.draw.rect(surf, NEON_BLUE,        (7, 12, 16, 16))
        # legs
        pygame.draw.rect(surf, (40, 40, 120),    (7,  28, 6, 12))
        pygame.draw.rect(surf, (40, 40, 120),    (17, 28, 6, 12))
        # feet
        pygame.draw.rect(surf, (60, 40, 20),     (5,  39, 8, 5))
        pygame.draw.rect(surf, (60, 40, 20),     (17, 39, 8, 5))
        # arms
        pygame.draw.rect(surf, NEON_BLUE,        (1,  13, 6, 10))
        pygame.draw.rect(surf, NEON_BLUE,        (23, 13, 6, 10))
        return surf

    def update(self, keys):
        """Move left/right based on arrow-key input."""
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_W, SCREEN_H))

#  TOKEN SPRITE
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
        r = self.RADIUS
        surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, GOLD,          (r, r), r)
        pygame.draw.circle(surf, (200, 160, 0), (r, r), r, 2)
        font = pygame.font.SysFont("arial", r, bold=True)
        s = font.render("$", True, (160, 120, 0))
        surf.blit(s, s.get_rect(center=(r, r)))
        return surf

    def update(self):
        self.rect.y += int(self.speed)
        if self.rect.top > SCREEN_H:
            self.kill()  

#  GAME CLASS
class ArcadeMazeGame:
    """
    Main game controller.
    Manages the state machine, story display, and mini-game logic.
    """

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen  = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.clock   = pygame.time.Clock()

        # fonts
        self.font_title  = pygame.font.SysFont("couriernew", 48, bold=True)
        self.font_large  = pygame.font.SysFont("couriernew", 28, bold=True)
        self.font_medium = pygame.font.SysFont("couriernew", 20)
        self.font_small  = pygame.font.SysFont("couriernew", 16)

        # sounds
        self.sfx_catch  = self._gen_beep(880, 80)
        self.sfx_win    = self._gen_beep(1200, 300)
        self.sfx_lose   = self._gen_beep(200, 400)

        self._reset_state()

    # sound helpers
    def _gen_beep(self, freq, duration_ms):
        """Generate a simple sine-wave beep Sound object."""
        import math, array
        sample_rate = 44100
        n_samples   = int(sample_rate * duration_ms / 1000)
        buf = array.array("h", [0] * n_samples)
        amplitude = 4000
        for i in range(n_samples):
            t = i / sample_rate
            buf[i] = int(amplitude * math.sin(2 * math.pi * freq * t))
        sound = pygame.sndarray.make_sound(
            pygame.sndarray.make_surface(buf) if False else
            pygame.mixer.Sound(buffer=buf)
        )
        return sound

    # state machine 
    def _reset_state(self):
        """Initialise / re-initialise all game variables."""
        self.state = STATE_MAIN_MENU

        # story display state
        self.story_queue      = []   
        self.story_index      = 0  
        self.story_line_index = 0    
        self.next_state       = None 

        # token rain state
        self.player        = None
        self.all_sprites   = pygame.sprite.Group()
        self.token_group   = pygame.sprite.Group()
        self.score         = 0
        self.spawn_timer   = 0
        self.game_start    = 0.0

    # story helpers
    def _start_story(self, story_beats, next_state):
        """
        Begin displaying a sequence of story beats.

        Parameters
        ----------
        story_beats : list of dicts  (speaker + lines)
        next_state  : str            game state to enter when done
        """
        self.story_queue      = story_beats
        self.story_index      = 0
        self.story_line_index = 0
        self.next_state       = next_state
        self.state            = STATE_STORY

    def _current_story_line(self):
        """Return (speaker, line_text) for the currently displayed story line."""
        beat = self.story_queue[self.story_index]
        return beat["speaker"], beat["lines"][self.story_line_index]

    def _advance_story(self):
        """Advance to the next story line, or exit story if finished."""
        beat = self.story_queue[self.story_index]
        if self.story_line_index < len(beat["lines"]) - 1:
            self.story_line_index += 1
        elif self.story_index < len(self.story_queue) - 1:
            self.story_index      += 1
            self.story_line_index  = 0
        else:
            self.state = self.next_state
            if self.next_state == STATE_TOKEN_RAIN:
                self._init_token_rain()

    # Token Rain setup 
    def _init_token_rain(self):
        """Initialise sprites and counters for the Token Rain mini-game."""
        self.all_sprites = pygame.sprite.Group()
        self.token_group = pygame.sprite.Group()

        self.player = Player(SCREEN_W // 2, SCREEN_H - 30)
        self.all_sprites.add(self.player)

        self.score       = 0
        self.spawn_timer = 0
        self.game_start  = time.time()

    # MAIN LOOP
    def run(self):
        """Main game loop, runs until the player quits."""
        while True:
            dt = self.clock.tick(FPS)
            self._handle_events()
            self._update()
            self._draw()

    # EVENT HANDLING
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MAIN_MENU:
                    if event.key == pygame.K_RETURN:
                        self._start_story(STORY_INTRO, STATE_STORY)
                        self.story_queue = STORY_INTRO + STORY_BEFORE_GAME1
                        self.next_state  = STATE_TOKEN_RAIN

                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                elif self.state == STATE_STORY:
                    if event.key not in (pygame.K_ESCAPE,):
                        self._advance_story()

                elif self.state in (STATE_WIN, STATE_LOSE):
                    if event.key == pygame.K_r:
                        self._reset_state()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                elif self.state == STATE_END:
                    if event.key == pygame.K_r:
                        self._reset_state()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    # UPDATE
    def _update(self):
        if self.state == STATE_TOKEN_RAIN:
            self._update_token_rain()

    def _update_token_rain(self):
        """Update Token Rain mini-game logic each frame."""
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # spawn tokens on a timer
        self.spawn_timer += 1
        if self.spawn_timer >= TOKEN_SPAWN_RATE:
            token = Token()
            self.token_group.add(token)
            self.all_sprites.add(token)
            self.spawn_timer = 0

        self.token_group.update()

        # collision: player catches token
        caught = pygame.sprite.spritecollide(self.player, self.token_group, True)
        if caught:
            self.score += len(caught)
            for _ in caught:
                try:
                    self.sfx_catch.play()
                except Exception:
                    pass
            if self.score >= TOKEN_GOAL:
                try:
                    self.sfx_win.play()
                except Exception:
                    pass
                self._start_story(STORY_AFTER_GAME1, STATE_END)

        # check time limit
        elapsed = time.time() - self.game_start
        if elapsed >= TOKEN_TIME_LIMIT and self.score < TOKEN_GOAL:
            try:
                self.sfx_lose.play()
            except Exception:
                pass
            self.state = STATE_LOSE

    # DRAW 
    def _draw(self):
        if self.state == STATE_MAIN_MENU:
            self._draw_main_menu()
        elif self.state == STATE_STORY:
            self._draw_story()
        elif self.state == STATE_TOKEN_RAIN:
            self._draw_token_rain()
        elif self.state == STATE_WIN:
            self._draw_result(won=True)
        elif self.state == STATE_LOSE:
            self._draw_result(won=False)
        elif self.state == STATE_END:
            self._draw_end()

        pygame.display.flip()

    # DRAW: Main Menu
    def _draw_main_menu(self):
        self.screen.fill(DARK_GRAY)
        self._draw_scanlines()

        # title
        title1 = self.font_title.render("THE ARCADE", True, NEON_GREEN)
        title2 = self.font_title.render("MAZE",       True, NEON_PINK)
        self.screen.blit(title1, title1.get_rect(center=(SCREEN_W // 2, 160)))
        self.screen.blit(title2, title2.get_rect(center=(SCREEN_W // 2, 220)))

        # blinking "press enter"
        if (pygame.time.get_ticks() // 600) % 2 == 0:
            prompt = self.font_medium.render("PRESS ENTER TO START", True, WHITE)
            self.screen.blit(prompt, prompt.get_rect(center=(SCREEN_W // 2, 360)))

        quit_txt = self.font_small.render("ESC  to quit", True, MID_GRAY)
        self.screen.blit(quit_txt, quit_txt.get_rect(center=(SCREEN_W // 2, 420)))

        # decorative pixel border
        pygame.draw.rect(self.screen, NEON_GREEN, (20, 20, SCREEN_W - 40, SCREEN_H - 40), 2)

    # Story Screen 
    def _draw_story(self):
        self.screen.fill(DARK_GRAY)
        self._draw_scanlines()

        speaker, line = self._current_story_line()

        # speaker box
        spk_surf = self.font_large.render(speaker, True, NEON_PINK)
        pygame.draw.rect(self.screen, MID_GRAY,    (40, 360, SCREEN_W - 80, 40))
        pygame.draw.rect(self.screen, NEON_PINK,   (40, 360, SCREEN_W - 80, 40), 2)
        self.screen.blit(spk_surf, (60, 368))

        # dialogue box
        pygame.draw.rect(self.screen, (10, 10, 20),  (40, 400, SCREEN_W - 80, 140))
        pygame.draw.rect(self.screen, NEON_GREEN,    (40, 400, SCREEN_W - 80, 140), 2)
        draw_text_wrapped(
            self.screen, line, self.font_medium, WHITE,
            pygame.Rect(60, 415, SCREEN_W - 120, 100)
        )

        # continue prompt (blinks)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            cont = self.font_small.render("[ Press any key to continue ]", True, NEON_GREEN)
            self.screen.blit(cont, cont.get_rect(bottomright=(SCREEN_W - 50, 535)))

        # progress indicator
        total_lines = sum(len(b["lines"]) for b in self.story_queue)
        done_lines  = sum(len(self.story_queue[i]["lines"]) for i in range(self.story_index)) \
                      + self.story_line_index + 1
        prog = self.font_small.render(f"{done_lines}/{total_lines}", True, MID_GRAY)
        self.screen.blit(prog, (50, 540))

    # DRAW: Token Rain game
    def _draw_token_rain(self):
        self.screen.fill((5, 5, 25))
        for i in range(0, SCREEN_H, 40):
            alpha = max(0, 40 - i // 15)
            s = pygame.Surface((SCREEN_W, 40), pygame.SRCALPHA)
            s.fill((0, 100, 255, alpha))
            self.screen.blit(s, (0, i))

        self._draw_scanlines()

        # ground platform
        pygame.draw.rect(self.screen, MID_GRAY, (0, SCREEN_H - 30, SCREEN_W, 30))
        pygame.draw.line(self.screen, NEON_BLUE, (0, SCREEN_H - 30), (SCREEN_W, SCREEN_H - 30), 2)

        # sprites
        self.all_sprites.draw(self.screen)

        # HUD
        elapsed  = time.time() - self.game_start
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

        # progress bar
        bar_w = int((self.score / TOKEN_GOAL) * (SCREEN_W - 40))
        pygame.draw.rect(self.screen, MID_GRAY, (20, 52, SCREEN_W - 40, 8))
        pygame.draw.rect(self.screen, GOLD,     (20, 52, bar_w,         8))

    # DRAW: Win / Lose 
    def _draw_result(self, won):
        self.screen.fill(DARK_GRAY)
        self._draw_scanlines()

        if won:
            msg   = "YOU WIN!"
            color = NEON_GREEN
            sub   = f"You caught all {TOKEN_GOAL} tokens!"
        else:
            msg   = "GAME OVER"
            color = RED
            sub   = "You ran out of time!"

        msg_surf = self.font_title.render(msg, True, color)
        sub_surf = self.font_large.render(sub, True, WHITE)
        r_surf   = self.font_medium.render("R  to retry    ESC  to quit", True, MID_GRAY)

        self.screen.blit(msg_surf, msg_surf.get_rect(center=(SCREEN_W // 2, 220)))
        self.screen.blit(sub_surf, sub_surf.get_rect(center=(SCREEN_W // 2, 300)))
        self.screen.blit(r_surf,   r_surf.get_rect(  center=(SCREEN_W // 2, 400)))

    # DRAW: End Screen 
    def _draw_end(self):
        self.screen.fill(DARK_GRAY)
        self._draw_scanlines()

        lines = [
            ("Realm 1 Complete!", NEON_GREEN, self.font_large,  280),
            ("R  to restart    ESC  to quit", MID_GRAY, self.font_medium, 420),
        ]
        for text, color, font, y in lines:
            surf = font.render(text, True, color)
            self.screen.blit(surf, surf.get_rect(center=(SCREEN_W // 2, y)))

        pygame.draw.rect(self.screen, NEON_PINK, (20, 20, SCREEN_W - 40, SCREEN_H - 40), 2)

    # DRAW: Scanline overlay (retro effect)
    def _draw_scanlines(self):
        """Draw subtle horizontal scanlines for a CRT feel."""
        scanline = pygame.Surface((SCREEN_W, 2), pygame.SRCALPHA)
        scanline.fill((0, 0, 0, 40))
        for y in range(0, SCREEN_H, 4):
            self.screen.blit(scanline, (0, y))

#  ENTRY POINT
if __name__ == "__main__":
    game = ArcadeMazeGame()
    game.run()

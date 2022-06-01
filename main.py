import pygame
import random
from config import *

class Paddle(pygame.sprite.Sprite):
  def __init__(self, color, width, height):
    super().__init__()
    self.image = pygame.Surface([width, height])
    self.image.fill(color)
    self.rect = self.image.get_rect()

class Ball(pygame.sprite.Sprite):
  def __init__(self, color, radius):
    super().__init__()
    self.image = pygame.Surface([radius*2, radius*2])
    self.image.fill(color)
    self.rect = self.image.get_rect()

class Particle(pygame.sprite.Sprite):
  def __init__(self, color, location, timer, velocity):
    super().__init__()
    self.timer = timer
    self.velocity = velocity
    self.image = pygame.Surface([timer*2, timer*2])
    self.image.fill(color)
    self.image.set_colorkey(color)
    self.rect = self.image.get_rect()
    self.rect.x = location[0]
    self.rect.y = location[1]

def set_text(string, color, coordx, coordy, fontSize):
  font = pygame.font.Font(FONT_SOURCE, fontSize) 
  text = font.render(string, True, color) 
  textRect = text.get_rect()
  textRect.center = (coordx, coordy) 
  return (text, textRect)

def main():
  score1 = 0
  score2 = 0
  current_round_start = False
  choose_ball_side = False
  goal = False
  
  ballx_velocity = 0
  bally_velocity = 0
  base_ballx_velocity = 1

  debug_message = "Starting game"
  win_message = "Adriel's Pong"
  paused = False

  pygame.init()
  sound_hit = pygame.mixer.Sound(HIT_SOUND[0])
  sound_lose = pygame.mixer.Sound(LOSE_SOUND[0])

  sound_hit.set_volume(HIT_SOUND[1])
  sound_lose.set_volume(LOSE_SOUND[1])
  screen = pygame.display.set_mode((w, h))
  pygame.display.set_caption("Adriel's Pong")

  Icon = pygame.image.load(ICON_SOURCE)
  pygame.display.set_icon(Icon)

  done = False
  clock = pygame.time.Clock()
  sprites = pygame.sprite.Group()
  particles = pygame.sprite.Group()
  paddle1 = Paddle(WHITE, PW, PH)
  paddle2 = Paddle(WHITE, PW, PH)
  ball = Ball(WHITE, BALL_RADIUS)

  paddle1.rect.x = 0
  paddle1.rect.centery = h/2

  paddle2.rect.x = w - PW
  paddle2.rect.centery = h/2

  ball.rect.centerx = w/2
  ball.rect.centery = h/2

  sprites.add(ball)
  sprites.add(paddle1)
  sprites.add(paddle2)

  while not done:
    for event in pygame.event.get():
      if event.type == pygame.USEREVENT:
        current_round_start = False
        goal = False

      if event.type == pygame.QUIT:
        done = True

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          paused = not paused
          sound_lose.play()

        if event.key == pygame.K_q:
          if not current_round_start:
            choose_ball_side = True
            paddle1.rect.centery = h/2
            paddle2.rect.centery = h/2
          current_round_start = True
        if event.key == pygame.K_r and not current_round_start and score1 + score2 != 0:
          score1 = 0
          score2 = 0
          base_ballx_velocity = 10
          paddle1.rect.centery = h/2
          paddle2.rect.centery = h/2
          ball.rect.centerx = w/2
          ball.rect.centery = h/2
          ballx_velocity = 0
          bally_velocity = 0
          debug_message = "Game restarted"
          win_message = "Adriel's Pong"
          sound_lose.play()
    else:
      screen.fill(BLACK)
      # print(ballx_velocity)
      pygame.draw.line(screen, GRAY, [w/2, 0], [w/2, h], 2*SCALE_FACTOR)
      particles.update()
      sprites.update()
      for particle in particles.sprites():
        particle.rect.x += particle.velocity[0]
        particle.rect.y += particle.velocity[1]
        particle.timer -= .1
        particle.velocity = (particle.velocity[0] * .5, particle.velocity[1] * .5)
        pygame.draw.circle(screen, particle.image.get_colorkey(), (particle.rect.x, particle.rect.y), particle.timer)

        if particle.timer <= 0:
          particles.remove(particle)

      particles.draw(screen)
      sprites.draw(screen)      

      score1_text = set_text(str(score1), WHITE, w/4, h/10, TEXT1_SIZE)
      score2_text = set_text(str(score2), WHITE, w/4 + w/2, h/10, TEXT1_SIZE)
      debug_text = set_text(debug_message, WHITE, w/2, h/24, TEXT4_SIZE)

      win_text = set_text(win_message, WHITE, w/2, h/4, TEXT2_SIZE)
      round_text = set_text("Press Q to start", WHITE, w/2, h/4+h/20, TEXT3_SIZE)
      restart_text = set_text("Press R to restart", WHITE, w/2, 3*h/4 - h/20, TEXT3_SIZE)
      pause_text = set_text("Press Esc to pause", WHITE, w/2, 3*h/4, TEXT3_SIZE)

      control1_text = set_text("W S", WHITE, w/4, 7*h/8, TEXT3_SIZE)
      control2_text = set_text("Up Down", WHITE, 3*w/4, 7*h/8, TEXT3_SIZE)

      speed_text = set_text(f"Speed: {str(abs(round(ballx_velocity, 2)))}", WHITE, w/2, h/15, TEXT4_SIZE)
      fill_bg_np = pygame.Surface((w, h), pygame.SRCALPHA)
      fill_bg_np.fill((0, 0, 0, 100))
      if not current_round_start:
        screen.blit(fill_bg_np, (0, 0))
        screen.blit(win_text[0], win_text[1])
        screen.blit(round_text[0], round_text[1])
        screen.blit(control1_text[0], control1_text[1])
        screen.blit(control2_text[0], control2_text[1])
        screen.blit(pause_text[0], pause_text[1])

        if score1 + score2 != 0:
          screen.blit(restart_text[0], restart_text[1])
      else:
        screen.blit(speed_text[0], speed_text[1])

      screen.blit(score1_text[0], score1_text[1])
      screen.blit(score2_text[0], score2_text[1])
      screen.blit(debug_text[0], debug_text[1])

      ball.rect.centery += bally_velocity
      ball.rect.centerx += ballx_velocity

      # handle ball collision with paddle
      if pygame.sprite.collide_rect(ball, paddle1):
        if BALL_XVELOCITY_FASTER_OVER_TIME[0]:
          base_ballx_velocity *= BALL_XVELOCITY_FASTER_OVER_TIME[1]
        ballx_velocity = abs(ballx_velocity+1) + base_ballx_velocity
        bally_velocity = random.randint(-Y_CHANGE_BALL, Y_CHANGE_BALL)
        debug_message = "Collision with paddle 1"
        for i in range(random.randint(15, 25)):
          particles.add(Particle(WHITE, (ball.rect.left, ball.rect.centery), random.randint(0, 15), (random.randint(0, 50), random.randint(-40, 40))))
        sound_hit.play()

      elif pygame.sprite.collide_rect(ball, paddle2):
        if BALL_XVELOCITY_FASTER_OVER_TIME[0]:
          base_ballx_velocity *= BALL_XVELOCITY_FASTER_OVER_TIME[1]
        ballx_velocity = -(abs(ballx_velocity-1) + base_ballx_velocity)
        bally_velocity = random.randint(-Y_CHANGE_BALL, Y_CHANGE_BALL)
        debug_message = "Collision with paddle 2"
        for i in range(random.randint(15, 25)):
          particles.add(Particle(WHITE, (ball.rect.right, ball.rect.centery), random.randint(0, 15), (-random.randint(0, 50), random.randint(-40, 40))))
        sound_hit.play()

      if ball.rect.y <= 0:
        bally_velocity = abs(bally_velocity)
        debug_message = "Collision with top"
        sound_hit.play()

      elif ball.rect.y >= h:
        bally_velocity = -abs(bally_velocity)
        debug_message = "Collision with bottom"
        sound_hit.play()

      if ball.rect.x <= 0:
        for i in range(random.randint(35, 70)):
          particles.add(Particle(YELLOW if i % 2 == 0 else ORANGE, (ball.rect.left, ball.rect.centery), random.randint(10, 20), (random.randint(0, 150), random.randint(-50, 50))))

        debug_message = "Collision with left"
        base_ballx_velocity = 1
        ball.rect.centerx = w/2
        ball.rect.centery = h/2
        ballx_velocity = 0
        bally_velocity = 0
        win_message = "Player 2 Wins!"
        score2 += 1
        goal = True
        sound_lose.play()
        pygame.time.set_timer(pygame.USEREVENT, 1000, 1)

      elif ball.rect.x >= w:
        for i in range(random.randint(35, 70)):
          particles.add(Particle(YELLOW if i % 2 == 0 else ORANGE, (ball.rect.right, ball.rect.centery), random.randint(10, 20), (-random.randint(0, 150), random.randint(-50, 50))))
        
        debug_message = "Collision with right"
        base_ballx_velocity = 1
        ball.rect.centerx = w/2
        ball.rect.centery = h/2
        ballx_velocity = 0
        bally_velocity = 0
        win_message = "Player 1 Wins!"
        score1 += 1
        goal = True
        sound_lose.play()

        pygame.time.set_timer(pygame.USEREVENT, 1000, 1)

      if current_round_start and choose_ball_side:
        sound_hit.play()
        if score1 == score2:
          r = random.randint(0, 1)
          m = ""
          if r: m = "right"
          else: m = "left"

          debug_message = f"Score is tied, choosing random side ({m})"
          if r:
            ballx_velocity += BALL_VELOCITY_DEFAULT
            bally_velocity = random.randint(-Y_CHANGE_BALL, Y_CHANGE_BALL)
          else:
            ballx_velocity -= BALL_VELOCITY_DEFAULT
            bally_velocity = random.randint(-Y_CHANGE_BALL, Y_CHANGE_BALL)
        
        elif score1 < score2:
          debug_message = "Player 1 score is lesser than player 2, choosing right"
          ballx_velocity += BALL_VELOCITY_DEFAULT
          bally_velocity = random.randint(-Y_CHANGE_BALL, Y_CHANGE_BALL)
        else:
          debug_message = "Player 2 score is lesser than player 1, choosing left"
          ballx_velocity -= BALL_VELOCITY_DEFAULT
          bally_velocity = random.randint(-Y_CHANGE_BALL, Y_CHANGE_BALL)

        choose_ball_side = False

      keys = pygame.key.get_pressed()

      if current_round_start and not paused and not goal:
        if keys[pygame.K_w]:
          if paddle1.rect.y > 0:
            paddle1.rect.y -= Y_CHANGE_PADDLE
        if keys[pygame.K_s]:
          if paddle1.rect.y < h - PH:
            paddle1.rect.y += Y_CHANGE_PADDLE
            
        if keys[pygame.K_UP]:
          if paddle2.rect.y > 0:
            paddle2.rect.y -= Y_CHANGE_PADDLE
        if keys[pygame.K_DOWN]:
          if paddle2.rect.y < h - PH:
            paddle2.rect.y += Y_CHANGE_PADDLE

      if paused:
        fill_bg = pygame.Surface((w, h), pygame.SRCALPHA)
        fill_bg.fill((0, 0, 0, 200))
        paused_text = set_text("Game Paused", WHITE, w/2, h/2 - h/25, TEXT1_SIZE)
        paused_text2 = set_text("Press Esc to unpause", WHITE, w/2, h/2 + h/25, TEXT3_SIZE)
        credit_text = set_text("Adriel J. 2022", WHITE, w/2, h - h/15, TEXT3_SIZE)

        screen.blit(fill_bg, (0, 0))
        screen.blit(paused_text[0], paused_text[1])
        screen.blit(paused_text2[0], paused_text2[1])
        screen.blit(credit_text[0], credit_text[1])

    pygame.display.flip()
    clock.tick(60) if not paused else clock.tick(5)

  pygame.quit()

if __name__ == '__main__':
  main()
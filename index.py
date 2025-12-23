import pygame
import random
from pygame.locals import *
class Apple:
    def __init__(self,parent_surface,block):
        self.parent_surface=parent_surface
        self.apple = pygame.image.load("resources/apple-Photoroom.png").convert_alpha()
        self.x,self.y=block.get_width()*3,block.get_width()*3;
        self.block_size = block.get_width()
    
    def draw(self):
        self.parent_surface.blit(self.apple,(self.x,self.y))
    
    def move(self,snake_x,snake_y):
        cols = self.parent_surface.get_width()//self.block_size
        rows = self.parent_surface.get_height()//self.block_size
        while(True):
            x=random.randint(1,cols-1)*self.apple.get_width()
            y=random.randint(1,rows-1)*self.apple.get_width()
            if(x,y) not in zip(snake_x,snake_y):
                self.x=x
                self.y=y
                break

class Snake:
    def __init__(self,parent_screen):
        self.parent_screen=parent_screen
        self.length=3;
        self.block = pygame.image.load("resources/block.jpg").convert() 
        self.block_x,self.block_y=[self.block.get_width()]*self.length,[self.block.get_width()]*self.length
        self.direction='down'

    def draw(self):
        for i in range(0,self.length):
            self.parent_screen.blit(self.block,(self.block_x[i],self.block_y[i]))
    
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.block_x[i]=self.block_x[i-1]
            self.block_y[i]=self.block_y[i-1]
        if(self.direction=='down'):
            self.block_y[0]+=self.block.get_width()
        if(self.direction=='up'):
            self.block_y[0]-=self.block.get_width()
        if(self.direction=='left'):
            self.block_x[0]-=self.block.get_width()
        if(self.direction=='right'):
            self.block_x[0]+=self.block.get_width()
        if(self.block_x[0]<0 or self.block_y[0]<0 or self.block_x[0]>self.parent_screen.get_width()-self.block.get_width() or self.block_y[0]>self.parent_screen.get_height()-self.block.get_height()):
            self.block_x[0]=max(0,min(self.block_x[0],self.parent_screen.get_width()-self.block.get_width()))
            self.block_y[0]=max(0,min(self.block_y[0],self.parent_screen.get_height()-self.block.get_height()))
        self.draw()

class Game:
    def __init__(self): 
        pygame.init()
        pygame.mixer.init() 
        self.surface = pygame.display.set_mode((950,750))
        self.loading_img = pygame.image.load("resources/loading_bg.jpg").convert()
        self.loading_img = pygame.transform.scale(self.loading_img,(self.surface.get_width(),self.surface.get_height()))
        self.background = pygame.image.load("resources/bg.jpg").convert()
        self.background = pygame.transform.scale(self.background,(self.surface.get_width(),self.surface.get_height()))
        pygame.display.set_caption("Snake_Game")
        self.icon = pygame.image.load("resources/icon.png").convert_alpha()
        pygame.display.set_icon(self.icon)
        self.snake=Snake(self.surface)
        self.snake.draw()
        self.apple=Apple(self.surface,self.snake.block)
        self.apple.draw()
        self.clock = pygame.time.Clock()
        self.score=0
        self.MOVE_DELAY = 200 # ms

    def play(self):
        self.surface.fill((255,255,255))
        self.surface.blit(self.background,(0,0))
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        if(self.is_collision(self.snake.block_x[0],self.apple.x,self.snake.block_y[0],self.apple.y)):
            pygame.mixer.Sound.play(pygame.mixer.Sound("resources/ding.mp3"))
            self.apple.move(self.snake.block_x,self.snake.block_y)
            self.snake.length+=1
            self.MOVE_DELAY= max(60,self.MOVE_DELAY-15)
            self.snake.block_x.append(self.snake.block_x[-1])
            self.snake.block_y.append(self.snake.block_y[-1])
            self.score+=1
        for i in range(1,self.snake.length):
            if(self.is_collision(self.snake.block_x[0],self.snake.block_x[i],self.snake.block_y[0],self.snake.block_y[i])):
                pygame.mixer.Sound.play(pygame.mixer.Sound("resources/crash.mp3"))
                raise "error"
            
    def show_game_over(self):
        self.game_over_image = pygame.image.load("resources/end_bg.png").convert_alpha()
        self.game_over_image = pygame.transform.scale(self.game_over_image,(self.surface.get_width(),self.surface.get_height()))
        self.surface.blit(self.game_over_image,(0,0))
        font=pygame.font.SysFont('constantia',30,bold=True)
        line1=font.render(f"Game Over! Your score is {self.score}",True,("crimson"))
        self.surface.blit(line1,(100,180))
        line2=font.render(f"To play again press Enter.",True,((0,0,0)))
        line3=font.render(f"To exit press Escape!",True,((0,0,0)))
        self.surface.blit(line2,(100,230))
        self.surface.blit(line3,(100,290))
        pygame.display.flip()
        pygame.mixer.music.stop()
    
    def game_reset(self):
        self.snake=Snake(self.surface)
        self.apple=Apple(self.surface,self.snake.block)
        self.MOVE_DELAY = 200
        self.score=0

    def display_score(self):
        font=pygame.font.SysFont('constantia',30,bold=True)
        text=font.render(f"score: {self.score}",True,(245,222,179))
        p1,p2=12,8
        box_w=text.get_width()+p1*2
        box_h=text.get_height()+p2*2
        pygame.draw.rect(self.surface, (0, 0, 0),(800,15,box_w,box_h),0,12) #filled background
        pygame.draw.rect(self.surface, (255, 0, 0), (800,15,box_w,box_h), 3, 12) #border
        self.surface.blit(text,(800+p1,13+p2))

    def is_collision(self,x1,x2,y1,y2):
        if(x1==x2 and y1==y2):
            return True
        else:
            return False
        
    def loading_screen(self,ms):
        self.surface.blit(self.loading_img,(0,0))
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()
        pygame.display.flip()
        pygame.time.delay(ms)
       
    def run(self):
        last_move = 0
        self.loading_screen(1800)
        running=True
        pause=False
        while(running):
            for event in pygame.event.get(): 
                if(event.type==KEYDOWN): 
                    if(event.key == K_ESCAPE):
                        print(f"Your final score is {self.score}")
                        running = False 
                    if(event.key == K_RETURN and pause==True):
                        pygame.mixer.music.play() 
                        self.game_reset()
                        pause=False 
                elif event.type == QUIT:
                    print(f"Your final score is {self.score}")
                    running = False
            keys = pygame.key.get_pressed()
            if(keys[K_UP]):
                self.snake.direction='up'
            if(keys[K_DOWN]):
                self.snake.direction='down'
            if(keys[K_LEFT]):
                self.snake.direction='left'
            if(keys[K_RIGHT]):
                self.snake.direction='right'
            now = pygame.time.get_ticks()
            if now - last_move > self.MOVE_DELAY:
                try:
                    if not pause:
                        self.play()
                        last_move = now
                except Exception:
                    self.show_game_over()
                    pause=True
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()    
    pygame.quit()
import pygame,sys
from setting import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)

        self.import_assets()

        self.status='down_idle'
        self.frame_index=0

        self.image=self.animations[self.status][self.frame_index]
        self.rect=self.image.get_rect(center=pos)

        self.direction=pygame.math.Vector2()
        self.pos=pygame.math.Vector2(self.rect.center)
        self.speed=200

        self.timers={
            'tool_use':Timer(350,self.use_tool)
        }

        self.selected_tool='axe'

    def use_tool(self):
        print(self.selected_tool)

    def import_assets(self):
        self.animations={
            'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
		    'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
            'right_water':[],'left_water':[],'up_water':[],'down_water':[]
        }

        for animation in self.animations.keys():
            full_path="../assets/graphics/character/"+animation
            self.animations[animation]=import_folder(full_path)

    def animate(self,dt):
        self.frame_index+=4*dt
        if self.frame_index>=len(self.animations[self.status]):
            self.frame_index=0
        self.image=self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys=pygame.key.get_pressed()

        if not self.timers['tool_use'].active:
            if keys[pygame.K_w]:
                self.direction.y=-1
                self.status='up'
            elif keys[pygame.K_s]:
                self.direction.y=1
                self.status = 'down'
            else:
                self.direction.y=0


            if keys[pygame.K_a]:
                self.direction.x=-1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x=1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_m]:
                self.timers['tool_use'].activate()
                self.direction=pygame.math.Vector2()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit(0)

    def get_status(self):
        if self.direction.magnitude()==0:
            self.status=self.status.split('_')[0]+'_idle'

        if self.timers['tool_use'].active:
            self.status = self.status.split('_')[0] +'_'+ self.selected_tool

    def move(self,dt):
        if self.direction.magnitude()>0:
            self.direction=self.direction.normalize()

        self.pos.x+=self.direction.x*self.speed*dt
        self.rect.centerx=self.pos.x

        self.pos.y+=self.direction.y*self.speed*dt
        self.rect.centery=self.pos.y

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)
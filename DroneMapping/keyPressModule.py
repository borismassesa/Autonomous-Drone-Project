import pygame

def init():
    pygame.init()
    window = pygame.display.set_mode((600, 600))

def getKey(keyName):
    output = False
    for event in pygame.event.get():
        pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, f'K_{keyName}')

    if keyInput[myKey]:
        output = True
    pygame.display.update()

    return output

def main():
    if getKey("LEFT"):
        print("Left key pressed")
    if getKey("RIGHT"):
        print("Right key pressed")

if __name__ == "__main__":
    init()
    while True:
        main()
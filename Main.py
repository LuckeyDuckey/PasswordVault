import pygame, PYRA, math, time, sys, random, os
from pygame.locals import *
import numpy as np

from Scripts.AppObject import AppObject
from Scripts.PasswordListElement import PasswordListElement
from Scripts.PasswordAddElement import PasswordAddElement
from Scripts.PasswordEditElement import PasswordEditElement

class App:
    def __init__(self, PasswordVault):
        pygame.init()
        pygame.display.set_caption("Password Vault")

        self.ScreenResolution = PYRA.Vec2([870, 780])
        self.Screen = pygame.display.set_mode(self.ScreenResolution)

        self.Clock = pygame.time.Clock()
        self.FpsCap = 140
        self.DeltaTime = 1 / self.FpsCap
        self.LastTime = time.time()

        AppObject.App = self
        self.PasswordVault = PasswordVault
        self.LoadApp()

        # Allow keys to repeat for text inputs
        pygame.key.set_repeat(500, 33)
        pygame.key.start_text_input()

    def LoadApp(self):
        from Scripts.BackgroundGlowEffect import BackgroundGlowEffect

        self.BackgroundGlowEffect = BackgroundGlowEffect(self.ScreenResolution * 0.5, PYRA.Vec2([1000, 1000]), [55, 55, 255], 0.1)

        from Scripts.NavigationBarElement import NavigationBarElement

        self.NavigationBarElement = NavigationBarElement()
        self.PageElement = PasswordListElement()

    def SwitchToListPage(self):
        if isinstance(self.PageElement, PasswordListElement):
            return

        self.PageElement = PasswordListElement()

    def SwitchToAddPage(self):
        if isinstance(self.PageElement, PasswordAddElement):
            return

        self.PageElement = PasswordAddElement()

    def SwitchToEditPage(self, PasswordRecord):
        if isinstance(self.PageElement, PasswordEditElement):
            return

        self.PageElement = PasswordEditElement(PasswordRecord)

    def Run(self):
        while True:
            self.Clock.tick(self.FpsCap)
            self.DeltaTime = time.time() - self.LastTime
            self.LastTime = time.time()
            
            MousePosition = PYRA.Vec2(pygame.mouse.get_pos())
            PygameEvents = pygame.event.get()
            PYRA.CursorState = pygame.SYSTEM_CURSOR_ARROW
            
            self.Screen.fill([38, 39, 43])

            self.NavigationBarElement.Container.Render(self.Screen, MousePosition, PygameEvents, self.DeltaTime)
            self.PageElement.Container.Render(self.Screen, MousePosition, PygameEvents, self.DeltaTime)
            
            self.BackgroundGlowEffect.Render(self.Screen, MousePosition, self.DeltaTime)

            pygame.mouse.set_cursor(PYRA.CursorState)
            pygame.display.update()

            for Event in PygameEvents:
                if Event.type == QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    import getpass
    from cryptography.fernet import InvalidToken
    from Scripts.PasswordVault import PasswordVault

    while True:
        MasterPassword = getpass.getpass("Enter master password: ")

        try:
            Vault = PasswordVault(MasterPassword)
            break
        except InvalidToken:
            print("Invalid master password, please try again.\n")

    App(Vault).Run()

import pygame, os, PYRA
from pygame.locals import *

# Note to self (self.TextInputFont, 20).size(" ") = [12, 23]

class AbstractElement:
    PrimaryContainerColor = [43, 44, 48]
    SecondaryContainerColor = [55, 55, 60]
    ShadowColor = [0, 0, 0]

    PrimaryTextColor = [255, 255, 255]
    SecondaryTextColor = [150, 150, 150]
    PreviewTextColor = [200, 200, 200]
    WarningTextColor = [255, 100, 100]

    IconButtonBaseColor = [255, 255, 255, 0]
    IconButtonHoveringColor = [255, 255, 255, 20]
    IconButtonClickingColor = [255, 255, 255, 35]

    TextButtonBaseColor = [25, 25, 30]
    TextButtonHoveringColor = [35, 35, 40]
    TextButtonClickingColor = [40, 40, 45]

    GeneralFont = "segoeuivariable"
    TextInputFont = "monospace"

    @staticmethod
    def DefaultEasingFunction(Time):
        return 4 * pow(Time, 3) if Time < 0.5 else 1 - pow(-2 * Time + 2, 3) / 2

    def CreateContainer(self):
        raise NotImplementedError("Child classes must implement CreateContainer()")

    def BuildChildElements(self):
        raise NotImplementedError("Child classes must implement BuildChildElements()")

    def LoadGenericIcon(self, FileName, IconSize):
        FilePath = f"{os.getcwd()}/Data/GenericIcons/{FileName}.png"
        GenericIcon = pygame.image.load(FilePath).convert_alpha()
        return pygame.transform.smoothscale(GenericIcon, IconSize)

    def LoadPasswordIcon(self, FilePath, IconSize):
        RawPasswordIcon = pygame.image.load(FilePath).convert_alpha()
        RawPasswordIconSize = PYRA.Vec2(RawPasswordIcon.get_size())
        MinRawPasswordIconSize = min(RawPasswordIconSize)

        # Clip and scale the image
        ClippedPasswordIcon = RawPasswordIcon.subsurface((RawPasswordIconSize - MinRawPasswordIconSize) * 0.5, PYRA.Vec2(MinRawPasswordIconSize))
        ScaledPasswordIcon = pygame.transform.smoothscale(ClippedPasswordIcon, IconSize)

        # Create rounded mask
        RoundedAlphaMask = pygame.Surface(IconSize).convert_alpha()
        RoundedAlphaMask.fill([0, 0, 0, 0])
        pygame.draw.rect(RoundedAlphaMask, [255, 255, 255], pygame.Rect(PYRA.Vec2(0), IconSize), border_radius=5)

        # Apply mask
        RoundedAlphaMask.blit(ScaledPasswordIcon, PYRA.Vec2(0), special_flags=pygame.BLEND_RGBA_MULT)
        return RoundedAlphaMask

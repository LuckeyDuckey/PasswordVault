import pygame, os, PYRA

from .AppObject import AppObject
from .AbstractElement import AbstractElement

class PasswordElement(AppObject, AbstractElement):
    def __init__(self, PasswordRecord):
        self.PasswordRecord = PasswordRecord
        self.PasswordIcon = self.LoadPasswordIcon(f"{os.getcwd()}/Data/PasswordIcons/{self.PasswordRecord['SiteName']}.png", PYRA.Vec2([40, 40]))

        self.GenericCopyIcon = self.LoadGenericIcon("CopyIcon", PYRA.Vec2([16, 16]))
        self.GenericSettingsIcon = self.LoadGenericIcon("SettingsIcon", PYRA.Vec2([20, 20]))

        self.Container = self.CreateContainer()
        self.Container.CalculateChildPositions()

    def CreateContainer(self):
        return PYRA.ContainerElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 15, 0, 0],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([720, 60]),
                Color = self.SecondaryContainerColor,
                CornerRadius = 5,
            ),
            ChildElementsParameters = PYRA.ChildElementsParameters(
                ChildElements = self.BuildChildElements(),
                Direction = "Horizontal",
                AlignContent = "Center",
                JustifyContent = "Start",
            ),
        )

    def BuildChildElements(self):
        return [
            self.CreatePasswordIconElement(),
            self.CreateSiteInformationContainer(),
            self.CreateUsernameTextElement(),
            self.CreateUsernameCopyElement(),
            self.CreatePasswordTextElement(),
            self.CreatePasswordCopyButtonElement(),
            self.CreateSettingsButtonElement(),
        ]

    def CreatePasswordIconElement(self):
        return PYRA.ImageElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 10, 0]
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2(50),
            ),
            ImageParameters = PYRA.ImageParameters(
                Image = self.PasswordIcon,
            ),
        )

    def CreateSiteInformationContainer(self):
        return PYRA.ContainerElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 10, 0],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([140, 40]),
            ),
            ChildElementsParameters = PYRA.ChildElementsParameters(
                ChildElements = [
                    self.CreateSiteNameTextElement(),
                    self.CreateCommentTextElement(),
                ],
                Direction = "Vertical",
                AlignContent = "Start",
                JustifyContent = "Center",
            ),
        )

    def CreateSiteNameTextElement(self):
        return PYRA.TextElement(
            PositionParameters = PYRA.PositionParameters(
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([150, 20]),
            ),
            TextParameters = PYRA.TextParameters(
                Text = self.PasswordRecord["SiteName"],
                Font = pygame.font.SysFont(self.GeneralFont, 15, bold=True),
                Color = self.PrimaryTextColor,
                Anchor = PYRA.Vec2([0, 0.5]),
            ),
        )

    def CreateCommentTextElement(self):
        return PYRA.TextElement(
            PositionParameters = PYRA.PositionParameters(
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([150, 20]),
            ),
            TextParameters = PYRA.TextParameters(
                Text = self.PasswordRecord["Comment"],
                Font = pygame.font.SysFont(self.GeneralFont, 12),
                Color = self.SecondaryTextColor,
                Anchor = PYRA.Vec2([0, 0.5]),
            ),
        )

    def CreateUsernameTextElement(self):
        return PYRA.TextElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 10, 0]
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([180, 20]),
            ),
            TextParameters = PYRA.TextParameters(
                Text = self.PasswordRecord["Username"],
                Font = pygame.font.SysFont(self.GeneralFont, 12),
                Color = self.SecondaryTextColor,
                Anchor = PYRA.Vec2([0, 0.5]),
            ),
        )

    def CreateUsernameCopyElement(self):
        return PYRA.ButtonElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 10, 0]
            ),
            ButtonParameters = PYRA.ButtonParameters(
                Callback = lambda Username = self.PasswordRecord["Username"] : pygame.scrap.put_text(Username),
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2(26),
                CornerRadius = 3,
            ),
            ImageParameters = PYRA.ImageParameters(
                Image = self.GenericCopyIcon,
            ),
            HoverAnimation = PYRA.HoverAnimation(
                AnimationParameters = PYRA.AnimationParameters(
                    Duration = 0.15,
                    EasingFunction = self.DefaultEasingFunction,
                ),
                OriginalColor = self.IconButtonBaseColor,
                HoverColor = self.IconButtonHoveringColor,
            ),
            ClickingAnimation = PYRA.ClickingAnimation(
                AnimationParameters = PYRA.AnimationParameters(
                    Duration = 0.05,
                    EasingFunction = self.DefaultEasingFunction,
                ),
                OriginalColor = self.IconButtonBaseColor,
                ClickingColor = self.IconButtonClickingColor,
            ),
        )

    def CreatePasswordTextElement(self):
        return PYRA.TextElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 10, 0]
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([180, 20]),
            ),
            TextParameters = PYRA.TextParameters(
                Text = self.PasswordRecord["Password"],
                Font = pygame.font.SysFont(self.GeneralFont, 12),
                Color = self.SecondaryTextColor,
                Anchor = PYRA.Vec2([0, 0.5]),
            ),
        )

    def CreatePasswordCopyButtonElement(self):
        return PYRA.ButtonElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 10, 0]
            ),
            ButtonParameters = PYRA.ButtonParameters(
                Callback = lambda Password = self.PasswordRecord["Password"] : pygame.scrap.put_text(Password),
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2(26),
                CornerRadius = 3,
            ),
            ImageParameters = PYRA.ImageParameters(
                Image = self.GenericCopyIcon,
            ),
            HoverAnimation = PYRA.HoverAnimation(
                AnimationParameters = PYRA.AnimationParameters(
                    Duration = 0.15,
                    EasingFunction = self.DefaultEasingFunction,
                ),
                OriginalColor = self.IconButtonBaseColor,
                HoverColor = self.IconButtonHoveringColor,
            ),
            ClickingAnimation = PYRA.ClickingAnimation(
                AnimationParameters = PYRA.AnimationParameters(
                    Duration = 0.05,
                    EasingFunction = self.DefaultEasingFunction,
                ),
                OriginalColor = self.IconButtonBaseColor,
                ClickingColor = self.IconButtonClickingColor,
            ),
        )

    def CreateSettingsButtonElement(self):
        return PYRA.ButtonElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 15, 0]
            ),
            ButtonParameters = PYRA.ButtonParameters(
                Callback = lambda PasswordRecord = self.PasswordRecord : self.App.SwitchToEditPage(PasswordRecord),
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2(20),
            ),
            ImageParameters = PYRA.ImageParameters(
                Image = self.GenericSettingsIcon,
            ),
        )

class PasswordListElement(AppObject, AbstractElement):
    def __init__(self):
        self.Container = self.CreateContainer()
        self.Container.CalculateChildPositions()

    def CreateContainer(self):
        return PYRA.ContainerElement(
            PositionParameters = PYRA.PositionParameters(
                Position = PYRA.Vec2([105, 15]),
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([750, 750]),
                Color = self.PrimaryContainerColor,
                CornerRadius = 5,
                ShadowParameters = PYRA.ShadowParameters(
                    Size = 20,
                    Color = self.ShadowColor,
                    Intensity = 50
                ),
            ),
            ChildElementsParameters = PYRA.ChildElementsParameters(
                ChildElements = self.BuildChildElements(),
                Direction = "Vertical",
                JustifyContent = "Start",
                AlignContent = "Center",
                Scrollable = True,
                Padding = [15, 15, 15, 15]
            ),
        )

    def BuildChildElements(self):
        ChildElements = []

        for PasswordRecord in self.App.PasswordVault.PasswordRecords:
            ChildElements.append(PasswordElement(PasswordRecord).Container)

        if len(ChildElements):
            ChildElements[-1].PositionParameters.Margin[1] = 0
            
        return ChildElements

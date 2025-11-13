import pygame, os, math, PYRA

import tkinter as tk
from tkinter import filedialog

from .AppObject import AppObject
from .AbstractElement import AbstractElement

class PasswordAddElement(AppObject, AbstractElement):
    def __init__(self):
        self.GenericUploadIcon = self.LoadGenericIcon("UploadIcon", PYRA.Vec2([32, 32]))
        self.PasswordIcon = self.GetGenericPasswordIcon()

        self.Container = self.CreateContainer()
        self.Container.CalculateChildPositions()

    def GetGenericPasswordIcon(self):
        PasswordIconSize = PYRA.Vec2([120, 120])
        PasswordIcon = pygame.Surface(PasswordIconSize).convert_alpha()
        PasswordIcon.fill([0, 0, 0, 0])

        # Draw the generic icon image
        pygame.draw.rect(PasswordIcon, [105, 105, 105], pygame.Rect(PYRA.Vec2(0), PasswordIconSize), border_radius=5)
        pygame.draw.aacircle(PasswordIcon, [155, 155, 155], PasswordIconSize * 0.5, 25)
        pygame.draw.aacircle(PasswordIcon, [155, 155, 155], PasswordIconSize * PYRA.Vec2([0.5, 1.175]), 50)

        return PasswordIcon

    def DrawDashedLine(self, Surface, StartPosition, EndPosition, StepSize=10, Width=3, Color=[75, 75, 75]):
        PositionDifference = EndPosition - StartPosition
        LineDistance = math.sqrt(pow(PositionDifference.x, 2) + pow(PositionDifference.y, 2))
        PositionDifference /= LineDistance
        
        CurrentDistance = 0
        while CurrentDistance < LineDistance:
            DashStartPosition = StartPosition + PositionDifference * (CurrentDistance + StepSize * 0.25)
            DashEndPosition = StartPosition + PositionDifference * (CurrentDistance + StepSize * 0.75)
            
            pygame.draw.line(Surface, Color, DashStartPosition, DashEndPosition, Width)
            CurrentDistance += StepSize

    def GetIconUploadButton(self):
        PasswordIconSize = PYRA.Vec2([120, 120])
        PasswordIconSurface = self.PasswordIcon.copy()
        PasswordIconSurface.blit(self.GenericUploadIcon, (PasswordIconSize - PYRA.Vec2(self.GenericUploadIcon.get_size())) * 0.5)

        UploadButtonSize = PYRA.Vec2([380, 160])
        UploadButtonSurface = pygame.Surface(UploadButtonSize).convert_alpha()
        UploadButtonSurface.fill([0, 0, 0, 0])

        # Top side, Bottom side, Left side, Right side
        self.DrawDashedLine(UploadButtonSurface, PYRA.Vec2([0, 0]), PYRA.Vec2([UploadButtonSize.x - 1, 0])) 
        self.DrawDashedLine(UploadButtonSurface, PYRA.Vec2([UploadButtonSize.x - 1, UploadButtonSize.y - 1]), PYRA.Vec2([0, UploadButtonSize.y - 1]))
        self.DrawDashedLine(UploadButtonSurface, PYRA.Vec2([0, UploadButtonSize.y - 1]), PYRA.Vec2([0, 0]))
        self.DrawDashedLine(UploadButtonSurface, PYRA.Vec2([UploadButtonSize.x - 1, 0]), PYRA.Vec2([UploadButtonSize.x - 1, UploadButtonSize.y - 1]))

        UploadButtonSurface.blit(PasswordIconSurface, (UploadButtonSize - PasswordIconSize) * 0.5)

        return UploadButtonSurface

    def ClickedIconUploadButton(self):
        TkinterRoot = tk.Tk()
        TkinterRoot.withdraw()

        ImageFilePath = filedialog.askopenfilename(
            title = "Select an Image",
            filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp")],
        )

        TkinterRoot.destroy()
        if not ImageFilePath:
            return
            
        self.PasswordIcon = self.LoadPasswordIcon(ImageFilePath, PYRA.Vec2([120, 120]))
        self.IconUploadButton.ImageParameters.Image = self.GetIconUploadButton()
        self.IconUploadButton.RenderSurfaceCache()

    def ClickedCreateButton(self):
        if not all(InputText and InputText.strip() for InputText in [
            self.SiteNameInput.UserInputText,
            self.CommentsInput.UserInputText,
            self.UsernameInput.UserInputText,
            self.PasswordInput.UserInputText,
        ]):
            self.InvalidInputsText.TextParameters.Color = self.WarningTextColor
            self.InvalidInputsText.RenderSurfaceCache()

            return

        self.App.PasswordVault.AddPassword({
            "SiteName": self.SiteNameInput.UserInputText,
            "Comment": self.CommentsInput.UserInputText,
            "Username": self.UsernameInput.UserInputText,
            "Password": self.PasswordInput.UserInputText,
        })

        pygame.image.save(self.PasswordIcon, f"{os.getcwd()}/Data/PasswordIcons/{self.SiteNameInput.UserInputText}.png")

        self.App.SwitchToListPage()

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
        return [
            self.CreateTitleTextElement(),
            self.CreateIconUploadButtonElement(),
            self.CreateSiteInformationTitlesContainerElement(),
            self.CreateSiteInformationInputsContainerElement(),
            self.CreateUsernameTitleElement(),
            self.CreateUsernameInputElement(),
            self.CreatePasswordTitleElement(),
            self.CreatePasswordInputElement(),
            self.CreateActionButtonsContainerElement(),
            self.CreateInvalidInputsTextElement(),
        ]

    def CreateTitleTextElement(self):
        return PYRA.TextElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [85, 25, 0, 0],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([180, 20]),
            ),
            TextParameters = PYRA.TextParameters(
                Text = "Add Password",
                Font = pygame.font.SysFont(self.GeneralFont, 25, True),
                Color = [255, 255, 255],
                Anchor = PYRA.Vec2([0.5, 0.5]),
            ),
        )

    def CreateIconUploadButtonElement(self):
        self.IconUploadButton = PYRA.ButtonElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 20, 0, 0],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([380, 160]),
                Color = self.SecondaryContainerColor,
                CornerRadius = 5,
                ShadowParameters = PYRA.ShadowParameters(
                    Size = 5,
                    Color = self.ShadowColor,
                    Intensity = 25
                ),
            ),
            ButtonParameters = PYRA.ButtonParameters(
                Callback = self.ClickedIconUploadButton,
            ),
            ImageParameters = PYRA.ImageParameters(
                Image = self.GetIconUploadButton(),
                Anchor = PYRA.Vec2([0.5, 0.5]),
            ),
            HoverAnimation = PYRA.HoverAnimation(
                AnimationParameters = PYRA.AnimationParameters(
                    Duration = 0.15,
                    EasingFunction = self.DefaultEasingFunction,
                ),
                OriginalColor = self.SecondaryContainerColor,
                HoverColor = [60, 60, 65],
            ),
            ClickingAnimation = PYRA.ClickingAnimation(
                AnimationParameters = PYRA.AnimationParameters(
                    Duration = 0.05,
                    EasingFunction = self.DefaultEasingFunction,
                ),
                OriginalColor = self.SecondaryContainerColor,
                ClickingColor = [65, 65, 70],
            ),
        )

        return self.IconUploadButton

    def CreateSiteInformationTitlesContainerElement(self):
        return PYRA.ContainerElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 10, 0, 0],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([380, 20]),
            ),
            ChildElementsParameters = PYRA.ChildElementsParameters(
                ChildElements = [
                    self.CreateSiteNameTitleElement(),
                    self.CreateCommentsTitleElement(),
                ],
                Direction = "Horizontal",
            ),
        )

    def CreateSiteNameTitleElement(self):
        return PYRA.TextElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 0, 15],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([183, 20]),
            ),
            TextParameters = PYRA.TextParameters(
                Text = "Site Name",
                Font = pygame.font.SysFont(self.GeneralFont, 15, True),
                Color = [255, 255, 255],
                Anchor = PYRA.Vec2([0, 0.5]),
            ),
        )

    def CreateCommentsTitleElement(self):
        return PYRA.TextElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 0, 15],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([183, 20]),
            ),
            TextParameters = PYRA.TextParameters(
                Text = "Comment",
                Font = pygame.font.SysFont(self.GeneralFont, 15, True),
                Color = [255, 255, 255],
                Anchor = PYRA.Vec2([0, 0.5]),
            ),
        )

    def CreateSiteInformationInputsContainerElement(self):
        return PYRA.ContainerElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 15, 0, 0],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([380, 45]),
            ),
            ChildElementsParameters = PYRA.ChildElementsParameters(
                ChildElements = [
                    self.CreateSiteNameInputElement(),
                    self.CreateCommentsInputElement(),
                ],
                Direction = "Horizontal",
            ),
        )

    def CreateSiteNameInputElement(self):
        self.SiteNameInput = PYRA.TextInputElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 0, 15],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([183, 45]),
                Color = self.SecondaryContainerColor,
                CornerRadius = 5,
                ShadowParameters = PYRA.ShadowParameters(
                    Size = 5,
                    Color = self.ShadowColor,
                    Intensity = 25
                ),
            ),
            TextInputParameters = PYRA.TextInputParameters(
                Callback = lambda UserTextInput : None,
                CharacterLength = 13,
                PreviewText = "Site Name",
                Font = pygame.font.SysFont(self.TextInputFont, 20),
                TextColor = self.PrimaryTextColor,
                PreviewTextColor = self.PreviewTextColor,
            ),
        )

        return self.SiteNameInput

    def CreateCommentsInputElement(self):
        self.CommentsInput = PYRA.TextInputElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 0, 15],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([183, 45]),
                Color = self.SecondaryContainerColor,
                CornerRadius = 5,
                ShadowParameters = PYRA.ShadowParameters(
                    Size = 5,
                    Color = self.ShadowColor,
                    Intensity = 25
                ),
            ),
            TextInputParameters = PYRA.TextInputParameters(
                Callback = lambda UserTextInput : None,
                CharacterLength = 13,
                PreviewText = "Comment",
                Font = pygame.font.SysFont(self.TextInputFont, 20),
                TextColor = self.PrimaryTextColor,
                PreviewTextColor = self.PreviewTextColor,
            ),
        )

        return self.CommentsInput

    def CreateUsernameTitleElement(self):
        return PYRA.TextElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 10, 0, 0],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([380, 20]),
            ),
            TextParameters = PYRA.TextParameters(
                Text = "Username",
                Font = pygame.font.SysFont(self.GeneralFont, 15, True),
                Color = [255, 255, 255],
                Anchor = PYRA.Vec2([0, 0.5]),
            ),
        )

    def CreateUsernameInputElement(self):
        self.UsernameInput = PYRA.TextInputElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 15, 0, 0],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([380, 45]),
                Color = self.SecondaryContainerColor,
                CornerRadius = 5,
                ShadowParameters = PYRA.ShadowParameters(
                    Size = 5,
                    Color = self.ShadowColor,
                    Intensity = 25
                ),
            ),
            TextInputParameters = PYRA.TextInputParameters(
                Callback = lambda UserTextInput : None,
                CharacterLength = 30,
                PreviewText = "Username",
                Font = pygame.font.SysFont(self.TextInputFont, 20),
                TextColor = self.PrimaryTextColor,
                PreviewTextColor = self.PreviewTextColor,
            ),
        )

        return self.UsernameInput

    def CreatePasswordTitleElement(self):
        return PYRA.TextElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 10, 0, 0],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([380, 20]),
            ),
            TextParameters = PYRA.TextParameters(
                Text = "Password",
                Font = pygame.font.SysFont(self.GeneralFont, 15, True),
                Color = [255, 255, 255],
                Anchor = PYRA.Vec2([0, 0.5]),
            ),
        )

    def CreatePasswordInputElement(self):
        self.PasswordInput = PYRA.TextInputElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 15, 0, 0],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([380, 45]),
                Color = self.SecondaryContainerColor,
                CornerRadius = 5,
                ShadowParameters = PYRA.ShadowParameters(
                    Size = 5,
                    Color = self.ShadowColor,
                    Intensity = 25
                ),
            ),
            TextInputParameters = PYRA.TextInputParameters(
                Callback = lambda UserTextInput : None,
                CharacterLength = 30,
                PreviewText = "Password",
                Font = pygame.font.SysFont(self.TextInputFont, 20),
                TextColor = self.PrimaryTextColor,
                PreviewTextColor = self.PreviewTextColor,
            ),
        )

        return self.PasswordInput

    def CreateActionButtonsContainerElement(self):
        return PYRA.ContainerElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [10, 15, 0, 0],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([380, 45]),
            ),
            ChildElementsParameters = PYRA.ChildElementsParameters(
                ChildElements = [
                    self.CreateCancelButtonElement(),
                    self.CreateCreateButtonElement(),
                ],
                Direction = "Horizontal",
            ),
        )

    def CreateCancelButtonElement(self):
        return PYRA.ButtonElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 0, 15],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([183, 45]),
                Color = self.TextButtonBaseColor,
                CornerRadius = 5,
                ShadowParameters = PYRA.ShadowParameters(
                    Size = 5,
                    Color = self.ShadowColor,
                    Intensity = 25
                ),
            ),
            ButtonParameters = PYRA.ButtonParameters(
                Callback = self.App.SwitchToListPage,
            ),
            TextParameters = PYRA.TextParameters(
                Text = "Cancel",
                Font = pygame.font.SysFont(self.GeneralFont, 20),
                Color = [255, 255, 255],
            ),
            HoverAnimation = PYRA.HoverAnimation(
                AnimationParameters = PYRA.AnimationParameters(
                    Duration = 0.15,
                    EasingFunction = self.DefaultEasingFunction,
                ),
                OriginalColor = self.TextButtonBaseColor,
                HoverColor = self.TextButtonHoveringColor,
            ),
            ClickingAnimation = PYRA.ClickingAnimation(
                AnimationParameters = PYRA.AnimationParameters(
                    Duration = 0.05,
                    EasingFunction = self.DefaultEasingFunction,
                ),
                OriginalColor = self.TextButtonBaseColor,
                ClickingColor = self.TextButtonClickingColor,
            ),
        )
        
    def CreateCreateButtonElement(self):
        return PYRA.ButtonElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 0, 0, 15],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([183, 45]),
                Color = self.TextButtonBaseColor,
                CornerRadius = 5,
                ShadowParameters = PYRA.ShadowParameters(
                    Size = 5,
                    Color = self.ShadowColor,
                    Intensity = 25
                ),
            ),
            ButtonParameters = PYRA.ButtonParameters(
                Callback = self.ClickedCreateButton,
            ),
            TextParameters = PYRA.TextParameters(
                Text = "Create",
                Font = pygame.font.SysFont(self.GeneralFont, 20),
                Color = [255, 255, 255],
            ),
            HoverAnimation = PYRA.HoverAnimation(
                AnimationParameters = PYRA.AnimationParameters(
                    Duration = 0.15,
                    EasingFunction = self.DefaultEasingFunction,
                ),
                OriginalColor = self.TextButtonBaseColor,
                HoverColor = self.TextButtonHoveringColor,
            ),
            ClickingAnimation = PYRA.ClickingAnimation(
                AnimationParameters = PYRA.AnimationParameters(
                    Duration = 0.05,
                    EasingFunction = self.DefaultEasingFunction,
                ),
                OriginalColor = self.TextButtonBaseColor,
                ClickingColor = self.TextButtonClickingColor,
            ),
        )

    def CreateInvalidInputsTextElement(self):
        self.InvalidInputsText = PYRA.TextElement(
            PositionParameters = PYRA.PositionParameters(
                Margin = [0, 10, 0, 0],
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([380, 20]),
            ),
            TextParameters = PYRA.TextParameters(
                Text = "* please provide a value for all input fields *",
                Font = pygame.font.SysFont(self.GeneralFont, 15, True),
                Color = self.PrimaryContainerColor,
                Anchor = PYRA.Vec2([0.5, 0.5]),
            ),
        )

        return self.InvalidInputsText

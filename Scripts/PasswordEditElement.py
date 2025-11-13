import pygame, os, math, PYRA

import tkinter as tk
from tkinter import filedialog

from .AppObject import AppObject
from .AbstractElement import AbstractElement

class PasswordEditElement(AppObject, AbstractElement):
    def __init__(self, PasswordRecord):
        self.PasswordRecord = PasswordRecord

        self.GenericUploadIcon = self.LoadGenericIcon("UploadIcon", PYRA.Vec2([32, 32]))
        self.PasswordIcon = self.LoadPasswordIcon(f"{os.getcwd()}/Data/PasswordIcons/{self.PasswordRecord['SiteName']}.png", PYRA.Vec2([120, 120]))

        self.Container = self.CreateContainer()
        self.Container.CalculateChildPositions()

        self.SiteNameInput.UserInputText = self.PasswordRecord["SiteName"]
        self.CommentsInput.UserInputText = self.PasswordRecord["Comment"]
        self.UsernameInput.UserInputText = self.PasswordRecord["Username"]
        self.PasswordInput.UserInputText = self.PasswordRecord["Password"]

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

    def ClickedSaveButton(self):
        if not all(InputText and InputText.strip() for InputText in [
            self.SiteNameInput.UserInputText,
            self.CommentsInput.UserInputText,
            self.UsernameInput.UserInputText,
            self.PasswordInput.UserInputText,
        ]) or (
            self.SiteNameInput.UserInputText != self.PasswordRecord["SiteName"] and
            [PasswordRecord for PasswordRecord in self.App.PasswordVault.PasswordRecords if PasswordRecord["SiteName"] == self.SiteNameInput.UserInputText]
        ):
            self.InvalidInputsText.TextParameters.Color = self.WarningTextColor
            self.InvalidInputsText.RenderSurfaceCache()

            return

        self.App.PasswordVault.EditPassword(self.PasswordRecord, {
            "SiteName": self.SiteNameInput.UserInputText,
            "Comment": self.CommentsInput.UserInputText,
            "Username": self.UsernameInput.UserInputText,
            "Password": self.PasswordInput.UserInputText,
        })

        pygame.image.save(self.PasswordIcon, f"{os.getcwd()}/Data/PasswordIcons/{self.SiteNameInput.UserInputText}.png")

        self.App.SwitchToListPage()

    def ClickedDeleteButton(self):
        self.App.PasswordVault.DeletePassword(self.PasswordRecord)
        os.remove(f"{os.getcwd()}/Data/PasswordIcons/{self.PasswordRecord['SiteName']}.png")

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
                Text = "Edit Password",
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
                    self.CreateDeleteButtonElement(),
                    self.CreateSaveButtonElement(),
                ],
                Direction = "Horizontal",
            ),
        )

    def CreateDeleteButtonElement(self):
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
                Callback = self.ClickedDeleteButton,
            ),
            TextParameters = PYRA.TextParameters(
                Text = "Delete",
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
        
    def CreateSaveButtonElement(self):
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
                Callback = self.ClickedSaveButton,
            ),
            TextParameters = PYRA.TextParameters(
                Text = "Save",
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
                Text = "* all fields required or site name already exists *",
                Font = pygame.font.SysFont(self.GeneralFont, 15, True),
                Color = self.PrimaryContainerColor,
                Anchor = PYRA.Vec2([0.5, 0.5]),
            ),
        )

        return self.InvalidInputsText

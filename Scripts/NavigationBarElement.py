import os, PYRA

from .AppObject import AppObject
from .AbstractElement import AbstractElement

class NavigationBarElement(AppObject, AbstractElement):
    def __init__(self):
        self.GenericHomeIcon = self.LoadGenericIcon("HomeIcon", PYRA.Vec2([26, 26]))
        self.GenericAddIcon = self.LoadGenericIcon("AddIcon", PYRA.Vec2([26, 26]))

        self.Container = self.CreateContainer()
        self.Container.CalculateChildPositions()

    def CreateContainer(self):
        return PYRA.ContainerElement(
            PositionParameters = PYRA.PositionParameters(
                Position = PYRA.Vec2([15, 15]),
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2([75, 750]),
                Color = self.PrimaryContainerColor,
                CornerRadius = 5,
                ShadowParameters = PYRA.ShadowParameters(
                    Size = 20,
                    Color = self.ShadowColor,
                    Intensity = 50
                ),
            ),
            ChildElementsParameters = PYRA.ChildElementsParameters(
                ChildElements = self.BuildChildElements()
            ),
        )

    def BuildChildElements(self):
        return [
            self.CreateHomeButtonElement(),
            self.CreateAddButtonElement(),
        ]

    def CreateHomeButtonElement(self):
        return PYRA.ButtonElement(
            PositionParameters = PYRA.PositionParameters(
                Position = PYRA.Vec2([10, 10]),
            ),
            ButtonParameters = PYRA.ButtonParameters(
                Callback = self.App.SwitchToListPage,
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2(55),
                CornerRadius = 3,
            ),
            ImageParameters = PYRA.ImageParameters(
                Image = self.GenericHomeIcon,
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
                ClickingColor = [255, 255, 255, 35],
            ),
        )

    def CreateAddButtonElement(self):
        return PYRA.ButtonElement(
            PositionParameters = PYRA.PositionParameters(
                Position = PYRA.Vec2([10, 740]),
                Anchor = PYRA.Vec2([0, 1.0]),
            ),
            ButtonParameters = PYRA.ButtonParameters(
                Callback = self.App.SwitchToAddPage,
            ),
            ContainerParameters = PYRA.ContainerParameters(
                Resolution = PYRA.Vec2(55),
                CornerRadius = 3,
            ),
            ImageParameters = PYRA.ImageParameters(
                Image = self.GenericAddIcon,
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
                ClickingColor = [255, 255, 255, 35],
            ),
        )

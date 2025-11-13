import pygame, random, PYRA
from pygame.locals import *
import numpy as np

class BackgroundGlowEffect:
    def __init__(self, StartPosition, GlowResolution, Color, Intensity):
        self.Position = StartPosition
        self.Resolution = GlowResolution
        self.GlowSurface = self.GenerateGlowSurface(Color, Intensity)
        
    def GenerateGlowSurface(self, Color, Intensity):
        # Generate normalized coordinate grids (0 to 1 range)
        CoordsX, CoordsY = np.meshgrid(
            np.linspace(0, 1, self.Resolution.x, dtype=np.float64),
            np.linspace(0, 1, self.Resolution.y, dtype=np.float64),
            indexing='ij'  # Ensures correct shape [x, y]
        )

        # Calculate glow intensity
        DistanceFromCenter = np.sqrt(pow(CoordsX - 0.5, 2) + pow(CoordsY - 0.5, 2))
        GlowIntensity = (0.5 - DistanceFromCenter) * 2 * Intensity

        # Apply color
        SurfaceArray = np.full((self.Resolution.x, self.Resolution.y, 3), Color, dtype=np.float64)
        SurfaceArray *= GlowIntensity[:, :, None]

        # Apply dithering to remove banding
        DitherNoise = np.random.uniform(-0.5, 0.5, SurfaceArray.shape)
        SurfaceArray = np.clip(SurfaceArray + DitherNoise, 0, 255)
        
        return pygame.surfarray.make_surface(SurfaceArray.astype(np.uint8)).convert_alpha()

    def Render(self, Display, MousePosition, DeltaTime):
        self.Position = self.Position + (MousePosition - self.Position) * min(10 * DeltaTime, 1)
        Display.blit(self.GlowSurface, self.Position - self.Resolution * 0.5, special_flags=BLEND_ADD)

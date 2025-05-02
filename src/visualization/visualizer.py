from abc import ABC

import matplotlib
import matplotlib.image as mpimg


class Visualizer(ABC):
    @staticmethod
    def _render_image(
        image_path: str,
        ax: matplotlib.axes.Axes,
    ) -> None:
        """Load an image and display it in the given axis grid position."""
        if image_path:
            img = mpimg.imread(image_path)
            ax.imshow(img)

    def _render_cell(
        self,
        image_path: str,
        ax: matplotlib.axes.Axes,
        show_axis: bool = False,
    ):
        if image_path:
            self._render_image(image_path=image_path, ax=ax)

        if not show_axis:
            ax.axis("off")

        ax.set_xticks([])
        ax.set_yticks([])

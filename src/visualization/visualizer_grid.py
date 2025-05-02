from matplotlib import pyplot as plt

from src.dataclass.grid import Grid
from src.dataclass.mask import Mask
from src.dataclass.point import Point
from src.repository.repository import Repository
from src.visualization.visualizer import Visualizer

OFFSET = 0.15


class VisualizerGrid(Visualizer):
    def draw(
        self,
        grid: Grid,
        repository: Repository,
        title: str = None,
        show_borders: bool = False,
        save_path: str | None = None,
        show: bool = False,
    ):
        nrows, ncols = grid.height, grid.width
        fig, ax = plt.subplots(
            nrows, ncols,
            figsize=(ncols, nrows),
        )

        if title:
            fig.suptitle(title)

        for x, y in grid.cells():
            cell_ax = ax[x, y]

            mask = Mask(pattern=grid.get_cells_around_point(Point(x=x, y=y)))
            cell = repository.get_cell_by_mask(mask=mask)
            image = cell.asset

            self._render_cell(
                image_path=image,
                ax=cell_ax,
                axis=show_borders,
            )

        plt.subplots_adjust(
            left=OFFSET,
            right=1 - OFFSET,
            bottom=OFFSET,
            top=1-OFFSET,
            hspace=0,
            wspace=0,
        )

        if save_path:
            plt.savefig(save_path, bbox_inches="tight", pad_inches=0)
        if show:
            plt.show()

        plt.close()


vis_grid = VisualizerGrid()

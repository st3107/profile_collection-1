import os
import time

import pandas as pd
import scipy.spatial.

from ophyd.sim import Syn2DGauss

omnia_xy_index_fp = "omnia_xy_index.txt"


class OmniaDetector(Syn2DGauss):
    def __init__(self, dbr, **kwargs):
        super().__init__(**kwargs)

        self.dbr = dbr
        if not os.path.exists(omnia_xy_index_fp):
            self.build_image_index()
        print(f"loading {omnia_xy_index_fp}")
        self.omnia_xy_index = pd.read_csv(
            omnia_xy_index_fp,
            sep="\t",
            header=0,
            index_col=0
        )

    def _compute(self):
        """
        Grid_X: 8.903
        Grid_Y: 768.94725
        sample_name: omnia
        """
        x = self._motor0.read()[self._motor_field0]['value']
        y = self._motor1.read()[self._motor_field1]['value']

        d = np.linalg.norm(self.omnia_xy_index['Grid_X', 'Grid_Y'] - )

    def build_image_index(self):
        print(f"creating {omnia_xy_index_fp}")
        t0 = time.time()
        grid_x = list()
        grid_y = list()
        uids = list()
        for h in self.dbr(sample_name='omnia'):
            grid_x.append(h.start["Grid_X"])
            grid_y.append(h.start["Grid_Y"])
            uids.append(h.start["uid"])

        df = pd.DataFrame(
            zip(grid_x, grid_y, uids),
            columns=("Grid_X", "Grid_Y", "uid")
        )
        df.to_csv(omnia_xy_index_fp, sep="\t")
        print(f"finished {omnia_xy_index_fp} in {time.time()-t0:.3}s")

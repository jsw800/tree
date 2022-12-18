import open3d


class TestTree(object):
    def __init__(self, points):
        import numpy as np
        self.points = points
        self.pcd = open3d.geometry.PointCloud()
        self.pcd.points = open3d.utility.Vector3dVector(self.points)
        self.vis = open3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(self.pcd)
        self.vis.run()
        opt = self.vis.get_render_option()
        opt.point_size = 7.5
        opt.background_color = np.asarray([0.1, 0.1, 0.1])

    def off(self):
        pass

    async def render_frame(self, rgb):
        self.pcd.colors = open3d.utility.Vector3dVector(rgb)
        self.vis.update_geometry(self.pcd)
        self.vis.update_renderer()
        self.vis.poll_events()

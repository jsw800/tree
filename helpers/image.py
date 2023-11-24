def process_image(points_3d, image):
    height, width, _ = image.shape

    x_min, x_max = points_3d[:,0].min(), points_3d[:,0].max()
    z_min, z_max = points_3d[:,2].min(), points_3d[:,2].max()

    xs = ((points_3d[:,0] - x_min) / (x_max - x_min) * (width - 1)).astype(int)
    zs = (1 - ((points_3d[:,2] - z_min) / (z_max - z_min))) * (height - 1)
    zs = zs.astype(int)

    colors = image[zs, xs]
    colors = colors[:, ::-1] / 255.0

    return colors

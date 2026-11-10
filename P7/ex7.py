
# Ex7: Pontos pertencentes a superfícies verticais (fachadas).
# Novo em relação ao ex6: uma superfície vertical tem normal horizontal, ou seja,
# θ ≈ 90°. Selecionam-se os pontos com |θ - 90°| < 10° e pintam-se a azul.

# imports --------------------
import argparse
from copy import deepcopy
import json
import random
import signal
import sys
from matplotlib import cm
from more_itertools import locate
import numpy as np
import open3d as o3d
import os

viewpoint = {
        "class_name" : "ViewTrajectory",
        "interval" : 29,
        "is_loop" : False,
        "trajectory" :
        [
                {
                        "boundingbox_max" : [ 6.5291471481323242, 34.024543762207031, 11.225864410400391 ],
                        "boundingbox_min" : [ -39.714397430419922, -16.512752532958984, -1.9472264051437378 ],
                        "field_of_view" : 60.0,
                        "front" : [ 0.90252725336848205, -0.21154048236017059, 0.37509356332783211 ],
                        "lookat" : [ -14.316933984735199, 2.1757857601535933, -0.14616852344082723 ],
                        "up" : [ -0.36710972183730356, 0.077374890705278865, 0.92695392464829884 ],
                        "zoom" : 0.3630252075195311
                }
        ],
        "version_major" : 1,
        "version_minor" : 0
}

# Main function
def main(): # this is our main function
    print("SAVI exercise")

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    # initialize argparser
    script_dir = os.path.dirname(os.path.abspath(__file__))

    ap = argparse.ArgumentParser()
    ap.add_argument("-pcf", "--point_cloud_file", type=str, required=False,
                    default=os.path.join(script_dir, "factory_no_floor.pcd"),
                    help="Path to the point cloud file")
    ap.add_argument("-mnp", "--max_num_planes", type=int, required=False,
                    default=15)
     
     
    args = ap.parse_args()
    args = vars(args) # transform the args into a dictionary
    print('Input args: ' + str(args))

    # Load the point cloud
    point_cloud = o3d.io.read_point_cloud(args['point_cloud_file'])
    print('Point cloud: ' + str(point_cloud))

    # -------------------------------------------------------------------------
    # Downsampling
    # -------------------------------------------------------------------------
    point_cloud_sampled = point_cloud.voxel_down_sample(voxel_size=0.2)

    # point_cloud_sampled.estimate_normals(search_params=o3d.geometry.KDTreeSearchParamHybrid(0.5, max_nn=30))
    point_cloud_sampled.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.5, max_nn=30))
    point_cloud_sampled.orient_normals_to_align_with_direction(orientation_reference=np.array([0, 0, 1]))

    # -------------------------------------------------------------------------
    # Visualization
    # -------------------------------------------------------------------------
    # Create drawing entities
    # entities = [point_cloud_sampled]
    # entities.extend(point_cloud_of_groups)

    normals = np.asarray(point_cloud_sampled.normals)   # (N, 3)
    z = np.array([0, 0, 1])

    # theta = arccos( n.z / (||n|| * ||z||) )
    cos_theta = (normals @ z) / (np.linalg.norm(normals, axis=1) * np.linalg.norm(z))
    theta = np.arccos(np.clip(cos_theta, -1.0, 1.0))    # radianos

    # Pontos com normal próxima da horizontal (θ ≈ 90°) -> superfícies verticais
    angle_threshold = np.deg2rad(10)   # tolerância de ±10°
    idxs = np.where(np.abs(theta - np.pi / 2) < angle_threshold)[0].tolist()

    point_cloud_vertical = point_cloud_sampled.select_by_index(idxs)
    point_cloud_vertical.paint_uniform_color([0, 0, 1])  # azul

    point_cloud_rest = point_cloud_sampled.select_by_index(idxs, invert=True)

    # -------------------------------------------------------------------------
    # Visualization
    # -------------------------------------------------------------------------
    entities = [point_cloud_rest, point_cloud_vertical]

    o3d.visualization.draw_geometries(entities,
                                      zoom=0.34,
                                      front=viewpoint['trajectory'][0]['front'],
                                      lookat=viewpoint['trajectory'][0]['lookat'],
                                      up=viewpoint['trajectory'][0]['up'])

      
if __name__ == "__main__":
    main()





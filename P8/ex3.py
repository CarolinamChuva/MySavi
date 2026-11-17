# ---------------------------------------------------------------------------
# Resumo - Parte 8, Ex3: registo global (FPFH + RANSAC) e refinamento com ICP
#
# - Downsampling das duas nuvens (voxel_size), estimativa de normais e
#   cálculo das features FPFH de cada ponto.
# - Transformação inicial automática com RANSAC a partir das associações
#   entre features (registration_ransac_based_on_feature_matching).
# - Refinamento com ICP point-to-plane (como no Ex2), a partir do RANSAC,
#   com threshold pequeno, usando as nuvens originais.
# - Erro face a T_true (translação em mm, rotação em graus) depois do
#   RANSAC e depois do ICP, com fitness e inlier_rmse.
#
# Conclusões:
# - O RANSAC global dá uma estimativa inicial razoável sem intervenção
#   manual (substitui o T_init do Ex2 e o alinhamento do Ex1); o ICP
#   refina-a e reduz o erro.
# - O resultado depende do voxel_size e é aleatório (várias execuções
#   podem dar resultados diferentes).
# ---------------------------------------------------------------------------
import json
import copy
from pathlib import Path
import numpy as np
import open3d as o3d

DIR = Path(__file__).parent
VOXEL = 0.05  # ajustar (ex.: 0.03 a 0.1 m)

src = o3d.io.read_point_cloud(str(DIR / "part_2.ply"))
tgt = o3d.io.read_point_cloud(str(DIR / "part_1.ply"))
T_true = np.array(json.load(open(DIR / "T_true.json"))["T_part_1_part_2"], dtype=float)

def draw(source, target, T):
    s, t = copy.deepcopy(source), copy.deepcopy(target)
    s.paint_uniform_color([1, 0.7, 0])
    t.paint_uniform_color([0, 0.65, 0.93])
    s.transform(T)
    o3d.visualization.draw_geometries([s, t])

def error(T):
    E = np.linalg.inv(T_true) @ T
    t_mm = np.linalg.norm(E[:3, 3]) * 1000
    ang = np.degrees(np.arccos(np.clip((np.trace(E[:3, :3]) - 1) / 2, -1, 1)))
    return t_mm, ang

def report(name, res):
    t, a = error(res.transformation)
    print(f"{name:10s} fit={res.fitness:.3f} rmse={res.inlier_rmse:.4f} "
          f"err_t={t:9.1f} mm err_r={a:7.2f}°")

def preprocess(pcd, voxel):
    down = pcd.voxel_down_sample(voxel)
    down.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 2, max_nn=30))
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        down, o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 5, max_nn=100))
    return down, fpfh

# 1) downsampling + normais + FPFH
src_down, src_fpfh = preprocess(src, VOXEL)
tgt_down, tgt_fpfh = preprocess(tgt, VOXEL)

# 2) RANSAC global
dist = VOXEL * 1.5
ransac = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
    src_down, tgt_down, src_fpfh, tgt_fpfh, True, dist,
    o3d.pipelines.registration.TransformationEstimationPointToPoint(False), 3,
    [o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
     o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(dist)],
    o3d.pipelines.registration.RANSACConvergenceCriteria(1000000, 0.999))
report("RANSAC", ransac)
draw(src, tgt, ransac.transformation)

# 3) ICP point-to-plane a partir do RANSAC (nuvens originais, com normais)
for pc in (src, tgt):
    pc.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

icp = o3d.pipelines.registration.registration_icp(
    src, tgt, 0.02, ransac.transformation,
    o3d.pipelines.registration.TransformationEstimationPointToPlane())
report("ICP", icp)
draw(src, tgt, icp.transformation)
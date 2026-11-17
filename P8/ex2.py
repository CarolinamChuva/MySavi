
# ---------------------------------------------------------------------------
# Resumo - Parte 8, Ex2: ICP com Open3D (part_2.ply -> part_1.ply)
#
# - Carrega as duas nuvens (source = part_2, target = part_1) e o T_true.json.
# - Estima as normais (necessárias para o ICP point-to-plane).
# - draw(): mostra as duas nuvens juntas, cada uma de uma cor.
# - error(): calcula o erro face a T_true, com E = inv(T_true) @ T
#   (translação em mm; rotação em graus, via arccos((tr(R_E) - 1) / 2)).
# - ICP point-to-point e point-to-plane a partir da identidade, com
#   thresholds 0.02, 0.05 e 0.2 m.
# - Estimativa inicial manual (T_init) e novo ICP; depois refinamento com
#   threshold 0.02 m a partir do resultado anterior.
# - Imprime fitness, inlier_rmse e erros para cada caso.


import json
import copy
import numpy as np
import open3d as o3d
from pathlib import Path

DIR = Path(__file__).parent   # pasta onde está o ex2.py (P8)

src = o3d.io.read_point_cloud(str(DIR / "part_2.ply"))
tgt = o3d.io.read_point_cloud(str(DIR / "part_1.ply"))
T_true = np.array(json.load(open(DIR / "T_true.json"))["T_part_1_part_2"], dtype=float)

# Normais (necessárias para point-to-plane)
for pc in (src, tgt):
    pc.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

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

P2P = o3d.pipelines.registration.TransformationEstimationPointToPoint()
P2L = o3d.pipelines.registration.TransformationEstimationPointToPlane()
crit = o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=200)

def run(T_init, thr, method):
    return o3d.pipelines.registration.registration_icp(src, tgt, thr, T_init, method, crit)

def report(name, res):
    t, a = error(res.transformation)
    print(f"{name:42s} fit={res.fitness:.3f} rmse={res.inlier_rmse:.4f} "
          f"err_t={t:9.1f} mm err_r={a:7.2f}°")

# 1) visualização inicial
draw(src, tgt, np.eye(4))

# 2) ICP a partir da identidade
for thr in (0.02, 0.05, 0.2):
    for name, m in (("p2p", P2P), ("p2l", P2L)):
        report(f"identidade, thr={thr}, {name}", run(np.eye(4), thr, m))

# 3) estimativa inicial manual -> SUBSTITUIR pela matriz do CloudCompare / à mão
T_init = np.eye(4)   # <-- colocar aqui a estimativa grosseira
draw(src, tgt, T_init)

results = {}
for name, m in (("p2p", P2P), ("p2l", P2L)):
    r1 = run(T_init, 0.2, m)                       # com limiar largo
    report(f"init manual, thr=0.2, {name}", r1)
    r2 = run(r1.transformation, 0.02, m)           # refinar com limiar pequeno
    report(f"init manual -> thr=0.02, {name}", r2)
    results[name] = r2

# visualizar o melhor resultado
draw(src, tgt, results["p2l"].transformation)
import unreal
import json
from pathlib import Path

anatomy_map_path = r"C:\Users\Dipenshu\Desktop\Codes\MRI3D\results\UCSF_PDGM_0232_nifti\meshes\anatomy_map.json"
tumor_map_path   = r"C:\Users\Dipenshu\Desktop\Codes\MRI3D\results\UCSF_PDGM_0232_nifti\meshes\tumor_map.json"
mesh_content_path = "/Game/Meshes/"

with open(anatomy_map_path) as f:
    anatomy_map = json.load(f)
with open(tumor_map_path) as f:
    tumor_map = json.load(f)

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
editor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
mat_factory = unreal.MaterialInstanceConstantFactoryNew()
parent_material = unreal.load_asset("/Game/Materials/M_BrainBase")

asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
assets = asset_registry.get_assets_by_path(mesh_content_path, recursive=True)

mesh_map = {}
for a in assets:
    if "StaticMesh" in str(a.asset_class_path):
        mesh_map[str(a.asset_name)] = a.get_asset()

print(f"Found {len(mesh_map)} meshes")

ANATOMY_COLORS = {
    # ── Ventricles ──────────────────────────────────────────────────────────
    "3rd_Ventricle":                          (0.50, 0.62, 0.76),
    "4th_Ventricle":                          (0.48, 0.60, 0.74),
    "Right_Lateral_Ventricle":                (0.52, 0.64, 0.77),
    "Left_Lateral_Ventricle":                 (0.52, 0.64, 0.77),
    "Right_Inf_Lat_Vent":                     (0.54, 0.66, 0.74),
    "Left_Inf_Lat_Vent":                      (0.54, 0.66, 0.74),

    # ── Cerebellum exterior ──────────────────────────────────────────────────
    "Right_Cerebellum_Exterior":              (0.55, 0.70, 0.60),
    "Left_Cerebellum_Exterior":               (0.55, 0.70, 0.60),
    "Cerebellar_Vermal_Lobules_I_V":          (0.58, 0.72, 0.62),
    "Cerebellar_Vermal_Lobules_VI_VII":       (0.58, 0.72, 0.62),
    "Cerebellar_Vermal_Lobules_VIII_X":       (0.58, 0.72, 0.62),

    # ── Cerebellum white matter ──────────────────────────────────────────────
    "Right_Cerebellum_White_Matter":          (0.68, 0.76, 0.65),
    "Left_Cerebellum_White_Matter":           (0.68, 0.76, 0.65),

    # ── Cerebral white matter ────────────────────────────────────────────────
    "Right_Cerebral_White_Matter":            (0.82, 0.80, 0.73),
    "Left_Cerebral_White_Matter":             (0.82, 0.80, 0.73),

    # ── Brain stem ───────────────────────────────────────────────────────────
    "Brain_Stem":                             (0.68, 0.62, 0.53),

    # ── Basal ganglia ────────────────────────────────────────────────────────
    "Right_Caudate":                          (0.64, 0.59, 0.74),
    "Left_Caudate":                           (0.64, 0.59, 0.74),
    "Right_Putamen":                          (0.62, 0.57, 0.72),
    "Left_Putamen":                           (0.62, 0.57, 0.72),
    "Right_Pallidum":                         (0.60, 0.54, 0.68),
    "Left_Pallidum":                          (0.60, 0.54, 0.68),
    "Right_Accumbens_Area":                   (0.67, 0.58, 0.67),
    "Left_Accumbens_Area":                    (0.67, 0.58, 0.67),

    # ── Thalamus / Ventral DC ────────────────────────────────────────────────
    "Right_Thalamus_Proper":                  (0.52, 0.67, 0.67),
    "Left_Thalamus_Proper":                   (0.52, 0.67, 0.67),
    "Right_Ventral_DC":                       (0.55, 0.68, 0.68),
    "Left_Ventral_DC":                        (0.55, 0.68, 0.68),

    # ── Hippocampus ──────────────────────────────────────────────────────────
    "Right_Hippocampus":                      (0.75, 0.65, 0.50),
    "Left_Hippocampus":                       (0.75, 0.65, 0.50),

    # ── Amygdala ─────────────────────────────────────────────────────────────
    "Right_Amygdala":                         (0.72, 0.59, 0.52),
    "Left_Amygdala":                          (0.72, 0.59, 0.52),

    # ── Basal forebrain ──────────────────────────────────────────────────────
    "Right_Basal_Forebrain":                  (0.72, 0.60, 0.62),
    "Left_Basal_Forebrain":                   (0.72, 0.60, 0.62),

    # ── Frontal cortex ───────────────────────────────────────────────────────
    "Right_MFC_medial_frontal_cortex":        (0.76, 0.63, 0.65),
    "Left_MFC_medial_frontal_cortex":         (0.76, 0.63, 0.65),
    "Right_MFG_middle_frontal_gyrus":         (0.74, 0.62, 0.64),
    "Left_MFG_middle_frontal_gyrus":          (0.74, 0.62, 0.64),
    "Right_SFG_superior_frontal_gyrus":       (0.76, 0.64, 0.66),
    "Left_SFG_superior_frontal_gyrus":        (0.76, 0.64, 0.66),
    "Right_MSFG_superior_frontal_gyrus":      (0.75, 0.63, 0.65),
    "Left_MSFG_superior_frontal_gyrus":       (0.75, 0.63, 0.65),
    "Right_FRP_frontal_pole":                 (0.77, 0.64, 0.66),
    "Left_FRP_frontal_pole":                  (0.77, 0.64, 0.66),

    # ── Motor cortex ─────────────────────────────────────────────────────────
    "Right_MPrG_precentral_gyrus":            (0.76, 0.67, 0.57),
    "Left_MPrG_precentral_gyrus":             (0.76, 0.67, 0.57),
    "Right_PrG_precentral_gyrus":             (0.74, 0.66, 0.56),
    "Left_PrG_precentral_gyrus":              (0.74, 0.66, 0.56),
    "Right_SMC_supplementary_motor_cortex":   (0.75, 0.67, 0.58),
    "Left_SMC_supplementary_motor_cortex":    (0.75, 0.67, 0.58),

    # ── Somatosensory / postcentral ──────────────────────────────────────────
    "Right_MPoG_postcentral_gyrus":           (0.78, 0.71, 0.62),
    "Left_MPoG_postcentral_gyrus":            (0.78, 0.71, 0.62),
    "Right_PoG_postcentral_gyrus":            (0.76, 0.70, 0.61),
    "Left_PoG_postcentral_gyrus":             (0.76, 0.70, 0.61),

    # ── Parietal cortex ──────────────────────────────────────────────────────
    "Right_PCu_precuneus":                    (0.58, 0.67, 0.76),
    "Left_PCu_precuneus":                     (0.58, 0.67, 0.76),
    "Right_SPL_superior_parietal_lobule":     (0.57, 0.66, 0.75),
    "Left_SPL_superior_parietal_lobule":      (0.57, 0.66, 0.75),
    "Right_AnG_angular_gyrus":                (0.59, 0.68, 0.76),
    "Left_AnG_angular_gyrus":                 (0.59, 0.68, 0.76),
    "Right_SMG_supramarginal_gyrus":          (0.57, 0.67, 0.74),
    "Left_SMG_supramarginal_gyrus":           (0.57, 0.67, 0.74),
    "Right_PO__parietal_operculum":           (0.58, 0.65, 0.73),
    "Left_PO__parietal_operculum":            (0.58, 0.65, 0.73),

    # ── Temporal cortex ──────────────────────────────────────────────────────
    "Right_STG_superior_temporal_gyrus":      (0.67, 0.73, 0.58),
    "Left_STG_superior_temporal_gyrus":       (0.67, 0.73, 0.58),
    "Right_MTG_middle_temporal_gyrus":        (0.66, 0.72, 0.57),
    "Left_MTG_middle_temporal_gyrus":         (0.66, 0.72, 0.57),
    "Right_ITG_inferior_temporal_gyrus":      (0.65, 0.71, 0.57),
    "Left_ITG_inferior_temporal_gyrus":       (0.65, 0.71, 0.57),
    "Right_TMP_temporal_pole":                (0.68, 0.74, 0.59),
    "Left_TMP_temporal_pole":                 (0.68, 0.74, 0.59),
    "Right_TTG_transverse_temporal_gyrus":    (0.66, 0.71, 0.58),
    "Left_TTG_transverse_temporal_gyrus":     (0.66, 0.71, 0.58),

    # ── Occipital cortex ─────────────────────────────────────────────────────
    "Right_SOG_superior_occipital_gyrus":     (0.64, 0.59, 0.75),
    "Left_SOG_superior_occipital_gyrus":      (0.64, 0.59, 0.75),
    "Right_MOG_middle_occipital_gyrus":       (0.63, 0.58, 0.74),
    "Left_MOG_middle_occipital_gyrus":        (0.63, 0.58, 0.74),
    "Right_IOG_inferior_occipital_gyrus":     (0.62, 0.57, 0.73),
    "Left_IOG_inferior_occipital_gyrus":      (0.62, 0.57, 0.73),
    "Right_OCP_occipital_pole":               (0.65, 0.60, 0.75),
    "Left_OCP_occipital_pole":                (0.65, 0.60, 0.75),
    "Right_Calc_calcarine_cortex":            (0.61, 0.61, 0.74),
    "Left_Calc_calcarine_cortex":             (0.61, 0.61, 0.74),
    "Right_Cun_cuneus":                       (0.62, 0.62, 0.74),
    "Left_Cun_cuneus":                        (0.62, 0.62, 0.74),
    "Right_LiG_lingual_gyrus":               (0.61, 0.61, 0.73),
    "Left_LiG_lingual_gyrus":                (0.61, 0.61, 0.73),
    "Right_OFuG_occipital_fusiform_gyrus":    (0.63, 0.60, 0.72),
    "Left_OFuG_occipital_fusiform_gyrus":     (0.63, 0.60, 0.72),

    # ── Cingulate cortex ─────────────────────────────────────────────────────
    "Right_ACgG_anterior_cingulate_gyrus":    (0.76, 0.64, 0.59),
    "Left_ACgG_anterior_cingulate_gyrus":     (0.76, 0.64, 0.59),
    "Right_MCgG_middle_cingulate_gyrus":      (0.75, 0.63, 0.58),
    "Left_MCgG_middle_cingulate_gyrus":       (0.75, 0.63, 0.58),
    "Right_PCgG_posterior_cingulate_gyrus":   (0.74, 0.63, 0.58),
    "Left_PCgG_posterior_cingulate_gyrus":    (0.74, 0.63, 0.58),

    # ── Orbital / prefrontal cortex ──────────────────────────────────────────
    "Right_AOrG_anterior_orbital_gyrus":      (0.76, 0.70, 0.54),
    "Left_AOrG_anterior_orbital_gyrus":       (0.76, 0.70, 0.54),
    "Right_LOrG_lateral_orbital_gyrus":       (0.75, 0.70, 0.54),
    "Left_LOrG_lateral_orbital_gyrus":        (0.75, 0.70, 0.54),
    "Right_MOrG_medial_orbital_gyrus":        (0.76, 0.71, 0.55),
    "Left_MOrG_medial_orbital_gyrus":         (0.76, 0.71, 0.55),
    "Right_POrG_posterior_orbital_gyrus":     (0.74, 0.69, 0.53),
    "Left_POrG_posterior_orbital_gyrus":      (0.74, 0.69, 0.53),
    "Right_GRe_gyrus_rectus":                 (0.75, 0.70, 0.54),
    "Left_GRe_gyrus_rectus":                  (0.75, 0.70, 0.54),
    "Right_OrIFG_orbital_part_of_the_IFG":   (0.74, 0.69, 0.53),
    "Left_OrIFG_orbital_part_of_the_IFG":    (0.74, 0.69, 0.53),

    # ── Insula / operculum ───────────────────────────────────────────────────
    "Right_AIns_anterior_insula":             (0.68, 0.59, 0.68),
    "Left_AIns_anterior_insula":              (0.68, 0.59, 0.68),
    "Right_PIns_posterior_insula":            (0.67, 0.58, 0.67),
    "Left_PIns_posterior_insula":             (0.67, 0.58, 0.67),
    "Right_CO__central_operculum":            (0.67, 0.59, 0.67),
    "Left_CO__central_operculum":             (0.67, 0.59, 0.67),
    "Right_FO__frontal_operculum":            (0.68, 0.59, 0.68),
    "Left_FO__frontal_operculum":             (0.68, 0.59, 0.68),

    # ── IFG variants ─────────────────────────────────────────────────────────
    "Right_OpIFG_opercular_part_of_the_IFG": (0.72, 0.62, 0.65),
    "Left_OpIFG_opercular_part_of_the_IFG":  (0.72, 0.62, 0.65),
    "Right_TrIFG_triangular_part_of_the_IFG":(0.71, 0.61, 0.64),
    "Left_TrIFG_triangular_part_of_the_IFG": (0.71, 0.61, 0.64),

    # ── Fusiform / parahippocampal / entorhinal ──────────────────────────────
    "Right_FuG_fusiform_gyrus":               (0.65, 0.68, 0.57),
    "Left_FuG_fusiform_gyrus":                (0.65, 0.68, 0.57),
    "Right_PHG_parahippocampal_gyrus":        (0.66, 0.69, 0.58),
    "Left_PHG_parahippocampal_gyrus":         (0.66, 0.69, 0.58),
    "Right_Ent_entorhinal_area":              (0.67, 0.70, 0.58),
    "Left_Ent_entorhinal_area":               (0.67, 0.70, 0.58),

    # ── Planum ───────────────────────────────────────────────────────────────
    "Right_PP__planum_polare":                (0.58, 0.68, 0.67),
    "Left_PP__planum_polare":                 (0.58, 0.68, 0.67),
    "Right_PT__planum_temporale":             (0.58, 0.67, 0.66),
    "Left_PT__planum_temporale":              (0.58, 0.67, 0.66),

    # ── Subcallosal area / poles ─────────────────────────────────────────────
    "Right_SCA_subcallosal_area":             (0.66, 0.62, 0.67),
    "Left_SCA_subcallosal_area":              (0.66, 0.62, 0.67),
}

DEFAULT_ANATOMY_COLOR = (0.68, 0.68, 0.68)


def get_anatomy_color(label_name):
    """Return (r, g, b) for a given anatomy label name."""
    return ANATOMY_COLORS.get(label_name, DEFAULT_ANATOMY_COLOR)


def spawn_mesh(mesh_name, label, r, g, b, opacity=1.0):
    mesh = mesh_map.get(mesh_name)
    if not mesh:
        return False
    actor = editor_subsystem.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(0, 0, 50),
        unreal.Rotator(0, 0, 0)
    )
    smc = actor.get_component_by_class(unreal.StaticMeshComponent)
    smc.set_static_mesh(mesh)
    actor.set_actor_label(label)
    mat = asset_tools.create_asset(
        f"M_{mesh_name}",
        "/Game/Materials",
        unreal.MaterialInstanceConstant,
        mat_factory
    )
    mat.set_editor_property("parent", parent_material)
    unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(
        mat, "BaseColor", unreal.LinearColor(r, g, b, 1.0)
    )
    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(
        mat, "Opacity", opacity
    )
    unreal.EditorAssetLibrary.save_asset(mat.get_path_name())
    smc.set_material(0, mat)
    return True


spawned = 0

if spawn_mesh("brain_shell", "Brain_Shell", 0.78, 0.78, 0.78, opacity=0.25):
    spawned += 1
    print("Spawned brain shell")

for label_id_str, info in anatomy_map.items():
    mesh_name = Path(info["file"]).stem
    label_name = info["name"]
    r, g, b = get_anatomy_color(label_name)
    if spawn_mesh(mesh_name, f"Anatomy_{mesh_name}", r, g, b, opacity=1.0):
        spawned += 1

for name, info in tumor_map.items():
    mesh_name = Path(info["file"]).stem
    r, g, b = info["color_rgb_0_1"]
    if spawn_mesh(mesh_name, f"Tumor_{name}", r, g, b, opacity=1.0):
        spawned += 1

print(f"Total spawned: {spawned} actors")
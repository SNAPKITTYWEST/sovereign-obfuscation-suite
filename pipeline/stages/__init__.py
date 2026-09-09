"""Pipeline stage registrations."""
from .stage_01_observable import stage_observable_boundary
from .stage_02_latent import stage_latent_geometry
from .stage_03_functor import stage_functor_reduction
from .stage_04_neural_math import stage_neural_math
from .stage_05_ast import stage_ast_representation
from .stage_06_xml import stage_xml_routing
from .stage_07_binary import stage_binary_stream
from .stage_08_integrity import stage_integrity_invariants
from .stage_09_agda import stage_agda_formalization
from .stage_10_rpg import stage_rpg_agent
from .stage_11_sparse import stage_sparse_activation
from .stage_12_neural_match import stage_neural_matching
from .stage_13_compute import stage_compute_monitor
from .stage_14_mirror import stage_mirror_space
from .stage_15_emergent import stage_emergent_behavior
from .stage_16_safety import stage_safety_axioms
from .stage_17_axiom_inv import stage_axiom_inversion
from .stage_18_parallel import stage_parallel_mirror
from .stage_19_async import stage_async_router
from .stage_20_orchestrator import stage_python_orchestration

ALL_STAGES = {
    1: stage_observable_boundary,
    2: stage_latent_geometry,
    3: stage_functor_reduction,
    4: stage_neural_math,
    5: stage_ast_representation,
    6: stage_xml_routing,
    7: stage_binary_stream,
    8: stage_integrity_invariants,
    9: stage_agda_formalization,
    10: stage_rpg_agent,
    11: stage_sparse_activation,
    12: stage_neural_matching,
    13: stage_compute_monitor,
    14: stage_mirror_space,
    15: stage_emergent_behavior,
    16: stage_safety_axioms,
    17: stage_axiom_inversion,
    18: stage_parallel_mirror,
    19: stage_async_router,
    20: stage_python_orchestration,
}

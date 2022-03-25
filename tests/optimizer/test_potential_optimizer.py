import time

import pytest
from loguru import logger

from simaple.core import AttackType, BaseStatType, JobType, Stat
from simaple.core.damage import INTBasedDamageLogic
from simaple.gear.potential import PotentialTier
from simaple.optimizer import WeaponPotentialOptimizer
from simaple.util import Timer


@pytest.mark.parametrize(
    "tiers",
    [
        (PotentialTier.unique, PotentialTier.unique, PotentialTier.unique),
        (PotentialTier.unique, PotentialTier.epic, PotentialTier.epic),
        (PotentialTier.legendary, PotentialTier.unique, PotentialTier.unique),
        (PotentialTier.legendary, PotentialTier.unique, PotentialTier.unique),
        (PotentialTier.legendary, PotentialTier.unique, PotentialTier.empty),
    ],
)
def test_optimizer(tiers):
    with Timer():
        optimizer = WeaponPotentialOptimizer(
            default_stat=Stat(
                INT=40000,
                LUK=5000,
                magic_attack=3000,
                critical_rate=80,
                critical_damage=100,
                damage_multiplier=300,
                ignored_defence=90,
                INT_static=10000,
            ),
            tiers=tiers,
            damage_logic=INTBasedDamageLogic(attack_range_constant=1.0, mastery=0.95),
        )
        output = optimizer.get_optimal_potential()
        logger.info(f"Optimization output {output}")

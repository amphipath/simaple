from simaple.core.damage import INTBasedDamageLogic
from simaple.job.builtin.util import parse_resource_path
from simaple.job.description import GeneralJobArgument
from simaple.job.job import Job
from simaple.job.passive_skill import PassiveSkillArgument, PassiveSkillset


def job_archmagefb(argument: PassiveSkillArgument):
    return Job(
        passive_skillset=PassiveSkillset.from_resource_file(
            parse_resource_path("passive_skill/archmagefb")
        ).all(argument),
        default_active_skillset=PassiveSkillset.from_resource_file(
            parse_resource_path("default_active_skill/archmagefb")
        ).all(argument),
        damage_logic=INTBasedDamageLogic(
            attack_range_constant=1.2,
            mastery=0.95 + 0.01 * (argument.combat_orders_level // 2),
        ),
    )

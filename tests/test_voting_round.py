from py_flare_common.fsp.epoch.timing import songbird

from observer.reward_epoch_manager import Entity, EntityMapper, SigningPolicy
from observer.voting_round import FtsoVotingRoundProtocol

ADDR = "0x0000000000000000000000000000000000000001"


def _signing_policy(entities: list[Entity]) -> SigningPolicy:
    mapper = EntityMapper()
    for e in entities:
        mapper.insert(e)
    return SigningPolicy(
        reward_epoch=songbird.reward_epoch(300),
        vote_power_block=0,
        start_voting_round=0,
        threshold=0,
        seed=0,
        signing_policy_bytes="",
        entities=entities,
        entity_mapper=mapper,
    )


def _entity() -> Entity:
    return Entity(
        identity_address=ADDR,
        submit_address=ADDR,
        submit_signatures_address=ADDR,
        signing_policy_address=ADDR,
        delegation_address=ADDR,
        public_key="",
        nodes=[],
        delegation_fee_bips=0,
        w_nat_weight=1,
        w_nat_capped_weight=1,
        registration_weight=1,
        normalized_weight=1,
    )


def test_calculate_medians_without_any_valid_reveal_leaves_no_medians():
    # A round where the observer saw no commit+reveal pair from anyone (on
    # songbird 2026-11-12, ~5 s blocks pushed reveals past the deadline) used to
    # crash the observer: max() of an empty feed-count dict.
    ftso = FtsoVotingRoundProtocol()

    ftso.calculate_medians(songbird.voting_epoch(1511542), _signing_policy([_entity()]))

    assert ftso.medians == []

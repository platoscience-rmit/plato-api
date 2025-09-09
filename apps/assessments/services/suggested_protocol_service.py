from apps.assessments.repositories.protocol_repository import ProtocolRepository
from apps.assessments.repositories.suggested_protocol_repository import SuggestedProtocolRepository
from apps.common.base_service import BaseService


class SuggestedProtocolService(BaseService):
    def __init__(self):
        self.protocol_repo = ProtocolRepository()
        self.repository = SuggestedProtocolRepository()

    def create_suggested_protocols(self, assessment, treatments):
        if len(treatments) != 3:
            raise Exception(f"Error creating suggested protocols: Expect 3 protocols but get {len(treatments)}.")
        return self.create(
            assessment=assessment,
            first_norm_study=treatments[0],
            second_norm_study=treatments[1],
            third_norm_study=treatments[2],
        )

from apps.assessments.repositories.protocol_repository import ProtocolRepository
from apps.assessments.repositories.suggested_protocol_repository import SuggestedProtocolRepository
from apps.common.base_service import BaseService


class ProtocolService(BaseService):
    def __init__(self):
        self.protocol_repo = ProtocolRepository()
        self.suggested_repo = SuggestedProtocolRepository()

    def create_suggested_protocols(self, assessment, first_protocol, second_protocol, third_protocol):
        first = self.protocol_repo.get_by_id(first_protocol)
        second = self.protocol_repo.get_by_id(second_protocol)
        third = self.protocol_repo.get_by_id(third_protocol)
        return self.suggested_repo.create(
            assessment=assessment,
            first_protocol=first,
            second_protocol=second,
            third_protocol=third,
        )

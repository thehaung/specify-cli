from specify_cli.integrations.base import (
    IntegrationBase,
    SkillsIntegration,
)
from specify_cli.integrations.amazonq import AmazonQIntegration
from specify_cli.integrations.cursor import CursorIntegration

INTEGRATION_REGISTRY: dict = {
    "amazonq": AmazonQIntegration,
    "cursor": CursorIntegration,
}

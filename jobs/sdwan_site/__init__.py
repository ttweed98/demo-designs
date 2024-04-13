"""Design to create a core backbone site."""
from nautobot.extras.jobs import StringVar, IPNetworkVar
from nautobot_design_builder.design_job import DesignJob

from .context import SDWANSiteContext


class CoreSiteDesign(DesignJob):
    """Create a core backbone site."""

    tenant = StringVar(label="Tenant")
    site_name = StringVar(label="Site Name", regex=r"\w{3}\d+")
    site_prefix = IPNetworkVar(label="Site Prefix", min_prefix_length=16, max_prefix_length=22)
    management_prefix = IPNetworkVar(label="Management Prefix", min_prefix_length=24, max_prefix_length=32)
    molex_silverpeak_prefix = IPNetworkVar(label="Molex Silverpeak Prefix", min_prefix_length=24, max_prefix_length=32)

    class Meta:
        """Metadata needed to implement the backbone site design."""

        name = "Sdwan Site Design"
        commit_default = False
        design_file = "designs/0001_design.yaml.j2"
        context_class = SDWANSiteContext

"""Design to create a core backbone site."""
from nautobot.extras.jobs import StringVar, IPNetworkVar
from nautobot_design_builder.design_job import DesignJob

from .context import SDWANSiteContext


class CoreSiteDesign(DesignJob):
    """Create a core backbone site."""

    tenant_name = StringVar(label="Tenant")
    site_name = StringVar(label="Site Name")
    site_prefix = IPNetworkVar(label="Site Prefix", min_prefix_length=27, max_prefix_length=32)
    management_prefix = IPNetworkVar(label="Management Prefix", min_prefix_length=28, max_prefix_length=32)
    molex_silverpeak_prefix = IPNetworkVar(label="Molex Silverpeak Prefix", min_prefix_length=28, max_prefix_length=32)
    design_file = StringVar(label="Design File")

    class Meta:
        """Metadata needed to implement the backbone site design."""

        name = "Sdwan Site Design"
        commit_default = False
        design_file = None  # Remove the hardcoded design file
        context_class = SDWANSiteContext

    def get_design_file(self):
        """Return the design file based on the instance's design_file variable."""
        return self.design_file  # Use the value of the design_file StringVar

    def run(self, **kwargs): 
        """Override the run method to set the design file before running the job."""
        # Set the design file based on user input
        self.Meta.design_file = self.get_design_file()
        super().run(kwargs['data'], kwargs['commit'])

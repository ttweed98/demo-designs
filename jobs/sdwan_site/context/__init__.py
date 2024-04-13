import ipaddress
import re

from nautobot_design_builder.context import Context


class SDWANSiteContext(Context):
    """Render context for core site design"""

    site_name: str
    tenant_name: str
    site_prefix: str
    management_prefix: str
    molex_silverpeak_prefix: str

    container_prefixes = {
        "-wrx-a": {
            "positions": [3, 6, 9, 11, 19, 21],
            "interfaces": ["loopback2", "vlan1650", "vlan1700", "vlan954", "vlan954-v"],
            "cidrs": ["/32", "/31", "/31", "/31", "/31", "/29"],
        },
        "-wrx-b": {
            "positions": [4, 8, 10, 13, 20, 21],
            "interfaces": ["loopback2", "vlan1650", "vlan1700", "vlan954", "vlan954-v"],
            "cidrs": ["/32", "/31", "/31", "/31", "/29", "/29"],
        },
    }
    management_devices = {
        "-wrx-a": {
            "positions": [3, 6, 9],
            "interfaces": ["loopback1", "vlan1651", "vlan1711"],
            "cidrs": ["/32", "/31", "/31"],
        },
        "-wrx-b": {
            "positions": [4, 8, 10],
            "interfaces": ["loopback1", "vlan1651", "vlan1711"],
            "cidrs": ["/32", "/31", "/31"],
        },
    }
    silver_peak_devices = {
        "-wrx-a": {
            "positions": [2],
            "interfaces": ["vlan1701"],
            "cidrs": ["/29"],
        },
        "-wrx-b": {
            "positions": [10],
            "interfaces": ["vlan1702"],
            "cidrs": ["/29"],
        },
    }

    def get_subnet(self, prefix):
        """Returns a network object based on the prefix"""
        return ipaddress.ip_network(prefix)

    def get_ip_addresses(self, subnet):
        """Returns a list of host addresses in the subnet"""
        return list(subnet.hosts())

    def get_device_ips(self, devices, ip_addresses):
        """Returns a dictionary of devices and their corresponding IP addresses"""
        return {
            device: {
                interface: str(ip_addresses[pos - 1]) + cidr
                for interface, pos, cidr in zip(
                    devices[device]["interfaces"], devices[device]["positions"], devices[device]["cidrs"]
                )
            }
            for device in devices
        }

    def get_interface_ip(self, device_name, interface_name, prefix, devices):
        """Returns the IP address of a specific interface on a device"""
        device_name = device_name.lower()  # Convert to lowercase
        match = re.search(r"(-wrx-[ab])$", device_name)
        if match is None:
            raise ValueError("Invalid device name. It should end with '-wrx-a' or '-wrx-b'.")
        device_suffix = match.group(1)

        subnet = self.get_subnet(prefix)
        ip_addresses = self.get_ip_addresses(subnet)
        device_ips = self.get_device_ips(devices, ip_addresses)

        try:
            return device_ips[device_suffix][interface_name]
        except KeyError:
            raise ValueError(f"Interface {interface_name} not found on device {device_name}")

    def get_site_interface_ip(self, device_name, interface_name):
        """Returns the site IP address of a specific interface on a device"""
        return self.get_interface_ip(device_name, interface_name, self.site_prefix, self.container_prefixes)

    def get_management_interface_ip(self, device_name, interface_name):
        """Returns the management IP address of a specific interface on a device"""
        return self.get_interface_ip(device_name, interface_name, self.management_prefix, self.management_devices)

    def get_silver_peak_interface_ip(self, device_name, interface_name):
        """Returns the Silver Peak IP address of a specific interface on a device"""
        return self.get_interface_ip(
            device_name, interface_name, self.molex_silverpeak_prefix, self.silver_peak_devices
        )


# c = SDWANSiteContext()
# print(c.get_site_interface_ip("site-wrx-a", "loopback2"))
# print(c.get_management_interface_ip("site-wrx-b", "loopback1"))
# print(c.get_silver_peak_interface_ip("site-wrx-b", "vlan1702"))

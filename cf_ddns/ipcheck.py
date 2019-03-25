# -*- coding: utf-8 -*-
"""Defines methods to return the current IP address for either IPv4 or IPv6.
"""

import socket
from netaddr import IPAddress
import requests


class IPCheck(object):
    """Contains methods to determine the current IPv4 or IPv6 address.

    Attributes:
      site: The domain name of a website to use to find the IP address
      ssl: A boolean specifying whether to use HTTPS to find the IP address
        (optional, defaults to True)
    """

    def __init__(self, site="google.com", ssl=True):
        self.site = site
        if ssl:
            self.port = 443
        elif not ssl:
            self.port = 80

    def _check_nat_ip(self):
        """
        Finds the current NAT address.

        Args:
          None
        Returns:
          A string
        """
        address = requests.get("http://ipecho.net/plain")
        return address.text

    def v4_check(self):
        """
        Finds the current IPv4 address.

        Args:
          None:
        Returns:
          A string
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((self.site, self.port))
        address = sock.getsockname()[0]
        sock.close()
        if IPAddress(address).is_private():
            address = self._check_nat_ip()
        return address

    def v6_check(self):
        """
        Finds the current IPv6 address.

        Args:
          None
        Returns:
          A string
        """
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sock.connect((self.site, self.port))
        address = sock.getsockname()[0]
        sock.close()
        return address

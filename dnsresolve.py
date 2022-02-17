#!/usr/bin/env python

"""
Python DNS Client
(C) 2014 David Lettier
lettier.com

A simple DNS client similar to `nslookup` or `host`.
Does not use any DNS libraries.
Handles only A type records.
"""
import sys
import socket
import aiodns
import asyncio
import pycares


class DNSResolve:
    def __init__(self, dnsIp, dnsPort):
        self._dnsIp = dnsIp
        self._dnsPort = dnsPort

    def DNSResolve(self, host_name_to, qtype):
        ip = []
        ip.append(self._dnsIp)
        try:
            loop = asyncio.new_event_loop()
            resolver = aiodns.DNSResolver(loop=loop)
            resolver.nameservers = ip
            f = resolver.query(host_name_to, qtype)
            result = loop.run_until_complete(f)
        except Exception as e:
            return None
        return result

    def getDCIp(self, domain, type="ANY"):
        domain = '_msdcs.' + domain
        # Convert data to bit string.
        dnsAnswer = self.DNSResolve(domain, type)
        if not dnsAnswer:
            print("dns search _msdcs error")
            sys.exit()
        items = []
        for data in dnsAnswer:
            if isinstance(data, pycares.ares_query_ns_result):
                items.append(str(data.host))
            elif isinstance(data, pycares.ares_query_soa_result):
                items.append(str(data.nsname))
            else:
                print("there have other type")
        items = list(set(items))

        ips = []
        for dnsDomain in items:
            ip = self.DNSResolve(dnsDomain, "A")
            if ip:
                ips.append(str(ip[0].host))
        return ips

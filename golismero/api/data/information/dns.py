#!/usr/bin/python
# -*- coding: utf-8 -*-

# Required since "dns" is both an external module and the name of this file.
from __future__ import absolute_import

"""
This package contains the classes that represent
the different types of DNS queries and responses.
"""

__license__ = """
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com
  Mario Vilas | mvilas<@>gmail.com

Golismero project site: http://golismero-project.com
Golismero project mail: golismero.project<@>gmail.com


This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""


#------------------------------------------------------------------------------
class DnsSEC(object):
    """
    DNSSEC Util
    """

    RSAMD5 = 1
    DH = 2
    DSA = 3
    ECC = 4
    RSASHA1 = 5
    DSANSEC3SHA1 = 6
    RSASHA1NSEC3SHA1 = 7
    RSASHA256 = 8
    RSASHA512 = 10
    INDIRECT = 252
    PRIVATEDNS = 253
    PRIVATEOID = 254

    ALGORITHM_BY_TEXT = {
        'RSAMD5' : RSAMD5,
        'DH' : DH,
        'DSA' : DSA,
        'ECC' : ECC,
        'RSASHA1' : RSASHA1,
        'DSANSEC3SHA1' : DSANSEC3SHA1,
        'RSASHA1NSEC3SHA1' : RSASHA1NSEC3SHA1,
        'RSASHA256' : RSASHA256,
        'RSASHA512' : RSASHA512,
        'INDIRECT' : INDIRECT,
        'PRIVATEDNS' : PRIVATEDNS,
        'PRIVATEOID' : PRIVATEOID,
    }

    ALGORITHM_BY_NUM = {
        RSAMD5 : 'RSAMD5',
        DH :'DH',
        DSA : 'DSA',
        ECC : 'ECC' ,
        RSASHA1 : 'RSASHA1',
        DSANSEC3SHA1 : 'DSANSEC3SHA1',
        RSASHA1NSEC3SHA1 : 'RSASHA1NSEC3SHA1',
        RSASHA256 : 'RSASHA256',
        RSASHA512 : 'RSASHA512',
        INDIRECT : 'INDIRECT',
        PRIVATEDNS : 'PRIVATEDNS',
        PRIVATEOID : 'PRIVATEOID',
    }


    #----------------------------------------------------------------------
    @staticmethod
    def algorithm_to_text(alg):
        """
        :return: From a numeric value, returns a text with the name of the algorithm.
        :rtype: str
        """
        if not isinstance(alg, int):
            raise TypeError("Expected int, got '%s'" % type(alg))

        if alg not in DnsSEC.ALGORITHM_BY_TEXT.values():
            raise TypeError("Invalid algorithm '%s'" % alg)

        return DnsSEC.ALGORITHM_BY_NUM[alg]


    @staticmethod
    def text_to_algorithm(alg):
        """
        :return: From a numeric text, returns the integer value of the algorithm
        :rtype: int
        """
        if not isinstance(alg, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(alg))

        if alg not in DnsSEC.ALGORITHM_BY_TEXT:
            raise TypeError("Invalid algorithm '%s'" % alg)

        return DnsSEC.ALGORITHM_BY_TEXT[alg]


#------------------------------------------------------------------------------
class DnsRegister(object):
    """
    Base class for DNS Registers
    """

    # Types of registers
    DNS_TYPES = (
        'A',
        'AAAA',
        'AFSDB',
        'CERT',
        'CNAME',
        'DNSKEY',
        'DS',
        'HINFO',
        'IPSECKEY',
        'ISDN',
        'LOC',
        'MX',
        'NAPTR',
        'NS',
        'NSAP',
        'NSEC',
        'NSEC3',
        'NSEC3PARAM',
        'PTR',
        'RP',
        'RRSIG',
        'SOA',
        'SPF',
        'SRV',
        'TXT',
        'WKS',
        'X25'
    )

    NONE = 0
    A = 1
    NS = 2
    MD = 3
    MF = 4
    CNAME = 5
    SOA = 6
    MB = 7
    MG = 8
    MR = 9
    NULL = 10
    WKS = 11
    PTR = 12
    HINFO = 13
    MINFO = 14
    MX = 15
    TXT = 16
    RP = 17
    AFSDB = 18
    X25 = 19
    ISDN = 20
    RT = 21
    NSAP = 22
    NSAP_PTR = 23
    SIG = 24
    KEY = 25
    PX = 26
    GPOS = 27
    AAAA = 28
    LOC = 29
    NXT = 30
    SRV = 33
    NAPTR = 35
    KX = 36
    CERT = 37
    A6 = 38
    DNAME = 39
    OPT = 41
    APL = 42
    DS = 43
    SSHFP = 44
    IPSECKEY = 45
    RRSIG = 46
    NSEC = 47
    DNSKEY = 48
    DHCID = 49
    NSEC3 = 50
    NSEC3PARAM = 51
    HIP = 55
    SPF = 99
    UNSPEC = 103
    TKEY = 249
    TSIG = 250
    IXFR = 251
    AXFR = 252
    MAILB = 253
    MAILA = 254
    ANY = 255
    TA = 32768
    DLV = 32769

    _by_text = {
        'NONE' : NONE,
        'A' : A,
        'NS' : NS,
        'MD' : MD,
        'MF' : MF,
        'CNAME' : CNAME,
        'SOA' : SOA,
        'MB' : MB,
        'MG' : MG,
        'MR' : MR,
        'NULL' : NULL,
        'WKS' : WKS,
        'PTR' : PTR,
        'HINFO' : HINFO,
        'MINFO' : MINFO,
        'MX' : MX,
        'TXT' : TXT,
        'RP' : RP,
        'AFSDB' : AFSDB,
        'X25' : X25,
        'ISDN' : ISDN,
        'RT' : RT,
        'NSAP' : NSAP,
        'NSAP-PTR' : NSAP_PTR,
        'SIG' : SIG,
        'KEY' : KEY,
        'PX' : PX,
        'GPOS' : GPOS,
        'AAAA' : AAAA,
        'LOC' : LOC,
        'NXT' : NXT,
        'SRV' : SRV,
        'NAPTR' : NAPTR,
        'KX' : KX,
        'CERT' : CERT,
        'A6' : A6,
        'DNAME' : DNAME,
        'OPT' : OPT,
        'APL' : APL,
        'DS' : DS,
        'SSHFP' : SSHFP,
        'IPSECKEY' : IPSECKEY,
        'RRSIG' : RRSIG,
        'NSEC' : NSEC,
        'DNSKEY' : DNSKEY,
        'DHCID' : DHCID,
        'NSEC3' : NSEC3,
        'NSEC3PARAM' : NSEC3PARAM,
        'HIP' : HIP,
        'SPF' : SPF,
        'UNSPEC' : UNSPEC,
        'TKEY' : TKEY,
        'TSIG' : TSIG,
        'IXFR' : IXFR,
        'AXFR' : AXFR,
        'MAILB' : MAILB,
        'MAILA' : MAILA,
        'ANY' : ANY,
        'TA' : TA,
        'DLV' : DLV,
    }


    #----------------------------------------------------------------------
    @staticmethod
    def name2id(id):
        """
        Get the number of the DNS Register identificator by their id.

        :param id: the id of the DNS code type.
        :type id: int

        :return: the name of DNS register type: A, AAAA, CNAME...
        :rtype: str
        """
        return DnsRegister._by_text[id]


    #----------------------------------------------------------------------
    @staticmethod
    def id2name(name):
        """
        Get the id of the DNS Register identificator by their name.

        :param name: the name of the DNS code type: A, AAAA, CNAME...
        :type name: str

        :return: the id number of DNS register type.
        :rtype: int
        """
        m_by_value = dict([(y, x) for x, y in DnsRegister._by_text.iteritems()])

        return m_by_value[name]


    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        """
        :param type: Type of DNS register. Valid types are: 'A', 'AAAA', 'AFSDB', 'CERT', 'CNAME', 'DNSKEY', 'DS', 'HINFO', 'IPSECKEY', 'ISDN', 'LOC', 'MX', 'NAPTR', 'NS', 'NSAP', 'NSEC', 'NSEC3', 'NSEC3PARAM', 'PTR', 'RP', 'RRSIG', 'SOA', 'SPF', 'SRV', 'TXT', 'WKS' or 'X25'.
        :type type: str
        """
        self._type               = None

        try:
            self._type           = kwargs['type']
        except KeyError:
            pass


        # Checks for types
        if not isinstance(self._type, basestring):
            raise TypeError("Expected str, got %s" % type(self._type))


    #----------------------------------------------------------------------
    @property
    def type(self):
        """
        :return: Type of DNS register
        :rtype: str
        """
        return self._type


    #----------------------------------------------------------------------
    @property
    def type_int(self):
        """
        :return:
        :rtype:
        """
        return self._by_text[self.type]


#------------------------------------------------------------------------------
class DNSRegisterAlgorithm(DnsRegister):


    #----------------------------------------------------------------------
    def __init__(self, algorithm, **kwargs):
        """
        :param algorithm: the DNSSEC algorithm for the certificate. Allowed values are in DnsSEC.ALGORITHM_BY_TEXT dict.
        :type algorithm: str | int
        """

        #
        # Check the algorithm
        #
        if isinstance(algorithm, basestring):
            self.__algorithm_value = DnsSEC.text_to_algorithm(algorithm)
            self.__algorithm_name  = DnsSEC.algorithm_to_text(self.__algorithm_value)
        elif isinstance(algorithm, int):
            self.__algorithm_name  = DnsSEC.algorithm_to_text(algorithm)
            self.__algorithm_value = DnsSEC.text_to_algorithm(self.__algorithm_name)
        else:
            raise TypeError("Not a valid algorithm, got %s" % type(subtype))

        super(DNSRegisterAlgorithm, self).__init__(**kwargs)


    #----------------------------------------------------------------------
    @property
    def algorithm_name(self):
        """
        :return: name of the DNSSEC algorithm
        :rtype: str
        """
        return self.__algorithm_name


    #----------------------------------------------------------------------
    @property
    def algorithm_value(self):
        """
        :return: integer with the DNSSEC algorithm value
        :rtype: int
        """
        return self.__algorithm_value


#------------------------------------------------------------------------------
class DnsRegisterA(DnsRegister):
    """
    Register type 'A'
    """


    #----------------------------------------------------------------------
    def __init__(self, address, **kwargs):
        """
        :param address: the IPv4 address.
        :type address: str
        """
        if not isinstance(address, basestring):
            raise TypeError("Expected str, got %s" % type(address))

        self.__address = address

        # Set type of register and the other options
        super(DnsRegisterA, self).__init__(type="A", **kwargs)


    #----------------------------------------------------------------------
    @property
    def address(self):
        """
        :return: the IPv4 address
        :rtype: str
        """
        return self.__address


#------------------------------------------------------------------------------
class DnsRegisterAAAA(DnsRegister):
    """
    Register type 'AAAA'
    """


    #----------------------------------------------------------------------
    def __init__(self, address, **kwargs):
        """
        :param address: the IPv6 address.
        :type address: str
        """
        if not isinstance(address, basestring):
            raise TypeError("Expected str, got %s" % type(address))

        self.__address = address

        # Set type of register and the other options
        super(DnsRegisterAAAA, self).__init__(type="AAAA", **kwargs)


    #----------------------------------------------------------------------
    @property
    def address(self):
        """
        :return: the IPv6 address
        :rtype: str
        """
        return self.__address


#------------------------------------------------------------------------------
class DnsRegisterAFSDB(DnsRegister):
    """
    Register type 'AFSDB'
    """

    #----------------------------------------------------------------------
    def __init__(self, subtype, hostname, **kwargs):
        """
        :param name: alias for the 'preference' attribute.
        :type name: str.

        :param address: alias for 'exchange' attribute.
        :type address: str
        """
        if not isinstance(subtype, basestring):
            raise TypeError("Expected str, got %s" % type(subtype))
        if not isinstance(hostname, basestring):
            raise TypeError("Expected str, got %s" % type(hostname))

        self.__subtype    = subtype
        self.__hostname   = hostname

        # Set type of register and the other options
        super(DnsRegisterAFSDB, self).__init__(type="AFSDB", **kwargs)


    #----------------------------------------------------------------------
    @property
    def subtype(self):
        """
        :return: alias for the 'preference' attribute..
        :rtype: str
        """
        return self.__subtype


    #----------------------------------------------------------------------
    @property
    def hostname(self):
        """
        :return: alias for 'exchange' attribute..
        :rtype: str
        """
        return self.__hostname


#------------------------------------------------------------------------------
class DnsRegisterCERT(DNSRegisterAlgorithm):
    """
    Register type 'CERT'
    """

    CERT_TYPE_BY_VAL = {
        1 : 'PKIX',
        2 : 'SPKI',
        3 : 'PGP',
        253 : 'URI',
        254 : 'OID',
    }

    CERT_TYPE_BY_NAME = {
        'PKIX' : 1,
        'SPKI' : 2,
        'PGP' : 3,
        'URI' : 253,
        'OID' : 254,
    }


    #----------------------------------------------------------------------
    def __init__(self, algorithm, certificate, certificate_type, key_tag, **kwargs):
        """
        :param algorithm: the DNSSEC algorithm for the certificate. Allowed values are in DnsSEC.ALGORITHM_BY_TEXT dict.
        :type algorithm: str | int

        :param certificate: the certificate
        :type certificate: str

        :param certificate_type: The type of the certificate. Allowed values are: DnsRegisterCERT.CERT_TYPE_BY_NAME or DnsRegisterCERT.CERT_TYPE_BY_VAL.
        :type certificate_type: int | str

        :param key_tag: the key tag.
        :type key_tag: int
        """

        #
        # Check the certificate type
        #
        if isinstance(certificate_type, basestring):
            self.__cert_type_value = DnsRegisterCERT.text_to_cert(certificate_type)
            self.__cert_type_name  = DnsRegisterCERT.cert_to_text(self.__cert_type_value)
        elif isinstance(certificate_type, int):
            self.__cert_type_name  = DnsRegisterCERT.cert_to_text(certificate_type)
            self.__cert_type_value = DnsRegisterCERT.text_to_cert(self.__cert_type_name)
        else:
            raise TypeError("Not a valid certificate_type, got %s" % type(certificate_type))
        if not isinstance(certificate, basestring):
            raise TypeError("Expected str, got %s" % type(certificate))
        if not isinstance(key_tag, int):
            raise TypeError("Expected int, got '%s'" % type(key_tag))

        self.__certificate = certificate
        self.__key_tag     = key_tag

        # Set type of register and the other options
        super(DnsRegisterCERT, self).__init__(algorithm, type="CERT", **kwargs)


    #----------------------------------------------------------------------
    @property
    def certificate(self):
        """
        :return: string with the certificate
        :rtype: str
        """
        return self.__certificate


    #----------------------------------------------------------------------
    @property
    def certificate_type_name(self):
        """
        :return: string with the name of the type of certificate
        :rtype: str
        """
        return self.__cert_type_name


    #----------------------------------------------------------------------
    @property
    def certificate_type_value(self):
        """
        :return: integer value of the type of certificate
        :rtype: int
        """
        return self.__cert_type_value


    #----------------------------------------------------------------------
    @property
    def key_tag(self):
        """
        :return: The key tag
        :rtype: int
        """
        return self.__key_tag


    #----------------------------------------------------------------------
    @staticmethod
    def cert_to_text(cert):
        """
        :return: From a numeric value, returns a text with the name of the type of cert.
        :rtype: str
        """
        if not isinstance(cert, int):
            raise TypeError("Expected int, got '%s'" % type(cert))

        if cert not in DnsRegisterCERT.CERT_TYPE_BY_VAL.values():
            raise TypeError("Invalid algorithm '%s'" % cert)

        return DnsRegisterCERT.CERT_TYPE_BY_VAL[cert]


    #----------------------------------------------------------------------
    @staticmethod
    def text_to_cert(cert):
        """
        :return: From a numeric text, returns the integer value of the type of cert
        :rtype: int
        """
        if not isinstance(cert, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(cert))

        if cert not in DnsRegisterCERT.CERT_TYPE_BY_NAME.values():
            raise TypeError("Invalid algorithm '%s'" % cert)

        return DnsRegisterCERT.CERT_TYPE_BY_NAME[cert]


#------------------------------------------------------------------------------
class DnsRegisterCNAME(DnsRegister):
    """
    Register type 'CNAME'
    """


    #----------------------------------------------------------------------
    def __init__(self, target, **kwargs):
        """
        :param target: name of the pointer host.
        :type target: str
        """
        if not isinstance(target, basestring):
            raise TypeError("Expected str, got %s" % type(target))

        self.__target  = target

        # Set type of register and the other options
        super(DnsRegisterCNAME, self).__init__(type="CNAME", **kwargs)


    #----------------------------------------------------------------------
    @property
    def target(self):
        """
        :return: name of the pointer host.
        :rtype: str
        """
        return self.__target


#------------------------------------------------------------------------------
class DnsRegisterDNSKEY(DNSRegisterAlgorithm):
    """
    Register type 'DNSKEY'
    """


    #----------------------------------------------------------------------
    def __init__(self, algorithm, flags, key, protocol, **kwargs):
        """
        :param algorithm: the DNSSEC algorithm for the certificate. Allowed values are in DnsSEC.ALGORITHM_BY_TEXT dict.
        :type algorithm: str | int

        :param flags: the key flags
        :type flags: int

        :param key: String with the public key
        :type key: str

        :param protocol: the protocol for which this key may be used.
        :type protocol: int
        """
        if not isinstance(flags, int):
            raise TypeError("Expected int, got '%s'" % type(flags))
        if not isinstance(key, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(key))
        if not isinstance(protocol, int):
            raise TypeError("Expected int, got '%s'" % type(protocol))

        self.__flags       = flags
        self.__key         = key
        self.__protocol    = protocol

        # Set type of register and the other options
        super(DnsRegisterDNSKEY, self).__init__(algorithm, type="DNSKEY", **kwargs)


    #----------------------------------------------------------------------
    @property
    def flags(self):
        """
        :return: flags for the record
        :rtype: int
        """
        return self.__flags


    #----------------------------------------------------------------------
    @property
    def key(self):
        """
        :return: String with the public key
        :rtype: str
        """
        return self.__key


    #----------------------------------------------------------------------
    @property
    def protocol(self):
        """
        :return: the protocol for which this key may be used.
        :rtype: int
        """
        return self.__protocol


#------------------------------------------------------------------------------
class DnsRegisterDS(DNSRegisterAlgorithm):
    """
    Register type 'DS'
    """


    #----------------------------------------------------------------------
    def __init__(self, algorithm, digest, digest_type, key_tag, **kwargs):
        """
        :param algorithm: the DNSSEC algorithm for the certificate. Allowed values are in DnsSEC.ALGORITHM_BY_TEXT dict.
        :type algorithm: str | int

        :param digest: string with the digest
        :type digest: str

        :param digest_type: the digest type
        :type digest_type: int

        :param key_tag: the key tag.
        :type key_tag: int
        """
        if not isinstance(digest, int):
            raise TypeError("Expected int, got '%s'" % type(digest))
        if not isinstance(digest_type, int):
            raise TypeError("Expected int, got '%s'" % type(digest_type))
        if not isinstance(key_tag, int):
            raise TypeError("Expected int, got '%s'" % type(key_tag))

        self.__digest      = digest
        self.__digest_type = digest_type
        self.__key_tag     = key_tag
        self.__protocol    = protocol

        # Set type of register and the other options
        super(DnsRegisterDS, self).__init__(algorithm, type="DS", **kwargs)


    #----------------------------------------------------------------------
    @property
    def key_tag(self):
        """
        :return: The key tag
        :rtype: int
        """
        return self.__key_tag


    #----------------------------------------------------------------------
    @property
    def digest(self):
        """
        :return: string with the digest
        :rtype: str
        """
        return self.__digest


    #----------------------------------------------------------------------
    @property
    def digest_type(self):
        """
        :return: the digest type
        :rtype: int
        """
        return self.__digest_type


#------------------------------------------------------------------------------
class DnsRegisterHINFO(DnsRegister):
    """
    Register type 'HINFO'
    """


    #----------------------------------------------------------------------
    def __init__(self, cpu, os, **kwargs):
        """
        :param cpu: the CPU type.
        :type cpu: str.

        :param os: the OS type
        :type os: str
        """
        if not isinstance(cpu, basestring):
            raise TypeError("Expected str, got %s" % type(cpu))
        if not isinstance(os, basestring):
            raise TypeError("Expected str, got %s" % type(os))

        self.__cpu    = cpu
        self.__os     = os

        # Set type of register and the other options
        super(DnsRegisterHINFO, self).__init__(type="HINFO", **kwargs)


    #----------------------------------------------------------------------
    @property
    def cpu(self):
        """
        :return: the CPU type
        :rtype: str
        """
        return self.__cpu


    #----------------------------------------------------------------------
    @property
    def os(self):
        """
        :return: the OS type
        :rtype: str
        """
        return self.__os


#------------------------------------------------------------------------------
class DnsRegisterIPSECKEY(DNSRegisterAlgorithm):
    """
    Register type 'IPSECKEY'
    """


    #----------------------------------------------------------------------
    def __init__(self, algorithm, gateway, gateway_type, key, precedence, **kwargs):
        """
        :param algorithm: the DNSSEC algorithm for the certificate. Allowed values are in DnsSEC.ALGORITHM_BY_TEXT dict.
        :type algorithm: str | int

        :param gateway: gateway address
        :type gateway: None, IPv4 address, IPV6 address, or domain name

        :param gateway_type: the gateway type
        :type gateway_type: int

        :param key: the public key.
        :type key: str

        :param precedence: the precedence for this key data.
        :type precedence: int
        """
        if not isinstance(gateway, basestring):
            raise TypeError("Expected int, got '%s'" % type(gateway))
        if isinstance(gateway_type, int):
            if gateway_type < 0 or gateway_type > 3:
                raise TypeError("Gateway type must be in 0-4 range")
        else:
            raise TypeError("Expected int, got '%s'" % type(gateway_type))
        if not isinstance(precedence, int):
            raise TypeError("Expected int, got '%s'" % type(precedence))

        self.__gateway         = gateway
        self.__gateway_type    = gateway_type
        self.__key             = key
        self.__precedence      = precedence

        # Set type of register and the other options
        super(DnsRegisterIPSECKEY, self).__init__(algorithm, type="IPSECKEY", **kwargs)


    #----------------------------------------------------------------------
    @property
    def gateway(self):
        """
        :return: gateway address
        :rtype: None, IPv4 address, IPV6 address, or domain name
        """
        return self.__gateway


    #----------------------------------------------------------------------
    @property
    def gateway_type(self):
        """
        :return: the gateway type
        :rtype: int
        """
        return self.__gateway_type


    #----------------------------------------------------------------------
    @property
    def key(self):
        """
        :return: the public key
        :rtype: str
        """
        return self.__key


    #----------------------------------------------------------------------
    @property
    def precedence(self):
        """
        :return: the precedence of this key data
        :rtype: int
        """
        return self.__precedence


#------------------------------------------------------------------------------
class DnsRegisterISDN(DnsRegister):
    """
    Register type 'ISDN'
    """


    #----------------------------------------------------------------------
    def __init__(self, address, subaddress = "", **kwargs):
        """
        :param address: the ISDN address.
        :type address: str

        :param subaddress: the ISDN subaddress.
        :type subaddress: str
        """
        if not isinstance(address, basestring):
            raise TypeError("Expected str, got %s" % type(address))
        if not isinstance(subaddress, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(subaddress))

        self.__address       = address
        self.__subaddress    = subaddress

        # Set type of register and the other options
        super(DnsRegisterISDN, self).__init__(type="ISDN", **kwargs)


    #----------------------------------------------------------------------
    @property
    def address(self):
        """
        :return: the ISDN address
        :rtype: str
        """
        return self.__address


    #----------------------------------------------------------------------
    @property
    def subaddress(self):
        """
        :return: the ISDN subaddress (or '' if not present)
        :rtype: str | ''
        """
        return self.__subaddress


#------------------------------------------------------------------------------
class DnsRegisterLOC(DnsRegister):
    """
    Register type 'LOC'
    """


    #----------------------------------------------------------------------
    def __init__(self, latitude, longitude, coordinates, **kwargs):
        """
        :param latitude: latitude
        :type latitude: float

        :param latitude: longitude
        :type longitude: float

        :param coordinates: string with the geolocation coordinates
        :type coordinates: str
        """

        if not isinstance(coordinates, basestring):
            raise TypeError("Expected str, got %s" % type(coordinates))
        if not isinstance(latitude, float):
            raise TypeError("Expected float, got '%s'" % type(latitude))
        if not isinstance(longitude, float):
            raise TypeError("Expected float, got '%s'" % type(longitude))

        self.__latitude       = latitude
        self.__longitude      = longitude
        self.__coordinates    = coordinates

        # Set type of register and the other options
        super(DnsRegisterLOC, self).__init__(type="LOC", **kwargs)


    #----------------------------------------------------------------------
    @property
    def coordinates(self):
        """
        :return: string with the phisical coordinates
        :rtype: str
        """
        return self.__coordinates


    #----------------------------------------------------------------------
    @property
    def latitude(self):
        """
        :return: latitude
        :rtype: float
        """
        return self.__latitude


    #----------------------------------------------------------------------
    @property
    def longitude(self):
        """
        :return: longitude
        :rtype: float
        """
        return self.__longitude


#------------------------------------------------------------------------------
class DnsRegisterMX(DnsRegister):
    """
    Register type 'MX'
    """


    #----------------------------------------------------------------------
    def __init__(self, exchange, preference, **kwargs):
        """
        :param exchange: string with then name of exchange server
        :type exchange: str

        :param preference: the preference value
        :type preference: int
        """

        if not isinstance(exchange, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(exchange))
        if not isinstance(preference, int):
            raise TypeError("Expected int, got '%s'" % type(preference))

        self.__exchange      = exchange
        self.__preference    = preference

        # Set type of register and the other options
        super(DnsRegisterMX, self).__init__(type="MX", **kwargs)


    #----------------------------------------------------------------------
    @property
    def exchange(self):
        """
        :return: string with the name of exchange server.
        :rtype: str
        """
        return self.__exchange


    #----------------------------------------------------------------------
    @property
    def preference(self):
        """
        :return: integer with the preference
        :rtype: int
        """
        return self.__preference


#------------------------------------------------------------------------------
class DnsRegisterNAPTR(DnsRegister):
    """
    Register type 'NAPTR'
    """


    #----------------------------------------------------------------------
    def __init__(self, order, preference, regex, replacement, service, **kwargs):
        """
        :param order: the order
        :type order: int

        :param preference: the preference
        :type preference: int

        :param regex: regular expression
        :type regex: str

        :param replacement: replacemente name
        :type replacement: str

        :param service: service name
        :type service: str
        """

        if not isinstance(order, int):
            raise TypeError("Expected int, got '%s'" % type(order))
        if not isinstance(preference, int):
            raise TypeError("Expected int, got '%s'" % type(preference))
        if not isinstance(regex, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(regex))
        if not isinstance(replacement, str):
            raise TypeError("Expected str, got '%s'" % type(replacement))

        self.__order            = order
        self.__preference       = preference
        self.__regex            = regex
        self.__replacement      = replacement
        self.__service          = service

        # Set type of register and the other options
        super(DnsRegisterNAPTR, self).__init__(type="NAPTR", **kwargs)


    #----------------------------------------------------------------------
    @property
    def order(self):
        """
        :return: the order
        :rtype: int
        """
        return self.__order

    #----------------------------------------------------------------------
    @property
    def preference(self):
        """
        :return: the preference
        :rtype: int
        """
        return self.__preference

    #----------------------------------------------------------------------
    @property
    def regex(self):
        """
        :return: regular expression
        :rtype: str
        """
        return self.__regex

    #----------------------------------------------------------------------
    @property
    def replacement(self):
        """
        :return: The replacemente name
        :rtype: str
        """
        return self.__replacement

    #----------------------------------------------------------------------
    @property
    def service(self):
        """
        :return: service name
        :rtype: str
        """
        return self.__service


#------------------------------------------------------------------------------
class DnsRegisterNS(DnsRegister):
    """
    Register type 'NS'
    """


    #----------------------------------------------------------------------
    def __init__(self, target, **kwargs):
        """
        :param target: server target
        :type target: str
        """
        if not isinstance(target, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(target))

        self.__target    = target

        # Set type of register and the other options
        super(DnsRegisterNS, self).__init__(type="NS", **kwargs)


    #----------------------------------------------------------------------
    @property
    def target(self):
        """
        :return: The target server
        :rtype: str
        """
        return self.__target


#------------------------------------------------------------------------------
class DnsRegisterNSAP(DnsRegister):
    """
    Register type 'NSAP'
    """


    #----------------------------------------------------------------------
    def __init__(self, address, **kwargs):
        """
        :param address: a NASP address
        :type address: str

        """
        if not isinstance(address, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(address))

        self.__address    = address

        # Set type of register and the other options
        super(DnsRegisterNSAP, self).__init__(type="NSAP", **kwargs)


    #----------------------------------------------------------------------
    @property
    def address(self):
        """
        :return: a NASP address
        :rtype: str
        """
        return self.__address


#------------------------------------------------------------------------------
class DnsRegisterNSEC(DnsRegister):
    """
    Register type 'NSEC'
    """


    #----------------------------------------------------------------------
    def __init__(self, next, **kwargs):
        """
        :param next: the next server name
        :type next: str
        """
        if not isinstance(next, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(next))

        self.__next    = next

        # Set type of register and the other options
        super(DnsRegisterNSEC, self).__init__(type="NSEC", **kwargs)


    #----------------------------------------------------------------------
    @property
    def next(self):
        """
        :return: the next server name
        :rtype: str
        """
        return self.__next


#------------------------------------------------------------------------------
class DnsRegisterNSEC3(DNSRegisterAlgorithm):
    """
    Register type 'NSEC3'
    """


    #----------------------------------------------------------------------
    def __init__(self, algorithm, flags, iterations, salt, **kwargs):
        """
        :param algorithm: the DNSSEC algorithm for the certificate. Allowed values are in DnsSEC.ALGORITHM_BY_TEXT dict.
        :type algorithm: str | int

        :param flags: the flags
        :type flags: int

        :param iterations: the number of iterations
        :type iterations: int

        :param salt: the salt
        :type salt: str
        """
        if not isinstance(flags, int):
            raise TypeError("Expected int, got '%s'" % type(flags))
        if not isinstance(iterations, int):
            raise TypeError("Expected int, got '%s'" % type(iterations))
        if not isinstance(salt, str):
            raise TypeError("Expected str, got '%s'" % type(salt))

        self.__flags         = flags
        self.__iterations    = iterations
        self.__salt          = salt

        # Set type of register and the other options
        super(DnsRegisterNSEC3, self).__init__(algorithm, type="NSEC3", **kwargs)


    #----------------------------------------------------------------------
    @property
    def salt(self):
        """
        :return: the salt
        :rtype: str
        """
        return self.__salt


    #----------------------------------------------------------------------
    @property
    def iterations(self):
        """
        :return: the number of iterations
        :rtype: int
        """
        return self.__iterations


    #----------------------------------------------------------------------
    @property
    def flags(self):
        """
        :return: the flags
        :rtype: int
        """
        return self.__flags


#------------------------------------------------------------------------------
class DnsRegisterNSEC3PARAM(DNSRegisterAlgorithm):
    """
    Register type 'NSEC3PARAM'
    """


    #----------------------------------------------------------------------
    def __init__(self, algorithm, flags, iterations, salt, **kwargs):
        """
        :param algorithm: the DNSSEC algorithm for the certificate. Allowed values are in DnsSEC.ALGORITHM_BY_TEXT dict.
        :type algorithm: str | int

        :param flags: the flags
        :type flags: int

        :param iterations: the number of iterations
        :type iterations: int

        :param salt: the salt
        :type salt: str
        """
        if not isinstance(flags, int):
            raise TypeError("Expected int, got '%s'" % type(flags))
        if not isinstance(iterations, int):
            raise TypeError("Expected int, got '%s'" % type(iterations))
        if not isinstance(salt, str):
            raise TypeError("Expected str, got '%s'" % type(salt))

        self.__flags         = flags
        self.__iterations    = iterations
        self.__salt          = salt

        # Set type of register and the other options
        super(DnsRegisterNSEC3PARAM, self).__init__(algorithm, type="NSEC3PARAM", **kwargs)


    #----------------------------------------------------------------------
    @property
    def salt(self):
        """
        :return: the salt
        :rtype: str
        """
        return self.__salt


    #----------------------------------------------------------------------
    @property
    def iterations(self):
        """
        :return: the number of iterations
        :rtype: int
        """
        return self.__iterations


    #----------------------------------------------------------------------
    @property
    def flags(self):
        """
        :return: the flags
        :rtype: int
        """
        return self.__flags


#------------------------------------------------------------------------------
class DnsRegisterPTR(DnsRegister):
    """
    Register type 'PTR'
    """


    #----------------------------------------------------------------------
    def __init__(self, target, **kwargs):
        """
        :param target: server target
        :type target: str
        """
        if not isinstance(target, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(target))

        self.__target    = target

        # Set type of register and the other options
        super(DnsRegisterPTR, self).__init__(type="PTR", **kwargs)


    #----------------------------------------------------------------------
    @property
    def target(self):
        """
        :return: The target server
        :rtype: str
        """
        return self.__target


#------------------------------------------------------------------------------
class DnsRegisterRP(DnsRegister):
    """
    Register type 'RP'
    """


    #----------------------------------------------------------------------
    def __init__(self, mbox, txt, **kwargs):
        """
        :param mbox: The responsible person's mailbox as string format
        :type mbox: str

        :param txt: The owner name of a node with TXT records, or the root name if no TXT records are associated with this RP.
        :type txt: str
        """

        if not isinstance(target, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(target))

        self.__mbox             = mbox
        self.__txt             = txt

        # Set type of register and the other options
        super(DnsRegisterRP, self).__init__(type="RP", **kwargs)


    #----------------------------------------------------------------------
    @property
    def mbox(self):
        """
        :return: The responsible person's mailbox as string format
        :rtype: str
        """
        return self.__mbox


    #----------------------------------------------------------------------
    @property
    def txt(self):
        """
        :return: The owner name of a node with TXT records, or the root name if no TXT records are associated with this RP.
        :rtype: str
        """
        return self.__txt


#------------------------------------------------------------------------------
class DnsRegisterRRSIG(DNSRegisterAlgorithm):
    """
    Register type 'RRSIG'
    """


    #----------------------------------------------------------------------
    def __init__(self, algorithm, expiration, interception, key_tag, labels, original_ttl, signer, type_coverded, **kwargs):
        """
        :param algorithm: the DNSSEC algorithm for the certificate. Allowed values are in DnsSEC.ALGORITHM_BY_TEXT dict.
        :type algorithm: str | int

        :param expiration: signature expiration time
        :type expiration: long

        :param key_tag: the key tag.
        :type key_tag: int

        :param labels: number of labels
        :type labels: int

        :param original_ttl: the original TTL
        :type original_ttl: long

        :param signer: the signer
        :type signer: str

        :param type_covered: the rdata type this signature covers
        :type type_covered: int
        """

        if not isinstance(expiration, long):
            raise TypeError("Expected long, got '%s'" % type(expiration))
        if not isinstance(key_tag, int):
            raise TypeError("Expected int, got '%s'" % type(key_tag))
        if not isinstance(labels, int):
            raise TypeError("Expected int, got '%s'" % type(labels))
        if not isinstance(original_ttl, long):
            raise TypeError("Expected long, got '%s'" % type(original_ttl))
        if not isinstance(signer, str):
            raise TypeError("Expected str, got '%s'" % type(signer))
        if not isinstance(type_coverded, int):
            raise TypeError("Expected int, got '%s'" % type(type_coverded))

        self.__expiration             = expiration
        self.__key_tag                = key_tag
        self.__labels                 = labels
        self.__original_ttl           = original_ttl
        self.__type_covered           = type_covered

        # Set type of register and the other options
        super(DnsRegisterRRSIG, self).__init__(algorithm, type="RRSIG", **kwargs)


    #----------------------------------------------------------------------
    @property
    def type_covered(self):
        """
        :return: the rdata type this signature covers
        :rtype:int
        """
        return self.__type_covered


    #----------------------------------------------------------------------
    @property
    def labels(self):
        """
        :return: number of labels
        :rtype: int
        """
        return self.__labels


    #----------------------------------------------------------------------
    @property
    def original_ttl(self):
        """
        :return: the original TTL
        :rtype: long
        """
        return self.__original_ttl


    #----------------------------------------------------------------------
    @property
    def expiration(self):
        """
        :return: signature expiration time
        :rtype: long
        """
        return self.__expiration


    #----------------------------------------------------------------------
    @property
    def key_tag(self):
        """
        :return: The key tag
        :rtype: int
        """
        return self.__key_tag


#------------------------------------------------------------------------------
class DnsRegisterSOA(DnsRegister):
    """
    Register type 'SOA'
    """


    #----------------------------------------------------------------------
    def __init__(self, mname, rname, refresh, expire, **kwargs):
        """
        :param mname: the SOA MNAME (master name) field
        :type mname: str

        :param rname: the SOA RNAME (responsible name) field
        :type rname: str

        :param refresh: The zone's refresh value (in seconds)
        :type refresh: int

        :param expire: The zone's expiration value (in seconds)
        :type expire: int
        """
        if not isinstance(mname, basestring):
            raise TypeError("Expected str, got %s" % type(mname))
        if not isinstance(rname, basestring):
            raise TypeError("Expected str, got %s" % type(rname))
        if not isinstance(refresh, int):
            raise TypeError("Expected int, got '%s'" % type(refresh))
        if not isinstance(expire, int):
            raise TypeError("Expected int, got '%s'" % type(expire))

        self.__mname             = mname
        self.__rname             = rname
        self.__refresh           = refresh
        self.__expire            = expire

        # Set type of register and the other options
        super(DnsRegisterSOA, self).__init__(type="SOA", **kwargs)


    #----------------------------------------------------------------------
    @property
    def mname(self):
        """
        :return: the SOA MNAME (master name) field
        :rtype: str
        """
        return self.__mname


    #----------------------------------------------------------------------
    @property
    def rname(self):
        """
        :return: the SOA RNAME (responsible name) field
        :rtype: str
        """
        return self.__rname


    #----------------------------------------------------------------------
    @property
    def refresh(self):
        """
        :return: The zone's refresh value (in seconds)
        :rtype: int
        """
        return self.__refresh


    #----------------------------------------------------------------------
    @property
    def expire(self):
        """
        :return: The zone's expiration value (in seconds)
        :rtype: int
        """
        return self.__expire


#------------------------------------------------------------------------------
class DnsRegisterTXT(DnsRegister):
    """
    Register type 'TXT'
    """


    #----------------------------------------------------------------------
    def __init__(self, strings, **kwargs):
        """
        :param strings: list of the string text
        :type strings: list(str)
        """

        if isinstance(strings, list):
            for l in strings:
                if not isinstance(l, basestring):
                    raise TypeError("Expected str, got %s" % type(l))
        else:
            raise TypeError("Expected str, got %s" % type(strings))

        self.__strings             = strings

        # Set type of register and the other options
        super(DnsRegisterTXT, self).__init__(type="TXT", **kwargs)


    #----------------------------------------------------------------------
    @property
    def strings(self):
        """
        :return: list of the text strings
        :rtype: list(str)
        """
        return self.__strings


#------------------------------------------------------------------------------
class DnsRegisterSPF(DnsRegister):
    """
    Register type 'SPF'
    """


    #----------------------------------------------------------------------
    def __init__(self, strings, **kwargs):
        """
        :param strings: list of the string text
        :type strings: list(str)
        """

        if isinstance(strings, list):
            for l in strings:
                if not isinstance(l, basestring):
                    raise TypeError("Expected str, got %s" % type(l))
        else:
            raise TypeError("Expected str, got %s" % type(strings))

        self.__strings             = strings

        # Set type of register and the other options
        super(DnsRegisterSPF, self).__init__(type="SPF", **kwargs)


    #----------------------------------------------------------------------
    @property
    def strings(self):
        """
        :return: list of the text strings
        :rtype: list(str)
        """
        return self.__strings


#------------------------------------------------------------------------------
class DnsRegisterSRV(DnsRegister):
    """
    Register type 'SRV'
    """


    #----------------------------------------------------------------------
    def __init__(self, target, priority, weight, port, **kwargs):
        """
        :param target: the target host name
        :type target: str

        :param priority: the priority
        :type priority: int

        :param weight: the weight
        :type weight: int

        :param port: the port of the service
        :type port: int
        """

        if not isinstance(target, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(target))
        if not isinstance(priority, int):
            raise TypeError("Expected int, got '%s'" % type(priority))
        if not isinstance(weight, int):
            raise TypeError("Expected int, got '%s'" % type(weight))
        if not isinstance(port, int):
            raise TypeError("Expected int, got '%s'" % type(port))

        self.__target             = target
        self.__priority           = priority
        self.__weight             = weight
        self.__port               = port

        # Set type of register and the other options
        super(DnsRegisterSRV, self).__init__(type="SRV", **kwargs)


    #----------------------------------------------------------------------
    @property
    def target(self):
        """
        :return: the target host name
        :rtype: str
        """
        return self.__target


    #----------------------------------------------------------------------
    @property
    def priority(self):
        """
        :return: the priority
        :rtype: int
        """
        return self.__priority


    #----------------------------------------------------------------------
    @property
    def weight(self):
        """
        :return: the weight
        :rtype: int
        """
        return self.__weight


    #----------------------------------------------------------------------
    @property
    def port(self):
        """
        :return: the port of the service
        :rtype: int
        """
        return self.__port


#------------------------------------------------------------------------------
class DnsRegisterWKS(DnsRegister):
    """
    Register type 'WKS'
    """


    #----------------------------------------------------------------------
    def __init__(self, address, protocol, bitmap, **kwargs):
        """
        :param address: the address
        :type address: str

        :param protocol: the protocol.
        :type protocol: int

        :param bitmap: the bitmap.
        :type bitmap: str
        """

        if not isinstance(address, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(address))
        if not isinstance(protocol, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(protocol))
        if not isinstance(bitmap, basestring):
            raise TypeError("Expected basestring, got '%s'" % type(bitmap))

        self.__address             = address
        self.__protocol            = protocol
        self.__bitmap              = bitmap

        # Set type of register and the other options
        super(DnsRegisterWKS, self).__init__(type="WKS", **kwargs)


    #----------------------------------------------------------------------
    @property
    def address(self):
        """
        :return: the address
        :rtype: str
        """
        return self.__address


    #----------------------------------------------------------------------
    @property
    def protocol(self):
        """
        :return: the protocol
        :rtype: int
        """
        return self.__protocol


    #----------------------------------------------------------------------
    @property
    def bitmap(self):
        """
        :return: the bitmap
        :rtype: str
        """
        return self.__bitmap


#------------------------------------------------------------------------------
class DnsRegisterX25(DnsRegister):
    """
    Register type 'X25'
    """


    #----------------------------------------------------------------------
    def __init__(self, address, **kwargs):
        """
        :param address: the PSDN address
        :type address: str
        """

        if not isinstance(address, basestring):
            raise TypeError("Expected str, got %s" % type(address))

        self.__address = address

        # Set type of register and the other options
        super(DnsRegisterX25, self).__init__(type="X25", **kwargs)


    #----------------------------------------------------------------------
    @property
    def address(self):
        """
        :return: the PSDN address
        :rtype: str
        """
        return self.__address
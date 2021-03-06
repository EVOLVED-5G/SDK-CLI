# coding: utf-8

"""
    NEF_Emulator

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class MonitoringNotification(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'external_id': 'str',
        'monitoring_type': 'MonitoringType',
        'location_info': 'LocationInfo',
        'ipv4_addr': 'str',
        'subscription': 'str'
    }

    attribute_map = {
        'external_id': 'externalId',
        'monitoring_type': 'monitoringType',
        'location_info': 'locationInfo',
        'ipv4_addr': 'ipv4Addr',
        'subscription': 'subscription'
    }

    def __init__(self, external_id='123456789@domain.com', monitoring_type=None, location_info=None, ipv4_addr=None, subscription=None):  # noqa: E501
        """MonitoringNotification - a model defined in Swagger"""  # noqa: E501
        self._external_id = None
        self._monitoring_type = None
        self._location_info = None
        self._ipv4_addr = None
        self._subscription = None
        self.discriminator = None
        if external_id is not None:
            self.external_id = external_id
        self.monitoring_type = monitoring_type
        if location_info is not None:
            self.location_info = location_info
        if ipv4_addr is not None:
            self.ipv4_addr = ipv4_addr
        self.subscription = subscription

    @property
    def external_id(self):
        """Gets the external_id of this MonitoringNotification.  # noqa: E501

        Globally unique identifier containing a Domain Identifier and a Local Identifier. \\<Local Identifier\\>@\\<Domain Identifier\\>  # noqa: E501

        :return: The external_id of this MonitoringNotification.  # noqa: E501
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """Sets the external_id of this MonitoringNotification.

        Globally unique identifier containing a Domain Identifier and a Local Identifier. \\<Local Identifier\\>@\\<Domain Identifier\\>  # noqa: E501

        :param external_id: The external_id of this MonitoringNotification.  # noqa: E501
        :type: str
        """

        self._external_id = external_id

    @property
    def monitoring_type(self):
        """Gets the monitoring_type of this MonitoringNotification.  # noqa: E501


        :return: The monitoring_type of this MonitoringNotification.  # noqa: E501
        :rtype: MonitoringType
        """
        return self._monitoring_type

    @monitoring_type.setter
    def monitoring_type(self, monitoring_type):
        """Sets the monitoring_type of this MonitoringNotification.


        :param monitoring_type: The monitoring_type of this MonitoringNotification.  # noqa: E501
        :type: MonitoringType
        """
        if monitoring_type is None:
            raise ValueError("Invalid value for `monitoring_type`, must not be `None`")  # noqa: E501

        self._monitoring_type = monitoring_type

    @property
    def location_info(self):
        """Gets the location_info of this MonitoringNotification.  # noqa: E501


        :return: The location_info of this MonitoringNotification.  # noqa: E501
        :rtype: LocationInfo
        """
        return self._location_info

    @location_info.setter
    def location_info(self, location_info):
        """Sets the location_info of this MonitoringNotification.


        :param location_info: The location_info of this MonitoringNotification.  # noqa: E501
        :type: LocationInfo
        """

        self._location_info = location_info

    @property
    def ipv4_addr(self):
        """Gets the ipv4_addr of this MonitoringNotification.  # noqa: E501

        String identifying an Ipv4 address  # noqa: E501

        :return: The ipv4_addr of this MonitoringNotification.  # noqa: E501
        :rtype: str
        """
        return self._ipv4_addr

    @ipv4_addr.setter
    def ipv4_addr(self, ipv4_addr):
        """Sets the ipv4_addr of this MonitoringNotification.

        String identifying an Ipv4 address  # noqa: E501

        :param ipv4_addr: The ipv4_addr of this MonitoringNotification.  # noqa: E501
        :type: str
        """

        self._ipv4_addr = ipv4_addr

    @property
    def subscription(self):
        """Gets the subscription of this MonitoringNotification.  # noqa: E501


        :return: The subscription of this MonitoringNotification.  # noqa: E501
        :rtype: str
        """
        return self._subscription

    @subscription.setter
    def subscription(self, subscription):
        """Sets the subscription of this MonitoringNotification.


        :param subscription: The subscription of this MonitoringNotification.  # noqa: E501
        :type: str
        """
        if subscription is None:
            raise ValueError("Invalid value for `subscription`, must not be `None`")  # noqa: E501

        self._subscription = subscription

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(MonitoringNotification, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MonitoringNotification):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

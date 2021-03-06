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

class QosMonitoringInformation(object):
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
        'req_qos_mon_params': 'list[RequestedQoSMonitoringParameters]',
        'rep_freqs': 'list[ReportingFrequency]',
        'lat_thresh_dl': 'int',
        'lat_thresh_ul': 'int',
        'lat_thresh_rp': 'int',
        'wait_time': 'int',
        'rep_period': 'int'
    }

    attribute_map = {
        'req_qos_mon_params': 'reqQosMonParams',
        'rep_freqs': 'repFreqs',
        'lat_thresh_dl': 'latThreshDl',
        'lat_thresh_ul': 'latThreshUl',
        'lat_thresh_rp': 'latThreshRp',
        'wait_time': 'waitTime',
        'rep_period': 'repPeriod'
    }

    def __init__(self, req_qos_mon_params=None, rep_freqs=None, lat_thresh_dl=None, lat_thresh_ul=None, lat_thresh_rp=None, wait_time=None, rep_period=None):  # noqa: E501
        """QosMonitoringInformation - a model defined in Swagger"""  # noqa: E501
        self._req_qos_mon_params = None
        self._rep_freqs = None
        self._lat_thresh_dl = None
        self._lat_thresh_ul = None
        self._lat_thresh_rp = None
        self._wait_time = None
        self._rep_period = None
        self.discriminator = None
        if req_qos_mon_params is not None:
            self.req_qos_mon_params = req_qos_mon_params
        if rep_freqs is not None:
            self.rep_freqs = rep_freqs
        if lat_thresh_dl is not None:
            self.lat_thresh_dl = lat_thresh_dl
        if lat_thresh_ul is not None:
            self.lat_thresh_ul = lat_thresh_ul
        if lat_thresh_rp is not None:
            self.lat_thresh_rp = lat_thresh_rp
        if wait_time is not None:
            self.wait_time = wait_time
        if rep_period is not None:
            self.rep_period = rep_period

    @property
    def req_qos_mon_params(self):
        """Gets the req_qos_mon_params of this QosMonitoringInformation.  # noqa: E501

        Indicates the requested QoS monitoring parameters to be measured  # noqa: E501

        :return: The req_qos_mon_params of this QosMonitoringInformation.  # noqa: E501
        :rtype: list[RequestedQoSMonitoringParameters]
        """
        return self._req_qos_mon_params

    @req_qos_mon_params.setter
    def req_qos_mon_params(self, req_qos_mon_params):
        """Sets the req_qos_mon_params of this QosMonitoringInformation.

        Indicates the requested QoS monitoring parameters to be measured  # noqa: E501

        :param req_qos_mon_params: The req_qos_mon_params of this QosMonitoringInformation.  # noqa: E501
        :type: list[RequestedQoSMonitoringParameters]
        """

        self._req_qos_mon_params = req_qos_mon_params

    @property
    def rep_freqs(self):
        """Gets the rep_freqs of this QosMonitoringInformation.  # noqa: E501

        Indicates the frequency for the reporting  # noqa: E501

        :return: The rep_freqs of this QosMonitoringInformation.  # noqa: E501
        :rtype: list[ReportingFrequency]
        """
        return self._rep_freqs

    @rep_freqs.setter
    def rep_freqs(self, rep_freqs):
        """Sets the rep_freqs of this QosMonitoringInformation.

        Indicates the frequency for the reporting  # noqa: E501

        :param rep_freqs: The rep_freqs of this QosMonitoringInformation.  # noqa: E501
        :type: list[ReportingFrequency]
        """

        self._rep_freqs = rep_freqs

    @property
    def lat_thresh_dl(self):
        """Gets the lat_thresh_dl of this QosMonitoringInformation.  # noqa: E501

        Threshold in units of milliseconds for downlink packet delay  # noqa: E501

        :return: The lat_thresh_dl of this QosMonitoringInformation.  # noqa: E501
        :rtype: int
        """
        return self._lat_thresh_dl

    @lat_thresh_dl.setter
    def lat_thresh_dl(self, lat_thresh_dl):
        """Sets the lat_thresh_dl of this QosMonitoringInformation.

        Threshold in units of milliseconds for downlink packet delay  # noqa: E501

        :param lat_thresh_dl: The lat_thresh_dl of this QosMonitoringInformation.  # noqa: E501
        :type: int
        """

        self._lat_thresh_dl = lat_thresh_dl

    @property
    def lat_thresh_ul(self):
        """Gets the lat_thresh_ul of this QosMonitoringInformation.  # noqa: E501

        Threshold in units of milliseconds for uplink packet delay  # noqa: E501

        :return: The lat_thresh_ul of this QosMonitoringInformation.  # noqa: E501
        :rtype: int
        """
        return self._lat_thresh_ul

    @lat_thresh_ul.setter
    def lat_thresh_ul(self, lat_thresh_ul):
        """Sets the lat_thresh_ul of this QosMonitoringInformation.

        Threshold in units of milliseconds for uplink packet delay  # noqa: E501

        :param lat_thresh_ul: The lat_thresh_ul of this QosMonitoringInformation.  # noqa: E501
        :type: int
        """

        self._lat_thresh_ul = lat_thresh_ul

    @property
    def lat_thresh_rp(self):
        """Gets the lat_thresh_rp of this QosMonitoringInformation.  # noqa: E501

        Threshold in units of milliseconds for round trip packet delay  # noqa: E501

        :return: The lat_thresh_rp of this QosMonitoringInformation.  # noqa: E501
        :rtype: int
        """
        return self._lat_thresh_rp

    @lat_thresh_rp.setter
    def lat_thresh_rp(self, lat_thresh_rp):
        """Sets the lat_thresh_rp of this QosMonitoringInformation.

        Threshold in units of milliseconds for round trip packet delay  # noqa: E501

        :param lat_thresh_rp: The lat_thresh_rp of this QosMonitoringInformation.  # noqa: E501
        :type: int
        """

        self._lat_thresh_rp = lat_thresh_rp

    @property
    def wait_time(self):
        """Gets the wait_time of this QosMonitoringInformation.  # noqa: E501

        Indicates the minimum waiting time (seconds) between subsequent reports. Only applicable when the \"repFreqs\" attribute includes \"EVENT_TRIGGERED\".  # noqa: E501

        :return: The wait_time of this QosMonitoringInformation.  # noqa: E501
        :rtype: int
        """
        return self._wait_time

    @wait_time.setter
    def wait_time(self, wait_time):
        """Sets the wait_time of this QosMonitoringInformation.

        Indicates the minimum waiting time (seconds) between subsequent reports. Only applicable when the \"repFreqs\" attribute includes \"EVENT_TRIGGERED\".  # noqa: E501

        :param wait_time: The wait_time of this QosMonitoringInformation.  # noqa: E501
        :type: int
        """

        self._wait_time = wait_time

    @property
    def rep_period(self):
        """Gets the rep_period of this QosMonitoringInformation.  # noqa: E501

        Indicates the time interval (seconds) between successive reporting. Only applicable when the \"repFreqs\" attribute includes\"PERIODIC\".  # noqa: E501

        :return: The rep_period of this QosMonitoringInformation.  # noqa: E501
        :rtype: int
        """
        return self._rep_period

    @rep_period.setter
    def rep_period(self, rep_period):
        """Sets the rep_period of this QosMonitoringInformation.

        Indicates the time interval (seconds) between successive reporting. Only applicable when the \"repFreqs\" attribute includes\"PERIODIC\".  # noqa: E501

        :param rep_period: The rep_period of this QosMonitoringInformation.  # noqa: E501
        :type: int
        """

        self._rep_period = rep_period

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
        if issubclass(QosMonitoringInformation, dict):
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
        if not isinstance(other, QosMonitoringInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

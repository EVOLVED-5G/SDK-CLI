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

class Path(object):
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
        'description': 'str',
        'points': 'list[Point]',
        'start_point': 'Point',
        'end_point': 'Point',
        'color': 'str',
        'id': 'int',
        'owner_id': 'int'
    }

    attribute_map = {
        'description': 'description',
        'points': 'points',
        'start_point': 'start_point',
        'end_point': 'end_point',
        'color': 'color',
        'id': 'id',
        'owner_id': 'owner_id'
    }

    def __init__(self, description=None, points=None, start_point=None, end_point=None, color=None, id=None, owner_id=None):  # noqa: E501
        """Path - a model defined in Swagger"""  # noqa: E501
        self._description = None
        self._points = None
        self._start_point = None
        self._end_point = None
        self._color = None
        self._id = None
        self._owner_id = None
        self.discriminator = None
        if description is not None:
            self.description = description
        if points is not None:
            self.points = points
        if start_point is not None:
            self.start_point = start_point
        if end_point is not None:
            self.end_point = end_point
        if color is not None:
            self.color = color
        self.id = id
        self.owner_id = owner_id

    @property
    def description(self):
        """Gets the description of this Path.  # noqa: E501


        :return: The description of this Path.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Path.


        :param description: The description of this Path.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def points(self):
        """Gets the points of this Path.  # noqa: E501


        :return: The points of this Path.  # noqa: E501
        :rtype: list[Point]
        """
        return self._points

    @points.setter
    def points(self, points):
        """Sets the points of this Path.


        :param points: The points of this Path.  # noqa: E501
        :type: list[Point]
        """

        self._points = points

    @property
    def start_point(self):
        """Gets the start_point of this Path.  # noqa: E501


        :return: The start_point of this Path.  # noqa: E501
        :rtype: Point
        """
        return self._start_point

    @start_point.setter
    def start_point(self, start_point):
        """Sets the start_point of this Path.


        :param start_point: The start_point of this Path.  # noqa: E501
        :type: Point
        """

        self._start_point = start_point

    @property
    def end_point(self):
        """Gets the end_point of this Path.  # noqa: E501


        :return: The end_point of this Path.  # noqa: E501
        :rtype: Point
        """
        return self._end_point

    @end_point.setter
    def end_point(self, end_point):
        """Sets the end_point of this Path.


        :param end_point: The end_point of this Path.  # noqa: E501
        :type: Point
        """

        self._end_point = end_point

    @property
    def color(self):
        """Gets the color of this Path.  # noqa: E501


        :return: The color of this Path.  # noqa: E501
        :rtype: str
        """
        return self._color

    @color.setter
    def color(self, color):
        """Sets the color of this Path.


        :param color: The color of this Path.  # noqa: E501
        :type: str
        """

        self._color = color

    @property
    def id(self):
        """Gets the id of this Path.  # noqa: E501


        :return: The id of this Path.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Path.


        :param id: The id of this Path.  # noqa: E501
        :type: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def owner_id(self):
        """Gets the owner_id of this Path.  # noqa: E501


        :return: The owner_id of this Path.  # noqa: E501
        :rtype: int
        """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, owner_id):
        """Sets the owner_id of this Path.


        :param owner_id: The owner_id of this Path.  # noqa: E501
        :type: int
        """
        if owner_id is None:
            raise ValueError("Invalid value for `owner_id`, must not be `None`")  # noqa: E501

        self._owner_id = owner_id

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
        if issubclass(Path, dict):
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
        if not isinstance(other, Path):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

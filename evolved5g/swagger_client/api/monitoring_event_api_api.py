# coding: utf-8

"""
    NEF_Emulator

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.1.0

    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from evolved5g.swagger_client.api_client import ApiClient


class MonitoringEventAPIApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post(self, body, scs_as_id, **kwargs):  # noqa: E501
        """Create Subscription  # noqa: E501

        Create new subscription.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post(body, scs_as_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MonitoringEventSubscriptionCreate body: (required)
        :param str scs_as_id: (required)
        :return: MonitoringEventReport
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post_with_http_info(body, scs_as_id, **kwargs)  # noqa: E501
        else:
            (data) = self.create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post_with_http_info(body, scs_as_id, **kwargs)  # noqa: E501
            return data

    def create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post_with_http_info(self, body, scs_as_id, **kwargs):  # noqa: E501
        """Create Subscription  # noqa: E501

        Create new subscription.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post_with_http_info(body, scs_as_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MonitoringEventSubscriptionCreate body: (required)
        :param str scs_as_id: (required)
        :return: MonitoringEventReport
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'scs_as_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post`")  # noqa: E501
        # verify the required parameter 'scs_as_id' is set
        if ('scs_as_id' not in params or
                params['scs_as_id'] is None):
            raise ValueError("Missing the required parameter `scs_as_id` when calling `create_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'scs_as_id' in params:
            path_params['scsAsId'] = params['scs_as_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2PasswordBearer']  # noqa: E501

        return self.api_client.call_api(
           self.api_client.configuration.available_endpoints["MONITORING_SUBSCRIPTIONS"], 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=self.get_response_type(body_params),  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_response_type(self,body_params):
        if body_params.maximum_number_of_reports ==1:
            return "MonitoringEventReport"
        else:
            return "MonitoringEventSubscription"

    def delete_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete(self, scs_as_id, subscription_id, **kwargs):  # noqa: E501
        """Delete Subscription  # noqa: E501

        Delete a subscription  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete(scs_as_id, subscription_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str scs_as_id: (required)
        :param str subscription_id: (required)
        :return: MonitoringEventSubscription
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete_with_http_info(scs_as_id, subscription_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete_with_http_info(scs_as_id, subscription_id, **kwargs)  # noqa: E501
            return data

    def delete_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete_with_http_info(self, scs_as_id, subscription_id, **kwargs):  # noqa: E501
        """Delete Subscription  # noqa: E501

        Delete a subscription  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete_with_http_info(scs_as_id, subscription_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str scs_as_id: (required)
        :param str subscription_id: (required)
        :return: MonitoringEventSubscription
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['scs_as_id', 'subscription_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'scs_as_id' is set
        if ('scs_as_id' not in params or
                params['scs_as_id'] is None):
            raise ValueError("Missing the required parameter `scs_as_id` when calling `delete_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete`")  # noqa: E501
        # verify the required parameter 'subscription_id' is set
        if ('subscription_id' not in params or
                params['subscription_id'] is None):
            raise ValueError("Missing the required parameter `subscription_id` when calling `delete_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'scs_as_id' in params:
            path_params['scsAsId'] = params['scs_as_id']  # noqa: E501
        if 'subscription_id' in params:
            path_params['subscriptionId'] = params['subscription_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2PasswordBearer']  # noqa: E501

        return self.api_client.call_api(
            self.api_client.configuration.available_endpoints["MONITORING_SUBSCRIPTION_SINGLE"], 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MonitoringEventSubscription',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def read_active_subscriptions_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_get(self, scs_as_id, **kwargs):  # noqa: E501
        """Read Active Subscriptions  # noqa: E501

        Read all active subscriptions  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_active_subscriptions_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_get(scs_as_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str scs_as_id: (required)
        :param int skip:
        :param int limit:
        :return: list[MonitoringEventSubscription]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.read_active_subscriptions_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_get_with_http_info(scs_as_id, **kwargs)  # noqa: E501
        else:
            (data) = self.read_active_subscriptions_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_get_with_http_info(scs_as_id, **kwargs)  # noqa: E501
            return data

    def read_active_subscriptions_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_get_with_http_info(self, scs_as_id, **kwargs):  # noqa: E501
        """Read Active Subscriptions  # noqa: E501

        Read all active subscriptions  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_active_subscriptions_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_get_with_http_info(scs_as_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str scs_as_id: (required)
        :param int skip:
        :param int limit:
        :return: list[MonitoringEventSubscription]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['scs_as_id', 'skip', 'limit']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method read_active_subscriptions_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'scs_as_id' is set
        if ('scs_as_id' not in params or
                params['scs_as_id'] is None):
            raise ValueError("Missing the required parameter `scs_as_id` when calling `read_active_subscriptions_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'scs_as_id' in params:
            path_params['scsAsId'] = params['scs_as_id']  # noqa: E501

        query_params = []
        if 'skip' in params:
            query_params.append(('skip', params['skip']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2PasswordBearer']  # noqa: E501

        return self.api_client.call_api(
           self.api_client.configuration.available_endpoints["MONITORING_SUBSCRIPTIONS"], 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[MonitoringEventSubscription]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def read_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get(self, scs_as_id, subscription_id, **kwargs):  # noqa: E501
        """Read Subscription  # noqa: E501

        Get subscription by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get(scs_as_id, subscription_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str scs_as_id: (required)
        :param str subscription_id: (required)
        :return: MonitoringEventSubscription
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.read_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get_with_http_info(scs_as_id, subscription_id, **kwargs)  # noqa: E501
        else:
            (data) = self.read_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get_with_http_info(scs_as_id, subscription_id, **kwargs)  # noqa: E501
            return data

    def read_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get_with_http_info(self, scs_as_id, subscription_id, **kwargs):  # noqa: E501
        """Read Subscription  # noqa: E501

        Get subscription by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get_with_http_info(scs_as_id, subscription_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str scs_as_id: (required)
        :param str subscription_id: (required)
        :return: MonitoringEventSubscription
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['scs_as_id', 'subscription_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method read_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'scs_as_id' is set
        if ('scs_as_id' not in params or
                params['scs_as_id'] is None):
            raise ValueError("Missing the required parameter `scs_as_id` when calling `read_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get`")  # noqa: E501
        # verify the required parameter 'subscription_id' is set
        if ('subscription_id' not in params or
                params['subscription_id'] is None):
            raise ValueError("Missing the required parameter `subscription_id` when calling `read_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'scs_as_id' in params:
            path_params['scsAsId'] = params['scs_as_id']  # noqa: E501
        if 'subscription_id' in params:
            path_params['subscriptionId'] = params['subscription_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2PasswordBearer']  # noqa: E501

        return self.api_client.call_api(
            self.api_client.configuration.available_endpoints["MONITORING_SUBSCRIPTION_SINGLE"], 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MonitoringEventSubscription',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put(self, body, scs_as_id, subscription_id, **kwargs):  # noqa: E501
        """Update Subscription  # noqa: E501

        Update/Replace an existing subscription resource  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put(body, scs_as_id, subscription_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MonitoringEventSubscription body: (required)
        :param str scs_as_id: (required)
        :param str subscription_id: (required)
        :return: MonitoringEventSubscription
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put_with_http_info(body, scs_as_id, subscription_id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put_with_http_info(body, scs_as_id, subscription_id, **kwargs)  # noqa: E501
            return data

    def update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put_with_http_info(self, body, scs_as_id, subscription_id, **kwargs):  # noqa: E501
        """Update Subscription  # noqa: E501

        Update/Replace an existing subscription resource  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put_with_http_info(body, scs_as_id, subscription_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MonitoringEventSubscription body: (required)
        :param str scs_as_id: (required)
        :param str subscription_id: (required)
        :return: MonitoringEventSubscription
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'scs_as_id', 'subscription_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put`")  # noqa: E501
        # verify the required parameter 'scs_as_id' is set
        if ('scs_as_id' not in params or
                params['scs_as_id'] is None):
            raise ValueError("Missing the required parameter `scs_as_id` when calling `update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put`")  # noqa: E501
        # verify the required parameter 'subscription_id' is set
        if ('subscription_id' not in params or
                params['subscription_id'] is None):
            raise ValueError("Missing the required parameter `subscription_id` when calling `update_subscription_api_v13gpp_monitoring_event_v1_scs_as_id_subscriptions_subscription_id_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'scs_as_id' in params:
            path_params['scsAsId'] = params['scs_as_id']  # noqa: E501
        if 'subscription_id' in params:
            path_params['subscriptionId'] = params['subscription_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2PasswordBearer']  # noqa: E501

        return self.api_client.call_api(
            self.api_client.configuration.available_endpoints["MONITORING_SUBSCRIPTION_SINGLE"], 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MonitoringEventSubscription',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

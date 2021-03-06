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


class GNBsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_gnb_api_v1_gn_bs_post(self, body, **kwargs):  # noqa: E501
        """Create Gnb  # noqa: E501

        Create new gNB.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_gnb_api_v1_gn_bs_post(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GNBCreate body: (required)
        :return: GNB
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_gnb_api_v1_gn_bs_post_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_gnb_api_v1_gn_bs_post_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def create_gnb_api_v1_gn_bs_post_with_http_info(self, body, **kwargs):  # noqa: E501
        """Create Gnb  # noqa: E501

        Create new gNB.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_gnb_api_v1_gn_bs_post_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GNBCreate body: (required)
        :return: GNB
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_gnb_api_v1_gn_bs_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_gnb_api_v1_gn_bs_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

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
            '/api/v1/gNBs', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GNB',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_gnb_api_v1_gn_bs_gnb_id_delete(self, g_nb_id, **kwargs):  # noqa: E501
        """Delete Gnb  # noqa: E501

        Delete a gNB.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_gnb_api_v1_gn_bs_gnb_id_delete(g_nb_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str g_nb_id: The gNB id of the gNB you want to delete (required)
        :return: GNB
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_gnb_api_v1_gn_bs_gnb_id_delete_with_http_info(g_nb_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_gnb_api_v1_gn_bs_gnb_id_delete_with_http_info(g_nb_id, **kwargs)  # noqa: E501
            return data

    def delete_gnb_api_v1_gn_bs_gnb_id_delete_with_http_info(self, g_nb_id, **kwargs):  # noqa: E501
        """Delete Gnb  # noqa: E501

        Delete a gNB.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_gnb_api_v1_gn_bs_gnb_id_delete_with_http_info(g_nb_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str g_nb_id: The gNB id of the gNB you want to delete (required)
        :return: GNB
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['g_nb_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_gnb_api_v1_gn_bs_gnb_id_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'g_nb_id' is set
        if ('g_nb_id' not in params or
                params['g_nb_id'] is None):
            raise ValueError("Missing the required parameter `g_nb_id` when calling `delete_gnb_api_v1_gn_bs_gnb_id_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'g_nb_id' in params:
            path_params['gNB_id'] = params['g_nb_id']  # noqa: E501

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
            '/api/v1/gNBs/{gNB_id}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GNB',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def read_gn_bs_api_v1_gn_bs_get(self, **kwargs):  # noqa: E501
        """Read Gnbs  # noqa: E501

        Retrieve gNBs.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_gn_bs_api_v1_gn_bs_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int skip:
        :param int limit:
        :return: list[GNB]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.read_gn_bs_api_v1_gn_bs_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.read_gn_bs_api_v1_gn_bs_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def read_gn_bs_api_v1_gn_bs_get_with_http_info(self, **kwargs):  # noqa: E501
        """Read Gnbs  # noqa: E501

        Retrieve gNBs.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_gn_bs_api_v1_gn_bs_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int skip:
        :param int limit:
        :return: list[GNB]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['skip', 'limit']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method read_gn_bs_api_v1_gn_bs_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

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
            '/api/v1/gNBs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[GNB]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def read_gnb_api_v1_gn_bs_gnb_id_get(self, g_nb_id, **kwargs):  # noqa: E501
        """Read Gnb  # noqa: E501

        Get gNB by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_gnb_api_v1_gn_bs_gnb_id_get(g_nb_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str g_nb_id: The gNB id of the gNB you want to retrieve (required)
        :return: GNB
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.read_gnb_api_v1_gn_bs_gnb_id_get_with_http_info(g_nb_id, **kwargs)  # noqa: E501
        else:
            (data) = self.read_gnb_api_v1_gn_bs_gnb_id_get_with_http_info(g_nb_id, **kwargs)  # noqa: E501
            return data

    def read_gnb_api_v1_gn_bs_gnb_id_get_with_http_info(self, g_nb_id, **kwargs):  # noqa: E501
        """Read Gnb  # noqa: E501

        Get gNB by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_gnb_api_v1_gn_bs_gnb_id_get_with_http_info(g_nb_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str g_nb_id: The gNB id of the gNB you want to retrieve (required)
        :return: GNB
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['g_nb_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method read_gnb_api_v1_gn_bs_gnb_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'g_nb_id' is set
        if ('g_nb_id' not in params or
                params['g_nb_id'] is None):
            raise ValueError("Missing the required parameter `g_nb_id` when calling `read_gnb_api_v1_gn_bs_gnb_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'g_nb_id' in params:
            path_params['gNB_id'] = params['g_nb_id']  # noqa: E501

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
            '/api/v1/gNBs/{gNB_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GNB',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_gnb_api_v1_gn_bs_gnb_id_put(self, body, g_nb_id, **kwargs):  # noqa: E501
        """Update Gnb  # noqa: E501

        Update a gNB.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_gnb_api_v1_gn_bs_gnb_id_put(body, g_nb_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GNBUpdate body: (required)
        :param str g_nb_id: The gNB id of the gNB you want to update (required)
        :return: GNB
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_gnb_api_v1_gn_bs_gnb_id_put_with_http_info(body, g_nb_id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_gnb_api_v1_gn_bs_gnb_id_put_with_http_info(body, g_nb_id, **kwargs)  # noqa: E501
            return data

    def update_gnb_api_v1_gn_bs_gnb_id_put_with_http_info(self, body, g_nb_id, **kwargs):  # noqa: E501
        """Update Gnb  # noqa: E501

        Update a gNB.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_gnb_api_v1_gn_bs_gnb_id_put_with_http_info(body, g_nb_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GNBUpdate body: (required)
        :param str g_nb_id: The gNB id of the gNB you want to update (required)
        :return: GNB
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'g_nb_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_gnb_api_v1_gn_bs_gnb_id_put" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_gnb_api_v1_gn_bs_gnb_id_put`")  # noqa: E501
        # verify the required parameter 'g_nb_id' is set
        if ('g_nb_id' not in params or
                params['g_nb_id'] is None):
            raise ValueError("Missing the required parameter `g_nb_id` when calling `update_gnb_api_v1_gn_bs_gnb_id_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'g_nb_id' in params:
            path_params['gNB_id'] = params['g_nb_id']  # noqa: E501

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
            '/api/v1/gNBs/{gNB_id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GNB',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

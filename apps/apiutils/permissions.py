#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019-03-26 14:53
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : permissions.py
# @software: PyCharm

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        print(obj)
        # Instance must have an attribute named `owner`.
        return obj.user_info == request.user


class IsServiceProvider(permissions.BasePermission):
    """
    如果是服务提供商，则允许发自媒体文章
    """
    
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.service_provider
        )


class IsRealNameUser(permissions.BasePermission):
    """
    验证是否是实名认证用户
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and (request.user.user_permission_name.permission_sn is "QX002")
        )
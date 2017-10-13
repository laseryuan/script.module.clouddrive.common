'''
    OneDrive for Kodi
    Copyright (C) 2015 - Carlos Guzman

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

    Created on Mar 1, 2015
    @author: Carlos Guzman (cguZZman) carlosguzmang@hotmail.com
'''
import time

from clouddrive.common.remote.oauth2 import OAuth2
from clouddrive.common.remote.signin import Signin


class Provider(OAuth2):
    name = ''
    _signin = Signin()
    _account_manager = None
    _driveid = None
    
    def __init__(self, name):
        self.name = name
        
    def create_pin(self, request_params={}):
        return self._signin.create_pin(self.name, request_params)
    
    def retrieve_tokens_info(self, pin_info, request_params={}):
        tokens_info = self._signin.retrieve_tokens_info(pin_info, request_params)
        if tokens_info:
            tokens_info['date'] = time.time()
        return tokens_info
    
    def configure(self, account_manager, driveid):
        self._account_manager = account_manager
        self._driveid = driveid
    
    def validate_configuration(self):
        if not self._account_manager:
            raise Exception('Account Manager not defined')
        if not self._driveid:
            raise Exception('DriveId not defined')
            
    def retrieve_access_tokens(self):
        self.validate_configuration()
        self._account_manager.load()
        account = self._account_manager.account_by_driveid(self._driveid)
        return account['access_tokens']
    
    def refresh_access_tokens(self, request_params={}):
        tokens = self.retrieve_access_tokens()
        tokens_info = self._signin.refresh_tokens(self.name, tokens['refresh_token'], request_params)
        if tokens_info:
            tokens_info['date'] = time.time()
        return tokens_info
    
    def persist_access_tokens(self, access_tokens):
        self.validate_configuration()
        self._account_manager.load()
        account = self._account_manager.account_by_driveid(self._driveid)
        account['access_tokens'] = access_tokens
        self._account_manager.add_account(account)
    
    def retrieve_account(self, request_params={}, access_tokens={}):
        raise NotImplementedError()
    
    def retrieve_drives(self, request_params={}, access_tokens={}):
        raise NotImplementedError()
    
    def drive_type_name(self, drive_type):
        return drive_type
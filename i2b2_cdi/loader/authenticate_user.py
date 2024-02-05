# Copyright 2023 Massachusetts General Hospital.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import os
import base64
from i2b2_cdi.common.file_util import get_package_path

def get_xml(username, password):
    xml_file_path = get_package_path('i2b2_cdi/loader/resources/post_i2b2.xml')
    with open(xml_file_path,'r') as f:
        xml_data = f.read()
    return xml_data.format(i2b2PmServiceUrl=os.environ['I2B2_PM_SERVICE_URL'], i2b2User=username, i2b2Password=password)

def get_sessionKey(xml):
    headers = {'Content-Type': 'application/xml', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br'}
    response= requests.post('http://i2b2-wildfly:8080/i2b2/services/PMService/getServices', data=xml, headers=headers).text
    for item in response.split("</password>"):
        if "SessionKey:" in item:
            return item[ item.find("SessionKey:")+len("SessionKey:") : ]

def encode_login(user, project, session_key):
    messageStr = user + "\\" + project + ":" + session_key
    message_bytes = messageStr.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message
    
if __name__ == "__main__":

    xml = get_xml('demo', 'demouser')
    sessionKey = get_sessionKey(xml)
    encoded_auth = encode_login('demo', 'demo', sessionKey)
    headers = {'Content-Type': 'application/xml', 'Authorization': 'Basic '+encoded_auth, 'X-Project-Name': 'Demo'} # set what your server accepts

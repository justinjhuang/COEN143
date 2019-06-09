#!/usr/bin/env python

################################################################################
# COPYRIGHT(c) 2018 STMicroelectronics                                         #
#                                                                              #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided that the following conditions are met:  #
#   1. Redistributions of source code must retain the above copyright notice,  #
#      this list of conditions and the following disclaimer.                   #
#   2. Redistributions in binary form must reproduce the above copyright       #
#      notice, this list of conditions and the following disclaimer in the     #
#      documentation and/or other materials provided with the distribution.    #
#   3. Neither the name of STMicroelectronics nor the names of its             #
#      contributors may be used to endorse or promote products derived from    #
#      this software without specific prior written permission.                #
#                                                                              #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  #
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE    #
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE   #
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE    #
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR          #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF         #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS     #
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN      #
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)      #
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE   #
# POSSIBILITY OF SUCH DAMAGE.                                                  #
################################################################################

################################################################################
# Author:  Davide Aliprandi, STMicroelectronics                                #
################################################################################


# DESCRIPTION
#
# This application example shows how to perform a Bluetooth Low Energy (BLE)
# scan, connect to a device, retrieve its exported features, and get push
# notifications from it.


# IMPORT

from __future__ import print_function

import os
import sys
import threading
import time

import firebase_admin
from blue_st_sdk.feature import FeatureListener
from blue_st_sdk.manager import Manager
from blue_st_sdk.manager import ManagerListener
from blue_st_sdk.node import NodeListener
from bluepy.btle import BTLEException
from firebase_admin import credentials, db

# PRECONDITIONS
#
# In case you want to modify the SDK, clone the repository and add the location
# of the "BlueSTSDK_Python" folder to the "PYTHONPATH" environment variable.
#
# On Linux:
#   export PYTHONPATH=/home/<user>/BlueSTSDK_Python


# CONSTANTS

# Presentation message.
INTRO = """####################
# SMART WINDOW v 1 #
####################"""

# Bluetooth Scanning time in seconds.
SCANNING_TIME_s = 5

data = None
dirty = True

s0 = None
s1 = None


# FUNCTIONS

#
# Printing intro.
#
def print_intro():
    print('\n' + INTRO + '\n')


# INTERFACES

#
# Implementation of the interface used by the Manager class to notify that a new
# node has been discovered or that the scanning starts/stops.
#
class MyManagerListener(ManagerListener):
    
    #
    # This method is called whenever a discovery process starts or stops.
    #
    # @param manager Manager instance that starts/stops the process.
    # @param enabled True if a new discovery starts, False otherwise.
    #
    def on_discovery_change(self, manager, enabled):
        print('Discovery %s.' % ('started' if enabled else 'stopped'))
        if not enabled:
            print()
    
    #
    # This method is called whenever a new node is discovered.
    #
    # @param manager Manager instance that discovers the node.
    # @param node    New node discovered.
    #
    def on_node_discovered(self, manager, node):
        print('New device discovered: %s.' % (node.get_name()))


#
# Implementation of the interface used by the Node class to notify that a node
# has updated its status.
#
class MyNodeListener(NodeListener):
    
    #
    # To be called whenever a node changes its status.
    #
    # @param node       Node that has changed its status.
    # @param new_status New node status.
    # @param old_status Old node status.
    #
    def on_status_change(self, node, new_status, old_status):
        print('Device %s from %s to %s.' %
              (node.get_name(), str(old_status), str(new_status)))


#
# Implementation of the interface used by the Feature class to notify that a
# feature has updated its data.
#
class TemperatureListener(FeatureListener):
    num = 0
    sensor = None
    
    #
    # To be called whenever the feature updates its data.
    #
    # @param feature Feature that has updated.
    # @param sample  Data extracted from the feature.
    #
    def on_update(self, feature, sample):
        print('temp', feature)


class PressureListener(FeatureListener):
    num = 0
    sensor = None
    
    #
    # To be called whenever the feature updates its data.
    #
    # @param feature Feature that has updated.
    # @param sample  Data extracted from the feature.
    #
    def on_update(self, feature, sample):
        print('pres', feature)


def bluetooth():
    global s0, s1
    
    try:
        # Creating Bluetooth Manager.
        manager = Manager.instance()
        manager_listener = MyManagerListener()
        manager.add_listener(manager_listener)
        
        while 2:
            # Synchronous discovery of Bluetooth devices.
            print('Scanning Bluetooth devices...\n')
            manager.discover(SCANNING_TIME_s)
            
            # Alternative 1: Asynchronous discovery of Bluetooth devices.
            # manager.discover(SCANNING_TIME_s, True)
            
            # Alternative 2: Asynchronous discovery of Bluetooth devices.
            # manager.start_discovery()
            # time.sleep(SCANNING_TIME_s)
            # manager.stop_discovery()
            
            # Getting discovered devices.
            discovered_devices = manager.get_nodes()
            
            # Listing discovered devices.
            if not discovered_devices:
                print('\nNo Bluetooth devices found.')
                continue
            print('\nAvailable Bluetooth devices:')
            i = 1
            for device in discovered_devices:
                print('%d) %s: [%s]' % (i, device.get_name(), device.get_tag()))
                i += 1
            
            # Selecting a device.
            while True:
                choice = int(input("\nSelect a device (\'0\' to quit): "))
                if 0 <= choice <= len(discovered_devices):
                    break
            if choice == 0:
                # Exiting.
                manager.remove_listener(manager_listener)
                print('Exiting...\n')
                sys.exit(0)
            device = discovered_devices[choice - 1]
            
            # Connecting to the device.
            node_listener = MyNodeListener()
            device.add_listener(node_listener)
            print('\nConnecting to %s...' % (device.get_name()))
            device.connect()
            print('Connection done.')
            
            if s0 is None:
                s0 = device
                sensor = 's0'
            elif s1 is None:
                s1 = device
                sensor = 's1'
            else:
                return
            
            # while True:
            # Getting features.
            # i = 1
            features = device.get_features()
            
            # for feature in features:
            #     print('%d) %s' % (i, feature.get_name()))
            
            temp_feature = features[1]
            pres_feature = features[2]
            
            # Enabling notifications.
            feature_listener = TemperatureListener()
            feature_listener.sensor = sensor
            temp_feature.add_listener(feature_listener)
            device.enable_notifications(temp_feature)
            feature_listener = PressureListener()
            feature_listener.sensor = sensor
            pres_feature.add_listener(feature_listener)
            device.enable_notifications(pres_feature)
            
            # Getting notifications.
            while True:
                device.wait_for_notifications(1)
            
            # # Disabling notifications.
            # device.disable_notifications(feature)
            # feature.remove_listener(feature_listener)
    
    except BTLEException as e:
        print(e)
        # Exiting.
        print('Exiting...\n')
        sys.exit(0)
    except KeyboardInterrupt:
        try:
            # Exiting.
            print('\nExiting...\n')
            sys.exit(0)
        except SystemExit:
            os._exit(0)


# MAIN APPLICATION

#
# Main application.
#
def main():
    global data, dirty, s0, s1
    
    # Printing intro.
    print_intro()
    
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('smartwindow-da455-firebase-adminsdk-mscl2-c5ad694b44.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smartwindow-da455.firebaseio.com/'
    })
    
    ref = db.reference('/')
    
    if os.path.isfile('key.txt'):
        with open('key.txt', 'r') as f:
            data_ref = ref.child(f.read())
            data = data_ref.get()
    else:
        data = {
            's1': {
                'temperature': 0,
                'humidity': 0
            },
            's2': {
                'temperature': 0,
                'humidity': 0
            }
        }
        data_ref = ref.push(data)
        # Get the unique key generated by push()
        new_id = data_ref.key
        with open('key.txt', 'w') as f:
            f.write(new_id)
    
    x = threading.Thread(target=bluetooth)
    x.start()
    
    while True:
        if dirty:
            data_ref.update(data)
            dirty = False
        time.sleep(5)


if __name__ == "__main__":
    main()

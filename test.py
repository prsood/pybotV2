import pandas as pd

user_dict={'ADI-MPL-LTE-PE-RTR-42-33': {'Bundle-Ether1': {'2020-04-06': 0,
                                                'peerBdevice': 'ADI-MPL-LTE-PE-RTR-42-34',
                                                'peerBinterface': 'Bundle-Ether1'},
                              'Bundle-Ether13': {'2020-04-06': 0,
                                                 'peerBdevice': 'ADI-MPL-LTE-PE-RTR-42-34',
                                                 'peerBinterface': 'Bundle-Ether13'},
                              'Bundle-Ether33': {'2020-04-06': 0,
                                                 'peerBdevice': 'ADI-MPL-LTE-PE-RTR-42-34',
                                                 'peerBinterface': 'Bundle-Ether33'},
                              'Bundle-Ether4': {'2020-04-06': 0,
                                                'peerBdevice': 'ADI-MPL-LTE-PE-RTR-42-34',
                                                'peerBinterface': 'Bundle-Ether4'},
                              'Bundle-Ether7': {'2020-04-06': 0,
                                                'peerBdevice': 'None',
                                                'peerBinterface': 'None'}},
            'ADI-MPL-LTE-PE-RTR-42-34': {'Bundle-Ether1': {'2020-04-06': 0,
                                                'peerBdevice': 'ADI-MPL-LTE-PE-RTR-42-33',
                                                'peerBinterface': 'Bundle-Ether1'},
                              'Bundle-Ether13': {'2020-04-06': 0,
                                                 'peerBdevice': 'ADI-MPL-LTE-PE-RTR-42-33',
                                                 'peerBinterface': 'Bundle-Ether13'},
                              'Bundle-Ether33': {'2020-04-06': 0,
                                                 'peerBdevice': 'ADI-MPL-LTE-PE-RTR-42-33',
                                                 'peerBinterface': 'Bundle-Ether33'},
                              'Bundle-Ether4': {'2020-04-06': 0,
                                                'peerBdevice': 'ADI-MPL-LTE-PE-RTR-42-33',
                                                'peerBinterface': 'Bundle-Ether4'},
                              'Bundle-Ether7': {'2020-04-06': 0,
                                                'peerBdevice': 'None',
                                                'peerBinterface': 'None'}},
             }
# print(type(user_dict))
try:
    if(user_dict['ADI-MPL-LTE-PE-RTR-42-34']['Bundle-Ether13']):
        del user_dict['ADI-MPL-LTE-PE-RTR-42-34']['Bundle-Ether13']
except:
    print("key error")

print(user_dict)
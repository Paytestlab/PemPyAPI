from netifaces import interfaces, ifaddresses, AF_INET, AF_LINK

class Interfaces(object):

    @staticmethod
    def remove_loopback_from_list(list, config, interface):
        for link in config[AF_LINK]:
            if(len(link['addr']) == 0):
                list.remove(interface);

        for link in config[AF_INET]:
            if 'broadcast' not in link.keys() and 'peer' in link.keys():
                list.remove(interface);

    @staticmethod
    def get_all_network_interfaces_with_broadcast():
        try:
            addresses = interfaces();
            for interface in addresses:
                config = ifaddresses(interface)
                # AF_INET is not always present
                if AF_INET in config.keys():
                    Interfaces.remove_loopback_from_list(addresses, config, interface);

            #print(addresses);
            return addresses
        except ImportError:
            return [] 


    @staticmethod
    def get_broadcast_address(iface_name):
        addresses = ifaddresses(iface_name);
        broadcast_list = [];
        if AF_INET in addresses.keys():
            for value in addresses[AF_INET]:
                if('broadcast' in value):
                    return value['broadcast']
                    #broadcast_list.append(value['broadcast']);

        #return broadcast_list;

    @staticmethod
    def get_local_ip_from_interface(iface_name):
         addresses = ifaddresses(iface_name);
         if AF_INET in addresses.keys():
             for value in addresses[AF_INET]:
                 if('addr' in value and len(value['addr']) > 0):
                     return value['addr'];

         return None;


#ifaces = Interfaces.get_all_network_interfaces_with_broadcast();
#for iface in ifaces:
#    print(Interfaces.get_local_ip_from_interface(iface));
from Mux.AxUDPCommandSender import AxUDPCommandSender;
from Mux.AxUDPCommandSenderManager import AxUDPCommandSenderManager;
import time;


device = bytearray((0x14, 0x07, 0xe0, 0x00, 0x03, 0x3f));
a = AxUDPCommandSenderManager();
if(a.device_lookup(device) is True):
    sender = a.get_sender_for_device(device);

    for i in reversed(range(0,17)):
        sender.set_port(i);
        time.sleep(1);




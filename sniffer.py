from collections import Counter                        # NEW
from scapy.all import sniff, wrpcap, IP, TCP, UDP, ICMP, Raw

protocol_counts = Counter()                            # NEW

def show_packet(packet):
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst

        if TCP in packet:
            proto = "TCP"
            sport = packet[TCP].sport
            dport = packet[TCP].dport
        elif UDP in packet:
            proto = "UDP"
            sport = packet[UDP].sport
            dport = packet[UDP].dport
        elif ICMP in packet:
            proto = "ICMP"
            sport = dport = "-"
        else:
            proto = "Other"
            sport = dport = "-"

        protocol_counts[proto] += 1                    # NEW

        print(proto, "|", src, ":", sport, "->", dst, ":", dport)

        if Raw in packet:
            data = packet[Raw].load
            text = "".join(chr(b) if 32 <= b < 127 else "." for b in data[:150])
            print("   Payload:", len(data), "bytes")
            print("   ", text)

packets = sniff(prn=show_packet, store=True, count=50)
wrpcap("capture.pcap", packets)
print("Sniffing... press Ctrl+C to stop")             # NEW
try:                                                   # NEW
    sniff(prn=show_packet, store=False)                # CHANGED
except KeyboardInterrupt:                              # NEW
    pass                                               # NEW

print("\n--- Summary ---")                             # NEW
for proto, count in protocol_counts.items():           # NEW
    print(proto, ":", count)                           # NEW
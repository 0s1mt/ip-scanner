import nmap
import argparse

def perform_scan(ip_range, scan_type):
    nm = nmap.PortScanner()

    print("Tarama başlatılıyor...")
    scan_arguments = '-F' if scan_type == 'hızlı' else '-sV'

    nm.scan(ip_range, arguments=scan_arguments)

    print("Tarama tamamlandı. Sonuçlar:")

    results = []

    for host in nm.all_hosts():
        host_info = {'IP': host, 'Ports': []}
        
        if "tcp" in nm[host]:
            for port, info in nm[host]["tcp"].items():
                port_info = {
                    'Port': port,
                    'Protokol': info['name'],
                    'Ürün': info['product'],
                    'Sürüm': info['version']
                }
                host_info['Ports'].append(port_info)

        results.append(host_info)

    return results

def save_results_to_file(results, output_file):
    with open(output_file, 'w') as file:
        for host_info in results:
            file.write(f"IP: {host_info['IP']}\n")
            for port_info in host_info['Ports']:
                file.write(f"  Port: {port_info['Port']}, Protokol: {port_info['Protokol']}, "
                           f"Ürün: {port_info['Ürün']}, Sürüm: {port_info['Sürüm']}\n")

def main():
    parser = argparse.ArgumentParser(description="Ağ Tarama Uygulaması")
    parser.add_argument("ip_range", help="Hedef IP adresini girin (tek bir IP veya IP aralığı)")
    parser.add_argument("scan_type", choices=["hızlı", "ayrıntılı"], help="Tarama türünü seçin (hızlı veya ayrıntılı)")
    parser.add_argument("-o", "--output", help="Sonuçları bir dosyaya kaydet")

    args = parser.parse_args()

    results = perform_scan(args.ip_range, args.scan_type)

    for host_info in results:
        print(f"IP: {host_info['IP']}")
        for port_info in host_info['Ports']:
            print(f"  Port: {port_info['Port']}, Protokol: {port_info['Protokol']}, "
                  f"Ürün: {port_info['Ürün']}, Sürüm: {port_info['Sürüm']}")

    if args.output:
        save_results_to_file(results, args.output)

if __name__ == "__main__":
    main()

from mininet.net import Mininet                      # Importa a classe Mininet do módulo mininet.net
from mininet.topo import Topo                        # Importa a classe Topo do módulo mininet.topo
from mininet.node import Controller, RemoteController # Importa as classes Controller e RemoteController do módulo mininet.node
from mininet.link import TCLink                      # Importa a classe TCLink do módulo mininet.link
from mininet.log import setLogLevel, info            # Importa as funções setLogLevel e info do módulo mininet.log
from mininet.node import CPULimitedHost              # Importa a classe CPULimitedHost do módulo mininet.node

class MyTopo(Topo):                                  # Define uma classe MyTopo que herda da classe Topo
    def build(self):                                 # Define um método build para construir a topologia
        h1 = self.addHost('h1', ip='10.0.0.1')       # Adiciona o host h1 à topologia com o endereço IP 10.0.0.1
        h2 = self.addHost('h2', ip='10.0.0.2')       # Adiciona o host h2 à topologia com o endereço IP 10.0.0.2
        s1 = self.addSwitch('s1')                    # Adiciona o switch s1 à topologia
        self.addLink(h1, s1, bw=10, delay='10ms')    # Adiciona um link entre h1 e s1 com largura de banda de 10 e atraso de 10ms
        self.addLink(h2, s1, bw=100, delay='5ms')   # Adiciona um link entre h2 e s1 com largura de banda de 100 e atraso de 5ms

def run():                                           # Define uma função run para iniciar a simulação
    c = RemoteController('c', ip='127.0.0.1', port=6633)  # Define um controlador remoto com endereço IP e porta específicos
    net = Mininet(topo=MyTopo(), controller=None, link=TCLink, host=CPULimitedHost)  # Cria uma instância da rede Mininet
    net.addController(c)                            # Adiciona o controlador à rede
    net.start()                                     # Inicia a rede
    h1, h2 = net.get('h1', 'h2')                    # Obtém as instâncias dos hosts h1 e h2
    h1.cmd('ifconfig h1-eth0 0')                    # Configura a interface h1-eth0 do host h1
    h2.cmd('ifconfig h2-eth0 0')                    # Configura a interface h2-eth0 do host h2
    h1.cmd('ip addr add 10.0.0.1/24 dev h1-eth0')   # Adiciona um endereço IP à interface h1-eth0
    h2.cmd('ip addr add 10.0.0.2/24 dev h2-eth0')   # Adiciona um endereço IP à interface h2-eth0
    h1.cmd('ip link set h1-eth0 up')                # Ativa a interface h1-eth0
    h2.cmd('ip link set h2-eth0 up')                # Ativa a interface h2-eth0
    h1.cmd('route add default gw 10.0.0.2')         # Adiciona uma rota padrão para o host h1
    h2.cmd('route add default gw 10.0.0.1')         # Adiciona uma rota padrão para o host h2
    info('Starting iperf server on h2...\n')        # Exibe uma mensagem indicando que o servidor iperf está iniciando em h2
    h2.sendCmd('iperf -s > iperf_server_log.txt &') # Inicia o servidor iperf no host h2
    info('Starting iperf client on h1 to connect to h2...\n')  # Exibe uma mensagem indicando que o cliente iperf está iniciando em h1 para se conectar a h2
    h1.cmd('iperf -c 10.0.0.2 > iperf_client_log.txt')  # Inicia o cliente iperf no host h1 para se conectar ao host h2
    net.stop()                                      # Para a simulação

if __name__ == '__main__':                           # Verifica se o script está sendo executado como programa principal
    setLogLevel('info')                             # Define o nível de log como 'info'
    run()                                           # Chama a função run para iniciar a simulação

# sd-eon-openflow
material oficina sd-eon openflow
- Acessar:
https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
baixe o putty  referente a arquitetura do seu computador e instale 

- Acessar:
https://mobaxterm.mobatek.net/download-home-edition.html#
baixar mobaXterm e instale 

- Acessar:
https://www.virtualbox.org/wiki/Downloads
baixar virtualbox referente a arquitetura do seu computador e instale 

- Acessar:
https://github.com/mininet/mininet/releases/
Escolher a imagem: *ovf.zip referente a arquitetura do seu computador 

- Descompaqutar o arquivo zip 
- Abrir o arquivo ovf e importar no virtualbox
- Apos importado iniciar a maquina virtual 

- no virtualbox va em arquivo>preferencias>Redes, adicione uma rede nat e habilite o dhcp
- antes de iniciar a maquina adicione outro adaptador de rede
- na maquina virtual agroa va em configuracoes>rede habilite duas placas de rede
- no adaptador 1 coloquen nat para ter acesso a internet an maquina 
- no adaptador 2 coloque host-only para ter acesso ao xterm e wireshark

inicie a maquina virtual 
login mininet 
senha mininet

vamos instalar alguns pacotes necessarios 
sudo apt-get install update 
sudo apt-get install install xterm vim htop iftop iotop iperf tcpdump tcpreplay xinit rcconf openbox lxpanel lxde-icon-theme nodm xscreensaver xfig sudo desktop-base menu pcmanfm git subversion imagemagick midori evince tree

apos isso no terminal da maquina virtual digite ifconfig e pegue o ip para que vc consiga acessar via ssh a maquina

abra o putty escolha ssh e digite o ip da maquina virtual

nos comandos observe sempre o ambiente que deve ser digitado o comando no inico da linha 

$ sudo mn --topo single,3 --mac --switch ovsk --controller remote

Isso diz ao Mininet para iniciar uma topologia de switch único (baseada em openvSwitch) de 3 hosts, definir o endereço MAC de cada host igual ao seu IP e apontar para um controlador remoto cujo padrão é o host local.

Aqui está o que o Mininet acabou de fazer:

Criou 3 hosts virtuais, cada um com um endereço IP separado.
Criou um único switch de software OpenFlow no kernel com 3 portas.
Conectou cada host virtual ao switch com um cabo Ethernet virtual.
Defina o endereço MAC de cada host igual ao seu IP.
Configure o switch OpenFlow para conectar-se a um controlador remoto.

Para ver a lista de nós disponíveis, no console do Mininet, execute:

mininet> nodes


Para ver uma lista de comandos disponíveis, no console do Mininet, execute:

mininet> help

Para executar um único comando em um nó, coloque o nome do nó antes do comando. Por exemplo, para verificar o IP de um host virtual, no console Mininet, execute:

mininet> h1 ifconfig

abra outro terminal SSH conecte na maquina e, Você usará ovs-ofctl para instalar manualmente os fluxos necessários. No seu terminal SSH:

# ovs-ofctl add-flow s2 in_port=1,actions=output:2
# ovs-ofctl add-flow s2 in_port=2,actions=output:1
 


Isso encaminhará os pacotes que chegam da porta 1 para a porta 2 e vice-versa. Verifique verificando a tabela de fluxo

# ovs-ofctl dump-flows s1

Agora, volte para o console do mininet e tente executar ping em h2 de h1. No console Mininet:

mininet> h1 ping -c3 h2

Para pingar todos os hosts 

mininet> pingall

Wireshark

o Wireshark funciona no Xterm com mobaXterm abra ele antes de conectar 


incie um terminal pytty com protocolo X11 habilitado 
-abra o putty 
-va em 
-connection>SSH>X11 e habilite o protocolo
- agora va em session e digite o ip com protoocolo ssh e connecte maquina


o X11 e uma especie de acesso remoto a aplicativos via ssh X11 

no terminal com X11 habilitado digite 
 $ sudo wireshark &

se nao abrir e apresentar erros tente 

$ sudo -E wireshark &

escolha a interface Loopback:lo

ao abrir o Wireshark para filtrar apenas os pacotes do openflow digite no filtro acima openflow_v1, isso vai mostrar apenas os pacotes do protocolo openflow

para ver as mensagem iniciais do openflow e so finalizar e inicar novamente 

 mininet> exit
  $> mn -c 

inicie o controlador 

 $sudo controller ptcp:6633

e inicie novamente a topologia 

sem tabela de rotas 
  $>sudo mn --topo single,3 --mac --switch ovsk --controller remote


com tabela de rotas 
$>sudo mn --topo single,3 --mac --switch ovsbr --controller remote

as seguintes mensagens podem aparecer 

Message	Type	Description
Hello	Controller->Switch	following the TCP handshake, the controller sends its version number to the switch.
Hello	Switch->Controller	the switch replies with its supported version number.
Features Request	Controller->Switch	the controller asks to see which ports are available.
Set Config	Controller->Switch	in this case, the controller asks the switch to send flow expirations.
Features Reply	Switch->Controller	the switch replies with a list of ports, port speeds, and supported tables and actions.
Port Status	Switch->Controller	enables the switch to inform that controller of changes to port speeds or connectivity. Ignore this one, it appears to be a bug.

comm um ping teremos as mensagens 

mininet> h1 ping -c1 h2

Message	Type	Description
Packet-In	Switch->Controller	a packet was received and it didn't match any entry in the switch's flow table, causing the packet to be sent to the controller.
Packet-Out	Controller->Switch	controller send a packet out one or more switch ports.
Flow-Mod	Controller->Switch	instructs a switch to add a particular flow to its flow table.
Flow-Expired	Switch->Controller	a flow timed out after a period of inactivity.


para gerar trafego e testar a velocidade das coneccoes podemos usar o iperf 

 mininet> iperf

teremos um trafego de teste gerado para testar os links 


simples servidor web

mininet> h1 python -m http.server 80 &

um wget no servidor web baixando a pagina web 

mininet> h2 wget -O - h1

encerrando o servidor web 

mininet> h1 kill %python






- teste 2 com python 


em outra janela inicie o controlador pox

cd ~/pox
./pox.py forwarding.l2_learning

na janela principal execute o arquivo em python 

$ sudo python testem.py


sudo mn --topo tree,depth=2,fanout=5 --controller=remote,ip=10.0.0.1,port=6633 --switch default,protocols=OpenFlow13,  --link tc,bw=1,delay=10ms

sudo mn --topo tree,depth=2,fanout=5 --controlle default  --switch default,protocols=OpenFlow13,  --link tc,bw=1,delay=10ms



executar fora depois entrar no sudo su pra abrir o xterm  
$ sudo xauth add $(xauth -f ~mininet/.Xauthority list|tail -1)



sudo mn --link tc,bw=1

reinicia o ssh 
sudo systemctl restart ssh
sudo systemctl status ssh





Sites importantes:

https://mininet.org/walkthrough/
https://mininet.org/walkthrough/#xterm-display
https://github.com/mininet/openflow-tutorial/wiki/Set-up-Virtual-Machine
https://github.com/mininet/openflow-tutorial/wiki#user-content-OpenFlow
https://mininet.org/walkthrough/#using-a-remote-controller
https://mininet.org/download/



Softwares:

https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
https://mobaxterm.mobatek.net/download-home-edition.html#
https://www.virtualbox.org/wiki/Downloads
https://github.com/mininet/mininet/releases/

material-oficina-sdn-openflow
https://www.dropbox.com/sh/dp6dnndf98qlpq6/AADi0-mcHftBIGJapZDCNrhpa?dl=0




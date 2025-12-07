"# LuisTiago_CDIG"

Olá

Este é um projeto relacionado com o IEEE 802.11 utilizando o GNU Radio como ferrramenta software e o ADALM_PLUTO para receber trasmissão WIFI.

Neste repositório git temos:

-> Pasta DOCS com a parte teórica do projeto;

-> A pasta GRC com o ficheiro flowchart;

-> Pasta Wireshark que inclui o código em pyhton utilizando uma FIFO para obter os dados em real-time, ou seja, o pluto recebe transmissão wifi e na aplicação wireshark é possível ver os resultados que estão na pasta "Resultados";

-> A pasta Pyhton apresenta os códigos utilizados no flowchart;

-> A pasta Resultados_offline que  apresenta graficos que se pode obter sem o pluto estar ligado, utilizando a gravação dos dados wifi obtidas pelo uso do pluto num dos testes passados / uso de recordings de wifi.

-> Pasta Wireshark que inclui o código em pyhton utilizando uma FIFO para obter os resultados em real-time, ou seja, o pluto recebe transmissão wifi e na aplicação wireshark é possível ver os resultados que estão na pasta "Resultados";

-> Para obter esta pasta git , façam: git clone https://github.com/Lumi-CH23/LuisTiago_CDIG.git;

Integração com Wireshark:

 Tramas decodificadas são enviadas via Socket PDU para o Wireshark, permitindo:

->inspeção de beacons, data frames, ACKs, QoS data, etc;
->identificação de BSSIDs, SSIDs, taxas, timestamp e parâmetros PHY;

Utilização do Pyhton Snippet 

 O projeto inclui um script Python integrado no GNU RAdio para:
 -> Sweep de frequenias: (canais: 1,6 e 11);
 -> Threshold automatico;


 Melhorias Implementadas ao Longo do Projeto

-AGC adaptativo com parâmetros ajustáveis
-Equalizador LMS substituindo LS para maior robustez
-Sweep de frequências
-Heatmap
-Socket PDU configurado corretamente para Wireshark
-Código Python modular, limpo e fácil de manter

Testes & Validação:

O sistema foi testado com:

->Routers domésticos;
->Hotspots de telemóvel;
->PlutoSDR;

Foram decodificados com sucesso:

Beacon frames;

Data frames;

ACKs;

QoS frames;


Créditos:

Projeto realizado no contexto académico, usando

GNU Radio;
gr-ieee802-11;
PlutoSDR;
Wireshark;

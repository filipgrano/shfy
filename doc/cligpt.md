# cligpt
cligpt is a command-line helper tool that takes a user prompt and returns shell commands, along with explanations of what they do. It uses OpenAI's GPT models to generate these suggestions and explanations.

## Usage
To use cligpt, simply type `cligpt <your_prompt>` into your terminal. For example, if you wanted to ping your network gateway, you could type:

```
filip@debluna:~$ cligpt find my network gateway and check if it is responding
Suggestion: ping $(ip route show default | awk '/default/ {print $3}') -c 1
Execute suggested command? (Y/N) | Explain command? (E): y
PING 192.168.226.2 (192.168.226.2) 56(84) bytes of data.
64 bytes from 192.168.226.2: icmp_seq=1 ttl=128 time=0.342 ms

--- 192.168.226.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.342/0.342/0.342/0.000 ms
filip@debluna:~$

```
By default cligpt will not explain the command, but you can ask it to by typing `e` when prompted. You can also configure it to always explain.

```
(venv) filip@debluna:~$ cligpt find my network gateway and check if it is responding. Say Hurray! if it is, and something is not right when it is not
Suggestion: ping -c 1 $(ip route show | awk '/default/ {print $3}') && echo "Hurray!" || echo "Something is not right"
Execute suggested command? (Y/N) | Explain command? (E): e
Explanation: The command finds the network gateway, pings it once, and outputs "Hurray!" if it responds, and "Something is not right" if it does not. It is safe to use. Task fulfilled.
Execute suggested command? (Y/N): y
PING 192.168.226.2 (192.168.226.2) 56(84) bytes of data.
64 bytes from 192.168.226.2: icmp_seq=1 ttl=128 time=0.323 ms

--- 192.168.226.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.323/0.323/0.323/0.000 ms
Hurray!
filip@debluna:~$

```

## Configuration
Configuration is not required. Cligpt can be configured by editing the `~/.config/oai_tools/config.yaml` file. See the [config-example.yaml](config-example.yaml) file for more details.
The configuration file allows you to set the log level, automatic command explanation, model, maximum tokens for each query, and temperature for each query.

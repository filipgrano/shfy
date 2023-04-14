# cligpt
cligpt is a command-line helper tool that takes a user prompt and returns shell commands, along with explanations of what they do. It uses OpenAI's GPT models to generate these suggestions and explanations.

## Usage
To use cligpt, simply type cligpt <your_prompt> into your terminal. For example, if you wanted to ping your network gateway, you could type:

```
$ cligpt Find my network gateway and check if it is responding
Suggestion: ping -c 1 $(ip route | grep default | awk '{print $3}') > /dev/null && echo "Gateway is responding"
Explanation: This command uses the "ping" tool to send a single packet to the default gateway of the network, which is determined by parsing the output of the "ip route" command. If the gateway responds, the command displays the message "Gateway is responding". It fulfills the requested task.
Execute suggested command? (Y/N): y
Gateway is responding
```

## Configuration
Configuration is not required. Cligpt can be configured by editing the `~/.config/oai_tools/config.yaml` file. See the [config-example.yaml](config-example.yaml) file for more details.
The configuration file allows you to set the log level, automatic command explanation, model, maximum tokens for each query, and temperature for each query.

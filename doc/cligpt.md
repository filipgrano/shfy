# Cligpt
Cligpt is your best friend when you don't remember how to do something on the command line. It takes a description of what you want to do and returns a command that does it (and a explanation of how it works). It can also be used as a shell completion tool. It uses OpenAI's GPT models to generate these suggestions and explanations.

## Configuration
Configuration is not required. Cligpt can be configured by editing the `~/.config/oai_tools/config.yaml` file. See the [config-example.yaml](config-example.yaml) file for more details.
The configuration file allows you to set the log level, automatic command explanation, model, maximum tokens for each query, and temperature for each query.

## Basic Usage
To use cligpt, simply type `cligpt <your_prompt>` into your terminal. For example, if you wanted to ping your network gateway, you could type:

```bash
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

```bash
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

## Shell Completion
cligpt can also be used as a shell completion tool. It can be configured to run automatically when you press a key combination (e.g. Ctrl-G) before pressing Enter. This way, you can type a command or description and press the key combination to get a suggested command. This is especially useful when you don't remember the exact command you need, but you know what it should do.

Completion is currently supported for Bash and Zsh. More shells can probably be supported by adding a completion script for them. If you want to add support for a shell, please open an issue or a pull request.

### BASH
Assuming cligpt_completion is in your $PATH. Add the following to your .bashrc or .bash_profile file:
```bash
### START CLIGPT ###
cligpt_completion() {
    tput sc

    current_command="${READLINE_LINE}"

    tput el1
    printf '%s [cligpt complete]' "${PS1@P}$current_command"

    completion=$(cligpt_complete "$current_command")

    tput rc
    READLINE_LINE="$completion"
    READLINE_POINT=${#completion}
    tput el
}

bind -x '"\C-x\C-g": cligpt_completion'

cligpt_explanation() {
    current_command="${READLINE_LINE}"

    tput el1
    printf '%s [cligpt explain]\n' "${PS1@P}$current_command"

    explanation=$(cligpt_explain "$current_command")
    printf 'Explanation: %s\n' "$explanation"
}

bind -x '"\C-x\C-f": cligpt_explanation'

read_user_input() {
    local prompt=$1
    local input

    local saved_stty=$(stty -g)
    read -ep "> $prompt" input < /dev/tty
    stty "$saved_stty"

    printf "%s" "$input"
}

cligpt_changes() {
    current_command="${READLINE_LINE}"

    tput el1
    printf '%s [cligpt]\n' "${PS1@P}$current_command"

    user_input=$(read_user_input "Changes: ")

    printf "[cligpt is working...]\n"
    completion=$(cligpt_complete "'$current_command'" "changes: '$user_input'")

    READLINE_LINE="$completion"
    READLINE_POINT=${#completion}
    tput el
}

bind -x '"\C-x\C-h": cligpt_changes'
### END CLIGPT ###
```
Restart your terminal. Now, when you type a command or description and press the key combination (Ctrl-G) before pressing Enter, the shell will display an indicator while cligpt is working, and the existing line will be replaced with the suggested command.

### ZSH
Assuming cligpt_completion is in your $PATH. Add the following to your .zshrc file:
```zsh
cligpt_complete() {
    # Get the current command line
    current_command="${BUFFER[0,CURSOR]}"

    # Save the current cursor position and print an indicator
    tput sc
    printf " [cligpt...]"

    # Get the completion from the cligpt_completion Python script
    completion=$(cligpt_completion "$current_command")

    # Restore the cursor position, clear the indicator, and update the command line
    tput rc
    tput el
    BUFFER="$completion"
    CURSOR=${#completion}
}

# Register the cligpt_complete function as a widget
zle -N cligpt_complete

bindkey '^G' cligpt_complete
```
Restart your terminal. Now, when you type a command or description and press the key combination (Ctrl-G) before pressing Enter, the shell will display an indicator while cligpt is working, and the existing line will be replaced with the suggested command.

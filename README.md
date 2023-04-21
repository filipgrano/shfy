# Shfy
Shfy (Shellify) is your best friend when you don't remember how to do something on the command line. 

It works both as a standalone command line tool and as a shell completion tool.

As a standalone command line tool, which should work in almost any shell, it takes a description of what you want to do and returns a command that does it (and an explanation of how it works and if it's safe). See the [basic usage](#basic-usage-as-a-standalone-command-line-tool) section for more details.

Shfy is most powerful as a shell completion tool. See the [shell completion](#shell-completion) section for more details.

Shfy uses OpenAI's GPT models to generate these suggestions and explanations.

[![IShfy demo video](resources/yt_demo_screenshot.png)](https://www.youtube.com/watch?v=uYIzrmKmMNc)

## Installation or Upgrade
`pip install --upgrade shfy`

## Configuration
The configuration is read from `~/.config/shfy/config.yaml` file. Configuration is optional. See the [config-example.yaml](resources/config-example.yaml) file for more details.

The configuration file allows you to set the log level, automatic command explanation, model, maximum tokens for each query, and temperature for each query.

### API Key
OpenAI's API key is required. 
The key is read from the `OPENAI_API_KEY` environment variable. If this variable is not set, the API key is read from the `~/.config/shfy/api_key` file.

## Basic Usage as a standalone command line tool
To use shfy, simply type `shfy <your_prompt>` into your terminal. This should work in almost any shell; it has been tested in Bash and Zsh on Linux and Powershell and CMD on Windows.

For example, if you wanted to ping your network gateway, you could type:

```bash
filip@debluna:~$ shfy find my network gateway and check if it is responding
Suggestion: ping $(ip route show default | awk '/default/ {print $3}') -c 1
Execute suggested command? (Y/N) | Explain command? (E): y
PING 192.168.226.2 (192.168.226.2) 56(84) bytes of data.
64 bytes from 192.168.226.2: icmp_seq=1 ttl=128 time=0.342 ms

--- 192.168.226.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.342/0.342/0.342/0.000 ms
filip@debluna:~$

```
By default shfy will not explain the command, but you can ask it to do so by typing `e` when prompted. You can also configure it to always explain.

```bash
(venv) filip@debluna:~$ shfy find my network gateway and check if it is responding. Say Hurray! if it is, and something is not right when it is not
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
Shfy works best as a shell completion tool. Currently setup instructions for Bash and Zsh are provided, more can likely be added with relative ease.

With shell completion you can gain three new superpowers:
1. Press Ctrl-X Ctrl-G to get a suggested command, based on the current line in the prompt. The existing line will be replaced with the suggested command.
2. Press Ctrl-X Ctrl-F to get an explanation of the current line.
3. Press Ctrl-X Ctrl-H to get a suggested command, based on what is currently in the prompt and the requested changes you enter at the displayed input prompt.

### BASH
Assuming shfy_complete and shfy_explain is in your $PATH. Add the following to your .bashrc or .bash_profile file to gain access to your new superpowers:
```bash
### START shfy ###
shfy_completion() {
    tput sc

    current_command="$READLINE_LINE"

    tput el1
    printf '%s [shfy complete]' "${PS1@P}$current_command"

    completion=$(shfy_complete "$current_command")

    tput rc
    READLINE_LINE="$completion"
    READLINE_POINT=${#completion}
    tput el
}

bind -x '"\C-x\C-g": shfy_completion'

shfy_explanation() {
    current_command="$READLINE_LINE"

    tput el1
    printf '%s [shfy explain]\n' "${PS1@P}$current_command"

    explanation=$(shfy_explain "$current_command")
    printf 'Explanation: %s\n' "$explanation"
}

bind -x '"\C-x\C-f": shfy_explanation'

read_user_input() {
    local prompt=$1
    local input

    local saved_stty=$(stty -g)
    read -ep "> $prompt" input < /dev/tty
    stty "$saved_stty"

    printf "%s" "$input"
}

shfy_changes() {
    current_command="$READLINE_LINE"

    tput el1
    printf '%s [shfy]\n' "${PS1@P}$current_command"

    user_input=$(read_user_input "Changes: ")

    printf "[shfy is working...]\n"
    completion=$(shfy_complete "'$current_command'" "changes: '$user_input'")

    READLINE_LINE="$completion"
    READLINE_POINT=${#completion}
    tput el
}

bind -x '"\C-x\C-h": shfy_changes'
### END shfy ###
```
Restart your terminal to access your new superpowers.

### ZSH
Assuming shfy_complete and shfy_explain is in your $PATH. Add the following to your .zshrc file to gain access to your new superpowers:
```zsh
### START shfy ###
shfy_completion() {
    local current_command="$BUFFER"

    printf " [shfy complete]"

    local completion=$(shfy_complete "$current_command")

    BUFFER="$completion"
    CURSOR=${#completion}
    zle reset-prompt
}

zle -N shfy_completion
bindkey '^X^G' shfy_completion

shfy_explanation() {
    local current_command="$BUFFER"

    printf " [shfy explain]"

    local explanation=$(shfy_explain "$current_command")
    printf '\nExplanation: %s\n' "$explanation"

    BUFFER="$current_command"
    CURSOR=${#current_command}
    zle reset-prompt
}

zle -N shfy_explanation
bindkey '^X^F' shfy_explanation

autoload -Uz read-from-minibuffer

shfy_changes() {
    local current_command="$BUFFER"

    printf " [shfy]"

    read-from-minibuffer '> Changes: '
    local user_input="$REPLY"

    printf " [shfy is working...]"

    local completion=$(shfy_complete "'$current_command'" "changes: '$user_input'")

    BUFFER="$completion"
    CURSOR=${#completion}
    zle reset-prompt
}

zle -N shfy_changes
bindkey '^X^H' shfy_changes
### END shfy ###
```

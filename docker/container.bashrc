# Only run the interactive extras for interactive shells
case "$-" in
*i*) ;;
*) return ;;
esac

# ---------- shell behavior ----------
export HISTCONTROL=ignoreboth:erasedups
export HISTSIZE=10000
export HISTFILESIZE=20000
shopt -s histappend checkwinsize

# ---------- locate workspace ----------
# The repo root is the colcon workspace (src/, build/, install/, log/).
for _d in "$PWD" "$HOME/cpp-workshop" "/workspaces/cpp-workshop"; do
	if [ -d "$_d/src" ] && [ -d "$_d/docker" ]; then
		export WS_DIR="$_d"
		break
	fi
done
unset _d

# ---------- ROS environment ----------
ws_source_env() {
	[ -f /opt/ros/jazzy/setup.bash ] && source /opt/ros/jazzy/setup.bash
	[ -n "${WS_DIR:-}" ] && [ -f "$WS_DIR/install/setup.bash" ] && source "$WS_DIR/install/setup.bash"
	return 0
}
ws_source_env

if [ -n "${WS_DIR:-}" ] && [ "$PWD" = "$HOME" ]; then
	cd "$WS_DIR" || true
fi

# ---------- prompt ----------
_ws_prompt() {
	local branch
	branch="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null)"
	[ -n "$branch" ] && branch=" \[\e[38;2;80;170;255m\]($branch)\[\e[0m\]"
	PS1="\[\e[38;2;233;60;171m\]\u\[\e[0m\]:\[\e[38;2;1;255;0m\]\w\[\e[0m\]${branch}\\$ "
}
PROMPT_COMMAND="_ws_prompt"

# ---------- aliases ----------
alias c='clear'
alias ll='ls -alF --color=auto'
alias la='ls -A --color=auto'
alias ..='cd ..'

alias rtl='ros2 topic list'
alias rte='ros2 topic echo'
alias rs='ws_source_env'

# ---------- helpers ----------
cb() { (cd "$WS_DIR" && colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON "$@") && ws_source_env; }
ct() { (cd "$WS_DIR" && colcon test "$@" && colcon test-result --verbose); }
ros-clean() { rm -rf "$WS_DIR/build" "$WS_DIR/install" "$WS_DIR/log"; }

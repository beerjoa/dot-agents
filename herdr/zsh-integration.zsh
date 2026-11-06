# Activate the Herdr Ghostty key table only for interactive attaches.
herdr() {
  emulate -L zsh
  local is_attach=1 terminal_id='' herdr_status=0

  case "${1-}" in
    -h|--help|-V|--version|status|update|channel|machine|workspace|worktree|tab|notification|agent|pane|integration|completion|config|server|--machine)
      is_attach=0
      ;;
    session)
      [[ "${2-}" == "attach" ]] || is_attach=0
      ;;
  esac

  if (( is_attach )) && [[ "${TERM_PROGRAM:-}" == "ghostty" && -z "${HERDR_ENV:-}" && -x /usr/bin/osascript ]]; then
    terminal_id=$(/usr/bin/osascript \
      -e 'tell application "Ghostty"' \
      -e 'set target_terminal to focused terminal of selected tab of front window' \
      -e 'perform action "activate_key_table:herdr" on target_terminal' \
      -e 'return id of target_terminal' \
      -e 'end tell' 2>/dev/null)
    if [[ -z "$terminal_id" ]]; then
      print -u2 -- 'Herdr: Ghostty key mode could not be activated; prefix shortcuts remain available.'
    fi
  fi

  command herdr "$@"
  herdr_status=$?

  if [[ -n "$terminal_id" ]]; then
    /usr/bin/osascript \
      -e 'on run argv' \
      -e 'set target_id to item 1 of argv' \
      -e 'tell application "Ghostty"' \
      -e 'set matches to every terminal whose id is target_id' \
      -e 'if (count of matches) > 0 then perform action "deactivate_key_table" on item 1 of matches' \
      -e 'end tell' \
      -e 'end run' \
      "$terminal_id" >/dev/null 2>&1
  fi

  return $herdr_status
}

# Log
# ---

echo-cyan:  ## echo with cyan font https://gist.github.com/iamnewton/8754917
	@echo -e "\e[36m${msg}\e[39m"
.PHONY: echo-cyan


echo-purple:  ## echo with purple font https://gist.github.com/iamnewton/8754917
	@echo -e "\e[35m${msg}\e[39m"
.PHONY: echo-purple

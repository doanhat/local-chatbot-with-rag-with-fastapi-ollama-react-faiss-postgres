# Define variables
OLLAMA_PID_FILE := /tmp/ollama.pid

# Default target
.PHONY: all
all: run

# Run Ollama (if not already running) and Docker Compose
.PHONY: run
run:
	@echo "Checking Ollama status..."
	@if pgrep -x "ollama" > /dev/null; then \
		echo "Ollama is already running."; \
	else \
		echo "Starting Ollama..."; \
		ollama serve > /dev/null 2>&1 & echo $$! > $(OLLAMA_PID_FILE); \
		echo "Ollama started with PID $$(cat $(OLLAMA_PID_FILE))"; \
		echo "Waiting for Ollama to initialize..."; \
		sleep 5; \
	fi
	@echo "Starting Docker Compose..."
	docker-compose up --build

# Stop Docker Compose (but not Ollama)
.PHONY: stop
stop:
	@echo "Stopping Docker Compose..."
	docker-compose down

# Stop both Docker Compose and Ollama
.PHONY: stop-all
stop-all: stop
	@echo "Stopping Ollama..."
	@if pgrep -x "ollama" > /dev/null; then \
		pkill ollama; \
		echo "Ollama stopped."; \
	else \
		echo "Ollama is not running."; \
	fi
	@if [ -f $(OLLAMA_PID_FILE) ]; then \
		rm $(OLLAMA_PID_FILE); \
	fi

# Clean up
.PHONY: clean
clean: stop-all
	@echo "Cleaning up..."
	docker-compose down -v

# Check Ollama logs
.PHONY: ollama-logs
ollama-logs:
	@echo "Checking Ollama logs..."
	@if [ "$$(uname)" = "Darwin" ]; then \
		log show --predicate 'process == "ollama"' --last 1h; \
	elif [ "$$(uname)" = "Linux" ]; then \
		journalctl -u ollama -n 100 --no-pager; \
	else \
		echo "Unsupported operating system for log viewing."; \
	fi

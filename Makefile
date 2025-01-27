all : reinstall_dependencies
	@echo 'Process completed ✅'
	
reinstall_dependencies:
	@echo "Installing dependencies..."
	@pip freeze | xargs pip uninstall -y
	@python3 -m pip install --upgrade pip
	@pip install -r requirements.txt

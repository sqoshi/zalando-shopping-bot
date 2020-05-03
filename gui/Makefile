main: print_bash compile give_permissions
	touch main
print_bash:
	echo '#!/bin/bash' > main
compile:
	echo 'python3 script.py' >> main
give_permissions:
	chmod +x main
clean:
	rm out
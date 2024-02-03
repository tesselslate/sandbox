# configuration
DESTINATION = /usr/local
CC          = cc
LD_FLAGS    = -lX11 -lxcb -lxcb-cursor -lxcb-keysyms

# configuration (cflags)
CFLAGS		  = -g -O0 -Wall -Wextra -pedantic -std=gnu11 -DDEBUG -fsanitize=address
#CFLAGS       = -Os -Wall -Wextra -Werror -pedantic -std=gnu11

# tasks
winman-display:
	mkdir -p out
	${CC} ${CFLAGS} -o out/winman wm.c ${LD_FLAGS}

clean:
	rm -f out/winman

run: winman-display
	sh run.sh

install: winman-display
	mkdir -p ${DESTINATION}/bin
	cp out/winman ${DESTINATION}/bin
	chmod 755 ${DESTINATION}/bin/winman

uninstall:
	rm -f ${DESTINATION}/bin/winman

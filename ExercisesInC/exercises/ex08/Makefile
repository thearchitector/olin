GLIBS = $$(pkg-config --cflags --libs glib-2.0)

ex_compile: ex_compile.c
	gcc ex_compile.c ${GLIBS} -o ex_compile

word_count: word_count.c
	gcc word_count.c $(GLIBS) -o word_count

build: $(addprefix build-,$(RUNS))
clean: $(addprefix clean-,$(RUNS))

build-%:
	make -C $* build

clean-%:
	make -C $* clean
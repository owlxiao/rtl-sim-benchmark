$(shell [ -d out ] || mkdir out)

targets = memory-access.pdf \
		  platform-info.tex platform-extra-info.tex

all: $(addprefix out/,$(targets))
	make -C report

define add_dep
out/$1: $(wildcard $(basename $1)*.py) $(all_data)
	python $$<

endef

$(eval $(foreach T,$(targets),$(call add_dep,$(T))))

clean:
	make -C report clean
	rm -rf out


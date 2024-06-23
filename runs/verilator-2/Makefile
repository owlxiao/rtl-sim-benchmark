BUILD_DIR = build
BIN_DIR = bin
CASE_ROOT = $(TEST_ROOT)/cases
ALL_CASES := $(patsubst $(CASE_ROOT)/%.fir,%,$(wildcard $(CASE_ROOT)/*.fir))

$(shell [ -d $(BUILD_DIR) ] || mkdir -p $(BUILD_DIR))
$(shell [ -d $(BIN_DIR)   ] || mkdir -p $(BIN_DIR))

.PHONY: build clean

build: $(patsubst %,bin/%.out,$(ALL_CASES))

clean:
	rm -rf build bin

#===-------------------------------------------------------------------------===
# FIRRTL to HW
#===-------------------------------------------------------------------------===

$(CASE_ROOT)/%.mlir: $(CASE_ROOT)/%.fir
	@echo === Firtool $< "->" $@
	@firtool --ir-hw $< -o $@

$(CASE_ROOT)%.sv: $(CASE_ROOT)/%.mlir
	@echo === Generate SystemVerilog "->" $@
	@firtool --lowering-options=disallowLocalVariables $< -o $@
	
TESTBENCH_SRCS = $(shell find $(abspath ./) -name "*.c" -or -name "*.cc" -or -name "*.cpp")

bin/%.out: $(CASE_ROOT)/%.sv $(CASE_ROOT)/plusarg_reader.v $(CASE_ROOT)/plusarg_reader.v $(TESTBENCH_SRCS)
	# Create build directory
	@mkdir -p $(BUILD_DIR)/$*

	verilator --sv --cc --exe --Wno-fatal -DSYNTHESIS -O3 --compiler clang \
		-CFLAGS "-I $(CASE_ROOT) -DDesign=V$* -O3 -march=native -std=c++2a" -threads 2 $^ \
		-Mdir $(BUILD_DIR)/$*/obj_dir

	bear -- make -j -C $(BUILD_DIR)/$*/obj_dir -fV$*.mk CXX=clang++

	cp $(BUILD_DIR)/$*/obj_dir/V$* $(BIN_DIR)/$*.out
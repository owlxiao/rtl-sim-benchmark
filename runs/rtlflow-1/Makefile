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

export VERILATOR_ROOT=$(RTLFLOW_ROOT)

#===-------------------------------------------------------------------------===
# FIRRTL to HW
#===-------------------------------------------------------------------------===

$(CASE_ROOT)/%.mlir: $(CASE_ROOT)/%.fir
	@echo === Firtool $< "->" $@
	@firtool --ir-hw $< -o $@

$(CASE_ROOT)%.sv: $(CASE_ROOT)/%.mlir
	@echo === Generate SystemVerilog "->" $@
	@firtool --lowering-options=disallowLocalVariables $< -o $@

TESTBENCH_SRCS = $(abspath tb.cu)

RTLflow = $(VERILATOR_ROOT)/bin/rtlflow
RTLflow_FLAGS = --stats -O3 --cc --exe -Wno-fatal -Wno-STMTDLY --output-split 250000000

bin/%.out: $(CASE_ROOT)/%.sv $(CASE_ROOT)/plusarg_reader.v $(CASE_ROOT)/plusarg_reader.v $(TESTBENCH_SRCS)
	# Create build directory
	@mkdir -p $(BUILD_DIR)/$* 

	$(RTLflow) $(RTLflow_FLAGS) --threads 2 \
		-CFLAGS "-I $(CASE_ROOT) -DDesign=V$* -O3 -arch=native -std=c++20 -DGPU_THREADS=1 -lineinfo" $^ \
		-Mdir $(BUILD_DIR)/$*/obj_dir --top-module $*

	bear -- make -j12 -C $(BUILD_DIR)/$*/obj_dir -fV$*.mk

	cp $(BUILD_DIR)/$*/obj_dir/V$* $(BIN_DIR)/$*.out


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

ARCILATOR_UTILS_ROOT ?= $(dir $(shell which arcilator))

$(BUILD_DIR)/%/%.ll $(BUILD_DIR)/%/%.h &: $(CASE_ROOT)/%.mlir
	# Create build directory
	@mkdir -p $(BUILD_DIR)/$*
	
	arcilator $^ --state-file=$(BUILD_DIR)/$*/$*.json -o $(BUILD_DIR)/$*/$*.ll

	python3 $(ARCILATOR_UTILS_ROOT)/arcilator-header-cpp.py $(BUILD_DIR)/$*/$*.json --view-depth 1 > $(BUILD_DIR)/$*/$*.h


#===-------------------------------------------------------------------------===
# Testbench
#===-------------------------------------------------------------------------===

bin/%.out: tb.cpp $(BUILD_DIR)/%/%.ll  $(BUILD_DIR)/%/%.h
	opt -O3 --march=native -S $(BUILD_DIR)/$*/$*.ll | llc -O3 --filetype=obj -o $(BUILD_DIR)/$*/$*.o

	bear -- clang++ -O3 -std=c++2a -march=native -no-pie -DDesign=$* \
		-I$(BUILD_DIR)/$* tb.cpp -I$(ARCILATOR_UTILS_ROOT) \
		$(BUILD_DIR)/$*/$*.o -o $@
BUILD_DIR = build
BIN_DIR = bin
CASE_ROOT = $(TEST_ROOT)/cases
FILTER_OUT_CASE = NutShell RocketChip
ALL_CASES := $(patsubst $(CASE_ROOT)/%.fir,%,$(wildcard $(CASE_ROOT)/*.fir))
ALL_CASES := $(filter-out $(FILTER_OUT_CASE), $(ALL_CASES))


$(shell [ -d $(BUILD_DIR) ] || mkdir -p $(BUILD_DIR))
$(shell [ -d $(BIN_DIR)   ] || mkdir -p $(BIN_DIR))

.PHONY: build clean

build: $(patsubst %,bin/%.out,$(ALL_CASES))

clean:
	rm -rf build bin

TESTBENCH_SRCS = $(abspath tb.cpp)

$(BUILD_DIR)/%/%.h: $(CASE_ROOT)/%.fir
	# Create build directory
	@mkdir -p $(BUILD_DIR)/$*

	essent $< -O3

	mv $(CASE_ROOT)/$*.h $(BUILD_DIR)/$*/$*.h


bin/%.out: $(BUILD_DIR)/%/%.h $(TESTBENCH_SRCS)
	bear -- clang++ -O3 -std=c++2a -march=native -DDesign=$* \
	-I$(BUILD_DIR)/$* -Iinclude tb.cpp -o $@


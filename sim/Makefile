DUT_FILES := rtl/counter.sv
TB_FILES  := tb/counter_tb.sv
TOP       := counter_tb
SNAPSHOT  := $(TOP)_opt

TESTNAME  ?= test1
SEED      ?= 1

WORK_DIR  := work
LOG_DIR   := ../logs/compile.log
DO_FILE   := run.do
YAML_CFG  := ../config/test_config.yaml

.PHONY: lib compile opt sim regress clean

lib:
	@mkdir -p $(LOG_DIR)
	vlib $(WORK_DIR)

compile: lib
	vlog -work $(WORK_DIR) -l $(LOG_DIR)/compile.log $(DUT_FILES) $(TB_FILES)

opt: compile
	vopt $(WORK_DIR).$(TOP) -work $(WORK_DIR) -o $(SNAPSHOT)

sim: opt
	@mkdir -p $(LOG_DIR)
	vsim -c $(SNAPSHOT) \
		-sv_seed $(SEED) \
		+UVM_TESTNAME=$(TESTNAME) \
		-l $(LOG_DIR)/$(TESTNAME)_seed_$(SEED).log \
		-do $(DO_FILE)

regress: opt
	@python3 -c 'import yaml; yaml.safe_load(open("$(YAML_CFG)")); print("YAML valid")'
	@python3 -c 'import yaml; cfg=yaml.safe_load(open("$(YAML_CFG)")); [print("{} {}".format(t["name"], t["seed"])) for t in cfg["tests"]]' | \
	while read test seed; do \
		echo "Running $$test with seed $$seed"; \
		$(MAKE) --no-print-directory sim TESTNAME=$$test SEED=$$seed || exit $$?; \
	done

clean:
	rm -rf $(WORK_DIR) $(LOG_DIR) transcript

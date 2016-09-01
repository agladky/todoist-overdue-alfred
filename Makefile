WORKFLOW := "Todoist\ overdue.alfredworkflow"
SRC_DIR := todoist-overdue-alfred
SRC :=  *
VPATH := $(SRC_DIR)

all: $(WORKFLOW)

$(WORKFLOW): $(SRC)
	cd $(SRC_DIR) && zip -r $@ . && mv $@ ..

install: $(WORKFLOW)
	open $<
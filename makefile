SHELL = /bin/bash

project_dependencies ?= $(addprefix $(project_root)/, \
		emissor \
		cltl-combot \
		cltl-requirements \
		cltl-backend \
		cltl-object-recognition \
		cltl-vad \
		cltl-asr \
		cltl-emissor-data \
		cltl-eliza \
		cltl-chat-ui \
		workshop-app)

git_remote ?= https://github.com/leolani

sources =

include util/make/makefile.base.mk
include util/make/makefile.py.base.mk
include util/make/makefile.git.mk

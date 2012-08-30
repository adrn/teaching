TARGET=APWSyllabusFall2012

SUBDIRS = AstronomyLabs

.PHONY: subdirs $(SUBDIRS)
subdirs: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@

include Makefile.include
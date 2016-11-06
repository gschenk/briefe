# target
T=brief
TARGET=$(addsuffix .pdf,$(T))

# configuration
STY = mydefs.sty mystyle.sty

# objects
OBJ =$(addsuffix .tex,$(T))
OBJ+= private/recipients.adr
OBJ+= private/sender.lco

# tex parser
TEX= pdflatex
TEXFLAGS=

# pdf viewer, fallback to ghostview
ifeq (, $(shell which evince))
  VIEWER:= gv
  VFLAGS:=
else
  VIEWER:= evince
  VFLAGS:=
endif


.PHONY: all clean cleaner view newrec

all: text

text:$(TARGET)

$(TARGET):$(OBJ) $(STY)
	$(TEX) -draftmode $(T)
	$(TEX) $(T)


cleaner: clean
	rm -f *.pdf *.log

clean:
	rm -f *.dvi *.aux *.out 

newrec:
	python addrEntry.py

view:
	test -e $(TARGET) && $(VIEWER) $(VFLAGS) $(TARGET) 2> /dev/null &


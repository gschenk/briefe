# target
T=brief
TARGET=$(addsuffix .pdf,$(T))

# configuration
STY = mydefs.sty

# objects
OBJ =$(addsuffix .tex,$(T))
OBJ+= private/recipientdat.tex private/senderdat.tex

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


.PHONY: all clean cleaner view

all: text

text:$(TARGET)

$(TARGET):$(OBJ) $(STY)
	$(TEX) -draftmode $(T)
	$(TEX) $(T)


cleaner: clean
	rm -f *.pdf *.log

clean:
	rm -f *.dvi *.aux *.out 


view:
	test -e $(TARGET) && $(VIEWER) $(VFLAGS) $(TARGET) 2> /dev/null &


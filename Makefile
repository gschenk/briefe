# target
T=brief
TARGET=$(addsuffix .pdf,$(T))

# file containing the recipient
# auto generated by a python script
RECIPIENT=private/recipient.lco

# the python script that generates from yaml address
# entries latex KOMA variables for the recipient
ADSCR = readAddress.py

# configuration
STY = mydefs.sty mystyle.sty

# objects
SRC =$(addsuffix .tex,$(T))

OBJ = $(SRC)
OBJ+= private/sender.lco
OBJ+= DIN5008A.lco


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

$(TARGET):$(OBJ) $(STY) $(RECIPIENT)
	$(TEX) -draftmode $(T)
	$(TEX) $(T)

$(RECIPIENT):$(SRC) $(ADSCR)
	python $(ADSCR) `head -n 1 $<` > $@

cleaner: clean
	rm -f *.pdf *.log rm private/recipient.lco

clean:
	rm -f *.dvi *.aux *.out

newrec:
	python enterAddress.py

view:
	test -e $(TARGET) && $(VIEWER) $(VFLAGS) $(TARGET) 2> /dev/null &


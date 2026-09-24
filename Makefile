.PHONY: paper demo clean

## Build the paper
paper:
	cd paper && latexmk -pdf no-final-save.tex

## Run the MC3 companion
demo:
	python code/mc3_demo.py

## Remove LaTeX build artifacts
clean:
	cd paper && latexmk -C

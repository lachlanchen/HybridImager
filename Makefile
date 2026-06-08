.PHONY: figures paper clean

figures:
	python3 scripts/draw_hybrid_camera_diagrams.py

paper: figures
	cd publications && pdflatex -interaction=nonstopmode -halt-on-error hybrid_camera_concept.tex

clean:
	rm -f publications/*.aux publications/*.log publications/*.out publications/*.toc publications/*.synctex.gz

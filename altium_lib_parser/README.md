# Parsing Altium lib

The tip is to export a schematic lib in .lia format, corresponding to a P-CAD library, which has the good taste to be a text format. Then it is possible to re-import a modified .lia using the Import Wizard.

Be careful, Altium is very sensitive to encoding and line feeds: modified file must be \\r\\r line breaks and ISO-8859-1 encoding.
